"""ข้อมูล HMDA: แยกประชากรและตัวแปรหลังตัดสินใจก่อนฝึกทุกขั้น"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

POST = set('action_taken purchaser_type interest_rate rate_spread hoepa_status total_loan_costs total_points_and_fees origination_charges discount_points lender_credits prepayment_penalty_term intro_rate_period negative_amortization interest_only_payment balloon_payment other_nonamortizing_features multifamily_affordable_units activity_year state_code'.split())
NUMERIC = 'loan_amount loan_to_value_ratio property_value income debt_to_income_ratio loan_term total_units tract_population ffiec_msa_md_median_family_income tract_to_msa_income_percentage tract_owner_occupied_units tract_one_to_four_family_homes tract_median_age_of_housing_units'.split()
CATEGORICAL = 'loan_type lien_status preapproval construction_method applicant_credit_score_type submission_of_application initially_payable_to_institution aus-1 conforming_loan_limit derived_loan_product_type derived_msa-md county_code lei'.split()
FEATURES = NUMERIC + CATEGORICAL
UNKNOWN = 'Unknown'


def sensitive_column(c):
    """credit_score_type ไม่ใช่คะแนนเครดิตจริง และไม่ใช่ตัวแปรประชากร"""
    return c in {'derived_race', 'derived_ethnicity', 'derived_sex'} or (
        c.startswith(('applicant_', 'co-applicant_')) and
        any(t in c for t in ('race', 'ethnicity', 'sex', 'age', 'observed')))


def prohibited(c):
    return c in POST or c.startswith('denial_reason-') or sensitive_column(c) or c == 'tract_minority_population_percent'


def missing(series):
    return series.isna() | series.astype(str).str.strip().str.lower().isin(['', 'exempt', 'na', 'n/a', 'nan', 'none'])


def dti_numeric(series):
    """แปลงช่วงเป็นค่ากึ่งกลางที่มีลำดับ ไม่เดาค่าจากผลอนุมัติ"""
    mapping = {'<20%': 10., '20%-<30%': 25., '30%-<36%': 33., '50%-60%': 55., '>60%': 65.}
    return pd.to_numeric(series.replace(mapping), errors='coerce')


def demographics(frame):
    race, eth = frame.derived_race.fillna(UNKNOWN), frame.derived_ethnicity.fillna(UNKNOWN)
    unavailable = race.str.contains('Not Available|Free Form Text Only|Unknown', case=False) | eth.str.contains('Not Available|Free Form Text Only|Unknown', case=False)
    # Hispanic รวมทุกเชื้อชาติ แม้ไม่มี race; ไม่มี ethnicity ไม่สมมุติว่า NH
    re = np.where(eth == 'Hispanic or Latino', 'Hispanic', np.where(unavailable, UNKNOWN,
         race.map({'White':'NH White', 'Black or African American':'NH Black', 'Asian':'NH Asian'}).fillna('Other')))
    sex = frame.derived_sex.where(frame.derived_sex.isin(['Male', 'Female', 'Joint']), UNKNOWN)
    age = frame.applicant_age.astype(str).where(frame.applicant_age.astype(str).isin(['<25','25-34','35-44','45-54','55-64','65-74','>74']), UNKNOWN)
    result = pd.DataFrame({'race_eth': re, 'sex': sex, 'age': age}, index=frame.index)
    result['intersection'] = np.where((result.race_eth != UNKNOWN) & (result.sex != UNKNOWN), result.race_eth + ' × ' + result.sex, UNKNOWN)
    return result


def reference_groups(s):
    return {c: s[c].to_numpy().astype(str) for c in ['race_eth','sex','age','intersection']}


def load_hmda(root, state='GA'):
    path = Path(root) / 'hmda' / f'hmda_2023_{state}.csv'
    if not path.exists():
        # urllib ติดตาม redirect ตามมาตรฐาน และเก็บแคชใช้รอบถัดไป
        import urllib.request
        path.parent.mkdir(parents=True, exist_ok=True)
        url = f'https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?states={state}&years=2023&actions_taken=1,2,3'
        temp = path.with_suffix('.part')
        urllib.request.urlretrieve(url, temp)
        temp.replace(path)
    frame = pd.read_csv(path, low_memory=False)
    stages = [{'stage':'ข้อมูลต้นทาง', 'n':len(frame)}]
    filters = [('ซื้อที่อยู่อาศัย', pd.to_numeric(frame.loan_purpose, errors='coerce') == 1),
        ('อยู่เอง', frame.occupancy_type == 1), ('ไม่ใช่ธุรกิจ', frame.business_or_commercial_purpose != 1),
        ('ไม่ใช่ reverse mortgage', frame.reverse_mortgage != 1), ('ไม่ใช่ open-end', frame['open-end_line_of_credit'] != 1),
        ('1–4 หน่วย', pd.to_numeric(frame.total_units, errors='coerce').between(1,4)),
        ('Single Family', frame.derived_dwelling_category.str.contains('Single Family', na=False)),
        ('ผลอนุมัติ/ปฏิเสธที่กำหนด', frame.action_taken.isin([1,2,3]))]
    keep = np.ones(len(frame), dtype=bool)
    for label, mask in filters:
        keep &= mask.to_numpy()
        stages.append({'stage':label,'n':int(keep.sum())})
    frame = frame.loc[keep].copy()
    y = frame.action_taken.isin([1,2]).to_numpy().astype(int)
    return frame, y, demographics(frame), pd.DataFrame(stages)


def split_hmda(frame, y, s, seed, max_rows=0):
    positions = np.arange(len(y)); strata = s.race_eth.to_numpy() + y.astype(str)
    if max_rows and len(y) > max_rows:
        positions, _ = train_test_split(positions, train_size=max_rows, stratify=strata, random_state=seed)
    train, rest = train_test_split(positions, test_size=.4, stratify=strata[positions], random_state=seed)
    val, test = train_test_split(rest, test_size=.5, stratify=strata[rest], random_state=seed)
    return {name: {'frame':frame.iloc[idx].copy(), 'y':y[idx], 's':s.iloc[idx].copy(), 'ids':frame.index.to_numpy()[idx]}
            for name, idx in [('train',train),('val',val),('test',test)]}


class LeakageGuard:
    """เลือกคอลัมน์จาก train เท่านั้น ไม่ใช้ missing ของ validation/test"""
    def fit(self, frame, y):
        self.fit_ids_ = frame.index.to_numpy().copy()
        self.audit_, self.features_ = [], []
        for c in frame.columns:
            m = missing(frame[c]).to_numpy()
            rates = [float(m[y == v].mean()) for v in [0,1]]
            gap = abs(rates[1]-rates[0])
            reason = ('ข้อมูลประชากร/หลังตัดสินใจ/ตัวแทนพื้นที่ที่ห้ามใช้' if prohibited(c) else
                      'missing gap > 10 จุดเปอร์เซ็นต์' if gap > .10 else
                      'อยู่นอกรายการตัวแปรก่อนตัดสินใจที่อนุญาต' if c not in FEATURES else '')
            if not reason: self.features_.append(c)
            self.audit_.append({'column':c,'missing_denied':rates[0],'missing_approved':rates[1],
                                'missing_gap':gap,'dropped':bool(reason),'reason':reason})
        assert all(not prohibited(c) for c in self.features_)
        return self

    def transform(self, frame):
        result = frame[self.features_].copy()
        for c in result:
            if c in NUMERIC:
                result[c] = dti_numeric(result[c]) if c == 'debt_to_income_ratio' else pd.to_numeric(result[c], errors='coerce')
                result[c] = result[c].replace([np.inf,-np.inf],np.nan).astype(float)
            else:
                result[c] = result[c].where(~missing(result[c]), '__missing__').astype(str)
        return result


class HMDAPreprocessor:
    """แทนค่าว่าง รวมค่าหายาก และ top-N ผู้ให้กู้ด้วย train เท่านั้น"""
    def __init__(self, min_frequency=20, lei_top_n=30, scale=True):
        self.min_frequency, self.lei_top_n, self.scale = min_frequency, lei_top_n, scale

    def prepare(self, frame):
        frame = frame.copy()
        if 'lei' in frame:
            frame['lei'] = frame.lei.where(frame.lei.isin(self.top_lei_), '__other__')
        return frame

    def fit(self, frame):
        assert all(not prohibited(c) for c in frame.columns)
        self.fit_ids_ = frame.index.to_numpy().copy()
        self.feature_names_in_ = list(frame.columns)
        self.top_lei_ = frame.lei.value_counts().head(self.lei_top_n).index.tolist() if 'lei' in frame else []
        self.numeric_ = [c for c in frame if c in NUMERIC]
        self.categorical_ = [c for c in frame if c not in NUMERIC]
        numeric = [SimpleImputer(strategy='median', keep_empty_features=True)]
        if self.scale: numeric.append(StandardScaler())
        self.encoder = ColumnTransformer([
            ('numeric',make_pipeline(*numeric),self.numeric_),
            ('category',OneHotEncoder(handle_unknown='infrequent_if_exist', min_frequency=self.min_frequency,
                                     sparse_output=False, dtype=np.float32),self.categorical_)], sparse_threshold=0)
        self.encoder.fit(self.prepare(frame))
        return self

    def transform(self, frame):
        return self.encoder.transform(self.prepare(frame)).astype(np.float32)

    def names(self):
        return self.encoder.get_feature_names_out().tolist()


def write_profile(output, stages, y, s):
    from .reporting import markdown_table
    stages.to_csv(output/'filter_counts.csv',index=False)
    rows=[]
    for name, values in reference_groups(s).items():
        for group in np.unique(values):
            mask=values==group
            rows.append({'dimension':name,'group':group,'n':int(mask.sum()),'approval_rate':float(y[mask].mean()),
                         'denial_rate':float(1-y[mask].mean()),'excluded_fairness':group==UNKNOWN})
    profile=pd.DataFrame(rows); profile.to_csv(output/'data_profile.csv',index=False)
    text=['# ข้อมูล HMDA หลังคัดกรอง','',markdown_table(stages,['stage'],['n']),'',
          'Unknown คงไว้ฝึก แต่ตัดจาก fairness เฉพาะมิติที่ไม่ทราบ และตัดกลุ่มเล็กตาม min_fair_group ใน CSV ผลทดลอง',
          '',markdown_table(profile,['dimension','group'],['n','approval_rate','denial_rate'])]
    (output/'data_profile.md').write_text('\n'.join(text),encoding='utf-8')
