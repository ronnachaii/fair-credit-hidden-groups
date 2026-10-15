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

ดูเวลาที่วัดจริงใน `results/environment.json` เป้าหมาย QUICK ประมาณไม่เกิน 20 นาทีบน CPU; **ยังไม่ได้ยืนยันการรัน Colab จริง** เวลาดาวน์โหลด/ติดตั้งขึ้นกับเครือข่าย เซลล์ท้ายเปิด Gradio ด้วย `launch(share=True)`

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

ERM-LGBM, ERM-MLP, JTT, GEORGE, HBAC, GDRO-geoproxy, GDRO-random-k2/4/8, GDRO-raw-k2/4/8, GDRO-scarf-k2/4/8, GDRO-oracle รวม 16 วิธีต่อ seed ใช้ full labels เพียงระดับเดียว ไม่มีการรัน label fraction ablation

MLP ทุกวิธีใช้ input/architecture เดียวกัน Group DRO ถ่วงค่าเฉลี่ย loss ต่อกลุ่มและอัปเดต exponentiated gradient JTT ระบุตัวอย่างผิดจากโมเดลรอบสั้น ค้น upweight [1,2,4] ด้วย validation average accuracy, normalize weighted loss และเลือก checkpoint บน validation ตรวจอัตราทายบวกเพื่อเตือน collapse ห้ามตีความ EO ต่ำจากการทายคลาสเดียวเป็นความสำเร็จ

GEORGE ใช้ hidden representation ของ ERM-MLP และ k-means ภายในแต่ละคลาส raw/SCARF ทำเช่นเดียวกัน **k ต่อคลาส จึงมี 2k กลุ่มรวม** ตอนใช้กับ validation/test/ผู้ขอรายใหม่ไม่มี y จึงเลือกศูนย์กลางที่ใกล้ที่สุดข้ามคลาส กลุ่มจากวิธีนี้อาจทำนายไม่ตรงกับการจัดกลุ่ม train ที่รู้ y; รายงาน fidelity เพื่อสะท้อนข้อจำกัด

HBAC ใช้ `unsupervised_bias_detection.cluster.BiasAwareHierarchicalKMeans` ของแพ็กเกจ 0.2.6 (ชื่อโมดูลจริงคือ `cluster`) ใช้ OOF classification error ของ ERM-LGBM บน train เป็น bias metric; แต่ละ fold fit missing-gap guard และ preprocessor แยก ส่งค่า -error ให้แพ็กเกจเพราะ API ถือ metric ต่ำว่าถูกเลือกปฏิบัติ แบ่งกลุ่มที่ metric กระจายมากสุดซ้ำ ๆ สูงสุด 4 กลุ่ม ไม่มี fallback ในผลที่ส่งเพราะแพ็กเกจใช้ได้

geoproxy แบ่ง quartile ของ minority percent บน train แนวคิดใช้พื้นที่อย่างเดียว **ไม่ใช่ BISG ที่สมบูรณ์** random-k สุ่ม k กลุ่มภายในแต่ละคลาส (รวม 2k) เพื่อควบคุมจำนวนกลุ่มและการใช้ y ให้ตรงกับ raw/SCARF/GEORGE oracle ใช้ race_eth × sex บน train (Unknown เป็นกลุ่มแยก) เป็นเพดานเทียบเท่านั้น

กติกาหลักเลือก checkpoint/จำนวนต้น/ค่า JTT ด้วย **validation average accuracy** ไม่ใช้ประชากร; ผลที่เลือกด้วย worst-group validation แสดงแยกและระบุว่าใช้ประชากร การเลือก k=2,4,8 และ raw/SCARF ใช้ **Silhouette train สูงสุด** เพราะวัดการแยกกลุ่มโดยไม่อาศัยข้อมูลประชากรหรือ fairness GEORGE เลือก k ด้วยกติกาเดียวกัน HBAC/geoproxy กำหนดสูงสุด 4 กลุ่มล่วงหน้า ตารางแสดงทุก k แยกจากตัวเลือกสุดท้ายหนึ่งวิธีต่อ seed ขนาดข้อมูลเป็น quick เท่านั้น ไม่ใช่ข้อสรุปว่า representation ดีที่สุดบนข้อมูลภายนอก

## คำอธิบายและตัวชี้วัด

ต้นไม้ one-vs-group ลึก ≤3 fit บน train จากตัวแปรเดิม (numeric หน่วยเดิมและ one-hot category) แปลงเส้นทางเป็น IF–THEN; วัด fidelity F1 และ coverage บน validation ความยาวกฎคือจำนวนเงื่อนไขรวมทุกเส้นทางบวก พร้อม max conditions per path จึงอาจเกิน 3 ในความยาวรวมได้

