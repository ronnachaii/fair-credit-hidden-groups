# HMDA: ค้นหากลุ่มผู้ขอสินเชื่อและทดลองลดอคติ

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ronnachaii/fair-credit-hidden-groups/blob/main/notebooks/pilot_colab.ipynb)

ต้นแบบวิจัยหัวข้อ 2.4: supervised model ทำนายอนุมัติสินเชื่อ และค้นหากลุ่มเสียเปรียบโดยไม่ใช้ประชากรเป็นตัวแปรต้น ระบบมี representation + clustering, กฎอธิบายกลุ่ม, group DRO และการประเมินกับประชากรจริง ผลไม่ได้รับประกันว่าจะลดอคติ และห้ามใช้เป็นระบบอนุมัติจริง

## รันในเครื่อง

```bash
~/.venvs/rsu-fair/bin/python -m pytest tests -q
~/.venvs/rsu-fair/bin/python run_pilot.py --quick
~/.venvs/rsu-fair/bin/python tools/build_notebook.py
~/.venvs/rsu-fair/bin/python tools/check_delivery.py
```

ใช้แพ็กเกจที่ติดตั้งแล้ว ไม่ต้อง pip install ในเครื่อง QUICK: GA 2023 ประมาณ 20,000 แถว แบ่ง 60/20/20, 3 seed (17,29,43), full labels เท่านั้น FULL: ทั้งรัฐ, 5 seed, epochs มากขึ้น (`--full`) เปลี่ยนรัฐด้วย `--state GA` ไฟล์ไม่อยู่ในแคชจึงจะดาวน์โหลดผ่าน FFIEC API (ต้องมีอินเทอร์เน็ต)

## Colab CPU ฟรี

เปิด `notebooks/pilot_colab.ipynb` เลือก CPU แล้ว Run all เซลล์แรกติดตั้ง requirements (เฉพาะ Colab); ปล่อย REPO_URL ว่างได้ เซลล์ `%%writefile` ฝังโค้ดเดียวกับ `src/` และ tests ครบ ไม่ต้องมี repo หรือข้อมูลเดิม ใช้ urllib ติดตาม redirect และแคช CSV จาก FFIEC:

`https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?states=GA&years=2023&actions_taken=1,2,3`

แพ็กเกจ HBAC 0.2.6 ระบุ `numpy<2` ใน metadata ขณะที่ venv นี้เป็น NumPy 2.4.6 และทดสอบ runtime ผ่าน Notebook จึงติดตั้ง core requirements และ kmodes ก่อน แล้วติดตั้ง HBAC ด้วย `--no-deps` เพื่อคง NumPy ชุดเดียวกับที่ทดสอบ ไม่ควรสั่ง `pip install -r requirements.txt` ตรง ๆ เพราะตัวแก้ dependency จะปฏิเสธข้อกำหนดคู่นี้; ในเครื่องไม่ติดตั้งเพิ่ม

ดูเวลาที่วัดจริงใน `results/environment.json` รอบ 5 ตั้งเป้า QUICK ประมาณไม่เกิน 8 นาทีบน Colab CPU เวลาดาวน์โหลด/ติดตั้งขึ้นกับเครือข่าย เซลล์ท้ายเปิด Gradio ด้วย `launch(share=True)`

## ทดสอบบน Colab แล้ว

ตามผลทดสอบที่ผู้ส่งงาน (Claude) แจ้งเมื่อ **15 ต.ค. 2569**: รอบ 2 ใช้ runtime ใหม่ CPU, Python 3.13 · numpy 2.1.3 · pandas 2.2.3 · scikit-learn 1.6.1 · scipy 1.16.3 รันครบทุกเซลล์ โหมด QUICK ประมาณ **3.4 นาที** และหน้าสาธิต Gradio ทำงาน

หลักฐานนี้เป็นของรอบ 2 ก่อนปรับ tuning รอบ 3–5; รอบ 5 ทดสอบใน venv ของเครื่องและ notebook fallback โดยยังไม่ได้ทดสอบ Colab runtime ใหม่ จึงไม่ใช้เวลา 3.4 นาทีรับรองรอบ 5 ไม่แก้ตรรกะเซลล์ติดตั้งที่ผ่านการทดสอบแล้ว และใช้ API ที่มีใน pandas 2.2 / scikit-learn 1.6

