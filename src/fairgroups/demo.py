"""Gradio สำหรับวิจัย: ค่าเริ่มต้นจาก train และไม่ต้องรับข้อมูลประชากร"""
import os
import sys
if sys.platform=='darwin': os.environ['OMP_NUM_THREADS']='1'
os.environ.setdefault('GRADIO_ANALYTICS_ENABLED','False')
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from .models import predict_mlp
from .representations import encode_scarf
from .explanations import card_text

PRIMARY=['loan_amount','income','property_value','loan_to_value_ratio','debt_to_income_ratio','loan_term','loan_type','lien_status',
         'tract_to_msa_income_percentage','tract_population','total_units']


def save_bundle(output,bundle):
    cards=pd.read_csv(output/'group_explanations.csv')
    cards=cards[(cards.seed==bundle['seed']) & (cards.method==bundle['method'])]
    bundle['cards']={int(r['group']):card_text(r) for r in cards.to_dict('records')}
    bundle['inputs']=[c for c in PRIMARY if c in bundle['defaults']][:8]
    joblib.dump(bundle,output/'demo_bundle.joblib',compress=3)


def load_bundle(output='results'):
    # โหลดเฉพาะไฟล์ที่สร้างเองในโฟลเดอร์งาน
    return joblib.load(Path(output)/'demo_bundle.joblib')


def predict_application(bundle,*values):
    if len(values)!=len(bundle['inputs']): raise ValueError('จำนวนตัวแปรไม่ตรงหน้าสาธิต')
    application=dict(bundle['defaults']);application.update(dict(zip(bundle['inputs'],values)))
    for c in bundle['processor'].categorical_: application[c]=str(application[c])
    frame=bundle['guard'].transform(pd.DataFrame([application]))
    x=bundle['processor'].transform(frame)
    erm=float(predict_mlp(bundle['erm'],x)[0]); fair=float(predict_mlp(bundle['fair'],x)[0])
    rep=x if bundle['representation']=='raw' else bundle['scarf_scaler'].transform(encode_scarf(bundle['scarf'],x)).astype(np.float32)
    group=int(bundle['clusterer'].predict(rep)[0])
    result={'โอกาสอนุมัติ ERM':erm,'โอกาสอนุมัติหลังฝึก DRO':fair,'กลุ่ม':group,'วิธี':bundle['method']}
    warning='⚠️ ต้นแบบเพื่อการวิจัยเท่านั้น ความน่าจะเป็นยังไม่ผ่านการปรับเทียบ ไม่ใช้อนุมัติสินเชื่อจริง และผลทดลองอาจไม่ได้ลดอคติ'
    return result,bundle['cards'].get(group,'ยังไม่มีการ์ดกลุ่มนี้')+'\n\n'+warning


def build_interface(output='results'):
    import gradio as gr
    bundle=load_bundle(output)
    inputs=[]
    for c in bundle['inputs']:
        default=bundle['defaults'][c]
        inputs.append(gr.Number(label=c,value=float(default)) if c in bundle['processor'].numeric_ else
                      gr.Textbox(label=c,value=str(default)))
    return gr.Interface(fn=lambda *values:predict_application(bundle,*values),inputs=inputs,
                        outputs=[gr.JSON(label='ผลคาดการณ์'),gr.Markdown(label='คำอธิบายกลุ่ม')],
                        title='ต้นแบบ HMDA: ค้นหากลุ่มผู้ขอสินเชื่อ',
                        description='เพื่อการวิจัยเท่านั้น ใช้ข้อมูลหลักประมาณ 8 ตัว; ช่องอื่นใช้ค่ากลาง/ฐานนิยมจาก train ไม่ใช่ระบบอนุมัติจริง',
                        flagging_mode='never',analytics_enabled=False)


if __name__=='__main__':
    build_interface().launch(share=True)