Welch t-test สำหรับต่อเนื่อง/χ² สำหรับหมวดหมู่ ใช้ test ที่ไม่ได้ fit cluster หรือกฎ ตามแนวคิด sample splitting; ปรับ Bonferroni ทั้ง family ของทุก seed/วิธี/กลุ่ม/ตัวแปรที่ส่งออก เป็นการสำรวจ ไม่ใช่หลักฐานเชิงสาเหตุและไม่ใช่ selective-inference guarantee ตัวแปรเดียวกันใช้กำหนด cluster จึงยังมี selection effects ได้ องค์ประกอบประชากร, ขนาด, อัตราอนุมัติจริง, ERM error, FPR/FNR วัดบน test; ไม่ส่งกลับไปเลือกโมเดล

Fairness หลักใช้ intersection: EO=max(ช่วง TPR,ช่วง FPR), demographic parity difference=ช่วงอัตราทายอนุมัติ, worst-group accuracy เพิ่ม approval-rate gap แยก race_eth/sex, ARI/NMI แยก race_eth/sex/age/intersection บน test หลังเลือกเสร็จ รายงาน precision/recall/F1/AUROC, Silhouette/DBI, เวลา/RSS/พารามิเตอร์/FLOPs FLOPs นับ Linear เท่านั้น ไม่ใช่ profiler CPU ทั้งระบบ; LGBM ใช้ tree/leaf count แทน Reconstruction error เป็น N/A สำหรับ SCARF ไม่มี decoder

## หน้าสาธิต

`src/fairgroups/demo.py` โหลด `results/demo_bundle.joblib` จาก seed แรกและวิธีเสนอที่เลือกด้วย Silhouette train ช่องหลัก 8 ตัวมีค่ากลาง/ฐานนิยม train; ตัวแปรที่ถูก leakage audit ตัดไม่แสดง และใช้ตัวแปรพื้นที่สำรองให้ครบ แสดงโอกาสอนุมัติ ERM เทียบ DRO, หมายเลขกลุ่ม และการ์ดอธิบายกลุ่มนั้น ความน่าจะเป็นยังไม่ calibrated และโมเดล DRO อาจไม่ลดอคติในผลจริง

ทดสอบ local โดยสร้าง interface และเรียก predict ไม่ launch ค้าง หากต้องการเปิดเอง:

```bash
PYTHONPATH=src ~/.venvs/rsu-fair/bin/python -m fairgroups.demo
```

## ไฟล์ผลและการติดตาม

- `results/hmda_pilot_results.csv`, `hmda_pilot_summary.md`: ผลทุกวิธีและสรุปจาก CSV เท่านั้น
- `clustering_results.csv`, `representation_resources.csv`, `alignment_fairness*.csv`, `jtt_validation_grid.csv`
- `group_cards.md`, `group_explanations.csv`, `group_feature_tests.csv`: คำอธิบายอัตโนมัติพร้อมผลทดสอบ
- `leakage_audit.json`, `data_profile.md`/`.csv`, `filter_counts.csv`, `environment.json`, `validation.json`, `figures/`
- `demo_bundle.joblib`: สถานะโมเดล/ตัวแปลง/กลุ่ม/ค่าตั้งต้นเพื่อเปิด demo อีกครั้ง

MLflow ใช้ `sqlite:///mlflow.db` เก็บ params/metrics/tags ไม่มี artifact รายรัน จำนวนไฟล์ใหม่ต้องไม่เกินประมาณ 200 (นับรวม AppleDouble ของ exFAT); ไม่ใช้ file store เดิม ตรวจ `environment.json` และ `validation.json` ขนาด SQLite อาจโตตามจำนวน runs เมื่อรันซ้ำ แต่ไม่แตกเป็นไฟล์ย่อยจำนวนมาก

ผล ACS รอบแรกเก็บไว้ใน `results/acs_round1/` ไม่ลบ โค้ด ACS ยังอยู่และเรียกได้ด้วย `--dataset acs`; ผลรันใหม่นี้ออก `results/acs_optional/` แยกจาก HMDA ไม่ใช่การทดลองหลักรอบนี้ ทดสอบด้วย pytest ครอบคลุมสูตร fairness/DRO, train-only fit, OOF, leakage guard, กลุ่มอ่อนไหว, JTT, SQLite, Gradio และ notebook fallback; หลักฐาน validation ระบุสิ่งที่รันจริง