## ข้อมูลและการป้องกันรั่ว

- กรองซื้อบ้าน, อยู่เอง, ไม่ใช่ธุรกิจ/reverse mortgage/open-end, Single Family 1–4 หน่วย; y=1 เมื่อ action_taken เป็น 1 หรือ 2, y=0 เมื่อเป็น 3 การอนุมัติคือผลที่ผู้ขอต้องการ
- แบ่ง stratified ตาม y × race_eth; การใช้ประชากรเพื่อออกแบบการประเมินแยกจากขั้นฝึก
- ตัดคอลัมน์หลังตัดสินใจทั้งหมดที่กำหนด เช่น action_taken, denial_reason-*, interest_rate, purchaser_type, ต้นทุน/ค่าธรรมเนียม และตัดประชากรทุกคอลัมน์ที่เกี่ยวกับ race/ethnicity/sex/age/observed
- ตรวจ missing/Exempt/NA gap ระหว่างอนุมัติและปฏิเสธ **บน train ของแต่ละ seed เท่านั้น** ถ้าเกิน 10 จุดเปอร์เซ็นต์ตัดคอลัมน์ออก เก็บการตัดสินใจทุกคอลัมน์ใน `leakage_audit.json` รายการตัวแปรที่ยอมให้ใช้เป็น whitelist ใน `hmda.py`; ไม่ใช้คอลัมน์อื่นโดยปริยาย
- `tract_minority_population_percent` ใช้ได้เฉพาะ `GDRO-geoproxy` ไม่เข้าโมเดล/SCARF/กฎอธิบาย หรือ baseline อื่น
- **HMDA สาธารณะไม่มีคะแนนเครดิต** `applicant_credit_score_type` เป็นประเภทวิธีคำนวณ ไม่ใช่คะแนนเครดิต
- เติม missing ด้วย median train; one-hot/หมวดหมู่หายาก/ผู้ให้กู้ top-30 และ scaler fit train เท่านั้น DTI ช่วงข้อความแปลงเป็นค่ากึ่งกลางมีลำดับ
- อายุผู้ขอเป็นข้อมูลอ่อนไหวที่ซ่อน ไม่สับสนกับอายุบ้านระดับพื้นที่
- race_eth = Hispanic (ทุกเชื้อชาติ), NH White, NH Black, NH Asian, Other; sex=Male/Female/Joint; age ตามช่วง HMDA; intersection=race_eth × sex
- Unknown/Not Available/Free Form Text Only อยู่ในข้อมูลฝึก ประเมิน fairness โดยตัดออกเฉพาะมิติที่ไม่ทราบ (Hispanic ที่ทราบ ethnicity จัดได้แม้ race ไม่ทราบ) กลุ่มเล็กกว่า 30 แถวตัดออกจาก fairness และรายงาน excluded_unknown_*/excluded_small_* ใน CSV แต่ไม่ตัดจาก accuracy รวม
- อัตรา missing ที่ต่างกันต่ำกว่าเกณฑ์ไม่ได้รับรองว่าปราศจากการรั่วทุกชนิด และ proxy ที่อนุญาต เช่น พื้นที่/ผู้ให้กู้อาจสัมพันธ์กับประชากร

## วิธีทดลองและการเลือก

ERM-LGBM, ERM-MLP, JTT, GEORGE, HBAC, GDRO-geoproxy, GDRO-random-k2/4/8, GDRO-raw-k2/4/8, GDRO-scarf-k2/4/8, GDRO-oracle รวม 16 ชื่อวิธีต่อ seed (DRO 13 วิธี × 4 รูปแบบ, baseline 3 วิธี) ใช้ full labels เพียงระดับเดียว ไม่มีการรัน label fraction ablation

MLP ทุกวิธีใช้ input/architecture เดียวกัน Group DRO ถ่วงค่าเฉลี่ย loss ต่อกลุ่มและอัปเดต exponentiated gradient JTT ระบุตัวอย่างผิดจากโมเดลรอบสั้น ค้น upweight [1,2,4] ด้วย inferred_worst_group พร้อม guard; กลุ่ม validation คือทายผิด/ถูกจากโมเดลรอบสั้น × y, normalize weighted loss และเลือก checkpoint บน validation ตรวจอัตราทายบวกเพื่อเตือน collapse ห้ามตีความ EO ต่ำจากการทายคลาสเดียวเป็นความสำเร็จ

