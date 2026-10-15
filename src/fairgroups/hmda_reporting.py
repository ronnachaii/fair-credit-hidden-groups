"""สร้างตารางและกราฟ ablation จาก CSV เท่านั้น ไม่ใช้ test เลือกวิธี"""
import os
from pathlib import Path
import pandas as pd
from .reporting import markdown_table

METRICS=['accuracy','positive_rate','approval_rate_gap_race_eth','approval_rate_gap_sex',
         'eo_gap','worst_group_accuracy']


def main_rows(results):
    """ERM ใช้ average; JTT และ DRO ใช้ inferred_worst_group"""
    erm=results.method.isin(['ERM-LGBM','ERM-MLP'])
    return results[(erm & results.selection.eq('average')) |
                   (~erm & results.selection.eq('inferred_worst_group'))].copy()


def oracle_sanity(results):
    """แยกตาม variant; ตรวจหลังเลือกแล้วและคงผลล้มเหลวไว้"""
    main=main_rows(results)
    erm=main[main.method.eq('ERM-MLP')].set_index('seed').worst_group_accuracy
    rows=[]
    oracle=main[main.method.eq('GDRO-oracle')]
    if 'dro_variant' not in oracle: oracle=oracle.assign(dro_variant='cy')
    for variant,part in oracle.groupby('dro_variant',sort=False):
        assert set(erm.index)==set(part.seed)
        for r in part.itertuples():
            rows.append({'dro_variant':variant,'seed':r.seed,'erm_worst_group':erm.loc[r.seed],
                         'oracle_worst_group':r.worst_group_accuracy,'gain':r.worst_group_accuracy-erm.loc[r.seed]})
    sanity=pd.DataFrame(rows)
    status=sanity.groupby('dro_variant').gain.mean().ge(-1e-12).to_dict()
    gains=sanity.groupby('dro_variant').gain.mean().to_dict()
    return sanity,status,gains


def tuning_tables(output):
    """เก็บประวัติรอบเก่าแยกจาก ablation รอบนี้"""
    fidelity=[];comparison=[]
    for name,folder in [(f'round{i}',output/f'round{i}') for i in [2,3,4]]+[('round5',output)]:
        path=folder/'group_explanations.csv'
        if path.exists():
            frame=pd.read_csv(path)
            for method,part in [('ทุกวิธี',frame),*list(frame.groupby('method'))]:
                fidelity.append({'round':name,'method':method,'n_groups':len(part),
                    'median_fidelity_f1':part.fidelity_f1.median(),'fraction_f1_ge_080':part.fidelity_f1.ge(.8).mean(),
                    'n_f1_below_050':int(part.fidelity_f1.lt(.5).sum())})
        path=folder/'hmda_pilot_results.csv'
        if path.exists():
            frame=pd.read_csv(path)
            main=main_rows(frame) if name in ['round4','round5'] else frame[frame.selection.eq('average')].copy()
            if 'dro_variant' not in main: main['dro_variant']='legacy'
            proposed=main[main.proposed_selected].copy();proposed['method']='Proposed (Silhouette)'
            main=pd.concat([main,proposed],ignore_index=True);main['round']=name
            comparison.append(main[['round','seed','method','dro_variant',*METRICS]])
    fidelity=pd.DataFrame(fidelity);fidelity.to_csv(output/'fidelity_comparison.csv',index=False)
    comparison=pd.concat(comparison,ignore_index=True);comparison.to_csv(output/'round_comparison.csv',index=False)
    return fidelity,comparison


