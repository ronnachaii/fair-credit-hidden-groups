"""สรุปรอบ 6 จาก CSV และคงรายงาน DRO เดิมไว้"""
import pandas as pd
from .reporting import markdown_table

METRICS = ['accuracy', 'f1', 'auroc', 'positive_rate', 'approval_rate_gap_race_eth',
           'approval_rate_gap_sex', 'eo_gap', 'worst_group_accuracy']


def sanity_table(frame):
    baseline=frame[frame.objective.eq('baseline')].set_index(['base','seed'])
    rows=[]
    for r in frame[(frame.objective.eq('parity') & frame.representation.eq('oracle')) |
                   frame.representation.eq('random') | frame.proposed_selected].itertuples():
        ref=baseline.loc[(r.base,r.seed)]
        rows.append({'base':r.base,'seed':r.seed,'method':r.method,'objective':r.objective,
            'representation':r.representation,'race_gap_reduction':ref.approval_rate_gap_race_eth-r.approval_rate_gap_race_eth,
            'accuracy_delta':r.accuracy-ref.accuracy,
            'race_gap_reduced':r.approval_rate_gap_race_eth < ref.approval_rate_gap_race_eth})
    return pd.DataFrame(rows)


def generate_postprocess_report(output):
    frame=pd.read_csv(output/'postprocess_results.csv')
    selected=frame[frame.proposed_selected | frame.selected_without_demographics].copy()
    selected.to_csv(output/'postprocess_selection.csv',index=False)
    sanity=sanity_table(frame);sanity.to_csv(output/'postprocess_sanity.csv',index=False)
    proposed=frame[frame.proposed_selected].copy();proposed['method']='Proposed (validation)'
    deployed=frame[frame.selected_without_demographics].copy();deployed['method']='Selected non-oracle (validation)'
    comparison=pd.concat([frame,proposed,deployed],ignore_index=True)
    # ตัวที่เลือกอาจต่าง objective ข้าม seed จึงรวมเป็นแถวเดียวต่อฐาน
    comparison.loc[comparison.method.isin(['Proposed (validation)','Selected non-oracle (validation)']),'objective']='selected'
    baseline=frame[frame.objective.eq('baseline')].set_index(['base','seed'])
    effects=[]
    for r in frame[frame.proposed_selected].itertuples():
        ref=baseline.loc[(r.base,r.seed)]
        effects.append({'base':r.base,'seed':r.seed,'method':r.method,'objective':r.objective,
            **{f'delta_{m}':getattr(r,m)-ref[m] for m in METRICS}})
    effects=pd.DataFrame(effects);effects.to_csv(output/'postprocess_selected_effects.csv',index=False)
    pp=frame[~frame.objective.eq('baseline')]
    text=['## ปรับเกณฑ์รายกลุ่ม','',
        'รอบ 6 เพิ่ม PP บนคะแนน ERM-LGBM/ERM-MLP ที่เลือก checkpoint ด้วย validation average accuracy เดิม; ไม่ฝึกฐานใหม่เพื่อ PP',
        'ทุกตารางอ่านจาก CSV; mean ± sample SD ข้าม seed; gap ใช้หน่วยสัดส่วน (0.01 = 1 จุดร้อยละ)',
        '- raw/SCARF ใช้ global cluster c ที่ fit train เท่านั้น k=2,4,8; GEORGE ใช้ hidden ERM และเลือก k ด้วย silhouette train; HBAC ใช้ OOF error train; geoproxy ใช้สัดส่วนประชากรระดับพื้นที่ (เป็น baseline ที่อาศัย proxy เชื้อชาติ)',
        '- random-k ใช้ hash แบบมี seed ของ x ที่แปลงแล้ว mod k ไม่ใช้ y/ประชากร และให้กลุ่มเดิมได้ตอนอนุมาน; รวม k=2,4,8 เทียบขนาดกลุ่ม raw/SCARF; ไม่รับรองว่ากลุ่มสุ่มจะไร้ความสัมพันธ์โดยบังเอิญในชุดเล็ก',
        '- PP-oracle ใช้ race_eth × sex ตอนหาเกณฑ์และตอนทำนาย เป็นเพดานบนเชิงกลไกเท่านั้น ไม่ใช่วิธีใช้จริง; Unknown เป็นกลุ่มแยกในการ fit แต่ไม่นับ fairness ตามกฎเดิม',
        '- เกณฑ์ fit เฉพาะ validation: กริด 0.05–0.95 ทีละ 0.01 รวม quantile 101 จุด, 0.5 และเกณฑ์ปฏิเสธทั้งหมด; กลุ่ม validation < min_dro_group=50 ถูกตรึง 0.5; กลุ่มใหม่ไม่พบใช้ 0.5',
        '- Parity ค้นช่วงอัตราอนุมัติด้วย bisection 20 ครั้ง เลือกจำนวนทายถูกสูงสุดที่ทำได้ในแต่ละช่วง; หาช่องว่างต่ำสุดบนกริดภายในความละเอียดประมาณ 1e-6',
        '- EO ลด max(TPR gap,FPR gap) ด้วย coordinate descent ไม่เกิน 10 sweeps เริ่มทั้ง 0.5 และ parity; ไม่รับรอง global optimum; อัตราที่ไม่มีตัวหารไม่นับ',
        '- ทั้งสองเป้าหมายบังคับ validation accuracy ≥ ฐานเดียวกันที่ threshold 0.5 − 0.02; มีเกณฑ์เดิมเป็น feasible fallback เสมอ จึงไม่ต้องเลือกตัวที่ตก guard',
        '- เลือกแยกแต่ละฐาน/seed จาก validation approval gap ระหว่างกลุ่มค้นพบ ตามด้วย accuracy สูงกว่า, EO ต่ำกว่า, ชื่อวิธี/เป้าหมายเมื่อเสมอ; ไม่ใช้ test หรือประชากรจริงเลือก',
        '- รายงานตัวเลือกสองชุด: proposed จำกัด raw/SCARF และตัวเลือก non-oracle รวม raw/SCARF/GEORGE/HBAC/geoproxy; random และ oracle ถูกกันออกจากการเลือกทั้งสองชุด',
        '- test ใช้ประชากรจริงเพื่อประเมินเท่านั้น; accuracy/F1/positive rate/EO ใช้คำตัดสินหลังปรับเกณฑ์ แต่ AUROC ใช้คะแนนเดิม จึงเท่าฐานทุกวิธีภายใน seed',
        '### ERM เทียบ PP ทุกวิธีและทุกเป้าหมาย (เฉลี่ย 3 seed ใน QUICK)','',
        markdown_table(comparison,['base','method','objective'],METRICS),'',
        '### ตัวที่เลือกด้วย validation แยกตาม seed','',
        markdown_table(selected,['base','seed','method','objective'],['proposed_selected',
            'selected_without_demographics','validation_approval_gap','validation_accuracy',
            'validation_accuracy_floor','accuracy_guard_passed',*METRICS]),'',
        '### ผลของวิธีเสนอที่เลือกแล้ว เทียบฐานเดียวกัน','',
        markdown_table(effects,['base'],[f'delta_{m}' for m in METRICS]),'',
        '### Sanity checks','',
        markdown_table(sanity,['base','method','objective'],['race_gap_reduction','accuracy_delta','race_gap_reduced'])]
    for base,part in sanity[sanity.representation.eq('oracle')].groupby('base'):
        passed=part.race_gap_reduction.mean()>0
        text.append(f"- oracle parity {base}: {'ผ่าน' if passed else 'ไม่ผ่าน'}; mean race gap reduction={part.race_gap_reduction.mean():.6f}; seed ลดได้ {int(part.race_gap_reduced.sum())}/{len(part)}")
    for base,part in effects.groupby('base'):
        failed=part[part.delta_accuracy < -.02-1e-12]
        text.append(f"- proposed {base}: mean test accuracy delta={part.delta_accuracy.mean():.6f}; test ลดเกิน 2 จุดร้อยละ {len(failed)}/{len(part)} seed (seed={failed.seed.tolist()}); validation guard ของตัวที่เลือกผ่านครบ")
    random=sanity[sanity.representation.eq('random')]
    for (base,objective),part in random.groupby(['base','objective']):
        text.append(f'- random {objective} {base}: mean race gap reduction={part.race_gap_reduction.mean():.6f}; ลดได้ {int(part.race_gap_reduced.sum())}/{len(part)} คู่ seed/k; ข้อมูลซ้ำข้าม k ไม่ใช่ตัวอย่างอิสระ จึงยังยืนยันการลดอย่างเป็นระบบไม่ได้')
    text.extend(['วิธีเสนอเทียบ random/oracle อ่านจากตารางเดียวกัน แยกฐานและเป้าหมาย; ห้ามเลือก k ของ random ด้วย test เพื่อทำคู่เทียบ',
        '### เวลาและหน่วยความจำเฉพาะขั้นปรับเกณฑ์','',
        markdown_table(pp,['base','method','objective'],['threshold_fit_seconds',
            'threshold_inference_seconds_per_1000','threshold_peak_process_rss_mb','threshold_peak_rss_increase_mb',
            'n_frozen_small_groups']),
        f"เวลารวม fit ทุกเกณฑ์ = {pp.threshold_fit_seconds.sum():.3f} วินาที; peak RSS process = {pp.threshold_peak_process_rss_mb.max():.2f} MiB; RSS เพิ่มสูงสุดระหว่าง fit = {pp.threshold_peak_rss_increase_mb.max():.2f} MiB",
        'RSS สุ่มทุก 10 ms รวม process ของฐานเดิม ไม่ใช่ขนาดโมเดล PP; เวลาอนุมาน PP นับเฉพาะ lookup/เปรียบเทียบเกณฑ์ ไม่รวมคำนวณคะแนนและค้นกลุ่มซึ่งใช้ pipeline เดิม',
        '### ข้อจำกัดรอบ 6','',
        '- guard เป็นเงื่อนไขบน validation ไม่รับรองว่า test accuracy จะลดไม่เกิน 2 จุด; การเลือกและ fit เกณฑ์บน validation เดียวกันอาจ optimistic',
        '- การทำ parity ของกลุ่มที่ค้นพบไม่รับรอง parity ของเชื้อชาติ/เพศจริง; ความตรงของกลุ่มเดิมต่ำ และ EO อาจแย่ลงแม้ approval gap ลด',
        '- random มีเพียง 3 seed และกลุ่มเล็กถูกตรึง 0.5 จึงไม่มีข้อรับรองเชิงสถิติ; oracle อาจยังมีช่องว่าง test จาก sampling/guard/กลุ่มเล็ก',
        '- test ชุดเดิมถูกเปิดดูหลายรอบ ผลทั้งหมดเป็น exploratory ต้องยืนยันด้วย holdout ใหม่; ไม่รัน FULL หรือทดสอบ Colab รอบ 6 สด; notebook fallback รันในเครื่องด้วยแคช ไม่ทดสอบติดตั้ง/เครือข่าย',
        '- หน้าสาธิตคงผล DRO เดิมและเพิ่มผล PP จากฐาน LGBM ของ proposed ที่เลือกด้วย validation seed แรก; คะแนนเดิมไม่เปลี่ยน มีเพียงเกณฑ์และคำตัดสินเปลี่ยน',''])
    summary=output/'hmda_pilot_summary.md'
    previous=summary.read_text().split('## ปรับเกณฑ์รายกลุ่ม')[0].rstrip()
    summary.write_text(previous+'\n\n'+'\n'.join(text),encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(15,6),sharex=True,sharey=True)
    for ax,base in zip(axes,['ERM-LGBM','ERM-MLP']):
        for (method,objective),part in comparison[comparison.base.eq(base)].groupby(['method','objective']):
            mark='*' if objective=='selected' else 'X' if objective=='baseline' else 'o' if objective=='parity' else '^'
            ax.scatter(part.approval_rate_gap_race_eth.mean(),part.accuracy.mean(),marker=mark,
                s=130 if mark in ['*','X'] else 35,label=f'{method}/{objective}',alpha=.8)
        ax.set(title=base,xlabel='Approval-rate gap: race/ethnicity',ylabel='Accuracy');ax.grid(alpha=.2)
    axes[-1].legend(fontsize=6,loc='center left',bbox_to_anchor=(1,.5))
    fig.tight_layout();fig.savefig(output/'figures/postprocess_tradeoff.png',dpi=140);plt.close(fig)