รอบ 5 ทดลอง `cy`, `cy_bal`, `c`, `c_bal` ครบทุกวิธีที่มีกลุ่ม (ยกเว้น JTT ซึ่งคง baseline เดิม) โดย `cy` = cluster × y และ `c` = cluster อย่างเดียว ส่วน `_bal` ใช้ class-balanced BCE จาก train เท่านั้น raw/SCARF/GEORGE แบบ cy คง k-means ภายในคลาสตามรอบ 4 (k ต่อคลาส) ส่วน c fit k-means บน representation ทั้ง train โดยไม่รับ y (k รวม) โดยเฉพาะ GEORGE แบบ c รวมการจัดกลุ่มข้ามคลาสบน ERM hidden representation เดิม จึงเปลี่ยนทั้งองค์ประกอบและจำนวน cluster; ไม่ใช่การเทียบที่คง cluster ทุกอย่าง

| รูปแบบ | กลุ่มฝึก/validation | Loss |
|---|---|---|
| cy | cluster × y | BCE |
| cy_bal | cluster × y | class-balanced BCE ใน base cluster ก่อน cross y |
| c | cluster | BCE |
| c_bal | cluster | class-balanced BCE ภายในกลุ่มหลังรวมเล็ก |

น้ำหนัก `w_i=n_c/(m_c*n_cy)` โดย m_c เป็นจำนวนคลาสที่พบใน base cluster: มวลต่อคลาสเท่ากันและค่าเฉลี่ยน้ำหนัก=1 ใช้ `mean(w*BCE)` ใน DRO group ไม่หาร sum(w) ซ้ำหลัง cross y เพราะจะล้างผลของ class balance; หาก cluster มีคลาสเดียว w=1 ดังนั้น cy_bal ของ class-conditioned raw/SCARF/GEORGE/random อาจเท่ากับ cy โดยนิยาม เป็นข้อจำกัดที่รายงานอย่างชัดเจน ตรวจ `class_weight_min/max` ในผล CSV ไม่อ้างว่าเป็น ablation ที่ให้ข้อมูลเพิ่มทั้งสี่แถวในทุกวิธี

รวมกลุ่ม train <50 เข้าศูนย์กลางใกล้ที่สุด: cy ภายในคลาสเดียวกัน, c ไม่ใช้ y ส่วน oracle เป็น race_eth × sex สำหรับ c และ race_eth × sex × y สำหรับ cy; Unknown คงไว้ฝึกแต่ไม่ใช้ validation fairness oracle รายงานเกณฑ์ขนาดที่ใช้ในกริด กลุ่มบน validation ใช้นิยาม c/cy เดียวกับฝึก แต่คง cluster ก่อนรวมเล็กเพื่อไม่ซ่อนกลุ่มยาก

ทุก DRO warm-start จาก ERM-MLP average แล้วเลือกกริด/checkpoint ด้วย `inferred_worst_group` บน validation ของวิธีและนิยามนั้น พร้อม guard validation accuracy ≥ ERM-MLP −0.02 ถ้าไม่มีตัวผ่าน เลือก accuracy ใกล้เกณฑ์ที่สุด ตามด้วย inferred worst-group; เมื่อผ่าน guard ใช้ worst-group ตามด้วย accuracy ถ้าเสมอคงตัวแรก ERM ใช้ average; JTT ใช้กลุ่มผิด/ถูกจากโมเดลรอบสั้น × y ตามรอบ 4 ผลเสริม `average` และ `worst_group` (ใช้ประชากรจริง) ยังค้นแยกทั้งหมด

กริด eta={0.01,0.1} × C={0,1} × lr={0.0002,0.001} × งบ 5 epoch = 8 candidate ต่อ method/seed/variant ตัดงบ 3 ซ้ำเพราะทุก checkpoint 1–3 อยู่ในงบ 5 แล้ว; `dro_grid.csv` เก็บน้ำหนักกลุ่ม min/max ทั้งสุดท้ายและ checkpoint ที่เลือก พร้อมระยะพารามิเตอร์ L2 จาก ERM และ validation score/guard แยก variant