def generate_reports(output):
    output=Path(output)
    results=pd.read_csv(output/'hmda_pilot_results.csv');main=main_rows(results)
    clusters=pd.read_csv(output/'clustering_results.csv');cards=pd.read_csv(output/'group_explanations.csv')
    resources=pd.read_csv(output/'representation_resources.csv');grid=pd.read_csv(output/'dro_grid.csv')
    proposed=main[main.proposed_selected].copy();proposed['method']='Proposed (Silhouette)'
    comparison=pd.concat([main,proposed],ignore_index=True)
    baseline=main[main.method.eq('ERM-MLP')].set_index('seed')
    sanity,status,gains=oracle_sanity(results);sanity.to_csv(output/'oracle_sanity.csv',index=False)
    fidelity,history=tuning_tables(output)
    chosen=proposed[proposed.proposed_variant_selected].copy()
    chosen[['seed','method','representation','k','dro_variant','validation_selection_score',
            'validation_average_accuracy','accuracy_guard_passed',*METRICS]].to_csv(output/'variant_selection.csv',index=False)
    effects=[]
    for variant,part in proposed.groupby('dro_variant',sort=False):
        ref=baseline.loc[part.seed]
        row={'dro_variant':variant,'n_seeds':len(part),'guard_pass_count':int(part.accuracy_guard_passed.sum())}
        row.update({m:part[m].mean() for m in METRICS})
        for metric in METRICS:
            row[f'delta_{metric}']=part[metric].to_numpy().mean()-ref[metric].to_numpy().mean()
        row['accuracy_within_2pp']=row['delta_accuracy']>=-.02-1e-12
        row['race_gap_reduced']=row['delta_approval_rate_gap_race_eth']<0
        row['sex_gap_reduced']=row['delta_approval_rate_gap_sex']<0
        row['eo_gap_reduced']=row['delta_eo_gap']<0
        row['all_targets_met']=all(row[k] for k in ['accuracy_within_2pp','race_gap_reduced','sex_gap_reduced','eo_gap_reduced'])
        effects.append(row)
    effects=pd.DataFrame(effects);effects.to_csv(output/'proposed_variant_effects.csv',index=False)
    inferred=results[results.representation.isin(['raw','scarf','GEORGE','HBAC','geoproxy'])].copy()
    erm_all=results[results.method.eq('ERM-MLP')].set_index(['selection','seed'])
    for target,metric,sign in [('eo_reduction','eo_gap',-1),('worst_group_gain','worst_group_accuracy',1)]:
        inferred[target]=inferred.apply(lambda r:sign*(r[metric]-erm_all.loc[
            ('average' if r.selection=='inferred_worst_group' else r.selection,r.seed),metric]),axis=1)
    inferred.to_csv(output/'alignment_fairness.csv',index=False)
    correlations=[]
    for (variant,selection),part in inferred.groupby(['dro_variant','selection']):
        for dim in ['race_eth','sex','age','intersection']:
            for metric in ['ari','nmi']:
                key=f'{metric}_{dim}'
                correlations.append({'dro_variant':variant,'selection':selection,'alignment':key,'n':len(part),
                    'pearson_eo_reduction':part[key].corr(part.eo_reduction),
                    'pearson_worst_group_gain':part[key].corr(part.worst_group_gain)})
    corr=pd.DataFrame(correlations);corr.to_csv(output/'alignment_fairness_correlations.csv',index=False)
    text=['# ผลนำร่อง HMDA รอบ 5: นิยามกลุ่มและ class-balanced loss','',
          'ทุกตัวเลขในตารางอ่านจาก CSV; mean ± sample SD ข้าม seed (QUICK 3 seed, full labels); threshold=0.5',
          'EO/worst-group ใช้ intersection race_eth × sex; Unknown และกลุ่มจริงที่เล็กกว่า min_fair_group ไม่นับ fairness; รายละเอียดจำนวนอยู่ใน CSV',
          '## นิยามการทดลองและการเลือกโดยไม่ใช้ประชากร','',
          '- cy/cy_bal: cluster × y; c/c_bal: cluster โดยไม่ผูก y; _bal ใช้ BCE ถ่วงน้ำหนักจาก train เท่านั้น',
          '- raw/SCARF/GEORGE แบบ cy จัด k กลุ่มต่อคลาส (รวม 2k) ตามรอบ 4; แบบ c จัด k กลุ่มบน representation ทั้ง train ไม่แยกคลาส โดยเฉพาะ GEORGE ใช้ ERM hidden representation เดิมแต่ fit global k-means ใหม่',
          '- จึงเปลี่ยนทั้งการใช้ y และจำนวน/องค์ประกอบ cluster ในการเทียบ c กับ cy ไม่ใช่ ablation ที่คง cluster ทุกอย่าง; HBAC/geoproxy/oracle คง base cluster เดิมได้',
          '- oracle: c=race_eth × sex, cy=race_eth × sex × y; oracle เท่านั้นใช้ประชากรเลือก validation; Unknown คงไว้ใน train แต่ไม่นับ validation fairness',
          '- random: c สุ่ม k กลุ่มไม่ใช้ y; cy คงกลุ่มสุ่มต่อคลาสตามรอบ 4; validation ใช้ RNG แยก seed คงที่และไม่ใช้ test',
          '- น้ำหนักภายใน base cluster c: w_i=n_c/(m_c × n_cy), m_c คือจำนวนคลาสที่พบจริง; น้ำหนักแต่ละคลาสรวม n_c/m_c และค่าเฉลี่ยน้ำหนัก=1; หากมีคลาสเดียวได้ w=1',
          '- c_bal คำนวณใน cluster หลังรวมกลุ่มเล็ก; cy_bal คำนวณใน base cluster ก่อน cross y/รวมเล็ก แล้วใช้ mean(w×BCE) ใน DRO group โดยไม่หาร sum(w) ซ้ำ; จึงเป็น cost-sensitive loss และเพิ่มสเกล loss ของ cy ที่เป็นคลาสหายาก ไม่รับรองว่าจะลด approval gap',
          '- cluster ที่ fit ภายในคลาสมี y ค่าเดียวอยู่แล้ว: cy_bal ของ raw/SCARF/GEORGE/random อาจเท่ากับ cy ตามสูตร ไม่ควรตีความเป็นการทดลอง class balance อิสระที่ให้ข้อมูลเพิ่ม; ตรวจ class_weight_min/max ใน CSV',
          '- รวม train group < min_dro_group เข้าศูนย์กลางใกล้สุด; cy รวมเฉพาะคลาสเดียวกัน, c ไม่ใช้ y รวม; validation ใช้ cluster ก่อนรวมเพื่อไม่ซ่อนกลุ่มยาก และนิยาม c/cy ตรงกับ train',
          '- เลือก checkpoint/กริดด้วย inferred_worst_group บน validation ของนิยามนั้น; guard validation accuracy ≥ ERM-MLP −0.02; ถ้าไม่ผ่านทุกตัวเลือก average ที่ใกล้เกณฑ์ที่สุด ตามด้วย worst-group; เสมอคงตัวแรก',
          '- เลือก k และ raw/SCARF ด้วย Silhouette train แยกนิยาม c/cy; จากนั้นเลือกรูปแบบใน 4 ตัวด้วย validation rank เดียวกันโดยไม่ดู test/ประชากร (variant order cy, cy_bal, c, c_bal ใช้ตัดสินเสมอ)',
          '- คะแนน worst-group ของ c กับ cy ต่างจำนวนกลุ่ม/ความยาก จึงเปรียบเทียบข้ามนิยามแล้วมีแนวโน้มเข้าข้าง c; ต้องมี holdout ใหม่ก่อนยืนยัน และอย่าตีความว่ารูปแบบที่เลือกดีที่สุดเชิง fairness จริง',
          '- กริด eta={0.01,0.1} × C={0,1} × lr={0.0002,0.001} × budget=5 epoch (8 candidate); ตัดการฝึก budget=3 ซ้ำ เพราะ checkpoint 1–3 อยู่ใน budget 5 แล้ว ไม่เพิ่ม ERM เป็น candidate; warm-start ERM เฉพาะพารามิเตอร์ optimizer/DRO weights เริ่มใหม่',
          '## ตารางหลัก: วิธี × รูปแบบ','',
          'ERM ใช้ selection=average; JTT/DRO ใช้ inferred_worst_group; guard เป็นสัดส่วน seed ที่ผ่าน (1=ครบ); ไม่มี guard สำหรับ ERM-LGBM แสดง N/A',
          markdown_table(comparison,['method','dro_variant'],METRICS+['accuracy_guard_passed']),'',
          '## วิธีเสนอแยก 4 รูปแบบ และผลเปลี่ยนเทียบ ERM-MLP','',
          markdown_table(effects,['dro_variant'],METRICS+['guard_pass_count','delta_accuracy',
              'delta_approval_rate_gap_race_eth','delta_approval_rate_gap_sex','delta_eo_gap','all_targets_met']),
          'all_targets_met ต้อง accuracy ลดไม่เกิน 0.02 และช่องว่าง race, sex, EO ลดทั้งสามพร้อมกันในค่าเฉลี่ย; ไม่ใช่นัยสำคัญทางสถิติ และ test guard นี้ต่างจาก validation guard',
          '## รูปแบบที่เลือกด้วย validation เท่านั้น (หนึ่งตัวต่อ seed)','',
          markdown_table(chosen,['seed','representation','k','dro_variant'],['validation_selection_score',
              'validation_average_accuracy','accuracy_guard_passed',*METRICS]),
          'หน้าสาธิตใช้ seed แรกและรูปแบบที่เลือกในตารางนี้ การ์ดใช้ cluster definition เดียวกัน; ไม่เลือก seed ด้วย test',
          '### รูปแบบที่เลือกแยกแต่ละวิธี (ไม่รวม oracle)','',
          markdown_table(main[main.variant_selected_without_demographics],['seed','method','dro_variant'],
              ['validation_selection_score','validation_average_accuracy','accuracy_guard_passed']),'',
          '## Sanity oracle แยกรูปแบบ','',
          markdown_table(sanity,['dro_variant'],['erm_worst_group','oracle_worst_group','gain'])]
    for variant in ['cy','cy_bal','c','c_bal']:
        text.append(f"- {variant}: {'ผ่าน' if status[variant] else 'ไม่ผ่าน'}; mean worst-group gain={gains[variant]:.6f}")
    text.extend(['oracle ที่ไม่ผ่านยังไม่ใช่เพดานบนที่ยืนยันแล้ว; การเปลี่ยนพารามิเตอร์จริงไม่รับรอง fairness; กลุ่มฝึก loss, validation worst accuracy และ test intersection เป็นคนละเป้าหมาย',
          '## ผลเสริม: average และ true worst_group (หลังใช้ประชากร validation)','',
          markdown_table(results[results.selection.isin(['average','worst_group'])],['selection','method','dro_variant'],METRICS),'',
          '## กริดที่เลือก: น้ำหนักกลุ่มและการขยับพารามิเตอร์','',
          markdown_table(grid[grid.selected],['selection','seed','method','dro_variant'],
              ['dro_eta','C','learning_rate','selected_epoch','validation_accuracy','validation_selection_score',
               'accuracy_guard_passed','parameter_l2_from_erm','final_group_weight_min','final_group_weight_max']),'',
          '## ความตรงของกลุ่ม (ประชากรบน test ใช้ประเมินหลังเลือกเสร็จ)','',
          markdown_table(clusters,['group_definition','representation','k'],['silhouette','davies_bouldin',
              'ari_race_eth','nmi_race_eth','ari_sex','nmi_sex','ari_age','nmi_age','ari_intersection','nmi_intersection']),
          'Silhouette/DBI ใช้ train ยกเว้น geoproxy รายงานบน test เชิงพรรณนา ไม่ใช้เลือก; HBAC/geoproxy ใช้ cluster ร่วมทั้ง 4 รูปแบบ','',
          '## คำอธิบายกลุ่มและ H2','',
          'ต้นไม้ balanced/unbalanced ลึก ≤3 fit train เลือก F1 validation รายกลุ่ม (เสมอ balanced); fidelity รายงาน validation เดียวที่เลือกจึง optimistic; F1<0.5 เตือนพร้อม SMD/ส่วนต่างสัดส่วน top 5 จาก train',
          'Welch t-test/χ² ใช้ test และ Bonferroni ทั้ง family; HBAC ทำการ์ดแยกนิยามเพื่อหน้าสาธิต แม้ base cluster เหมือนกัน ไม่ถือเป็นหลักฐานอิสระเพิ่ม',
          markdown_table(cards,['group_definition','method'],['fidelity_f1','fidelity_precision','fidelity_recall','rule_length','coverage']),
          markdown_table(fidelity,['round','method'],['n_groups','median_fidelity_f1','fraction_f1_ge_080','n_f1_below_050']),'',
          '## เทียบกับผลรอบก่อน (round4 เก็บสำเนาก่อนรันใหม่)','',
          markdown_table(history[history.method.isin(['ERM-LGBM','ERM-MLP','GDRO-oracle','Proposed (Silhouette)'])],
              ['round','method','dro_variant'],METRICS),'',
          'รอบ 4 oracle มีแต่ intersection บน validation แม้ train cross y; รอบ 5 แก้ validation oracle ให้ตรง c/cy จึงไม่ใช่เปรียบเทียบเกณฑ์เดิมทุกขั้น',
          '## Alignment กับ fairness เชิงสำรวจ','',
          markdown_table(corr,['dro_variant','selection','alignment'],['pearson_eo_reduction','pearson_worst_group_gain']),
          'หลาย k/รูปแบบใช้ข้อมูลและ seed ซ้ำ ไม่เป็นอิสระและไม่แสดงเหตุผลเชิงสาเหตุ','',
          '## ประสิทธิภาพระบบ','',
          markdown_table(results,['selection','method','dro_variant'],['train_seconds','inference_seconds_per_1000',
              'peak_memory_mb','parameters','flops_per_row','tree_count','leaf_count']),
          markdown_table(resources,['representation'],['discovery_train_seconds','peak_memory_mb','parameters','flops_per_row']),
          'เวลาแต่ละแถวรวม preprocessing/discovery ที่ใช้ร่วมกัน ห้ามบวกเป็นเวลาทั้งชุด; FLOPs นับ Linear โมเดลตัดสินใจ; runtime_summary.csv แสดงเวลาทั้งชุด','',
          '## ข้อจำกัด','',
          '- อัตราอนุมัติสูง ต้องอ่าน positive rate/AUROC/F1 ร่วมกับ accuracy; EO ผันผวนเมื่อกลุ่มมีผู้ปฏิเสธน้อย แม้ขนาดรวมผ่าน 30 แถว',
          '- HMDA สาธารณะไม่มีคะแนนเครดิตจริง applicant_credit_score_type เป็นประเภทวิธีคำนวณ; ห้ามอ้างว่าแทนข้อมูลเครดิตครบ',
          '- ใช้ผลสินเชื่อย้อนหลัง ไม่ใช่หลักฐานการเลือกปฏิบัติ; proxy และ Unknown ยังมีข้อจำกัด',
          '- cy class-conditioned clustering ใช้ y ตอน fit แต่ตอนใช้จริง nearest center ไม่รู้ y จึงอาจไม่ตรงกลุ่มฝึก; c ไม่มีปัญหานี้ใน k-means แต่ representation GEORGE และ HBAC ใช้ป้าย train ตามวิธี',
          '- เปิดดู test ซ้ำหลายรอบแล้ว ผลเป็น exploratory ต้องข้อมูล holdout ใหม่; การเลือก variant ด้วย validation ลดการใช้ประชากรแต่ไม่แก้ multiple selection',
          '- ไม่ทดสอบ FULL หรือ Colab รอบ 5 สด; รอบ 2 ผู้สั่งแจ้ง Colab CPU ผ่าน 15 ต.ค. 2569 (~3.4 นาที, Gradio ทำงาน); fallback ใช้แคชในเครื่อง ไม่ทดสอบ download/install/network',
          '- Gradio เติมตัวแปรที่ไม่กรอกจาก median/mode train ความน่าจะเป็นยังไม่ calibrate ใช้เพื่อวิจัยเท่านั้น',''])
    (output/'hmda_pilot_summary.md').write_text('\n'.join(text),encoding='utf-8')
    plot_results(output,results,clusters,cards,proposed)
    if (output/'postprocess_results.csv').exists():
        from .postprocess_reporting import generate_postprocess_report
        generate_postprocess_report(output)


