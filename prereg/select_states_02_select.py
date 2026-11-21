"""ใช้เกณฑ์ C1-C5 และเลือกรัฐแบบ farthest-point (ระยะ total variation ของสัดส่วนเชื้อชาติ/ชาติพันธุ์ที่ทราบ 5 กลุ่ม) เริ่มจาก GA
ตัดสินเสมอด้วยรหัสรัฐเรียงตัวอักษร  ใช้: python -I เลือกรัฐ_02_select.py --prof <โฟลเดอร์ผล> --n23 state_n.json --n24 state_n24.json
state_n*.json = {รัฐ: จำนวนใบคำขอซื้อบ้านที่ actions_taken 1-3 จาก aggregations API ปี 2023/2024}"""
import argparse, glob, json
import numpy as np, pandas as pd
ap = argparse.ArgumentParser(); ap.add_argument("--prof", required=True); ap.add_argument("--n23", required=True)
ap.add_argument("--n24", required=True); ap.add_argument("--k", type=int, default=3)
a = ap.parse_args()
prof = {}
for f in glob.glob(f"{a.prof}/profile_*_2023.json"):
    r = json.load(open(f)); prof[r["state"]] = r
n23, n24 = json.load(open(a.n23)), json.load(open(a.n24))
G = ['NH White', 'NH Black', 'Hispanic', 'NH Asian', 'Other']
def comp(s):
    v = np.array([prof[s]['race_share'].get(g, 0) for g in G]); return v / v.sum()
tv = lambda x, y: 0.5 * np.abs(comp(x) - comp(y)).sum()
rows = []
for s, p in prof.items():
    est24 = p['filtered'] * n24[s] / n23[s]  # ประมาณจำนวนกรองปี 2567 จากอัตราส่วนจำนวนดิบ (ต้องยืนยันตอนดาวน์โหลดจริง)
    ok = dict(C1=p['filtered'] >= 100000 and est24 >= 100000, C2=p['cells_lt150'] == 0,
              C4=p['n_lei'] >= 100 and p['top1_lei_share'] <= 0.20, C5=p['unknown_race_share'] <= 0.30)
    rows.append(dict(state=s, filtered_2023=p['filtered'], est_filtered_2024=round(est24), unknown_race=round(p['unknown_race_share'], 3),
                     min_cell=p['min_cell'], n_lei=p['n_lei'], top1_lei=round(p['top1_lei_share'], 3), **ok, all_ok=all(ok.values()),
                     **{g: round(float(x), 3) for g, x in zip(G, comp(s))}, TV_vs_GA=round(tv(s, 'GA'), 3)))
df = pd.DataFrame(rows).set_index('state').sort_values('filtered_2023', ascending=False)
cand = sorted(s for s in df.index if df.loc[s, 'all_ok'] and s != 'GA'); chosen = ['GA']
for i in range(a.k):
    pick = sorted(cand, key=lambda s: (-min(tv(s, c) for c in chosen), s))[0]
    print(f"เลือกลำดับ {i+1}: {pick}  (ระยะ TV ต่ำสุดถึงรัฐที่เลือกแล้ว = {min(tv(pick, c) for c in chosen):.3f})")
    chosen.append(pick); cand.remove(pick)
df.to_csv(f"{a.prof}/เลือกรัฐ_ผลโปรไฟล์.csv", encoding="utf-8-sig")
print(df.to_string())