เลือก k และ raw/SCARF ด้วย Silhouette train แยกนิยาม c/cy จากนั้นเลือก variant ด้วย validation rank เดียวกัน ไม่ดูประชากรหรือ test; คะแนน worst-group ต่างนิยามต่างความยาก จึงอาจเข้าข้าง c ต้องระวังการตีความ ผลสรุปใน `variant_selection.csv` และ flag `proposed_variant_selected` ใช้หน้าสาธิต seed แรก; `proposed_selected` คือผู้ชนะ Silhouette ของแต่ละ variant (ยังมีสี่แถวต่อ seed) ส่วน `variant_selected_without_demographics` เลือก variant รายวิธี ไม่รวม oracle

เก็บรอบ 4 ไว้ `results/round4/` ก่อนรันใหม่ (รอบก่อนหน้าใน round2/round3) ตรวจ sanity oracle ≥ ERM-MLP ด้วยค่าเฉลี่ย test worst-group แยกรูปแบบ ไม่ซ่อนรูปแบบที่ไม่ผ่าน `oracle_sanity.csv` บันทึกราย seed และ `proposed_variant_effects.csv` เปรียบเทียบ accuracy/ช่องว่างกับ ERM ผล test เป็นเชิงสำรวจเพราะเคยเปิดดูหลายรอบ ต้อง holdout ใหม่; กริดรอบ 5 กำหนดก่อนรันและไม่ปรับจาก test รอบนี้

HBAC ใช้ `unsupervised_bias_detection.cluster.BiasAwareHierarchicalKMeans` ของแพ็กเกจ 0.2.6 บน train โดย bias metric = -OOF error จาก ERM-LGBM; แต่ละ fold fit leakage guard/preprocessor แยก สูงสุด 4 กลุ่ม ใช้ base cluster ร่วมทั้ง 4 รูปแบบ geoproxy ใช้ quantile ของ minority percent จาก train เฉพาะ baseline นี้ เป็นแนวคิดใช้พื้นที่อย่างเดียว ไม่ใช่ BISG ที่สมบูรณ์ ตัวแปรดังกล่าวไม่อยู่ใน input โมเดลตัดสินใจ

## คำอธิบายและตัวชี้วัด

ต้นไม้ one-vs-group ลึก ≤3 fit บน train จากตัวแปรเดิม (numeric หน่วยเดิมและ one-hot category) แปลงเส้นทางเป็น IF–THEN; วัด fidelity F1 และ coverage บน validation ความยาวกฎคือจำนวนเงื่อนไขรวมทุกเส้นทางบวก พร้อม max conditions per path จึงอาจเกิน 3 ในความยาวรวมได้

ฝึกต้นไม้ทั้ง `class_weight="balanced"` และไม่ถ่วงน้ำหนัก เลือก F1 บน validation ของป้าย cluster สูงกว่ารายกลุ่ม (เสมอเลือก balanced) บันทึก `surrogate_class_weight`, F1 ทั้งสองแบบ และ selection split โดยไม่ใช้ประชากร ทั้งสองแบบใช้ `min_samples_leaf=max(5,min(n_group,n_rest)//20)` เพิ่ม precision/recall บน validation ถ้า F1 <0.5 การ์ดเตือนว่าอธิบายได้ไม่ดีและแสดงตัวแปรต่างจากส่วนที่เหลือสูงสุด 5 ตัวจาก train: SMD=(mean_group−mean_rest)/√((var_group+var_rest)/2) สำหรับต่อเนื่อง หรือส่วนต่างสัดส่วนของหมวดที่ต่างมากที่สุดสำหรับตัวแปรกลุ่ม (นับ missing ด้วย) เรียงตามค่าสัมบูรณ์ เป็นการพรรณนาที่ไม่ได้ทำให้กฎผ่าน H2 โดยอัตโนมัติ สรุปมัธยฐาน F1 และสัดส่วน ≥0.80 แยกวิธี/รอบใน `fidelity_comparison.csv`

