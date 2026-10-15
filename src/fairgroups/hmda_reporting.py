"""สร้างตารางผลจาก CSV เท่านั้น ไม่ใส่ค่าผลทดลองด้วยมือ"""
import os
from pathlib import Path
import pandas as pd
from .reporting import markdown_table


def generate_reports(output):
    output=Path(output); results=pd.read_csv(output/'hmda_pilot_results.csv')
    clusters=pd.read_csv(output/'clustering_results.csv'); explanations=pd.read_csv(output/'group_explanations.csv')
    resources=pd.read_csv(output/'representation_resources.csv'); jtt=pd.read_csv(output/'jtt_validation_grid.csv')
    main=results[results.selection=='average']
    baseline=results[results.method=='ERM-MLP'].set_index(['selection','seed'])
    inferred=results[results.representation.isin(['raw','scarf','GEORGE','HBAC','geoproxy'])].copy()
    inferred['eo_reduction']=inferred.apply(lambda r:baseline.loc[(r.selection,r.seed),'eo_gap']-r.eo_gap,axis=1)
    inferred['worst_group_gain']=inferred.apply(lambda r:r.worst_group_accuracy-baseline.loc[(r.selection,r.seed),'worst_group_accuracy'],axis=1)
    inferred.to_csv(output/'alignment_fairness.csv',index=False)
    correlations=[]
    for selection,part in inferred.groupby('selection'):
        for dim in ['race_eth','sex','age','intersection']:
            for metric in ['ari','nmi']:
                key=f'{metric}_{dim}'
                correlations.append({'selection':selection,'alignment':key,'n':len(part),
                                     'pearson_eo_reduction':part[key].corr(part.eo_reduction),
                                     'pearson_worst_group_gain':part[key].corr(part.worst_group_gain)})
    corr=pd.DataFrame(correlations);corr.to_csv(output/'alignment_fairness_correlations.csv',index=False)
    metrics=['accuracy','eo_gap','dp_difference','worst_group_accuracy','approval_rate_gap_race_eth','approval_rate_gap_sex','positive_rate']
    text=['# ผลนำร่อง HMDA','', 'ทุกตัวเลขในตารางอ่านจาก CSV; mean ± sample SD ข้าม seed · full labels เท่านั้น',
          'เกณฑ์ทำนาย 0.5 · EO/worst-group หลักใช้ race_eth × sex · Unknown ไม่นับ fairness; กลุ่มเล็กกว่า min_fair_group ไม่นับและบันทึกจำนวนใน CSV',
          '## ผลหลัก เลือก checkpoint ด้วย validation average accuracy','',markdown_table(main,['method'],metrics),'',
          '## วิธีที่เลือกโดยไม่ใช้ข้อมูลประชากร','',
          'เลือก k ภายใน raw/scarf/GEORGE ด้วย Silhouette train สูงสุด; เลือก raw หรือ SCARF จากคะแนนเดียวกัน ไม่ใช้ test และไม่ใช้ ARI/NMI หรือ fairness เลือก',
          'k หมายถึงต่อคลาสสำหรับ raw/scarf/GEORGE/random (รวม 2k กลุ่ม); HBAC ใช้สูงสุด 4 กลุ่มและ geoproxy ใช้ 4 quantile ที่กำหนดล่วงหน้า',
          markdown_table(main[main.selected_without_demographics],['representation','k'],metrics),'',
          'ตัวเลือกสุดท้ายของวิธีเสนอ (หนึ่งแถวต่อ seed):',
          markdown_table(main[main.proposed_selected],['seed','method'],metrics),'',
          '## การเลือกด้วย worst-group validation (ใช้ประชากรจริง; ผลเสริม)','',
          markdown_table(results[results.selection=='worst_group'],['method'],metrics),'',
          '## ความตรงกับประชากรบน test หลังเลือกเสร็จ','',
          'Silhouette/DBI ของ raw/scarf/GEORGE/HBAC วัด train; geoproxy วัด test เพื่อพรรณนาเท่านั้น ไม่ใช้เลือก',
          markdown_table(clusters,['representation','k'],['silhouette','davies_bouldin','ari_race_eth','nmi_race_eth','ari_sex','nmi_sex','ari_age','nmi_age','ari_intersection','nmi_intersection']),'',
          '## คำอธิบายกลุ่ม','',
          'ต้นไม้ลึกไม่เกิน 3 จากตัวแปรต้นเดิม; fidelity F1 และ coverage บน validation; t-test/χ² บน test อิสระจากการ fit กลุ่ม ปรับ Bonferroni ทั้ง family ทุกกลุ่ม/วิธี/seed/ตัวแปร',
          markdown_table(explanations,['method'],['fidelity_f1','rule_length','coverage','n_test','erm_error']),'',
          '## ความสัมพันธ์เชิงสำรวจกับการลดอคติเทียบ ERM-MLP','',
          markdown_table(corr,['selection','alignment'],['pearson_eo_reduction','pearson_worst_group_gain']),
          'แถว k ซ้ำและ seed ไม่เป็นอิสระทั้งหมด ค่าสหสัมพันธ์ไม่แสดงเหตุและผล','',
          '## ประสิทธิภาพระบบ','',
          markdown_table(results,['selection','method'],['train_seconds','inference_seconds_per_1000','peak_memory_mb','parameters','flops_per_row','tree_count','leaf_count']),'',
          'เวลาแต่ละวิธีรวม preprocessing/discovery ที่ใช้ร่วมกัน จึงห้ามรวมแถวเป็นเวลาทั้งชุด; FLOPs นับเฉพาะ Linear ของโมเดลตัดสินใจ; ต้นไม้รายงานจำนวนต้น/ใบแทน',
          markdown_table(resources,['representation'],['discovery_train_seconds','peak_memory_mb','parameters','flops_per_row']),'',
          '## ตรวจ JTT','',markdown_table(jtt,['seed','upweight'],['validation_accuracy','positive_rate']),
          'กริดเลือกด้วย validation average accuracy เท่านั้น; normalized weighted loss และ checkpoint เลือกก่อนประเมิน test',
          '## ข้อจำกัด','',
          '- HMDA สาธารณะไม่มีคะแนนเครดิต; applicant_credit_score_type เป็นประเภทวิธีคำนวณ ไม่ใช่คะแนน',
          '- อัตราอนุมัติสูง: accuracy/EO ต่ำอาจเกิดจากทายอนุมัติแทบทั้งหมด อ่าน positive_rate, F1, AUROC และข้อเตือนร่วมกัน',
          '- EO ของ intersection อาจไวต่อกลุ่มที่มีตัวอย่างปฏิเสธน้อย แม้ผ่านเกณฑ์ขนาดรวม 30 แถว จึงยังไม่ใช่ข้อสรุปที่แน่นอน',
          '- จัดกลุ่มภายในคลาสใช้ y บน train ตามวิธี GEORGE; ตอนใช้จริงหาศูนย์กลางใกล้สุดข้ามคลาสโดยไม่รู้ y จึงอาจสอดคล้องกับกลุ่มฝึกไม่สมบูรณ์',
          '- oracle ใช้ประชากร train เป็นเพดานเทียบ มี Unknown เป็นกลุ่มแยก ไม่ใช่วิธีที่เสนอ',
          '- การทดสอบตัวแปรเป็นเชิงสำรวจ; การแก้หลายการทดสอบไม่ได้ขจัดปัญหา cluster ที่นิยามจากตัวแปรเดียวกัน',
          '- ยังไม่ได้รัน Colab จริงหรือ FULL; QUICK ใช้ epochs น้อย ไม่รับประกันประโยชน์ด้าน fairness',
          '- Gradio ใช้ค่ากลาง/ฐานนิยม train เติมช่องที่ไม่ได้กรอก ผลเป็นต้นแบบวิจัยเท่านั้น','']
    collapsed=main[(main.method=='JTT') & ((main.positive_rate>=.995)|(main.positive_rate<=.005))]
    if len(collapsed): text.append('คำเตือน JTT ทายข้างเดียวใน test: '+', '.join(str(v) for v in collapsed.seed))
    (output/'hmda_pilot_summary.md').write_text('\n'.join(text),encoding='utf-8')
    os.environ.setdefault('MPLCONFIGDIR',str(output/'.matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    figs=output/'figures';figs.mkdir(exist_ok=True)
    for selection,part in results.groupby('selection'):
        fig,ax=plt.subplots(figsize=(10,6))
        for method,g in part.groupby('method'):
            ax.errorbar(g.eo_gap.mean(),g.accuracy.mean(),xerr=g.eo_gap.std(),yerr=g.accuracy.std(),fmt='o',label=method)
        ax.set(xlabel='EO gap',ylabel='Accuracy',title=selection);ax.legend(fontsize=7,loc='center left',bbox_to_anchor=(1,0.5))
        fig.tight_layout();fig.savefig(figs/f'accuracy_eo_{selection}.png',dpi=140);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for rep,g in clusters.groupby('representation'):
        axes[0].scatter(g.ari_intersection,g.nmi_intersection,label=rep)
    axes[0].set(xlabel='ARI intersection',ylabel='NMI intersection');axes[0].legend(fontsize=7)
    for method,g in explanations.groupby('method'):
        axes[1].scatter(g.coverage,g.fidelity_f1,label=method)
    axes[1].set(xlabel='Validation rule coverage',ylabel='Validation fidelity F1');axes[1].legend(fontsize=6)
    fig.tight_layout();fig.savefig(figs/'alignment_explanations.png',dpi=140);plt.close(fig)
