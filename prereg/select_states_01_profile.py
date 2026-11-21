"""โปรไฟล์ 'นับอย่างเดียว' ของข้อมูล HMDA ต่อรัฐ สำหรับเกณฑ์เลือกรัฐ C1-C5 (ไม่รันโมเดล ไม่ดูอัตราอนุมัติรายกลุ่ม)
ใช้ตัวกรองและ demographics() เดียวกับต้นแบบ (03_ต้นแบบ/src/fairgroups/hmda.py)

วิธีรัน (ใช้ python ของ venv ที่มี pandas/sklearn):
  python -I เลือกรัฐ_01_profile.py --src <03_ต้นแบบ/src> --data <โฟลเดอร์ CSV> --year 2023 --out <โฟลเดอร์ผล> GA CA OH ...
ไฟล์ CSV ชื่อ hmda_<year>_<STATE>.csv ดาวน์โหลดจาก FFIEC Data Browser API (actions_taken=1,2,3 [&loan_purposes=1])
"""
import argparse, json, sys
from pathlib import Path
import numpy as np, pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True); ap.add_argument("--data", required=True)
ap.add_argument("--year", default="2023"); ap.add_argument("--out", required=True)
ap.add_argument("states", nargs="+")
a = ap.parse_args()
sys.path.insert(0, a.src)
from fairgroups.hmda import demographics  # noqa: E402

COLS = ['loan_purpose', 'occupancy_type', 'business_or_commercial_purpose', 'reverse_mortgage', 'open-end_line_of_credit',
        'total_units', 'derived_dwelling_category', 'action_taken', 'derived_race', 'derived_ethnicity', 'derived_sex',
        'applicant_age', 'lei']
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
for st in a.states:
    f = pd.read_csv(Path(a.data) / f"hmda_{a.year}_{st}.csv", usecols=COLS, low_memory=False)
    keep = ((pd.to_numeric(f.loan_purpose, errors='coerce') == 1) & (f.occupancy_type == 1) &
            (f.business_or_commercial_purpose != 1) & (f.reverse_mortgage != 1) & (f['open-end_line_of_credit'] != 1) &
            pd.to_numeric(f.total_units, errors='coerce').between(1, 4) &
            f.derived_dwelling_category.str.contains('Single Family', na=False) & f.action_taken.isin([1, 2, 3]))
    f = f.loc[keep].copy()
    d = demographics(f)
    known = d.intersection != 'Unknown'
    cell = d.loc[known, 'intersection'].value_counts()
    lei = f.lei.value_counts()
    lei.to_json(out / f"lei_{st}_{a.year}.json")
    rec = dict(state=st, year=a.year, filtered=len(f), unknown_race_share=float((d.race_eth == 'Unknown').mean()),
               known_both=int(known.sum()), n_cells=int(len(cell)), min_cell=int(cell.min()), cells_lt150=int((cell < 150).sum()),
               race_share={k: round(float(v), 4) for k, v in d.race_eth.value_counts(normalize=True).items()},
               n_lei=int(len(lei)), top1_lei_share=float(lei.iloc[0] / len(f)),
               smallest_cells={k: int(v) for k, v in cell.nsmallest(3).items()})
    json.dump(rec, open(out / f"profile_{st}_{a.year}.json", "w"), ensure_ascii=False)
    print(st, rec["filtered"], flush=True)