Welch t-test สำหรับต่อเนื่อง/χ² สำหรับหมวดหมู่ ใช้ test ที่ไม่ได้ fit cluster หรือกฎ ตามแนวคิด sample splitting; ปรับ Bonferroni ทั้ง family ของทุก seed/วิธี/กลุ่ม/ตัวแปรที่ส่งออก เป็นการสำรวจ ไม่ใช่หลักฐานเชิงสาเหตุและไม่ใช่ selective-inference guarantee ตัวแปรเดียวกันใช้กำหนด cluster จึงยังมี selection effects ได้ องค์ประกอบประชากร, ขนาด, อัตราอนุมัติจริง, ERM error, FPR/FNR วัดบน test; ไม่ส่งกลับไปเลือกโมเดล

Fairness หลักใช้ intersection: EO=max(ช่วง TPR,ช่วง FPR), demographic parity difference=ช่วงอัตราทายอนุมัติ, worst-group accuracy เพิ่ม approval-rate gap แยก race_eth/sex, ARI/NMI แยก race_eth/sex/age/intersection บน test หลังเลือกเสร็จ รายงาน precision/recall/F1/AUROC, Silhouette/DBI, เวลา/RSS/พารามิเตอร์/FLOPs FLOPs นับ Linear เท่านั้น ไม่ใช่ profiler CPU ทั้งระบบ; LGBM ใช้ tree/leaf count แทน Reconstruction error เป็น N/A สำหรับ SCARF ไม่มี decoder

## หน้าสาธิต

`src/fairgroups/demo.py` โหลด `results/demo_bundle.joblib` จาก seed แรก โดยเลือกวิธีเสนอด้วย Silhouette train แล้วเลือกรูปแบบด้วย validation; การ์ดตรงกับนิยาม c/cy ของรูปแบบที่เลือก ช่องหลัก 8 ตัวมีค่ากลาง/ฐานนิยม train; ตัวแปรที่ถูก leakage audit ตัดไม่แสดง และใช้ตัวแปรพื้นที่สำรองให้ครบ แสดงโอกาสอนุมัติ ERM เทียบ DRO, หมายเลขกลุ่ม และการ์ดอธิบายกลุ่มนั้น ความน่าจะเป็นยังไม่ calibrated และโมเดล DRO อาจไม่ลดอคติในผลจริง

ทดสอบ local โดยสร้าง interface และเรียก predict ไม่ launch ค้าง หากต้องการเปิดเอง:

```bash
PYTHONPATH=src ~/.venvs/rsu-fair/bin/python -m fairgroups.demo
```

## ไฟล์ผลและการติดตาม

- `results/hmda_pilot_results.csv`, `hmda_pilot_summary.md`: ผลทุกวิธีและสรุปจาก CSV เท่านั้น
- `clustering_results.csv`, `representation_resources.csv`, `alignment_fairness*.csv`, `jtt_validation_grid.csv`
- `dro_grid.csv`, `round_comparison.csv`, `fidelity_comparison.csv`: กริด DRO และผลก่อน/หลังปรับ; สำเนารอบ 2/3/4 อยู่ใน `results/round2/`, `results/round3/`, `results/round4/`; `oracle_sanity.csv` เก็บผล sanity จริง
- `variant_selection.csv`, `proposed_variant_effects.csv`, `figures/dro_variants.png`: ผลการเลือกรูปแบบและกราฟ accuracy vs approval gap แยก 4 รูปแบบ
- `group_cards.md`, `group_explanations.csv`, `group_feature_tests.csv`: คำอธิบายอัตโนมัติพร้อมผลทดสอบ
- `leakage_audit.json`, `data_profile.md`/`.csv`, `filter_counts.csv`, `environment.json`, `validation.json`, `figures/`
- `demo_bundle.joblib`: สถานะโมเดล/ตัวแปลง/กลุ่ม/ค่าตั้งต้นเพื่อเปิด demo อีกครั้ง

MLflow ใช้ `sqlite:///mlflow.db` เก็บ params/metrics/tags ไม่มี artifact รายรัน จำนวนไฟล์ใหม่ต้องไม่เกินประมาณ 200 (นับรวม AppleDouble ของ exFAT); ไม่ใช้ file store เดิม ตรวจ `environment.json` และ `validation.json` ขนาด SQLite อาจโตตามจำนวน runs เมื่อรันซ้ำ แต่ไม่แตกเป็นไฟล์ย่อยจำนวนมาก