def plot_results(output,results,clusters,cards,proposed):
    """กราฟแยกรูปแบบ ไม่วาดเส้นเชื่อมให้เข้าใจผิดเป็นแนวโน้มเวลา"""
    os.environ.setdefault('MPLCONFIGDIR',str(output/'.matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    figs=output/'figures';figs.mkdir(exist_ok=True)
    main=main_rows(results)
    baseline=main[main.method.eq('ERM-MLP')]
    fig,axes=plt.subplots(2,2,figsize=(14,10),sharex=True,sharey=True)
    for ax,variant in zip(axes.flat,['cy','cy_bal','c','c_bal']):
        for method,g in main[main.dro_variant.eq(variant)].groupby('method'):
            ax.errorbar(g.approval_rate_gap_race_eth.mean(),g.accuracy.mean(),
                        xerr=g.approval_rate_gap_race_eth.std(),yerr=g.accuracy.std(),fmt='o',label=method,alpha=.75)
        p=proposed[proposed.dro_variant.eq(variant)]
        ax.scatter(p.approval_rate_gap_race_eth.mean(),p.accuracy.mean(),marker='*',s=200,color='black',label='Proposed (Silhouette)')
        ax.scatter(baseline.approval_rate_gap_race_eth.mean(),baseline.accuracy.mean(),marker='X',s=100,color='red',label='ERM-MLP')
        ax.set(title=variant,xlabel='Approval gap: race/ethnicity',ylabel='Accuracy');ax.grid(alpha=.2)
    handles,labels=axes[0,0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='center left',bbox_to_anchor=(.8,.5),fontsize=8)
    fig.tight_layout(rect=(0,0,.8,1));fig.savefig(figs/'dro_variants.png',dpi=140);plt.close(fig)
    for selection,part in results.groupby('selection'):
        fig,ax=plt.subplots(figsize=(12,6))
        for (method,variant),g in part.groupby(['method','dro_variant']):
            ax.scatter(g.eo_gap.mean(),g.accuracy.mean(),label=f'{method}/{variant}',s=20)
        ax.set(xlabel='EO gap',ylabel='Accuracy',title=selection)
        ax.legend(fontsize=5,ncol=2,loc='center left',bbox_to_anchor=(1,.5))
        fig.tight_layout();fig.savefig(figs/f'accuracy_eo_{selection}.png',dpi=140);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    for rep,g in clusters.groupby('representation'): axes[0].scatter(g.ari_intersection,g.nmi_intersection,label=rep)
    for (d,method),g in cards.groupby(['group_definition','method']): axes[1].scatter(g.coverage,g.fidelity_f1,label=f'{method}/{d}',s=15)
    axes[0].set(xlabel='ARI intersection',ylabel='NMI intersection');axes[0].legend(fontsize=6)
    axes[1].set(xlabel='Validation rule coverage',ylabel='Validation fidelity F1');axes[1].legend(fontsize=5)
    fig.tight_layout();fig.savefig(figs/'alignment_explanations.png',dpi=140);plt.close(fig)