ผล ACS รอบแรกเก็บไว้ใน `results/acs_round1/` ไม่ลบ โค้ด ACS ยังอยู่และเรียกได้ด้วย `--dataset acs`; ผลรันใหม่นี้ออก `results/acs_optional/` แยกจาก HMDA ไม่ใช่การทดลองหลักรอบนี้ ทดสอบด้วย pytest ครอบคลุมสูตร fairness/DRO, train-only fit, OOF, leakage guard, กลุ่มอ่อนไหว, JTT, SQLite, Gradio และ notebook fallback; หลักฐาน validation ระบุสิ่งที่รันจริง

## ผลตรวจรอบ 5 ในเครื่อง

QUICK ครบ 489 แถว / 60 clustering rows ใช้ 354.65 วินาที (5.91 นาที), peak RSS 1632.2 MiB และเพิ่ม 6 ไฟล์ระหว่างรัน Validation เลือก c ทั้ง 3 seed (SCARF k=2,4,2); accuracy ของวิธีเสนอลด 0.09 จุดร้อยละเทียบ ERM-MLP แต่ race approval gap และ EO ยังแย่กว่า จึงยังไม่มีรูปแบบที่ผ่านเป้าหมายรวม Sanity oracle ไม่ผ่านทั้ง 4 รูปแบบ รายละเอียดและข้อจำกัดใน `CODEX_REPORT_05.md` และ `results/hmda_pilot_summary.md` ข้อมูล Colab ที่ทดสอบสดยังเป็นรอบ 2

pytest ในโฟลเดอร์หลักผ่าน 34 tests; build_notebook ผ่าน 36 cells / 28 embedded files; check_delivery ผ่าน รวม fallback QUICK 326.26 วินาที และผลทำนาย/คำอธิบาย/กริดตรง main ทั้งหมด fallback post-pilot ผ่าน 33 tests และข้ามหลักฐาน ACS เก่า 1 test ซึ่งไม่ได้ฝังใน notebook โฟลเดอร์ว่าง ตรวจรายละเอียดใน `results/validation.json`

## รอบ 6: ปรับเกณฑ์รายกลุ่ม (post-processing)

เพิ่ม `src/fairgroups/postprocess.py` โดยใช้คะแนนจาก ERM-LGBM/ERM-MLP เดิม ไม่ติดตั้งแพ็กเกจเพิ่มและไม่พึ่ง fairlearn กลุ่ม raw/SCARF ใช้ global k-means แบบ c บน train (k=2,4,8); GEORGE เลือก k ด้วย silhouette train เดิม; HBAC/geoproxy ใช้กลุ่มเดิม ส่วน random-k ใช้ hash ของ x แบบมี seed เพื่อให้รายเดิมได้กลุ่มเดิมโดยไม่ใช้ป้าย/ข้อมูลประชากร

หา threshold บน validation เท่านั้น บังคับ accuracy ≥ ฐานเดียวกันที่ 0.5 − 0.02 และตรึงกลุ่ม validation <50 รายที่ 0.5 กลุ่มไม่เคยพบก็ใช้ 0.5 กริดรวม 0.05–0.95, quantile 101 จุด, 0.5 และเกณฑ์ปฏิเสธทั้งหมด เป้าหมาย parity ค้นช่วงอัตราอนุมัติด้วย bisection; EO ใช้ coordinate descent จากเกณฑ์เดิมและ parity จึงไม่รับรอง global optimum EO อัตราที่ไม่มีตัวหารไม่นับ

เลือกแยกฐาน/seed ด้วย validation approval gap ของกลุ่มค้นพบ ตามด้วย accuracy, EO และชื่อวิธี/เป้าหมายเมื่อเสมอ ตัวเลือก proposed จำกัด raw/SCARF; ตัวเลือก non-oracle รวม GEORGE/HBAC/geoproxy เพิ่มด้วย กัน random/oracle ออกจากการเลือกทั้งสองชุด PP-oracle ใช้ race_eth × sex ตอนหาเกณฑ์และทำนาย จึงเป็นเพดานบนเชิงกลไกที่ใช้จริงไม่ได้ Test ใช้ประชากรจริงวัดผลอย่างเดียว และ AUROC คำนวณจากคะแนนเดิม ส่วนตัวชี้วัดคำตัดสินใช้ผลหลังปรับเกณฑ์

- `results/round5/`: สำเนาผลรอบ 5 พร้อม `snapshot_sha256.json` สำหรับตรวจว่าไม่เปลี่ยน
- `results/postprocess_results.csv`, `postprocess_thresholds.csv`: ผลทุกวิธี/เป้าหมาย/ฐานและเกณฑ์ต่อกลุ่ม
- `results/postprocess_selection.csv`, `postprocess_selected_effects.csv`, `postprocess_sanity.csv`, `postprocess_audit.json`: ตัวที่เลือก ผลต่างจากฐาน sanity และ ID หลักฐาน validation-only
- `results/hmda_pilot_summary.md` หัวข้อ “ปรับเกณฑ์รายกลุ่ม” และ `results/figures/postprocess_tradeoff.png`: ตารางครบและกราฟ

รัน `run_pilot.py --quick` ตามคำสั่งเดิม จะคงการทดลอง DRO และเพิ่ม PP อัตโนมัติ หน้าสาธิตแสดง DRO เดิมพร้อมคะแนน LGBM เดิม เกณฑ์ กลุ่ม และคำตัดสิน PP จาก proposed ที่เลือกด้วย validation seed แรก ทุก PP run บันทึก MLflow SQLite โดยไม่มี artifact รายรัน เวลา/RSS ของขั้นหาเกณฑ์แยกจากฐาน และเวลา lookup เกณฑ์ไม่รวมคำนวณคะแนน/ค้นกลุ่ม

การลดช่องว่างของกลุ่มที่ค้นพบไม่รับรองการลดช่องว่างเชื้อชาติ/เพศจริง และ validation guard ไม่รับรอง test guard ผลเป็น exploratory เพราะใช้ test เดิมหลายรอบ ต้องยืนยันด้วย holdout ใหม่ ยังไม่ทดสอบ FULL/Colab รอบ 6 สด; notebook fallback ทดสอบในเครื่องด้วยแคชโดยไม่ติดตั้ง/ดาวน์โหลดใหม่ ดูผลจริงและเวลาใน `CODEX_REPORT_06.md` และ `results/validation.json`

## ผลตรวจรอบ 6 ในเครื่อง

QUICK จบ 412.55 วินาที (เพิ่มจากรอบ 5 57.90 วินาที); PP fit รวม 4.638 วินาที ครบ 162 แถวผล / 816 แถวเกณฑ์ วิธีเสนอที่เลือกด้วย validation เป็น raw-k2 / SCARF-k2 / raw-k2 ตาม seed 17/29/43 ทั้งสองฐาน และเลือก parity ทั้งหมด Approval gap race/sex ลดในค่าเฉลี่ยและ accuracy เฉลี่ยลดไม่เกิน 2 จุด แต่ EO/worst-group แย่ลง และ LGBM seed 43 เสีย test accuracy 2.1 จุด จึงยังไม่อ้างว่าผ่านเป้าหมายความเป็นธรรมทุกมิติ Oracle parity ลด race gap ครบทั้ง 3 seed ทั้งสองฐาน Random ให้ผลผสม รายละเอียดและตารางทุกวิธีอยู่ใน `CODEX_REPORT_06.md`

pytest ชุดหลักผ่าน 40 tests; notebook 39 cells / 31 embedded files; check_delivery ผ่าน รวม fallback QUICK 384.45 วินาที ผลทำนาย PP/เกณฑ์และ DRO/กริด/คำอธิบายตรงชุดหลักทั้งหมด fallback หลังรันผ่าน 39 tests ข้าม 1 test หลักฐาน ACS ที่ไม่ได้ฝังไว้ ตรวจสำเนารอบ 5 ด้วย SHA-256 และยืนยัน predictive metrics DRO เดิม 489 แถวตรงกันทั้งหมด เพิ่มไฟล์สุทธิเทียบรอบ 5 ที่บันทึกไว้ 109 ไฟล์รวมสำเนาแล้ว ดู `results/validation.json` ทั้งนี้ยังไม่ได้ทดสอบ Colab รอบ 6 สด

> หมายเหตุ: ใน GitHub เก็บหลักฐานกันข้อมูลรั่วเป็น `results/leakage_audit.json.gz` (ไฟล์เต็ม ~75 MB) — คลายด้วย `gunzip -k results/leakage_audit.json.gz` · เมื่อรัน `run_pilot.py` ใหม่จะสร้าง `leakage_audit.json` ขึ้นเองทุกครั้ง
