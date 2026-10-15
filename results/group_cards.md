# การ์ดอธิบายกลุ่ม HMDA

กฎ one-hot ที่ ≤ 0.5 หมายถึงไม่มีค่านั้น; สถิติต่างกลุ่มเป็นเชิงสำรวจ ไม่ใช่เหตุและผล

### GDRO-raw-k4 · cy · seed 17 · กลุ่ม 0
- IF tract_one_to_four_family_homes ≤ 50 AND tract_population ≤ 1934 AND property_value ≤ 4.45e+05 THEN อยู่กลุ่มนี้
- IF tract_one_to_four_family_homes ≤ 50 AND tract_population ≤ 1934 AND property_value > 4.45e+05 THEN อยู่กลุ่มนี้
- IF tract_one_to_four_family_homes > 50 AND tract_population ≤ 1000 AND tract_owner_occupied_units > 393 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 151/46/56 · coverage กฎบน validation 0.0115
- Fidelity F1 0.9565 · precision 0.9565 · recall 0.9565 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.0893 · ERM error 0.0536 · FPR 0.0196 · FNR 0.4000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.5e-121), derived_msa-md (p_adj=7e-13), county_code (p_adj=3.8e-112), loan_amount (p_adj=2.3e-12), loan_term (p_adj=1.5e-13), property_value (p_adj=2e-16), construction_method (p_adj=8.3e-71), income (p_adj=3.5e-13), debt_to_income_ratio (p_adj=1.7e-06), applicant_credit_score_type (p_adj=3.8e-06), aus-1 (p_adj=1.2e-40), tract_population (p_adj=0), ffiec_msa_md_median_family_income (p_adj=0.0014), tract_to_msa_income_percentage (p_adj=0), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=0), tract_median_age_of_housing_units (p_adj=0)
- องค์ประกอบ race_eth: Hispanic 3.6% (ทั้งชุด 9.1%), NH Asian 3.6% (ทั้งชุด 6.8%), NH Black 33.9% (ทั้งชุด 22.0%), NH White 42.9% (ทั้งชุด 41.8%), Other 3.6% (ทั้งชุด 2.3%), Unknown 12.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 46.4% (ทั้งชุด 27.1%), Joint 25.0% (ทั้งชุด 30.7%), Male 26.8% (ทั้งชุด 35.6%), Unknown 1.8% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 26.8% (ทั้งชุด 31.4%), 35-44 32.1% (ทั้งชุด 26.6%), 45-54 21.4% (ทั้งชุด 17.5%), 55-64 3.6% (ทั้งชุด 11.7%), 65-74 7.1% (ทั้งชุด 5.5%), <25 7.1% (ทั้งชุด 5.9%), >74 1.8% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 17 · กลุ่ม 1
- IF debt_to_income_ratio ≤ 52 AND initially_payable_to_institution_3 > 0.5 AND submission_of_application_2 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio ≤ 52 AND initially_payable_to_institution_3 > 0.5 AND submission_of_application_2 > 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 52 AND loan_term > 306 AND debt_to_income_ratio ≤ 60 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 52 AND loan_term > 306 AND debt_to_income_ratio > 60 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1087/642/646 · coverage กฎบน validation 0.1742
- Fidelity F1 0.4347 · precision 0.4175 · recall 0.4533 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- **กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี**
- คำอธิบายสำรอง: ตัวแปรที่ต่างจากส่วนที่เหลือมากที่สุด คำนวณบน train เท่านั้น
  - debt_to_income_ratio: SMD 0.599; ค่าเฉลี่ยกลุ่ม 48.31, ส่วนที่เหลือ 40.62
  - loan_term: SMD 0.398; ค่าเฉลี่ยกลุ่ม 359.1, ส่วนที่เหลือ 346.1
  - ffiec_msa_md_median_family_income: SMD 0.268; ค่าเฉลี่ยกลุ่ม 9.524e+04, ส่วนที่เหลือ 9.141e+04
  - loan_type = 1: สัดส่วนต่าง -0.192; กลุ่ม 44.9%, ส่วนที่เหลือ 64.1%
  - income: SMD -0.191; ค่าเฉลี่ยกลุ่ม 102.7, ส่วนที่เหลือ 127.6
- อนุมัติจริง 0.8142 · ERM error 0.0789 · FPR 0.3417 · FNR 0.0190
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.035), derived_msa-md (p_adj=2e-44), county_code (p_adj=1.2e-31), derived_loan_product_type (p_adj=1e-82), loan_type (p_adj=1.1e-84), loan_term (p_adj=7.4e-58), construction_method (p_adj=1.9e-13), income (p_adj=2.6e-24), debt_to_income_ratio (p_adj=7.9e-146), aus-1 (p_adj=1.6e-45), tract_population (p_adj=3e-06), ffiec_msa_md_median_family_income (p_adj=3.8e-106), tract_owner_occupied_units (p_adj=0.023)
- องค์ประกอบ race_eth: Hispanic 12.1% (ทั้งชุด 9.1%), NH Asian 5.3% (ทั้งชุด 6.8%), NH Black 35.3% (ทั้งชุด 22.0%), NH White 26.0% (ทั้งชุด 41.8%), Other 2.6% (ทั้งชุด 2.3%), Unknown 18.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 35.1% (ทั้งชุด 27.1%), Joint 27.9% (ทั้งชุด 30.7%), Male 30.7% (ทั้งชุด 35.6%), Unknown 6.3% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 29.1% (ทั้งชุด 31.4%), 35-44 28.6% (ทั้งชุด 26.6%), 45-54 19.5% (ทั้งชุด 17.5%), 55-64 10.7% (ทั้งชุด 11.7%), 65-74 5.9% (ทั้งชุด 5.5%), <25 5.0% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 17 · กลุ่ม 2
- IF construction_method_2 > 0.5 AND aus-1_6 > 0.5 AND tract_one_to_four_family_homes > 464 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 712/341/355 · coverage กฎบน validation 0.0717
- Fidelity F1 0.8280 · precision 0.9059 · recall 0.7625 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.4394 · ERM error 0.1972 · FPR 0.0955 · FNR 0.3269
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.8e-234), derived_msa-md (p_adj=1.5e-48), county_code (p_adj=4.1e-105), derived_loan_product_type (p_adj=7.5e-89), loan_type (p_adj=3.7e-47), lien_status (p_adj=3.5e-52), loan_amount (p_adj=8.8e-234), loan_term (p_adj=1e-76), property_value (p_adj=6.1e-151), construction_method (p_adj=0), income (p_adj=5.8e-62), applicant_credit_score_type (p_adj=9.4e-179), aus-1 (p_adj=1e-292), tract_population (p_adj=1.5e-13), ffiec_msa_md_median_family_income (p_adj=1.1e-28), tract_to_msa_income_percentage (p_adj=3.9e-17), tract_owner_occupied_units (p_adj=2.1e-09), tract_median_age_of_housing_units (p_adj=5.5e-15)
- องค์ประกอบ race_eth: Hispanic 6.5% (ทั้งชุด 9.1%), NH Asian 2.8% (ทั้งชุด 6.8%), NH Black 24.2% (ทั้งชุด 22.0%), NH White 44.2% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.3%), Unknown 20.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.9% (ทั้งชุด 27.1%), Joint 27.0% (ทั้งชุด 30.7%), Male 32.7% (ทั้งชุด 35.6%), Unknown 5.4% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.1% (ทั้งชุด 31.4%), 35-44 23.9% (ทั้งชุด 26.6%), 45-54 18.0% (ทั้งชุด 17.5%), 55-64 11.8% (ทั้งชุด 11.7%), 65-74 5.6% (ทั้งชุด 5.5%), <25 8.7% (ทั้งชุด 5.9%), >74 1.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 17 · กลุ่ม 3
- IF total_units > 1.5 AND tract_median_age_of_housing_units ≤ 53.5 AND applicant_credit_score_type_1111 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 10/11/8 · coverage กฎบน validation 0.0015
- Fidelity F1 0.5882 · precision 0.8333 · recall 0.4545 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8750 · ERM error 0.1250 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.6e-74), county_code (p_adj=3.5e-41), applicant_credit_score_type (p_adj=0.022), submission_of_application (p_adj=1.6e-05), initially_payable_to_institution (p_adj=0.0002), aus-1 (p_adj=2.7e-06)
- องค์ประกอบ race_eth: Hispanic 25.0% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 12.5% (ทั้งชุด 22.0%), NH White 37.5% (ทั้งชุด 41.8%), Other 0.0% (ทั้งชุด 2.3%), Unknown 25.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 12.5% (ทั้งชุด 27.1%), Joint 50.0% (ทั้งชุด 30.7%), Male 25.0% (ทั้งชุด 35.6%), Unknown 12.5% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 62.5% (ทั้งชุด 31.4%), 35-44 12.5% (ทั้งชุด 26.6%), 45-54 12.5% (ทั้งชุด 17.5%), 55-64 0.0% (ทั้งชุด 11.7%), 65-74 12.5% (ทั้งชุด 5.5%), <25 0.0% (ทั้งชุด 5.9%), >74 0.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 17 · กลุ่ม 4
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND aus-1_6 ≤ 0.5 AND tract_owner_occupied_units ≤ 1781 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2532/801/759 · coverage กฎบน validation 0.1930
- Fidelity F1 0.8875 · precision 0.9041 · recall 0.8714 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8775 · ERM error 0.0909 · FPR 0.6667 · FNR 0.0105
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.2e-28), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.0078), derived_loan_product_type (p_adj=2.8e-32), loan_type (p_adj=1.4e-33), loan_amount (p_adj=6.9e-63), loan_term (p_adj=4.4e-60), property_value (p_adj=5.9e-68), income (p_adj=2.3e-23), applicant_credit_score_type (p_adj=1.3e-14), submission_of_application (p_adj=1.6e-12), initially_payable_to_institution (p_adj=7e-13), aus-1 (p_adj=1.4e-32), tract_population (p_adj=5.4e-29), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=2.2e-35), tract_median_age_of_housing_units (p_adj=2.1e-22)
- องค์ประกอบ race_eth: Hispanic 6.7% (ทั้งชุด 9.1%), NH Asian 1.6% (ทั้งชุด 6.8%), NH Black 15.9% (ทั้งชุด 22.0%), NH White 58.0% (ทั้งชุด 41.8%), Other 2.9% (ทั้งชุด 2.3%), Unknown 14.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 22.7% (ทั้งชุด 27.1%), Joint 32.7% (ทั้งชุด 30.7%), Male 37.5% (ทั้งชุด 35.6%), Unknown 7.1% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 31.2% (ทั้งชุด 31.4%), 35-44 21.7% (ทั้งชุด 26.6%), 45-54 14.0% (ทั้งชุด 17.5%), 55-64 14.5% (ทั้งชุด 11.7%), 65-74 6.6% (ทั้งชุด 5.5%), <25 10.1% (ทั้งชุด 5.9%), >74 1.8% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 17 · กลุ่ม 5
- IF ffiec_msa_md_median_family_income ≤ 9.11e+04 AND ffiec_msa_md_median_family_income > 8.405e+04 AND tract_one_to_four_family_homes ≤ 1423 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 9.11e+04 AND tract_owner_occupied_units ≤ 1298 AND property_value ≤ 7.5e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4124/1098/1130 · coverage กฎบน validation 0.4240
- Fidelity F1 0.7530 · precision 0.6203 · recall 0.9581 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9071 · ERM error 0.0681 · FPR 0.6857 · FNR 0.0049
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.4e-11), derived_msa-md (p_adj=2.9e-136), county_code (p_adj=8.8e-131), conforming_loan_limit (p_adj=1.4e-05), derived_loan_product_type (p_adj=6.5e-18), loan_type (p_adj=8e-16), loan_term (p_adj=3.5e-29), construction_method (p_adj=5.2e-29), debt_to_income_ratio (p_adj=1.2e-18), applicant_credit_score_type (p_adj=1.6e-05), aus-1 (p_adj=1.6e-25), tract_population (p_adj=6.8e-147), ffiec_msa_md_median_family_income (p_adj=0), tract_to_msa_income_percentage (p_adj=2e-30), tract_owner_occupied_units (p_adj=1.2e-236), tract_one_to_four_family_homes (p_adj=4.8e-270), tract_median_age_of_housing_units (p_adj=4e-20)
- องค์ประกอบ race_eth: Hispanic 11.7% (ทั้งชุด 9.1%), NH Asian 9.6% (ทั้งชุด 6.8%), NH Black 22.4% (ทั้งชุด 22.0%), NH White 35.7% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.3%), Unknown 18.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 29.7% (ทั้งชุด 27.1%), Joint 27.8% (ทั้งชุด 30.7%), Male 35.8% (ทั้งชุด 35.6%), Unknown 6.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 36.2% (ทั้งชุด 31.4%), 35-44 25.7% (ทั้งชุด 26.6%), 45-54 16.0% (ทั้งชุด 17.5%), 55-64 11.0% (ทั้งชุด 11.7%), 65-74 5.0% (ทั้งชุด 5.5%), <25 5.1% (ทั้งชุด 5.9%), >74 1.1% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 17 · กลุ่ม 6
- IF property_value ≤ 7.6e+05 AND income > 317.5 AND loan_amount > 5.2e+05 THEN อยู่กลุ่มนี้
- IF property_value > 7.6e+05 AND income ≤ 247.5 AND tract_to_msa_income_percentage > 192.9 THEN อยู่กลุ่มนี้
- IF property_value > 7.6e+05 AND income > 247.5 AND tract_population ≤ 6142 THEN อยู่กลุ่มนี้
- IF property_value > 7.6e+05 AND income > 247.5 AND tract_population > 6142 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 637/231/204 · coverage กฎบน validation 0.0480
- Fidelity F1 0.7896 · precision 0.8698 · recall 0.7229 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9510 · ERM error 0.0392 · FPR 0.7000 · FNR 0.0052
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=8.5e-16), derived_msa-md (p_adj=0.00022), county_code (p_adj=2e-17), conforming_loan_limit (p_adj=0), derived_loan_product_type (p_adj=7e-22), loan_type (p_adj=3.3e-21), loan_amount (p_adj=1.2e-42), loan_term (p_adj=9.2e-06), property_value (p_adj=6e-45), construction_method (p_adj=0.00056), income (p_adj=4.7e-23), debt_to_income_ratio (p_adj=5.3e-19), aus-1 (p_adj=3.9e-09), ffiec_msa_md_median_family_income (p_adj=4.8e-18), tract_to_msa_income_percentage (p_adj=5.4e-42), tract_one_to_four_family_homes (p_adj=0.0033)
- องค์ประกอบ race_eth: Hispanic 3.9% (ทั้งชุด 9.1%), NH Asian 15.2% (ทั้งชุด 6.8%), NH Black 5.4% (ทั้งชุด 22.0%), NH White 54.9% (ทั้งชุด 41.8%), Other 2.5% (ทั้งชุด 2.3%), Unknown 18.1% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 12.7% (ทั้งชุด 27.1%), Joint 48.5% (ทั้งชุด 30.7%), Male 32.4% (ทั้งชุด 35.6%), Unknown 6.4% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 23.5% (ทั้งชุด 31.4%), 35-44 39.2% (ทั้งชุด 26.6%), 45-54 22.5% (ทั้งชุด 17.5%), 55-64 12.7% (ทั้งชุด 11.7%), 65-74 1.0% (ทั้งชุด 5.5%), <25 1.0% (ทั้งชุด 5.9%), >74 0.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 17 · กลุ่ม 7
- IF tract_owner_occupied_units > 1374 AND tract_population ≤ 5150 AND tract_median_age_of_housing_units ≤ 30.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1374 AND tract_population > 5150 AND aus-1_6 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2747/830/842 · coverage กฎบน validation 0.2162
- Fidelity F1 0.8224 · precision 0.8058 · recall 0.8398 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9121 · ERM error 0.0582 · FPR 0.5946 · FNR 0.0065
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0005), derived_msa-md (p_adj=5.9e-38), county_code (p_adj=8.5e-134), derived_loan_product_type (p_adj=1.3e-06), loan_type (p_adj=8.5e-07), loan_amount (p_adj=3.6e-10), loan_term (p_adj=4.2e-16), property_value (p_adj=1.2e-10), construction_method (p_adj=5.9e-17), debt_to_income_ratio (p_adj=0.0038), aus-1 (p_adj=9.9e-16), tract_population (p_adj=7e-242), ffiec_msa_md_median_family_income (p_adj=1.8e-24), tract_to_msa_income_percentage (p_adj=5.6e-36), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=1.2e-253), tract_median_age_of_housing_units (p_adj=4.6e-124)
- องค์ประกอบ race_eth: Hispanic 8.1% (ทั้งชุด 9.1%), NH Asian 8.8% (ทั้งชุด 6.8%), NH Black 19.0% (ทั้งชุด 22.0%), NH White 43.1% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.3%), Unknown 19.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 20.5% (ทั้งชุด 27.1%), Joint 32.4% (ทั้งชุด 30.7%), Male 40.4% (ทั้งชุด 35.6%), Unknown 6.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 29.3% (ทั้งชุด 31.4%), 35-44 28.5% (ทั้งชุด 26.6%), 45-54 19.7% (ทั้งชุด 17.5%), 55-64 11.3% (ทั้งชุด 11.7%), 65-74 5.6% (ทั้งชุด 5.5%), <25 4.0% (ทั้งชุด 5.9%), >74 1.5% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 0
- IF tract_population ≤ 357.5 AND construction_method_2 > 0.5 AND aus-1_6 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF tract_population ≤ 357.5 AND construction_method_2 > 0.5 AND aus-1_6 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 150/43/57 · coverage กฎบน validation 0.0103
- Fidelity F1 0.9762 · precision 1.0000 · recall 0.9535 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.1053 · ERM error 0.0526 · FPR 0.0196 · FNR 0.3333
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.7e-137), derived_msa-md (p_adj=1.6e-15), county_code (p_adj=1.8e-120), loan_type (p_adj=0.02), loan_amount (p_adj=1.4e-07), loan_term (p_adj=8.9e-15), property_value (p_adj=6.3e-28), construction_method (p_adj=1.5e-72), income (p_adj=4.6e-06), debt_to_income_ratio (p_adj=3.3e-06), applicant_credit_score_type (p_adj=5.6e-07), aus-1 (p_adj=6.2e-42), tract_population (p_adj=6e-86), ffiec_msa_md_median_family_income (p_adj=0.00014), tract_to_msa_income_percentage (p_adj=4.3e-36), tract_owner_occupied_units (p_adj=4.6e-100), tract_one_to_four_family_homes (p_adj=3.8e-74), tract_median_age_of_housing_units (p_adj=1.7e-26)
- องค์ประกอบ race_eth: Hispanic 3.5% (ทั้งชุด 9.1%), NH Asian 3.5% (ทั้งชุด 6.8%), NH Black 31.6% (ทั้งชุด 22.0%), NH White 45.6% (ทั้งชุด 41.8%), Other 3.5% (ทั้งชุด 2.3%), Unknown 12.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 47.4% (ทั้งชุด 27.1%), Joint 26.3% (ทั้งชุด 30.7%), Male 24.6% (ทั้งชุด 35.6%), Unknown 1.8% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.1% (ทั้งชุด 31.4%), 35-44 29.8% (ทั้งชุด 26.6%), 45-54 21.1% (ทั้งชุด 17.5%), 55-64 5.3% (ทั้งชุด 11.7%), 65-74 7.0% (ทั้งชุด 5.5%), <25 7.0% (ทั้งชุด 5.9%), >74 1.8% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 1
- IF derived_loan_product_type_FHA:First Lien ≤ 0.5 AND lei_549300AG64NHILB7ZP05 > 0.5 AND property_value ≤ 3.5e+05 THEN อยู่กลุ่มนี้
- IF derived_loan_product_type_FHA:First Lien > 0.5 AND ffiec_msa_md_median_family_income > 8.405e+04 AND preapproval_2 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 314/273/296 · coverage กฎบน validation 0.1620
- Fidelity F1 0.5711 · precision 0.4059 · recall 0.9634 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8311 · ERM error 0.0878 · FPR 0.5200 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: derived_msa-md (p_adj=1.3e-28), county_code (p_adj=1.6e-22), derived_loan_product_type (p_adj=1.7e-204), loan_type (p_adj=5.3e-207), loan_term (p_adj=2.7e-45), construction_method (p_adj=2.3e-05), income (p_adj=0.006), debt_to_income_ratio (p_adj=2.7e-26), submission_of_application (p_adj=0.033), aus-1 (p_adj=4.7e-138), tract_population (p_adj=6.8e-18), ffiec_msa_md_median_family_income (p_adj=7.5e-288), tract_to_msa_income_percentage (p_adj=1.9e-06), tract_owner_occupied_units (p_adj=2.3e-22), tract_one_to_four_family_homes (p_adj=2.7e-42)
- องค์ประกอบ race_eth: Hispanic 12.5% (ทั้งชุด 9.1%), NH Asian 3.7% (ทั้งชุด 6.8%), NH Black 49.0% (ทั้งชุด 22.0%), NH White 14.5% (ทั้งชุด 41.8%), Other 0.7% (ทั้งชุด 2.3%), Unknown 19.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 41.2% (ทั้งชุด 27.1%), Joint 24.0% (ทั้งชุด 30.7%), Male 26.0% (ทั้งชุด 35.6%), Unknown 8.8% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.4% (ทั้งชุด 31.4%), 35-44 32.1% (ทั้งชุด 26.6%), 45-54 19.9% (ทั้งชุด 17.5%), 55-64 11.1% (ทั้งชุด 11.7%), 65-74 1.7% (ทั้งชุด 5.5%), <25 4.4% (ทั้งชุด 5.9%), >74 0.3% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 2
- IF loan_type_1 ≤ 0.5 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND debt_to_income_ratio ≤ 60 THEN อยู่กลุ่มนี้
- IF loan_type_1 ≤ 0.5 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND debt_to_income_ratio > 60 THEN อยู่กลุ่มนี้
- IF loan_type_1 ≤ 0.5 AND ffiec_msa_md_median_family_income > 1.015e+05 AND loan_type_2 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF loan_type_1 > 0.5 AND ffiec_msa_md_median_family_income ≤ 9.58e+04 AND initially_payable_to_institution_3 > 0.5 THEN อยู่กลุ่มนี้
- IF loan_type_1 > 0.5 AND ffiec_msa_md_median_family_income > 9.58e+04 AND lei_5493003GQDUH26DNNH17 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 349/106/100 · coverage กฎบน validation 0.2303
- Fidelity F1 0.1597 · precision 0.0890 · recall 0.7736 · เงื่อนไขรวม 15 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- **กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี**
- คำอธิบายสำรอง: ตัวแปรที่ต่างจากส่วนที่เหลือมากที่สุด คำนวณบน train เท่านั้น
  - ffiec_msa_md_median_family_income: SMD -0.759; ค่าเฉลี่ยกลุ่ม 8.098e+04, ส่วนที่เหลือ 9.208e+04
  - debt_to_income_ratio: SMD 0.578; ค่าเฉลี่ยกลุ่ม 48.36, ส่วนที่เหลือ 41.09
  - property_value: SMD -0.555; ค่าเฉลี่ยกลุ่ม 2.756e+05, ส่วนที่เหลือ 3.964e+05
  - loan_type = 1: สัดส่วนต่าง -0.459; กลุ่ม 17.8%, ส่วนที่เหลือ 63.7%
  - income: SMD -0.443; ค่าเฉลี่ยกลุ่ม 77.09, ส่วนที่เหลือ 126.8
- อนุมัติจริง 0.8500 · ERM error 0.0700 · FPR 0.3333 · FNR 0.0235
- ตัวแปรต่างชัดหลัง Bonferroni: derived_msa-md (p_adj=3e-43), county_code (p_adj=1.2e-23), derived_loan_product_type (p_adj=2e-33), loan_type (p_adj=1.8e-32), loan_amount (p_adj=6e-17), loan_term (p_adj=9e-31), property_value (p_adj=3.1e-24), income (p_adj=1.5e-17), aus-1 (p_adj=8.6e-20), ffiec_msa_md_median_family_income (p_adj=2e-08)
- องค์ประกอบ race_eth: Hispanic 5.0% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 28.0% (ทั้งชุด 22.0%), NH White 44.0% (ทั้งชุด 41.8%), Other 5.0% (ทั้งชุด 2.3%), Unknown 18.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 35.0% (ทั้งชุด 27.1%), Joint 24.0% (ทั้งชุด 30.7%), Male 36.0% (ทั้งชุด 35.6%), Unknown 5.0% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.0% (ทั้งชุด 31.4%), 35-44 22.0% (ทั้งชุด 26.6%), 45-54 14.0% (ทั้งชุด 17.5%), 55-64 15.0% (ทั้งชุด 11.7%), 65-74 7.0% (ทั้งชุด 5.5%), <25 8.0% (ทั้งชุด 5.9%), >74 4.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 3
- IF construction_method_2 > 0.5 AND tract_one_to_four_family_homes > 1716 AND loan_term ≤ 328.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 202/92/93 · coverage กฎบน validation 0.0248
- Fidelity F1 0.6911 · precision 0.6667 · recall 0.7174 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.3763 · ERM error 0.1720 · FPR 0.1034 · FNR 0.2857
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=8.2e-47), derived_msa-md (p_adj=1.4e-59), county_code (p_adj=1.1e-70), derived_loan_product_type (p_adj=9.8e-18), loan_type (p_adj=3.9e-08), lien_status (p_adj=1.4e-10), loan_amount (p_adj=1.9e-43), loan_term (p_adj=2.3e-11), property_value (p_adj=2.2e-29), construction_method (p_adj=7.4e-96), income (p_adj=4.3e-11), applicant_credit_score_type (p_adj=2.6e-89), submission_of_application (p_adj=0.039), initially_payable_to_institution (p_adj=0.047), aus-1 (p_adj=4.5e-74), tract_population (p_adj=0.0018), ffiec_msa_md_median_family_income (p_adj=1.7e-14), tract_owner_occupied_units (p_adj=8.4e-10), tract_one_to_four_family_homes (p_adj=1.6e-18)
- องค์ประกอบ race_eth: Hispanic 8.6% (ทั้งชุด 9.1%), NH Asian 1.1% (ทั้งชุด 6.8%), NH Black 19.4% (ทั้งชุด 22.0%), NH White 55.9% (ทั้งชุด 41.8%), Other 4.3% (ทั้งชุด 2.3%), Unknown 10.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 32.3% (ทั้งชุด 27.1%), Joint 37.6% (ทั้งชุด 30.7%), Male 28.0% (ทั้งชุด 35.6%), Unknown 2.2% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.1% (ทั้งชุด 31.4%), 35-44 23.7% (ทั้งชุด 26.6%), 45-54 18.3% (ทั้งชุด 17.5%), 55-64 8.6% (ทั้งชุด 11.7%), 65-74 6.5% (ทั้งชุด 5.5%), <25 10.8% (ทั้งชุด 5.9%), >74 2.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 4
- IF aus-1_6 ≤ 0.5 AND loan_amount ≤ 6e+04 AND derived_msa-md_12060 > 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 ≤ 0.5 AND loan_amount > 6e+04 AND aus-1_7 > 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND ffiec_msa_md_median_family_income ≤ 8.98e+04 AND income ≤ 1 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND ffiec_msa_md_median_family_income > 8.98e+04 AND loan_amount ≤ 3.3e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 147/125/122 · coverage กฎบน validation 0.0717
- Fidelity F1 0.5777 · precision 0.4146 · recall 0.9520 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.6311 · ERM error 0.2131 · FPR 0.2222 · FNR 0.2078
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.2e-06), derived_msa-md (p_adj=1.3e-06), county_code (p_adj=7.2e-11), derived_loan_product_type (p_adj=5.1e-247), loan_type (p_adj=8e-13), lien_status (p_adj=1.4e-244), loan_amount (p_adj=4.4e-77), loan_term (p_adj=3.8e-15), property_value (p_adj=6.4e-35), construction_method (p_adj=7.3e-40), income (p_adj=6.8e-21), applicant_credit_score_type (p_adj=1.5e-15), aus-1 (p_adj=1.4e-93), ffiec_msa_md_median_family_income (p_adj=6.9e-122), tract_to_msa_income_percentage (p_adj=1.4e-10)
- องค์ประกอบ race_eth: Hispanic 8.2% (ทั้งชุด 9.1%), NH Asian 1.6% (ทั้งชุด 6.8%), NH Black 24.6% (ทั้งชุด 22.0%), NH White 36.1% (ทั้งชุด 41.8%), Other 2.5% (ทั้งชุด 2.3%), Unknown 27.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 32.8% (ทั้งชุด 27.1%), Joint 27.9% (ทั้งชุด 30.7%), Male 32.8% (ทั้งชุด 35.6%), Unknown 6.6% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 29.5% (ทั้งชุด 31.4%), 35-44 30.3% (ทั้งชุด 26.6%), 45-54 16.4% (ทั้งชุด 17.5%), 55-64 15.6% (ทั้งชุด 11.7%), 65-74 0.0% (ทั้งชุด 5.5%), <25 7.4% (ทั้งชุด 5.9%), >74 0.8% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 5
- IF loan_amount ≤ 4.6e+05 AND tract_owner_occupied_units ≤ 1182 AND income > 599 THEN อยู่กลุ่มนี้
- IF loan_amount ≤ 4.6e+05 AND tract_owner_occupied_units > 1182 AND derived_loan_product_type_Conventional:First Lien > 0.5 THEN อยู่กลุ่มนี้
- IF loan_amount > 4.6e+05 AND tract_owner_occupied_units > 584 AND derived_loan_product_type_FHA:First Lien ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 172/278/298 · coverage กฎบน validation 0.3142
- Fidelity F1 0.3479 · precision 0.2124 · recall 0.9604 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- **กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี**
- คำอธิบายสำรอง: ตัวแปรที่ต่างจากส่วนที่เหลือมากที่สุด คำนวณบน train เท่านั้น
  - loan_amount: SMD 0.953; ค่าเฉลี่ยกลุ่ม 5.641e+05, ส่วนที่เหลือ 3.21e+05
  - property_value: SMD 0.939; ค่าเฉลี่ยกลุ่ม 7.033e+05, ส่วนที่เหลือ 3.889e+05
  - tract_owner_occupied_units: SMD 0.899; ค่าเฉลี่ยกลุ่ม 1510, ส่วนที่เหลือ 1094
  - ffiec_msa_md_median_family_income: SMD 0.808; ค่าเฉลี่ยกลุ่ม 1.011e+05, ส่วนที่เหลือ 9.162e+04
  - tract_to_msa_income_percentage: SMD 0.689; ค่าเฉลี่ยกลุ่ม 138.7, ส่วนที่เหลือ 107.3
- อนุมัติจริง 0.9329 · ERM error 0.0537 · FPR 0.7500 · FNR 0.0036
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.9e-13), derived_msa-md (p_adj=1.5e-24), county_code (p_adj=3.6e-112), conforming_loan_limit (p_adj=2.6e-07), derived_loan_product_type (p_adj=4.2e-34), loan_type (p_adj=1.9e-32), loan_amount (p_adj=1.4e-74), property_value (p_adj=2.7e-75), construction_method (p_adj=1.9e-06), income (p_adj=7.3e-33), debt_to_income_ratio (p_adj=3.1e-14), initially_payable_to_institution (p_adj=0.019), aus-1 (p_adj=2.6e-12), tract_population (p_adj=1.3e-19), ffiec_msa_md_median_family_income (p_adj=9.1e-136), tract_to_msa_income_percentage (p_adj=1.2e-47), tract_owner_occupied_units (p_adj=1.4e-61), tract_one_to_four_family_homes (p_adj=6.5e-14), tract_median_age_of_housing_units (p_adj=1.3e-18)
- องค์ประกอบ race_eth: Hispanic 5.4% (ทั้งชุด 9.1%), NH Asian 23.5% (ทั้งชุด 6.8%), NH Black 9.7% (ทั้งชุด 22.0%), NH White 41.9% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.3%), Unknown 17.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 19.8% (ทั้งชุด 27.1%), Joint 40.6% (ทั้งชุด 30.7%), Male 33.2% (ทั้งชุด 35.6%), Unknown 6.4% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 25.8% (ทั้งชุด 31.4%), 35-44 38.6% (ทั้งชุด 26.6%), 45-54 20.8% (ทั้งชุด 17.5%), 55-64 9.1% (ทั้งชุด 11.7%), 65-74 4.7% (ทั้งชุด 5.5%), <25 0.0% (ทั้งชุด 5.9%), >74 1.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 6
- IF derived_loan_product_type_Conventional:First Lien ≤ 0.5 AND tract_one_to_four_family_homes ≤ 546 AND tract_population > 3190 THEN อยู่กลุ่มนี้
- IF derived_loan_product_type_Conventional:First Lien > 0.5 AND derived_msa-md_12060 ≤ 0.5 AND tract_median_age_of_housing_units > 49.5 THEN อยู่กลุ่มนี้
- IF derived_loan_product_type_Conventional:First Lien > 0.5 AND derived_msa-md_12060 > 0.5 AND debt_to_income_ratio ≤ 52 THEN อยู่กลุ่มนี้
- IF derived_loan_product_type_Conventional:First Lien > 0.5 AND derived_msa-md_12060 > 0.5 AND debt_to_income_ratio > 52 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 241/379/397 · coverage กฎบน validation 0.4000
- Fidelity F1 0.3669 · precision 0.2269 · recall 0.9578 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- **กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี**
- คำอธิบายสำรอง: ตัวแปรที่ต่างจากส่วนที่เหลือมากที่สุด คำนวณบน train เท่านั้น
  - ffiec_msa_md_median_family_income: SMD 0.856; ค่าเฉลี่ยกลุ่ม 1.015e+05, ส่วนที่เหลือ 9.156e+04
  - tract_one_to_four_family_homes: SMD -0.742; ค่าเฉลี่ยกลุ่ม 1137, ส่วนที่เหลือ 1549
  - tract_owner_occupied_units: SMD -0.702; ค่าเฉลี่ยกลุ่ม 802.1, ส่วนที่เหลือ 1106
  - tract_population: SMD -0.481; ค่าเฉลี่ยกลุ่ม 3799, ส่วนที่เหลือ 4514
  - debt_to_income_ratio: SMD 0.463; ค่าเฉลี่ยกลุ่ม 47.25, ส่วนที่เหลือ 41.19
- อนุมัติจริง 0.8564 · ERM error 0.0680 · FPR 0.4035 · FNR 0.0118
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0015), derived_msa-md (p_adj=1.8e-43), county_code (p_adj=7.1e-47), derived_loan_product_type (p_adj=1.3e-48), loan_type (p_adj=7.9e-46), loan_amount (p_adj=9.6e-17), loan_term (p_adj=2e-20), property_value (p_adj=2e-21), construction_method (p_adj=9.8e-07), income (p_adj=1.2e-20), aus-1 (p_adj=1.2e-19), tract_population (p_adj=4.3e-36), ffiec_msa_md_median_family_income (p_adj=3.5e-296), tract_to_msa_income_percentage (p_adj=8.9e-40), tract_owner_occupied_units (p_adj=3.3e-89), tract_one_to_four_family_homes (p_adj=9.2e-63), tract_median_age_of_housing_units (p_adj=6e-16)
- องค์ประกอบ race_eth: Hispanic 17.4% (ทั้งชุด 9.1%), NH Asian 9.1% (ทั้งชุด 6.8%), NH Black 22.2% (ทั้งชุด 22.0%), NH White 31.5% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.3%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 36.8% (ทั้งชุด 27.1%), Joint 19.4% (ทั้งชุด 30.7%), Male 36.0% (ทั้งชุด 35.6%), Unknown 7.8% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 34.5% (ทั้งชุด 31.4%), 35-44 28.7% (ทั้งชุด 26.6%), 45-54 14.6% (ทั้งชุด 17.5%), 55-64 12.3% (ทั้งชุด 11.7%), 65-74 4.5% (ทั้งชุด 5.5%), <25 5.0% (ทั้งชุด 5.9%), >74 0.3% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 7
- IF construction_method_1 ≤ 0.5 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND derived_loan_product_type_Conventional:First Lien > 0.5 THEN อยู่กลุ่มนี้
- IF construction_method_1 > 0.5 AND applicant_credit_score_type_1111 > 0.5 AND tract_population ≤ 4886 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 385/171/177 · coverage กฎบน validation 0.0803
- Fidelity F1 0.6545 · precision 0.5016 · recall 0.9415 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.3785 · ERM error 0.2429 · FPR 0.1545 · FNR 0.3881
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.8e-202), derived_msa-md (p_adj=1.8e-119), county_code (p_adj=1.7e-244), derived_loan_product_type (p_adj=5.2e-21), loan_type (p_adj=1.5e-20), loan_amount (p_adj=8.4e-58), loan_term (p_adj=1.4e-28), property_value (p_adj=2.4e-153), construction_method (p_adj=6.8e-211), income (p_adj=1.1e-30), applicant_credit_score_type (p_adj=6.6e-142), submission_of_application (p_adj=1.5e-87), initially_payable_to_institution (p_adj=1.1e-87), aus-1 (p_adj=2e-216), tract_population (p_adj=2.1e-37), ffiec_msa_md_median_family_income (p_adj=5.1e-161), tract_to_msa_income_percentage (p_adj=0.00059), tract_owner_occupied_units (p_adj=7.3e-31), tract_median_age_of_housing_units (p_adj=5e-17)
- องค์ประกอบ race_eth: Hispanic 3.4% (ทั้งชุด 9.1%), NH Asian 0.6% (ทั้งชุด 6.8%), NH Black 26.0% (ทั้งชุด 22.0%), NH White 50.3% (ทั้งชุด 41.8%), Other 1.1% (ทั้งชุด 2.3%), Unknown 18.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 33.9% (ทั้งชุด 27.1%), Joint 31.6% (ทั้งชุด 30.7%), Male 30.5% (ทั้งชุด 35.6%), Unknown 4.0% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 29.4% (ทั้งชุด 31.4%), 35-44 20.3% (ทั้งชุด 26.6%), 45-54 17.5% (ทั้งชุด 17.5%), 55-64 14.7% (ทั้งชุด 11.7%), 65-74 5.6% (ทั้งชุด 5.5%), <25 10.7% (ทั้งชุด 5.9%), >74 1.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 8
- IF derived_loan_product_type_FHA:First Lien ≤ 0.5 AND derived_loan_product_type_FSA/RHS:First Lien > 0.5 AND tract_median_age_of_housing_units ≤ 30.5 THEN อยู่กลุ่มนี้
- IF derived_loan_product_type_FHA:First Lien ≤ 0.5 AND derived_loan_product_type_FSA/RHS:First Lien > 0.5 AND tract_median_age_of_housing_units > 30.5 THEN อยู่กลุ่มนี้
- IF derived_loan_product_type_FHA:First Lien > 0.5 AND derived_msa-md_12060 ≤ 0.5 AND tract_owner_occupied_units ≤ 1833 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 951/329/334 · coverage กฎบน validation 0.0973
- Fidelity F1 0.8858 · precision 0.8175 · recall 0.9666 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8563 · ERM error 0.1078 · FPR 0.7292 · FNR 0.0035
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.3e-09), derived_msa-md (p_adj=1.1e-125), county_code (p_adj=1.8e-123), derived_loan_product_type (p_adj=7.8e-231), loan_type (p_adj=6.6e-233), loan_amount (p_adj=4.1e-55), loan_term (p_adj=1.3e-58), property_value (p_adj=5.7e-96), income (p_adj=8.2e-43), aus-1 (p_adj=9.9e-179), ffiec_msa_md_median_family_income (p_adj=2.3e-140), tract_owner_occupied_units (p_adj=0.012), tract_median_age_of_housing_units (p_adj=3.5e-08)
- องค์ประกอบ race_eth: Hispanic 9.0% (ทั้งชุด 9.1%), NH Asian 0.3% (ทั้งชุด 6.8%), NH Black 24.0% (ทั้งชุด 22.0%), NH White 48.8% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.3%), Unknown 15.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 31.1% (ทั้งชุด 27.1%), Joint 28.7% (ทั้งชุด 30.7%), Male 32.6% (ทั้งชุด 35.6%), Unknown 7.5% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 37.7% (ทั้งชุด 31.4%), 35-44 24.0% (ทั้งชุด 26.6%), 45-54 13.8% (ทั้งชุด 17.5%), 55-64 10.8% (ทั้งชุด 11.7%), 65-74 3.3% (ทั้งชุด 5.5%), <25 10.2% (ทั้งชุด 5.9%), >74 0.3% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 9
- IF derived_msa-md_12060 > 0.5 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND tract_owner_occupied_units ≤ 1594 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2850/549/545 · coverage กฎบน validation 0.3167
- Fidelity F1 0.5870 · precision 0.4207 · recall 0.9709 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9394 · ERM error 0.0404 · FPR 0.6061 · FNR 0.0039
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=7.2e-15), derived_msa-md (p_adj=1.8e-74), county_code (p_adj=3e-78), derived_loan_product_type (p_adj=1.3e-83), loan_type (p_adj=1.3e-78), loan_amount (p_adj=7.1e-26), property_value (p_adj=7e-37), construction_method (p_adj=1.8e-14), income (p_adj=1.2e-16), debt_to_income_ratio (p_adj=1.1e-21), submission_of_application (p_adj=1.5e-10), initially_payable_to_institution (p_adj=7.4e-06), aus-1 (p_adj=4.3e-76), tract_population (p_adj=1.6e-09), ffiec_msa_md_median_family_income (p_adj=0), tract_to_msa_income_percentage (p_adj=5.7e-12), tract_owner_occupied_units (p_adj=8.2e-07), tract_one_to_four_family_homes (p_adj=1.7e-42)
- องค์ประกอบ race_eth: Hispanic 8.6% (ทั้งชุด 9.1%), NH Asian 16.1% (ทั้งชุด 6.8%), NH Black 12.5% (ทั้งชุด 22.0%), NH White 44.8% (ทั้งชุด 41.8%), Other 2.9% (ทั้งชุด 2.3%), Unknown 15.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 24.2% (ทั้งชุด 27.1%), Joint 33.4% (ทั้งชุด 30.7%), Male 37.8% (ทั้งชุด 35.6%), Unknown 4.6% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 39.1% (ทั้งชุด 31.4%), 35-44 27.5% (ทั้งชุด 26.6%), 45-54 16.0% (ทั้งชุด 17.5%), 55-64 9.2% (ทั้งชุด 11.7%), 65-74 3.9% (ทั้งชุด 5.5%), <25 3.7% (ทั้งชุด 5.9%), >74 0.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 10
- IF derived_msa-md_12060 ≤ 0.5 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND construction_method_1 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1216/410/371 · coverage กฎบน validation 0.1580
- Fidelity F1 0.7466 · precision 0.6155 · recall 0.9488 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9407 · ERM error 0.0350 · FPR 0.4545 · FNR 0.0086
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.4e-11), derived_msa-md (p_adj=3.2e-164), county_code (p_adj=1.3e-163), derived_loan_product_type (p_adj=3.3e-53), loan_type (p_adj=1.6e-50), loan_amount (p_adj=3e-05), loan_term (p_adj=4.3e-05), construction_method (p_adj=0.00015), debt_to_income_ratio (p_adj=6.7e-19), aus-1 (p_adj=6.9e-30), tract_population (p_adj=3.8e-11), ffiec_msa_md_median_family_income (p_adj=2.9e-112), tract_to_msa_income_percentage (p_adj=0.00014)
- องค์ประกอบ race_eth: Hispanic 7.0% (ทั้งชุด 9.1%), NH Asian 3.2% (ทั้งชุด 6.8%), NH Black 4.9% (ทั้งชุด 22.0%), NH White 66.3% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.3%), Unknown 15.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 21.3% (ทั้งชุด 27.1%), Joint 38.0% (ทั้งชุด 30.7%), Male 33.7% (ทั้งชุด 35.6%), Unknown 7.0% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 27.5% (ทั้งชุด 31.4%), 35-44 16.4% (ทั้งชุด 26.6%), 45-54 16.7% (ทั้งชุด 17.5%), 55-64 17.8% (ทั้งชุด 11.7%), 65-74 11.6% (ทั้งชุด 5.5%), <25 7.0% (ทั้งชุด 5.9%), >74 3.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 11
- IF tract_owner_occupied_units > 1583 AND tract_owner_occupied_units > 1839 AND loan_type_1 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1301/358/354 · coverage กฎบน validation 0.0493
- Fidelity F1 0.5477 · precision 0.7716 · recall 0.4246 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9181 · ERM error 0.0593 · FPR 0.6552 · FNR 0.0062
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0022), derived_msa-md (p_adj=3.8e-30), county_code (p_adj=3.1e-117), derived_loan_product_type (p_adj=1.3e-07), loan_type (p_adj=2.7e-07), loan_term (p_adj=0.0012), construction_method (p_adj=9.2e-07), submission_of_application (p_adj=0.027), aus-1 (p_adj=4e-11), tract_population (p_adj=7.1e-93), ffiec_msa_md_median_family_income (p_adj=1.2e-12), tract_to_msa_income_percentage (p_adj=1e-08), tract_owner_occupied_units (p_adj=3.4e-131), tract_one_to_four_family_homes (p_adj=8.6e-100), tract_median_age_of_housing_units (p_adj=4.1e-80)
- องค์ประกอบ race_eth: Hispanic 9.6% (ทั้งชุด 9.1%), NH Asian 6.8% (ทั้งชุด 6.8%), NH Black 13.8% (ทั้งชุด 22.0%), NH White 45.8% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.3%), Unknown 21.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 18.1% (ทั้งชุด 27.1%), Joint 32.8% (ทั้งชุด 30.7%), Male 41.8% (ทั้งชุด 35.6%), Unknown 7.3% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.2% (ทั้งชุด 31.4%), 35-44 26.8% (ทั้งชุด 26.6%), 45-54 19.2% (ทั้งชุด 17.5%), 55-64 13.6% (ทั้งชุด 11.7%), 65-74 5.6% (ทั้งชุด 5.5%), <25 4.2% (ทั้งชุด 5.9%), >74 2.3% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 12
- IF conforming_loan_limit_C ≤ 0.5 AND income > 250.5 AND loan_type_1 > 0.5 THEN อยู่กลุ่มนี้
- IF conforming_loan_limit_C > 0.5 AND income > 868.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 283/99/73 · coverage กฎบน validation 0.0238
- Fidelity F1 0.8557 · precision 0.8737 · recall 0.8384 · เงื่อนไขรวม 5 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9452 · ERM error 0.0685 · FPR 1.0000 · FNR 0.0145
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=6.2e-23), conforming_loan_limit (p_adj=0), derived_loan_product_type (p_adj=1.9e-05), loan_type (p_adj=7.4e-06), loan_amount (p_adj=2.8e-18), loan_term (p_adj=8.7e-56), property_value (p_adj=1.5e-19), income (p_adj=9.5e-10), debt_to_income_ratio (p_adj=6.7e-07), aus-1 (p_adj=7.4e-20), ffiec_msa_md_median_family_income (p_adj=1.6e-05), tract_to_msa_income_percentage (p_adj=4.2e-12)
- องค์ประกอบ race_eth: Hispanic 4.1% (ทั้งชุด 9.1%), NH Asian 12.3% (ทั้งชุด 6.8%), NH Black 5.5% (ทั้งชุด 22.0%), NH White 54.8% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.3%), Unknown 20.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 8.2% (ทั้งชุด 27.1%), Joint 45.2% (ทั้งชุด 30.7%), Male 39.7% (ทั้งชุด 35.6%), Unknown 6.8% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 20.5% (ทั้งชุด 31.4%), 35-44 37.0% (ทั้งชุด 26.6%), 45-54 27.4% (ทั้งชุด 17.5%), 55-64 13.7% (ทั้งชุด 11.7%), 65-74 1.4% (ทั้งชุด 5.5%), <25 0.0% (ทั้งชุด 5.9%), >74 0.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 13
- IF loan_type_3 ≤ 0.5 AND derived_msa-md_42340 > 0.5 AND aus-1_1 > 0.5 THEN อยู่กลุ่มนี้
- IF loan_type_3 > 0.5 AND tract_owner_occupied_units ≤ 2216 AND tract_owner_occupied_units ≤ 1904 THEN อยู่กลุ่มนี้
- IF loan_type_3 > 0.5 AND tract_owner_occupied_units ≤ 2216 AND tract_owner_occupied_units > 1904 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1338/448/455 · coverage กฎบน validation 0.1333
- Fidelity F1 0.9011 · precision 0.8293 · recall 0.9866 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8901 · ERM error 0.0747 · FPR 0.5600 · FNR 0.0148
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.6e-109), derived_msa-md (p_adj=1.9e-83), county_code (p_adj=3.6e-58), derived_loan_product_type (p_adj=0), loan_type (p_adj=0), loan_term (p_adj=8e-69), property_value (p_adj=7.7e-08), construction_method (p_adj=8.2e-07), income (p_adj=9.4e-11), debt_to_income_ratio (p_adj=1.2e-11), applicant_credit_score_type (p_adj=0.00013), aus-1 (p_adj=1.3e-64), ffiec_msa_md_median_family_income (p_adj=2.3e-14), tract_median_age_of_housing_units (p_adj=0.019)
- องค์ประกอบ race_eth: Hispanic 6.4% (ทั้งชุด 9.1%), NH Asian 1.8% (ทั้งชุด 6.8%), NH Black 27.3% (ทั้งชุด 22.0%), NH White 40.0% (ทั้งชุด 41.8%), Other 3.1% (ทั้งชุด 2.3%), Unknown 21.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 13.2% (ทั้งชุด 27.1%), Joint 31.9% (ทั้งชุด 30.7%), Male 48.6% (ทั้งชุด 35.6%), Unknown 6.4% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.8% (ทั้งชุด 31.4%), 35-44 24.2% (ทั้งชุด 26.6%), 45-54 15.8% (ทั้งชุด 17.5%), 55-64 11.4% (ทั้งชุด 11.7%), 65-74 9.7% (ทั้งชุด 5.5%), <25 7.5% (ทั้งชุด 5.9%), >74 2.6% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 14
- IF loan_type_2 > 0.5 AND derived_msa-md_12060 > 0.5 AND debt_to_income_ratio ≤ 60 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1510/286/285 · coverage กฎบน validation 0.1360
- Fidelity F1 0.6699 · precision 0.5110 · recall 0.9720 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8596 · ERM error 0.0877 · FPR 0.5500 · FNR 0.0122
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=9.2e-11), derived_msa-md (p_adj=2.3e-33), county_code (p_adj=4.9e-59), derived_loan_product_type (p_adj=3.8e-194), loan_type (p_adj=1.3e-196), loan_term (p_adj=9.3e-60), property_value (p_adj=1.1e-21), construction_method (p_adj=0.0035), income (p_adj=1.3e-29), debt_to_income_ratio (p_adj=1.6e-27), applicant_credit_score_type (p_adj=0.00038), aus-1 (p_adj=3.6e-96), tract_population (p_adj=6.2e-17), ffiec_msa_md_median_family_income (p_adj=0), tract_to_msa_income_percentage (p_adj=4.1e-34), tract_owner_occupied_units (p_adj=2e-07), tract_one_to_four_family_homes (p_adj=2.7e-11)
- องค์ประกอบ race_eth: Hispanic 13.7% (ทั้งชุด 9.1%), NH Asian 2.1% (ทั้งชุด 6.8%), NH Black 43.5% (ทั้งชุด 22.0%), NH White 21.4% (ทั้งชุด 41.8%), Other 1.1% (ทั้งชุด 2.3%), Unknown 18.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 38.2% (ทั้งชุด 27.1%), Joint 26.0% (ทั้งชุด 30.7%), Male 28.1% (ทั้งชุด 35.6%), Unknown 7.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 29.8% (ทั้งชุด 31.4%), 35-44 26.3% (ทั้งชุด 26.6%), 45-54 23.5% (ทั้งชุด 17.5%), 55-64 8.4% (ทั้งชุด 11.7%), 65-74 3.5% (ทั้งชุด 5.5%), <25 8.4% (ทั้งชุด 5.9%), >74 0.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · cy · seed 17 · กลุ่ม 15
- IF loan_amount ≤ 3e+04 AND tract_population ≤ 5871 AND aus-1_6 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF loan_amount ≤ 3e+04 AND tract_population ≤ 5871 AND aus-1_6 > 0.5 THEN อยู่กลุ่มนี้
- IF loan_amount > 3e+04 AND aus-1_1111 > 0.5 AND tract_median_age_of_housing_units > 27.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 591/54/43 · coverage กฎบน validation 0.0272
- Fidelity F1 0.1840 · precision 0.1376 · recall 0.2778 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- **กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี**
- คำอธิบายสำรอง: ตัวแปรที่ต่างจากส่วนที่เหลือมากที่สุด คำนวณบน train เท่านั้น
  - loan_amount: SMD -1.379; ค่าเฉลี่ยกลุ่ม 1.08e+05, ส่วนที่เหลือ 3.357e+05
  - loan_term: SMD -1.048; ค่าเฉลี่ยกลุ่ม 273, ส่วนที่เหลือ 350.5
  - property_value: SMD -0.982; ค่าเฉลี่ยกลุ่ม 1.953e+05, ส่วนที่เหลือ 4.019e+05
  - ffiec_msa_md_median_family_income: SMD -0.746; ค่าเฉลี่ยกลุ่ม 8.077e+04, ส่วนที่เหลือ 9.233e+04
  - aus-1 = 6: สัดส่วนต่าง +0.596; กลุ่ม 74.1%, ส่วนที่เหลือ 14.5%
- อนุมัติจริง 0.5116 · ERM error 0.1860 · FPR 0.2857 · FNR 0.0909
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.2e-24), derived_msa-md (p_adj=1.2e-10), county_code (p_adj=9.6e-12), derived_loan_product_type (p_adj=9.3e-20), lien_status (p_adj=8.4e-20), loan_amount (p_adj=5.4e-16), loan_term (p_adj=0.0047), property_value (p_adj=1.2e-11), construction_method (p_adj=4.6e-10), income (p_adj=1.7e-07), applicant_credit_score_type (p_adj=9.9e-20), aus-1 (p_adj=2.1e-15), tract_population (p_adj=0.013), ffiec_msa_md_median_family_income (p_adj=7.1e-11)
- องค์ประกอบ race_eth: Hispanic 7.0% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 23.3% (ทั้งชุด 22.0%), NH White 55.8% (ทั้งชุด 41.8%), Other 0.0% (ทั้งชุด 2.3%), Unknown 14.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 27.9% (ทั้งชุด 27.1%), Joint 18.6% (ทั้งชุด 30.7%), Male 44.2% (ทั้งชุด 35.6%), Unknown 9.3% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 41.9% (ทั้งชุด 31.4%), 35-44 18.6% (ทั้งชุด 26.6%), 45-54 16.3% (ทั้งชุด 17.5%), 55-64 4.7% (ทั้งชุด 11.7%), 65-74 9.3% (ทั้งชุด 5.5%), <25 4.7% (ทั้งชุด 5.9%), >74 4.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 17 · กลุ่ม 0
- IF debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 ≤ 0.5 AND tract_one_to_four_family_homes ≤ 16.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 > 0.5 AND lei_549300DD4R4SYK5RAQ92 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND derived_loan_product_type_Conventional:First Lien ≤ 0.5 AND tract_population ≤ 4600 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND income ≤ 94 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND income > 94 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 695/205/230 · coverage กฎบน validation 0.0617
- Fidelity F1 0.7920 · precision 0.7247 · recall 0.8732 · เงื่อนไขรวม 15 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.0217 · ERM error 0.0217 · FPR 0.0000 · FNR 1.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.1e-73), derived_msa-md (p_adj=1.2e-10), county_code (p_adj=2.4e-37), derived_loan_product_type (p_adj=8.6e-09), loan_type (p_adj=3.8e-09), loan_amount (p_adj=2.6e-23), loan_term (p_adj=2.5e-20), property_value (p_adj=1.8e-28), construction_method (p_adj=2.3e-123), income (p_adj=5.7e-53), debt_to_income_ratio (p_adj=1.1e-77), applicant_credit_score_type (p_adj=4e-40), initially_payable_to_institution (p_adj=1.2e-107), aus-1 (p_adj=1.9e-97), tract_population (p_adj=2.9e-14), ffiec_msa_md_median_family_income (p_adj=4.4e-08), tract_to_msa_income_percentage (p_adj=3.8e-18), tract_owner_occupied_units (p_adj=2.6e-14), tract_one_to_four_family_homes (p_adj=2.1e-06)
- องค์ประกอบ race_eth: Hispanic 10.0% (ทั้งชุด 9.1%), NH Asian 4.8% (ทั้งชุด 6.8%), NH Black 30.9% (ทั้งชุด 22.0%), NH White 35.2% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.3%), Unknown 17.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 41.7% (ทั้งชุด 27.1%), Joint 23.5% (ทั้งชุด 30.7%), Male 28.7% (ทั้งชุด 35.6%), Unknown 6.1% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.4% (ทั้งชุด 31.4%), 35-44 26.1% (ทั้งชุด 26.6%), 45-54 20.4% (ทั้งชุด 17.5%), 55-64 10.0% (ทั้งชุด 11.7%), 65-74 5.7% (ทั้งชุด 5.5%), <25 6.5% (ทั้งชุด 5.9%), >74 0.9% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 17 · กลุ่ม 1
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio ≤ 52 AND initially_payable_to_institution_3 > 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio > 52 AND debt_to_income_ratio ≤ 60 THEN อยู่กลุ่มนี้
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio > 52 AND debt_to_income_ratio > 60 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND debt_to_income_ratio ≤ 60 AND construction_method_2 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND debt_to_income_ratio ≤ 60 AND construction_method_2 > 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND debt_to_income_ratio > 60 AND loan_term > 320.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1265/594/587 · coverage กฎบน validation 0.3095
- Fidelity F1 0.5371 · precision 0.3974 · recall 0.8283 · เงื่อนไขรวม 18 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.5741 · ERM error 0.2470 · FPR 0.2760 · FNR 0.2255
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.3e-57), derived_msa-md (p_adj=0.0044), county_code (p_adj=1.7e-27), preapproval (p_adj=0.00014), loan_amount (p_adj=1.2e-34), loan_term (p_adj=7.8e-14), property_value (p_adj=7.5e-60), construction_method (p_adj=1.7e-106), income (p_adj=7.9e-37), applicant_credit_score_type (p_adj=4.9e-35), initially_payable_to_institution (p_adj=0.00021), aus-1 (p_adj=2.7e-129), tract_population (p_adj=0.0017), ffiec_msa_md_median_family_income (p_adj=0.00022), tract_to_msa_income_percentage (p_adj=3.2e-19), tract_owner_occupied_units (p_adj=0.00019)
- องค์ประกอบ race_eth: Hispanic 7.8% (ทั้งชุด 9.1%), NH Asian 2.9% (ทั้งชุด 6.8%), NH Black 32.4% (ทั้งชุด 22.0%), NH White 37.0% (ทั้งชุด 41.8%), Other 2.2% (ทั้งชุด 2.3%), Unknown 17.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 33.7% (ทั้งชุด 27.1%), Joint 26.6% (ทั้งชุด 30.7%), Male 33.7% (ทั้งชุด 35.6%), Unknown 6.0% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.7% (ทั้งชุด 31.4%), 35-44 24.7% (ทั้งชุด 26.6%), 45-54 17.5% (ทั้งชุด 17.5%), 55-64 13.1% (ทั้งชุด 11.7%), 65-74 3.7% (ทั้งชุด 5.5%), <25 9.0% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 17 · กลุ่ม 2
- IF preapproval_1 ≤ 0.5 AND debt_to_income_ratio ≤ 60 AND lei_549300FGXN1K3HLB1R50 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 8000/2546/2479 · coverage กฎบน validation 0.8735
- Fidelity F1 0.8354 · precision 0.7221 · recall 0.9910 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9306 · ERM error 0.0694 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1e-161), derived_msa-md (p_adj=9.9e-13), county_code (p_adj=2.2e-15), derived_loan_product_type (p_adj=8.7e-09), preapproval (p_adj=1e-63), loan_type (p_adj=7.1e-09), loan_amount (p_adj=8.2e-06), loan_term (p_adj=5.3e-15), property_value (p_adj=1.4e-05), construction_method (p_adj=8.5e-94), debt_to_income_ratio (p_adj=9.4e-07), applicant_credit_score_type (p_adj=1e-38), initially_payable_to_institution (p_adj=2.3e-34), aus-1 (p_adj=1.3e-81), tract_population (p_adj=0.0028), ffiec_msa_md_median_family_income (p_adj=1.4e-12), tract_to_msa_income_percentage (p_adj=0.045), tract_owner_occupied_units (p_adj=0.021)
- องค์ประกอบ race_eth: Hispanic 10.5% (ทั้งชุด 9.1%), NH Asian 8.0% (ทั้งชุด 6.8%), NH Black 21.0% (ทั้งชุด 22.0%), NH White 40.3% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.3%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 25.9% (ทั้งชุด 27.1%), Joint 31.1% (ทั้งชุด 30.7%), Male 36.9% (ทั้งชุด 35.6%), Unknown 6.1% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 31.9% (ทั้งชุด 31.4%), 35-44 26.5% (ทั้งชุด 26.6%), 45-54 18.0% (ทั้งชุด 17.5%), 55-64 11.3% (ทั้งชุด 11.7%), 65-74 5.7% (ทั้งชุด 5.5%), <25 5.3% (ทั้งชุด 5.9%), >74 1.3% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 17 · กลุ่ม 3
- IF preapproval_1 ≤ 0.5 AND lei_549300MGPZBLQDIL7538 ≤ 0.5 AND lei_549300FGXN1K3HLB1R50 > 0.5 THEN อยู่กลุ่มนี้
- IF preapproval_1 ≤ 0.5 AND lei_549300MGPZBLQDIL7538 > 0.5 AND derived_loan_product_type_Conventional:First Lien ≤ 0.5 THEN อยู่กลุ่มนี้
- IF preapproval_1 ≤ 0.5 AND lei_549300MGPZBLQDIL7538 > 0.5 AND derived_loan_product_type_Conventional:First Lien > 0.5 THEN อยู่กลุ่มนี้
- IF preapproval_1 > 0.5 AND property_value ≤ 2.5e+05 THEN อยู่กลุ่มนี้
- IF preapproval_1 > 0.5 AND property_value > 2.5e+05 AND tract_owner_occupied_units ≤ 1448 THEN อยู่กลุ่มนี้
- IF preapproval_1 > 0.5 AND property_value > 2.5e+05 AND tract_owner_occupied_units > 1448 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2040/655/704 · coverage กฎบน validation 0.1040
- Fidelity F1 0.6443 · precision 0.8293 · recall 0.5267 · เงื่อนไขรวม 17 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9915 · ERM error 0.0085 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.3e-194), derived_msa-md (p_adj=0.028), county_code (p_adj=2.6e-12), derived_loan_product_type (p_adj=1.5e-07), preapproval (p_adj=3.4e-184), loan_type (p_adj=2.7e-07), loan_amount (p_adj=2.7e-05), loan_term (p_adj=2.3e-05), property_value (p_adj=9.9e-09), construction_method (p_adj=1.3e-14), income (p_adj=1.7e-06), debt_to_income_ratio (p_adj=1.9e-20), submission_of_application (p_adj=0.0042), initially_payable_to_institution (p_adj=1e-05), aus-1 (p_adj=5.1e-34), tract_to_msa_income_percentage (p_adj=1e-13), tract_owner_occupied_units (p_adj=0.0043)
- องค์ประกอบ race_eth: Hispanic 5.0% (ทั้งชุด 9.1%), NH Asian 6.4% (ทั้งชุด 6.8%), NH Black 13.9% (ทั้งชุด 22.0%), NH White 53.1% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.3%), Unknown 19.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 21.2% (ทั้งชุด 27.1%), Joint 35.2% (ทั้งชุด 30.7%), Male 35.1% (ทั้งชุด 35.6%), Unknown 8.5% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.7% (ทั้งชุด 31.4%), 35-44 28.6% (ทั้งชุด 26.6%), 45-54 15.2% (ทั้งชุด 17.5%), 55-64 12.4% (ทั้งชุด 11.7%), 65-74 6.0% (ทั้งชุด 5.5%), <25 5.5% (ทั้งชุด 5.9%), >74 1.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k8 · c · seed 17 · กลุ่ม 0
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND loan_term > 337 AND tract_owner_occupied_units ≤ 1781 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2477/833/800 · coverage กฎบน validation 0.2120
- Fidelity F1 0.8876 · precision 0.8797 · recall 0.8956 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8725 · ERM error 0.0887 · FPR 0.6275 · FNR 0.0100
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.1e-28), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.0036), derived_loan_product_type (p_adj=4.7e-44), loan_type (p_adj=1.5e-45), loan_amount (p_adj=1.4e-73), loan_term (p_adj=3.3e-61), property_value (p_adj=2.2e-86), income (p_adj=1e-35), applicant_credit_score_type (p_adj=1.2e-12), submission_of_application (p_adj=1.8e-11), initially_payable_to_institution (p_adj=2.5e-11), aus-1 (p_adj=1.6e-29), tract_population (p_adj=5.2e-20), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=6.6e-24), tract_median_age_of_housing_units (p_adj=2.2e-22)
- องค์ประกอบ race_eth: Hispanic 7.0% (ทั้งชุด 9.1%), NH Asian 1.6% (ทั้งชุด 6.8%), NH Black 16.9% (ทั้งชุด 22.0%), NH White 55.9% (ทั้งชุด 41.8%), Other 3.1% (ทั้งชุด 2.3%), Unknown 15.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 22.5% (ทั้งชุด 27.1%), Joint 33.1% (ทั้งชุด 30.7%), Male 37.2% (ทั้งชุด 35.6%), Unknown 7.1% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 32.4% (ทั้งชุด 31.4%), 35-44 21.5% (ทั้งชุด 26.6%), 45-54 13.6% (ทั้งชุด 17.5%), 55-64 13.9% (ทั้งชุด 11.7%), 65-74 6.9% (ทั้งชุด 5.5%), <25 10.0% (ทั้งชุด 5.9%), >74 1.8% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k8 · c · seed 17 · กลุ่ม 1
- IF loan_amount ≤ 1e+06 AND income > 1062 THEN อยู่กลุ่มนี้
- IF loan_amount > 1e+06 AND property_value ≤ 1.415e+06 AND income > 462 THEN อยู่กลุ่มนี้
- IF loan_amount > 1e+06 AND property_value > 1.415e+06 AND tract_to_msa_income_percentage ≤ 118.9 THEN อยู่กลุ่มนี้
- IF loan_amount > 1e+06 AND property_value > 1.415e+06 AND tract_to_msa_income_percentage > 118.9 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 152/53/39 · coverage กฎบน validation 0.0115
- Fidelity F1 0.9091 · precision 0.9783 · recall 0.8491 · เงื่อนไขรวม 11 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9487 · ERM error 0.0513 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4e-06), conforming_loan_limit (p_adj=2.9e-307), loan_amount (p_adj=1.5e-10), loan_term (p_adj=1.1e-34), property_value (p_adj=3.1e-12), income (p_adj=1.7e-05), debt_to_income_ratio (p_adj=0.001), aus-1 (p_adj=1.5e-09), ffiec_msa_md_median_family_income (p_adj=5.2e-05), tract_to_msa_income_percentage (p_adj=2.4e-05)
- องค์ประกอบ race_eth: Hispanic 2.6% (ทั้งชุด 9.1%), NH Asian 15.4% (ทั้งชุด 6.8%), NH Black 10.3% (ทั้งชุด 22.0%), NH White 51.3% (ทั้งชุด 41.8%), Other 2.6% (ทั้งชุด 2.3%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 7.7% (ทั้งชุด 27.1%), Joint 43.6% (ทั้งชุด 30.7%), Male 41.0% (ทั้งชุด 35.6%), Unknown 7.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 15.4% (ทั้งชุด 31.4%), 35-44 38.5% (ทั้งชุด 26.6%), 45-54 30.8% (ทั้งชุด 17.5%), 55-64 15.4% (ทั้งชุด 11.7%), 65-74 0.0% (ทั้งชุด 5.5%), <25 0.0% (ทั้งชุด 5.9%), >74 0.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k8 · c · seed 17 · กลุ่ม 2
- IF ffiec_msa_md_median_family_income ≤ 9.11e+04 AND ffiec_msa_md_median_family_income > 8.405e+04 AND tract_owner_occupied_units ≤ 990 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 9.11e+04 AND tract_owner_occupied_units ≤ 1322 AND property_value ≤ 5e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3764/1262/1273 · coverage กฎบน validation 0.3603
- Fidelity F1 0.8280 · precision 0.7765 · recall 0.8867 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8649 · ERM error 0.0778 · FPR 0.5058 · FNR 0.0109
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3e-16), derived_msa-md (p_adj=9e-159), county_code (p_adj=2.6e-158), conforming_loan_limit (p_adj=4.5e-07), derived_loan_product_type (p_adj=1.1e-25), loan_type (p_adj=6.7e-27), loan_amount (p_adj=8.4e-10), loan_term (p_adj=9.5e-66), property_value (p_adj=1.1e-28), construction_method (p_adj=1.2e-32), income (p_adj=4.2e-31), debt_to_income_ratio (p_adj=2.3e-14), applicant_credit_score_type (p_adj=5.1e-10), aus-1 (p_adj=4.5e-27), tract_population (p_adj=4.6e-68), ffiec_msa_md_median_family_income (p_adj=1.9e-307), tract_to_msa_income_percentage (p_adj=1.4e-161), tract_owner_occupied_units (p_adj=1.2e-180), tract_one_to_four_family_homes (p_adj=3.5e-149), tract_median_age_of_housing_units (p_adj=6.4e-18)
- องค์ประกอบ race_eth: Hispanic 13.9% (ทั้งชุด 9.1%), NH Asian 6.4% (ทั้งชุด 6.8%), NH Black 29.3% (ทั้งชุด 22.0%), NH White 29.5% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.3%), Unknown 18.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.8% (ทั้งชุด 27.1%), Joint 25.3% (ทั้งชุด 30.7%), Male 33.2% (ทั้งชุด 35.6%), Unknown 6.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 33.9% (ทั้งชุด 31.4%), 35-44 25.7% (ทั้งชุด 26.6%), 45-54 17.8% (ทั้งชุด 17.5%), 55-64 11.2% (ทั้งชุด 11.7%), 65-74 4.4% (ทั้งชุด 5.5%), <25 5.9% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k8 · c · seed 17 · กลุ่ม 3
- IF tract_owner_occupied_units ≤ 1418 AND tract_population > 5184 AND tract_owner_occupied_units > 1230 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1418 AND tract_population ≤ 5613 AND property_value ≤ 6.3e+05 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1418 AND tract_population > 5613 AND loan_term > 319 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2497/817/829 · coverage กฎบน validation 0.2505
- Fidelity F1 0.8334 · precision 0.7565 · recall 0.9278 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8890 · ERM error 0.0603 · FPR 0.4891 · FNR 0.0068
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.00014), derived_msa-md (p_adj=5.4e-43), county_code (p_adj=2.1e-132), conforming_loan_limit (p_adj=0.026), derived_loan_product_type (p_adj=2e-08), loan_type (p_adj=4.8e-09), loan_term (p_adj=8e-45), construction_method (p_adj=1.7e-14), aus-1 (p_adj=6.3e-09), tract_population (p_adj=1.5e-247), ffiec_msa_md_median_family_income (p_adj=2e-24), tract_to_msa_income_percentage (p_adj=7.6e-09), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=7.7e-269), tract_median_age_of_housing_units (p_adj=2.1e-109)
- องค์ประกอบ race_eth: Hispanic 8.8% (ทั้งชุด 9.1%), NH Asian 6.6% (ทั้งชุด 6.8%), NH Black 24.0% (ทั้งชุด 22.0%), NH White 39.3% (ทั้งชุด 41.8%), Other 2.5% (ทั้งชุด 2.3%), Unknown 18.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 22.8% (ทั้งชุด 27.1%), Joint 30.6% (ทั้งชุด 30.7%), Male 39.9% (ทั้งชุด 35.6%), Unknown 6.6% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.8% (ทั้งชุด 31.4%), 35-44 29.1% (ทั้งชุด 26.6%), 45-54 18.2% (ทั้งชุด 17.5%), 55-64 12.3% (ทั้งชุด 11.7%), 65-74 5.5% (ทั้งชุด 5.5%), <25 4.6% (ทั้งชุด 5.9%), >74 1.4% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k8 · c · seed 17 · กลุ่ม 4
- IF property_value ≤ 5.5e+05 AND tract_to_msa_income_percentage > 146.5 AND derived_msa-md_12060 > 0.5 THEN อยู่กลุ่มนี้
- IF property_value > 5.5e+05 AND tract_one_to_four_family_homes ≤ 2007 AND property_value ≤ 1.47e+06 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1742/600/615 · coverage กฎบน validation 0.1698
- Fidelity F1 0.7349 · precision 0.6922 · recall 0.7833 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9350 · ERM error 0.0504 · FPR 0.7000 · FNR 0.0052
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1e-19), derived_msa-md (p_adj=7.9e-40), county_code (p_adj=5.2e-63), conforming_loan_limit (p_adj=5.2e-25), derived_loan_product_type (p_adj=1.8e-64), loan_type (p_adj=3.7e-60), loan_amount (p_adj=2.6e-135), loan_term (p_adj=4.4e-65), property_value (p_adj=2.6e-139), construction_method (p_adj=5.6e-16), income (p_adj=1.1e-69), debt_to_income_ratio (p_adj=2e-32), aus-1 (p_adj=7.7e-37), tract_population (p_adj=1.5e-10), ffiec_msa_md_median_family_income (p_adj=1.9e-78), tract_to_msa_income_percentage (p_adj=3.8e-118), tract_one_to_four_family_homes (p_adj=3.3e-29)
- องค์ประกอบ race_eth: Hispanic 4.6% (ทั้งชุด 9.1%), NH Asian 15.4% (ทั้งชุด 6.8%), NH Black 10.9% (ทั้งชุด 22.0%), NH White 49.1% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.3%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 19.5% (ทั้งชุด 27.1%), Joint 40.7% (ทั้งชุด 30.7%), Male 34.1% (ทั้งชุด 35.6%), Unknown 5.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.9% (ทั้งชุด 31.4%), 35-44 32.7% (ทั้งชุด 26.6%), 45-54 18.5% (ทั้งชุด 17.5%), 55-64 9.6% (ทั้งชุด 11.7%), 65-74 5.5% (ทั้งชุด 5.5%), <25 1.6% (ทั้งชุด 5.9%), >74 1.1% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k8 · c · seed 17 · กลุ่ม 5
- IF loan_term ≤ 202 AND construction_method_2 ≤ 0.5 AND tract_median_age_of_housing_units ≤ 14.5 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 202 AND construction_method_2 ≤ 0.5 AND tract_median_age_of_housing_units > 14.5 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 202 AND construction_method_2 > 0.5 AND tract_owner_occupied_units > 909.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 392/131/128 · coverage กฎบน validation 0.0267
- Fidelity F1 0.8824 · precision 0.9813 · recall 0.8015 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8984 · ERM error 0.0703 · FPR 0.3846 · FNR 0.0348
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=9.7e-06), derived_loan_product_type (p_adj=5.1e-176), loan_type (p_adj=5.8e-13), lien_status (p_adj=5.2e-173), loan_amount (p_adj=3.8e-19), loan_term (p_adj=1.5e-78), debt_to_income_ratio (p_adj=1.5e-07), aus-1 (p_adj=4.8e-06)
- องค์ประกอบ race_eth: Hispanic 4.7% (ทั้งชุด 9.1%), NH Asian 13.3% (ทั้งชุด 6.8%), NH Black 19.5% (ทั้งชุด 22.0%), NH White 40.6% (ทั้งชุด 41.8%), Other 0.0% (ทั้งชุด 2.3%), Unknown 21.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 25.8% (ทั้งชุด 27.1%), Joint 22.7% (ทั้งชุด 30.7%), Male 40.6% (ทั้งชุด 35.6%), Unknown 10.9% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 24.2% (ทั้งชุด 31.4%), 35-44 25.8% (ทั้งชุด 26.6%), 45-54 23.4% (ทั้งชุด 17.5%), 55-64 13.3% (ทั้งชุด 11.7%), 65-74 7.8% (ทั้งชุด 5.5%), <25 3.1% (ทั้งชุด 5.9%), >74 2.3% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k8 · c · seed 17 · กลุ่ม 6
- IF total_units > 1.5 AND loan_type_3 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF total_units > 1.5 AND loan_type_3 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 39/11/8 · coverage กฎบน validation 0.0030
- Fidelity F1 0.9565 · precision 0.9167 · recall 1.0000 · เงื่อนไขรวม 4 · สูงสุดต่อเส้นทาง 2
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8750 · ERM error 0.1250 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.6e-74), county_code (p_adj=3.5e-41), applicant_credit_score_type (p_adj=0.022), submission_of_application (p_adj=1.6e-05), initially_payable_to_institution (p_adj=0.0002), aus-1 (p_adj=2.7e-06)
- องค์ประกอบ race_eth: Hispanic 25.0% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 12.5% (ทั้งชุด 22.0%), NH White 37.5% (ทั้งชุด 41.8%), Other 0.0% (ทั้งชุด 2.3%), Unknown 25.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 12.5% (ทั้งชุด 27.1%), Joint 50.0% (ทั้งชุด 30.7%), Male 25.0% (ทั้งชุด 35.6%), Unknown 12.5% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 62.5% (ทั้งชุด 31.4%), 35-44 12.5% (ทั้งชุด 26.6%), 45-54 12.5% (ทั้งชุด 17.5%), 55-64 0.0% (ทั้งชุด 11.7%), 65-74 12.5% (ทั้งชุด 5.5%), <25 0.0% (ทั้งชุด 5.9%), >74 0.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k8 · c · seed 17 · กลุ่ม 7
- IF construction_method_2 > 0.5 AND loan_term ≤ 346.5 AND tract_owner_occupied_units ≤ 1502 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 937/293/308 · coverage กฎบน validation 0.0690
- Fidelity F1 0.9033 · precision 0.9312 · recall 0.8771 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.2500 · ERM error 0.2110 · FPR 0.0649 · FNR 0.6494
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0), derived_msa-md (p_adj=1.1e-78), county_code (p_adj=3.3e-174), derived_loan_product_type (p_adj=9e-41), loan_type (p_adj=6.8e-39), loan_amount (p_adj=1.1e-225), loan_term (p_adj=5.5e-107), property_value (p_adj=1.5e-269), construction_method (p_adj=0), income (p_adj=3.7e-83), debt_to_income_ratio (p_adj=3.4e-06), applicant_credit_score_type (p_adj=2.5e-191), aus-1 (p_adj=0), tract_population (p_adj=6.5e-40), ffiec_msa_md_median_family_income (p_adj=5.7e-39), tract_to_msa_income_percentage (p_adj=8.1e-38), tract_owner_occupied_units (p_adj=2.1e-35), tract_one_to_four_family_homes (p_adj=6.6e-13)
- องค์ประกอบ race_eth: Hispanic 6.8% (ทั้งชุด 9.1%), NH Asian 1.0% (ทั้งชุด 6.8%), NH Black 24.4% (ทั้งชุด 22.0%), NH White 47.1% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.3%), Unknown 18.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 37.7% (ทั้งชุด 27.1%), Joint 28.2% (ทั้งชุด 30.7%), Male 30.5% (ทั้งชุด 35.6%), Unknown 3.6% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.8% (ทั้งชุด 31.4%), 35-44 24.0% (ทั้งชุด 26.6%), 45-54 19.2% (ทั้งชุด 17.5%), 55-64 9.7% (ทั้งชุด 11.7%), 65-74 5.2% (ทั้งชุด 5.5%), <25 10.1% (ทั้งชุด 5.9%), >74 1.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k2 · c · seed 17 · กลุ่ม 0
- IF loan_term ≤ 306 AND aus-1_6 ≤ 0.5 AND ffiec_msa_md_median_family_income ≤ 9.11e+04 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 306 AND aus-1_6 > 0.5 AND property_value ≤ 3.2e+05 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 306 AND aus-1_6 > 0.5 AND property_value > 3.2e+05 THEN อยู่กลุ่มนี้
- IF loan_term > 306 AND aus-1_1111 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2031/663/637 · coverage กฎบน validation 0.1027
- Fidelity F1 0.7244 · precision 0.9465 · recall 0.5867 · เงื่อนไขรวม 11 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.5463 · ERM error 0.1570 · FPR 0.1488 · FNR 0.1638
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1e-293), derived_msa-md (p_adj=4.6e-149), county_code (p_adj=2.5e-177), derived_loan_product_type (p_adj=4e-120), loan_type (p_adj=1.6e-84), lien_status (p_adj=7.7e-50), loan_amount (p_adj=1.9e-20), loan_term (p_adj=8.2e-63), property_value (p_adj=3.4e-11), construction_method (p_adj=0), applicant_credit_score_type (p_adj=1.1e-179), submission_of_application (p_adj=1.3e-62), initially_payable_to_institution (p_adj=2.7e-60), aus-1 (p_adj=0), tract_population (p_adj=1.7e-46), ffiec_msa_md_median_family_income (p_adj=2.5e-87), tract_to_msa_income_percentage (p_adj=2e-13), tract_owner_occupied_units (p_adj=3.1e-31), tract_one_to_four_family_homes (p_adj=0.0049)
- องค์ประกอบ race_eth: Hispanic 6.1% (ทั้งชุด 9.1%), NH Asian 1.4% (ทั้งชุด 6.8%), NH Black 20.1% (ทั้งชุด 22.0%), NH White 53.8% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.3%), Unknown 16.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 32.2% (ทั้งชุด 27.1%), Joint 30.8% (ทั้งชุด 30.7%), Male 31.9% (ทั้งชุด 35.6%), Unknown 5.2% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.9% (ทั้งชุด 31.4%), 35-44 22.9% (ทั้งชุด 26.6%), 45-54 18.4% (ทั้งชุด 17.5%), 55-64 12.6% (ทั้งชุด 11.7%), 65-74 6.8% (ทั้งชุด 5.5%), <25 8.3% (ทั้งชุด 5.9%), >74 2.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k2 · c · seed 17 · กลุ่ม 1
- IF loan_term ≤ 306 AND aus-1_6 ≤ 0.5 AND ffiec_msa_md_median_family_income > 9.11e+04 THEN อยู่กลุ่มนี้
- IF loan_term > 306 AND aus-1_1111 ≤ 0.5 AND aus-1_6 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF loan_term > 306 AND aus-1_1111 ≤ 0.5 AND aus-1_6 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 9969/3337/3363 · coverage กฎบน validation 0.8972
- Fidelity F1 0.9573 · precision 0.9237 · recall 0.9934 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8918 · ERM error 0.0678 · FPR 0.5604 · FNR 0.0080
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1e-293), derived_msa-md (p_adj=4.6e-149), county_code (p_adj=2.5e-177), derived_loan_product_type (p_adj=4e-120), loan_type (p_adj=1.6e-84), lien_status (p_adj=7.7e-50), loan_amount (p_adj=1.9e-20), loan_term (p_adj=8.2e-63), property_value (p_adj=3.4e-11), construction_method (p_adj=0), applicant_credit_score_type (p_adj=1.1e-179), submission_of_application (p_adj=1.3e-62), initially_payable_to_institution (p_adj=2.7e-60), aus-1 (p_adj=0), tract_population (p_adj=1.7e-46), ffiec_msa_md_median_family_income (p_adj=2.5e-87), tract_to_msa_income_percentage (p_adj=2e-13), tract_owner_occupied_units (p_adj=3.1e-31), tract_one_to_four_family_homes (p_adj=0.0049)
- องค์ประกอบ race_eth: Hispanic 9.7% (ทั้งชุด 9.1%), NH Asian 7.8% (ทั้งชุด 6.8%), NH Black 22.3% (ทั้งชุด 22.0%), NH White 39.5% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.3%), Unknown 18.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 26.2% (ทั้งชุด 27.1%), Joint 30.7% (ทั้งชุด 30.7%), Male 36.4% (ทั้งชุด 35.6%), Unknown 6.8% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 31.9% (ทั้งชุด 31.4%), 35-44 27.3% (ทั้งชุด 26.6%), 45-54 17.4% (ทั้งชุด 17.5%), 55-64 11.5% (ทั้งชุด 11.7%), 65-74 5.2% (ทั้งชุด 5.5%), <25 5.5% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · c · seed 17 · กลุ่ม 0
- IF debt_to_income_ratio ≤ 60 AND construction_method_1 ≤ 0.5 AND aus-1_6 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio ≤ 60 AND construction_method_1 > 0.5 AND initially_payable_to_institution_3 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 10520/3552/3515 · coverage กฎบน validation 0.8742
- Fidelity F1 0.9789 · precision 0.9866 · recall 0.9713 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9292 · ERM error 0.0703 · FPR 0.9839 · FNR 0.0006
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.5e-191), derived_msa-md (p_adj=1.8e-31), county_code (p_adj=1.3e-71), derived_loan_product_type (p_adj=4e-13), preapproval (p_adj=0.0011), loan_type (p_adj=4.1e-13), loan_amount (p_adj=3e-52), loan_term (p_adj=8.4e-42), property_value (p_adj=2e-68), construction_method (p_adj=2.9e-276), income (p_adj=8.5e-72), debt_to_income_ratio (p_adj=2.2e-32), applicant_credit_score_type (p_adj=3.4e-110), initially_payable_to_institution (p_adj=1.9e-94), aus-1 (p_adj=2.2e-233), tract_population (p_adj=1.1e-16), ffiec_msa_md_median_family_income (p_adj=6.2e-20), tract_to_msa_income_percentage (p_adj=3e-32), tract_owner_occupied_units (p_adj=4.5e-16), tract_one_to_four_family_homes (p_adj=0.00036)
- องค์ประกอบ race_eth: Hispanic 9.1% (ทั้งชุด 9.1%), NH Asian 7.3% (ทั้งชุด 6.8%), NH Black 20.9% (ทั้งชุด 22.0%), NH White 42.4% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.3%), Unknown 18.1% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 25.7% (ทั้งชุด 27.1%), Joint 31.4% (ทั้งชุด 30.7%), Male 36.1% (ทั้งชุด 35.6%), Unknown 6.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 31.9% (ทั้งชุด 31.4%), 35-44 26.6% (ทั้งชุด 26.6%), 45-54 17.3% (ทั้งชุด 17.5%), 55-64 11.7% (ทั้งชุด 11.7%), 65-74 5.5% (ทั้งชุด 5.5%), <25 5.6% (ทั้งชุด 5.9%), >74 1.4% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · c · seed 17 · กลุ่ม 1
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 > 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio > 60 AND income ≤ 81.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio > 60 AND income > 81.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND construction_method_2 ≤ 0.5 AND debt_to_income_ratio > 52 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND construction_method_2 > 0.5 AND debt_to_income_ratio ≤ 52 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND construction_method_2 > 0.5 AND debt_to_income_ratio > 52 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1480/448/485 · coverage กฎบน validation 0.1345
- Fidelity F1 0.8438 · precision 0.7732 · recall 0.9286 · เงื่อนไขรวม 18 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.1670 · ERM error 0.1670 · FPR 0.0050 · FNR 0.9753
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.5e-191), derived_msa-md (p_adj=1.8e-31), county_code (p_adj=1.3e-71), derived_loan_product_type (p_adj=4e-13), preapproval (p_adj=0.0011), loan_type (p_adj=4.1e-13), loan_amount (p_adj=3e-52), loan_term (p_adj=8.4e-42), property_value (p_adj=2e-68), construction_method (p_adj=2.9e-276), income (p_adj=8.5e-72), debt_to_income_ratio (p_adj=2.2e-32), applicant_credit_score_type (p_adj=3.4e-110), initially_payable_to_institution (p_adj=1.9e-94), aus-1 (p_adj=2.2e-233), tract_population (p_adj=1.1e-16), ffiec_msa_md_median_family_income (p_adj=6.2e-20), tract_to_msa_income_percentage (p_adj=3e-32), tract_owner_occupied_units (p_adj=4.5e-16), tract_one_to_four_family_homes (p_adj=0.00036)
- องค์ประกอบ race_eth: Hispanic 9.1% (ทั้งชุด 9.1%), NH Asian 3.1% (ทั้งชุด 6.8%), NH Black 30.1% (ทั้งชุด 22.0%), NH White 37.3% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.3%), Unknown 17.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 37.1% (ทั้งชุด 27.1%), Joint 25.4% (ทั้งชุด 30.7%), Male 32.6% (ทั้งชุด 35.6%), Unknown 4.9% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.0% (ทั้งชุด 31.4%), 35-44 26.8% (ทั้งชุด 26.6%), 45-54 19.6% (ทั้งชุด 17.5%), 55-64 11.3% (ทั้งชุด 11.7%), 65-74 4.9% (ทั้งชุด 5.5%), <25 8.2% (ทั้งชุด 5.9%), >74 1.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 17 · กลุ่ม 0
- IF loan_term ≤ 306 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND tract_owner_occupied_units ≤ 1632 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 306 AND ffiec_msa_md_median_family_income > 1.015e+05 AND loan_term ≤ 162 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 970/296/304 · coverage กฎบน validation 0.0722
- Fidelity F1 0.9333 · precision 0.9446 · recall 0.9223 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.3882 · ERM error 0.1743 · FPR 0.0699 · FNR 0.3390
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.1e-212), derived_msa-md (p_adj=1.2e-86), county_code (p_adj=3.4e-148), derived_loan_product_type (p_adj=9.2e-76), loan_type (p_adj=4.5e-39), lien_status (p_adj=7.8e-46), loan_amount (p_adj=3.9e-216), loan_term (p_adj=3.2e-72), property_value (p_adj=1.6e-147), construction_method (p_adj=0), income (p_adj=5.1e-65), applicant_credit_score_type (p_adj=5.3e-118), aus-1 (p_adj=6.6e-258), tract_population (p_adj=3.4e-27), ffiec_msa_md_median_family_income (p_adj=4.3e-52), tract_to_msa_income_percentage (p_adj=6.4e-24), tract_owner_occupied_units (p_adj=2e-21), tract_one_to_four_family_homes (p_adj=0.0066)
- องค์ประกอบ race_eth: Hispanic 4.6% (ทั้งชุด 9.1%), NH Asian 1.6% (ทั้งชุด 6.8%), NH Black 28.3% (ทั้งชุด 22.0%), NH White 43.8% (ทั้งชุด 41.8%), Other 1.3% (ทั้งชุด 2.3%), Unknown 20.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 38.8% (ทั้งชุด 27.1%), Joint 27.0% (ทั้งชุด 30.7%), Male 28.9% (ทั้งชุด 35.6%), Unknown 5.3% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 31.2% (ทั้งชุด 31.4%), 35-44 23.7% (ทั้งชุด 26.6%), 45-54 19.1% (ทั้งชุด 17.5%), 55-64 9.9% (ทั้งชุด 11.7%), 65-74 6.2% (ทั้งชุด 5.5%), <25 7.9% (ทั้งชุด 5.9%), >74 2.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 17 · กลุ่ม 1
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND loan_term > 334 AND tract_owner_occupied_units ≤ 1420 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2208/766/699 · coverage กฎบน validation 0.1913
- Fidelity F1 0.9001 · precision 0.9007 · recall 0.8995 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8512 · ERM error 0.0916 · FPR 0.5385 · FNR 0.0134
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.2e-22), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.023), derived_loan_product_type (p_adj=1.7e-32), loan_type (p_adj=1.1e-33), loan_amount (p_adj=6.6e-89), loan_term (p_adj=1.7e-66), property_value (p_adj=1.7e-101), income (p_adj=1.5e-44), applicant_credit_score_type (p_adj=1.1e-09), submission_of_application (p_adj=9.6e-10), initially_payable_to_institution (p_adj=1.3e-09), aus-1 (p_adj=9.6e-22), tract_population (p_adj=1.7e-39), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=4.2e-55), tract_median_age_of_housing_units (p_adj=6.4e-23)
- องค์ประกอบ race_eth: Hispanic 7.9% (ทั้งชุด 9.1%), NH Asian 1.3% (ทั้งชุด 6.8%), NH Black 17.6% (ทั้งชุด 22.0%), NH White 55.5% (ทั้งชุด 41.8%), Other 3.0% (ทั้งชุด 2.3%), Unknown 14.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 24.3% (ทั้งชุด 27.1%), Joint 30.0% (ทั้งชุด 30.7%), Male 38.2% (ทั้งชุด 35.6%), Unknown 7.4% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 32.8% (ทั้งชุด 31.4%), 35-44 22.3% (ทั้งชุด 26.6%), 45-54 14.4% (ทั้งชุด 17.5%), 55-64 12.6% (ทั้งชุด 11.7%), 65-74 6.4% (ทั้งชุด 5.5%), <25 9.7% (ทั้งชุด 5.9%), >74 1.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 17 · กลุ่ม 2
- IF ffiec_msa_md_median_family_income > 8.405e+04 AND tract_owner_occupied_units ≤ 1300 AND property_value ≤ 5.5e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3992/1319/1353 · coverage กฎบน validation 0.3885
- Fidelity F1 0.8277 · precision 0.7651 · recall 0.9014 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8492 · ERM error 0.0820 · FPR 0.4314 · FNR 0.0200
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0018), derived_msa-md (p_adj=4.6e-166), county_code (p_adj=5.6e-171), conforming_loan_limit (p_adj=1.1e-06), derived_loan_product_type (p_adj=1.1e-08), loan_type (p_adj=2.6e-09), loan_amount (p_adj=9e-16), loan_term (p_adj=4.9e-15), property_value (p_adj=2.1e-28), construction_method (p_adj=1e-10), income (p_adj=1.6e-23), debt_to_income_ratio (p_adj=3.3e-08), aus-1 (p_adj=3.3e-08), tract_population (p_adj=1.1e-132), ffiec_msa_md_median_family_income (p_adj=1.4e-272), tract_to_msa_income_percentage (p_adj=9.2e-108), tract_owner_occupied_units (p_adj=3.9e-261), tract_one_to_four_family_homes (p_adj=8.8e-228), tract_median_age_of_housing_units (p_adj=4.2e-25)
- องค์ประกอบ race_eth: Hispanic 12.7% (ทั้งชุด 9.1%), NH Asian 7.0% (ทั้งชุด 6.8%), NH Black 26.8% (ทั้งชุด 22.0%), NH White 33.7% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.3%), Unknown 17.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 33.4% (ทั้งชุด 27.1%), Joint 26.1% (ทั้งชุด 30.7%), Male 34.4% (ทั้งชุด 35.6%), Unknown 6.1% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 34.5% (ทั้งชุด 31.4%), 35-44 24.8% (ทั้งชุด 26.6%), 45-54 17.2% (ทั้งชุด 17.5%), 55-64 11.2% (ทั้งชุด 11.7%), 65-74 4.8% (ทั้งชุด 5.5%), <25 6.3% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 17 · กลุ่ม 3
- IF tract_owner_occupied_units ≤ 1254 AND property_value > 4.4e+05 AND tract_owner_occupied_units > 786 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value ≤ 2.4e+05 AND tract_owner_occupied_units > 1502 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.4e+05 AND tract_owner_occupied_units ≤ 1416 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.4e+05 AND tract_owner_occupied_units > 1416 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4830/1619/1644 · coverage กฎบน validation 0.4133
- Fidelity F1 0.8576 · precision 0.8488 · recall 0.8666 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9033 · ERM error 0.0608 · FPR 0.5660 · FNR 0.0067
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.6e-16), derived_msa-md (p_adj=4.8e-63), county_code (p_adj=9.9e-121), conforming_loan_limit (p_adj=1.5e-24), derived_loan_product_type (p_adj=3.3e-16), loan_type (p_adj=2.4e-12), lien_status (p_adj=0.032), loan_amount (p_adj=2e-138), loan_term (p_adj=2.1e-21), property_value (p_adj=2.4e-137), construction_method (p_adj=2.3e-49), income (p_adj=8e-63), debt_to_income_ratio (p_adj=2.5e-14), applicant_credit_score_type (p_adj=9.2e-06), aus-1 (p_adj=1.5e-31), tract_population (p_adj=1.2e-268), ffiec_msa_md_median_family_income (p_adj=1.4e-63), tract_to_msa_income_percentage (p_adj=2.4e-158), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=2.3e-213), tract_median_age_of_housing_units (p_adj=5.4e-104)
- องค์ประกอบ race_eth: Hispanic 7.5% (ทั้งชุด 9.1%), NH Asian 9.9% (ทั้งชุด 6.8%), NH Black 18.7% (ทั้งชุด 22.0%), NH White 42.2% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.3%), Unknown 19.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 21.0% (ทั้งชุด 27.1%), Joint 35.5% (ทั้งชุด 30.7%), Male 36.9% (ทั้งชุด 35.6%), Unknown 6.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.3% (ทั้งชุด 31.4%), 35-44 30.5% (ทั้งชุด 26.6%), 45-54 18.9% (ทั้งชุด 17.5%), 55-64 12.0% (ทั้งชุด 11.7%), 65-74 5.4% (ทั้งชุด 5.5%), <25 3.7% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 17 · กลุ่ม 0
- IF loan_term ≤ 306 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND tract_owner_occupied_units ≤ 1632 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 306 AND ffiec_msa_md_median_family_income > 1.015e+05 AND loan_term ≤ 162 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 970/296/304 · coverage กฎบน validation 0.0722
- Fidelity F1 0.9333 · precision 0.9446 · recall 0.9223 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.3882 · ERM error 0.1743 · FPR 0.0699 · FNR 0.3390
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.1e-212), derived_msa-md (p_adj=1.2e-86), county_code (p_adj=3.4e-148), derived_loan_product_type (p_adj=9.2e-76), loan_type (p_adj=4.5e-39), lien_status (p_adj=7.8e-46), loan_amount (p_adj=3.9e-216), loan_term (p_adj=3.2e-72), property_value (p_adj=1.6e-147), construction_method (p_adj=0), income (p_adj=5.1e-65), applicant_credit_score_type (p_adj=5.3e-118), aus-1 (p_adj=6.6e-258), tract_population (p_adj=3.4e-27), ffiec_msa_md_median_family_income (p_adj=4.3e-52), tract_to_msa_income_percentage (p_adj=6.4e-24), tract_owner_occupied_units (p_adj=2e-21), tract_one_to_four_family_homes (p_adj=0.0066)
- องค์ประกอบ race_eth: Hispanic 4.6% (ทั้งชุด 9.1%), NH Asian 1.6% (ทั้งชุด 6.8%), NH Black 28.3% (ทั้งชุด 22.0%), NH White 43.8% (ทั้งชุด 41.8%), Other 1.3% (ทั้งชุด 2.3%), Unknown 20.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 38.8% (ทั้งชุด 27.1%), Joint 27.0% (ทั้งชุด 30.7%), Male 28.9% (ทั้งชุด 35.6%), Unknown 5.3% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 31.2% (ทั้งชุด 31.4%), 35-44 23.7% (ทั้งชุด 26.6%), 45-54 19.1% (ทั้งชุด 17.5%), 55-64 9.9% (ทั้งชุด 11.7%), 65-74 6.2% (ทั้งชุด 5.5%), <25 7.9% (ทั้งชุด 5.9%), >74 2.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 17 · กลุ่ม 1
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND loan_term > 334 AND tract_owner_occupied_units ≤ 1420 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2208/766/699 · coverage กฎบน validation 0.1913
- Fidelity F1 0.9001 · precision 0.9007 · recall 0.8995 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8512 · ERM error 0.0916 · FPR 0.5385 · FNR 0.0134
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.2e-22), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.023), derived_loan_product_type (p_adj=1.7e-32), loan_type (p_adj=1.1e-33), loan_amount (p_adj=6.6e-89), loan_term (p_adj=1.7e-66), property_value (p_adj=1.7e-101), income (p_adj=1.5e-44), applicant_credit_score_type (p_adj=1.1e-09), submission_of_application (p_adj=9.6e-10), initially_payable_to_institution (p_adj=1.3e-09), aus-1 (p_adj=9.6e-22), tract_population (p_adj=1.7e-39), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=4.2e-55), tract_median_age_of_housing_units (p_adj=6.4e-23)
- องค์ประกอบ race_eth: Hispanic 7.9% (ทั้งชุด 9.1%), NH Asian 1.3% (ทั้งชุด 6.8%), NH Black 17.6% (ทั้งชุด 22.0%), NH White 55.5% (ทั้งชุด 41.8%), Other 3.0% (ทั้งชุด 2.3%), Unknown 14.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 24.3% (ทั้งชุด 27.1%), Joint 30.0% (ทั้งชุด 30.7%), Male 38.2% (ทั้งชุด 35.6%), Unknown 7.4% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 32.8% (ทั้งชุด 31.4%), 35-44 22.3% (ทั้งชุด 26.6%), 45-54 14.4% (ทั้งชุด 17.5%), 55-64 12.6% (ทั้งชุด 11.7%), 65-74 6.4% (ทั้งชุด 5.5%), <25 9.7% (ทั้งชุด 5.9%), >74 1.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 17 · กลุ่ม 2
- IF ffiec_msa_md_median_family_income > 8.405e+04 AND tract_owner_occupied_units ≤ 1300 AND property_value ≤ 5.5e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3992/1319/1353 · coverage กฎบน validation 0.3885
- Fidelity F1 0.8277 · precision 0.7651 · recall 0.9014 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8492 · ERM error 0.0820 · FPR 0.4314 · FNR 0.0200
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0018), derived_msa-md (p_adj=4.6e-166), county_code (p_adj=5.6e-171), conforming_loan_limit (p_adj=1.1e-06), derived_loan_product_type (p_adj=1.1e-08), loan_type (p_adj=2.6e-09), loan_amount (p_adj=9e-16), loan_term (p_adj=4.9e-15), property_value (p_adj=2.1e-28), construction_method (p_adj=1e-10), income (p_adj=1.6e-23), debt_to_income_ratio (p_adj=3.3e-08), aus-1 (p_adj=3.3e-08), tract_population (p_adj=1.1e-132), ffiec_msa_md_median_family_income (p_adj=1.4e-272), tract_to_msa_income_percentage (p_adj=9.2e-108), tract_owner_occupied_units (p_adj=3.9e-261), tract_one_to_four_family_homes (p_adj=8.8e-228), tract_median_age_of_housing_units (p_adj=4.2e-25)
- องค์ประกอบ race_eth: Hispanic 12.7% (ทั้งชุด 9.1%), NH Asian 7.0% (ทั้งชุด 6.8%), NH Black 26.8% (ทั้งชุด 22.0%), NH White 33.7% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.3%), Unknown 17.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 33.4% (ทั้งชุด 27.1%), Joint 26.1% (ทั้งชุด 30.7%), Male 34.4% (ทั้งชุด 35.6%), Unknown 6.1% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 34.5% (ทั้งชุด 31.4%), 35-44 24.8% (ทั้งชุด 26.6%), 45-54 17.2% (ทั้งชุด 17.5%), 55-64 11.2% (ทั้งชุด 11.7%), 65-74 4.8% (ทั้งชุด 5.5%), <25 6.3% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 17 · กลุ่ม 3
- IF tract_owner_occupied_units ≤ 1254 AND property_value > 4.4e+05 AND tract_owner_occupied_units > 786 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value ≤ 2.4e+05 AND tract_owner_occupied_units > 1502 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.4e+05 AND tract_owner_occupied_units ≤ 1416 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.4e+05 AND tract_owner_occupied_units > 1416 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4830/1619/1644 · coverage กฎบน validation 0.4133
- Fidelity F1 0.8576 · precision 0.8488 · recall 0.8666 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9033 · ERM error 0.0608 · FPR 0.5660 · FNR 0.0067
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.6e-16), derived_msa-md (p_adj=4.8e-63), county_code (p_adj=9.9e-121), conforming_loan_limit (p_adj=1.5e-24), derived_loan_product_type (p_adj=3.3e-16), loan_type (p_adj=2.4e-12), lien_status (p_adj=0.032), loan_amount (p_adj=2e-138), loan_term (p_adj=2.1e-21), property_value (p_adj=2.4e-137), construction_method (p_adj=2.3e-49), income (p_adj=8e-63), debt_to_income_ratio (p_adj=2.5e-14), applicant_credit_score_type (p_adj=9.2e-06), aus-1 (p_adj=1.5e-31), tract_population (p_adj=1.2e-268), ffiec_msa_md_median_family_income (p_adj=1.4e-63), tract_to_msa_income_percentage (p_adj=2.4e-158), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=2.3e-213), tract_median_age_of_housing_units (p_adj=5.4e-104)
- องค์ประกอบ race_eth: Hispanic 7.5% (ทั้งชุด 9.1%), NH Asian 9.9% (ทั้งชุด 6.8%), NH Black 18.7% (ทั้งชุด 22.0%), NH White 42.2% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.3%), Unknown 19.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 21.0% (ทั้งชุด 27.1%), Joint 35.5% (ทั้งชุด 30.7%), Male 36.9% (ทั้งชุด 35.6%), Unknown 6.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.3% (ทั้งชุด 31.4%), 35-44 30.5% (ทั้งชุด 26.6%), 45-54 18.9% (ทั้งชุด 17.5%), 55-64 12.0% (ทั้งชุด 11.7%), 65-74 5.4% (ทั้งชุด 5.5%), <25 3.7% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 29 · กลุ่ม 0
- IF initially_payable_to_institution_3 ≤ 0.5 AND debt_to_income_ratio > 60 AND loan_term > 324 THEN อยู่กลุ่มนี้
- IF initially_payable_to_institution_3 > 0.5 AND submission_of_application_2 ≤ 0.5 AND tract_to_msa_income_percentage ≤ 89.83 THEN อยู่กลุ่มนี้
- IF initially_payable_to_institution_3 > 0.5 AND submission_of_application_2 ≤ 0.5 AND tract_to_msa_income_percentage > 89.83 THEN อยู่กลุ่มนี้
- IF initially_payable_to_institution_3 > 0.5 AND submission_of_application_2 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1129/589/617 · coverage กฎบน validation 0.0435
- Fidelity F1 0.1861 · precision 0.4080 · recall 0.1205 · เงื่อนไขรวม 11 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- **กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี**
- คำอธิบายสำรอง: ตัวแปรที่ต่างจากส่วนที่เหลือมากที่สุด คำนวณบน train เท่านั้น
  - debt_to_income_ratio: SMD 0.570; ค่าเฉลี่ยกลุ่ม 48.09, ส่วนที่เหลือ 40.81
  - loan_term: SMD 0.373; ค่าเฉลี่ยกลุ่ม 358.5, ส่วนที่เหลือ 346.3
  - ffiec_msa_md_median_family_income: SMD 0.189; ค่าเฉลี่ยกลุ่ม 9.419e+04, ส่วนที่เหลือ 9.145e+04
  - initially_payable_to_institution = 3: สัดส่วนต่าง +0.187; กลุ่ม 19.2%, ส่วนที่เหลือ 0.5%
  - loan_type = 1: สัดส่วนต่าง -0.162; กลุ่ม 47.5%, ส่วนที่เหลือ 63.7%
- อนุมัติจริง 0.8023 · ERM error 0.0972 · FPR 0.4590 · FNR 0.0081
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.3e-10), derived_msa-md (p_adj=1.5e-44), county_code (p_adj=1.2e-30), derived_loan_product_type (p_adj=2.1e-90), loan_type (p_adj=1.6e-91), loan_term (p_adj=2.3e-62), property_value (p_adj=6.2e-05), construction_method (p_adj=8.8e-10), income (p_adj=5.1e-28), debt_to_income_ratio (p_adj=9.1e-137), aus-1 (p_adj=2.4e-48), tract_population (p_adj=8.9e-07), ffiec_msa_md_median_family_income (p_adj=8.8e-107), tract_median_age_of_housing_units (p_adj=0.0034)
- องค์ประกอบ race_eth: Hispanic 12.6% (ทั้งชุด 9.1%), NH Asian 5.0% (ทั้งชุด 6.8%), NH Black 32.7% (ทั้งชุด 22.0%), NH White 24.6% (ทั้งชุด 41.8%), Other 3.1% (ทั้งชุด 2.4%), Unknown 21.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 31.1% (ทั้งชุด 28.3%), Joint 26.4% (ทั้งชุด 30.0%), Male 34.5% (ทั้งชุด 35.3%), Unknown 7.9% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.7% (ทั้งชุด 29.9%), 35-44 29.0% (ทั้งชุด 27.0%), 45-54 18.3% (ทั้งชุด 17.5%), 55-64 11.2% (ทั้งชุด 11.8%), 65-74 6.0% (ทั้งชุด 5.2%), <25 5.3% (ทั้งชุด 7.2%), >74 1.5% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 29 · กลุ่ม 1
- IF total_units > 2.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2/2/6 · coverage กฎบน validation 0.0005
- Fidelity F1 1.0000 · precision 1.0000 · recall 1.0000 · เงื่อนไขรวม 1 · สูงสุดต่อเส้นทาง 1
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 1.0000 · ERM error 0.0000 · FPR N/A · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.7e-134), loan_term (p_adj=4.4e-67), applicant_credit_score_type (p_adj=0.015), submission_of_application (p_adj=2.2e-06), initially_payable_to_institution (p_adj=1.1e-05), aus-1 (p_adj=5.5e-05)
- องค์ประกอบ race_eth: Hispanic 0.0% (ทั้งชุด 9.1%), NH Asian 16.7% (ทั้งชุด 6.8%), NH Black 33.3% (ทั้งชุด 22.0%), NH White 50.0% (ทั้งชุด 41.8%), Other 0.0% (ทั้งชุด 2.4%), Unknown 0.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 16.7% (ทั้งชุด 28.3%), Joint 50.0% (ทั้งชุด 30.0%), Male 33.3% (ทั้งชุด 35.3%), Unknown 0.0% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 50.0% (ทั้งชุด 29.9%), 35-44 33.3% (ทั้งชุด 27.0%), 45-54 0.0% (ทั้งชุด 17.5%), 55-64 16.7% (ทั้งชุด 11.8%), 65-74 0.0% (ทั้งชุด 5.2%), <25 0.0% (ทั้งชุด 7.2%), >74 0.0% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 29 · กลุ่ม 2
- IF construction_method_2 ≤ 0.5 AND loan_amount ≤ 1.2e+05 AND loan_term ≤ 330 THEN อยู่กลุ่มนี้
- IF construction_method_2 > 0.5 AND aus-1_6 ≤ 0.5 AND loan_amount ≤ 1.9e+05 THEN อยู่กลุ่มนี้
- IF construction_method_2 > 0.5 AND aus-1_6 > 0.5 AND tract_population > 1011 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 684/362/342 · coverage กฎบน validation 0.0995
- Fidelity F1 0.8500 · precision 0.8116 · recall 0.8923 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.3918 · ERM error 0.1871 · FPR 0.1587 · FNR 0.2313
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=7.7e-243), derived_msa-md (p_adj=1e-60), county_code (p_adj=2.3e-130), derived_loan_product_type (p_adj=3.1e-74), loan_type (p_adj=1.4e-42), lien_status (p_adj=4e-40), loan_amount (p_adj=1.5e-228), loan_term (p_adj=2.5e-82), property_value (p_adj=1.8e-150), construction_method (p_adj=0), income (p_adj=9.2e-64), applicant_credit_score_type (p_adj=1.2e-155), initially_payable_to_institution (p_adj=0.04), aus-1 (p_adj=2.3e-286), tract_population (p_adj=2.8e-18), ffiec_msa_md_median_family_income (p_adj=3.9e-36), tract_to_msa_income_percentage (p_adj=1e-16), tract_owner_occupied_units (p_adj=9.7e-16), tract_median_age_of_housing_units (p_adj=1.2e-12)
- องค์ประกอบ race_eth: Hispanic 10.2% (ทั้งชุด 9.1%), NH Asian 2.3% (ทั้งชุด 6.8%), NH Black 22.8% (ทั้งชุด 22.0%), NH White 44.7% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.4%), Unknown 17.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 41.2% (ทั้งชุด 28.3%), Joint 27.5% (ทั้งชุด 30.0%), Male 28.1% (ทั้งชุด 35.3%), Unknown 3.2% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 26.3% (ทั้งชุด 29.9%), 35-44 24.3% (ทั้งชุด 27.0%), 45-54 17.3% (ทั้งชุด 17.5%), 55-64 13.2% (ทั้งชุด 11.8%), 65-74 7.3% (ทั้งชุด 5.2%), <25 10.8% (ทั้งชุด 7.2%), >74 0.9% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 29 · กลุ่ม 3
- IF tract_median_age_of_housing_units ≤ 4.5 AND tract_owner_occupied_units ≤ 261.5 AND property_value ≤ 3.8e+05 THEN อยู่กลุ่มนี้
- IF tract_median_age_of_housing_units ≤ 4.5 AND tract_owner_occupied_units ≤ 261.5 AND property_value > 3.8e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 145/58/41 · coverage กฎบน validation 0.0150
- Fidelity F1 0.9831 · precision 0.9667 · recall 1.0000 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.0732 · ERM error 0.0976 · FPR 0.0526 · FNR 0.6667
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.1e-76), derived_msa-md (p_adj=1.2e-08), county_code (p_adj=3.6e-142), loan_amount (p_adj=2.4e-12), loan_term (p_adj=3e-11), property_value (p_adj=1e-13), construction_method (p_adj=5.9e-59), income (p_adj=9.2e-06), applicant_credit_score_type (p_adj=0.01), aus-1 (p_adj=1.2e-30), tract_population (p_adj=4.4e-182), ffiec_msa_md_median_family_income (p_adj=0.01), tract_to_msa_income_percentage (p_adj=0), tract_owner_occupied_units (p_adj=1.4e-99), tract_one_to_four_family_homes (p_adj=1.6e-89), tract_median_age_of_housing_units (p_adj=4.3e-50)
- องค์ประกอบ race_eth: Hispanic 0.0% (ทั้งชุด 9.1%), NH Asian 2.4% (ทั้งชุด 6.8%), NH Black 46.3% (ทั้งชุด 22.0%), NH White 48.8% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.4%), Unknown 0.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 53.7% (ทั้งชุด 28.3%), Joint 26.8% (ทั้งชุด 30.0%), Male 19.5% (ทั้งชุด 35.3%), Unknown 0.0% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 41.5% (ทั้งชุด 29.9%), 35-44 26.8% (ทั้งชุด 27.0%), 45-54 12.2% (ทั้งชุด 17.5%), 55-64 7.3% (ทั้งชุด 11.8%), 65-74 4.9% (ทั้งชุด 5.2%), <25 7.3% (ทั้งชุด 7.2%), >74 0.0% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 29 · กลุ่ม 4
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND aus-1_6 ≤ 0.5 AND tract_owner_occupied_units ≤ 1781 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2637/801/774 · coverage กฎบน validation 0.1913
- Fidelity F1 0.8799 · precision 0.9007 · recall 0.8602 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8992 · ERM error 0.0904 · FPR 0.7692 · FNR 0.0144
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.6e-15), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.0027), derived_loan_product_type (p_adj=3.6e-35), loan_type (p_adj=4.9e-36), loan_amount (p_adj=3e-87), loan_term (p_adj=1.1e-64), property_value (p_adj=1.4e-87), income (p_adj=1.2e-32), applicant_credit_score_type (p_adj=2.9e-05), submission_of_application (p_adj=0.0004), initially_payable_to_institution (p_adj=3.2e-08), aus-1 (p_adj=4.4e-24), tract_population (p_adj=1.1e-14), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=2.1e-21), tract_one_to_four_family_homes (p_adj=0.012), tract_median_age_of_housing_units (p_adj=6.6e-29)
- องค์ประกอบ race_eth: Hispanic 8.0% (ทั้งชุด 9.1%), NH Asian 2.3% (ทั้งชุด 6.8%), NH Black 15.5% (ทั้งชุด 22.0%), NH White 56.7% (ทั้งชุด 41.8%), Other 2.5% (ทั้งชุด 2.4%), Unknown 15.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 25.1% (ทั้งชุด 28.3%), Joint 29.5% (ทั้งชุด 30.0%), Male 39.5% (ทั้งชุด 35.3%), Unknown 5.9% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.4% (ทั้งชุด 29.9%), 35-44 23.5% (ทั้งชุด 27.0%), 45-54 15.9% (ทั้งชุด 17.5%), 55-64 11.5% (ทั้งชุด 11.8%), 65-74 6.6% (ทั้งชุด 5.2%), <25 12.8% (ทั้งชุด 7.2%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 29 · กลุ่ม 5
- IF property_value ≤ 7.1e+05 AND property_value > 5.9e+05 AND tract_to_msa_income_percentage > 173.8 THEN อยู่กลุ่มนี้
- IF property_value > 7.1e+05 AND income ≤ 172.5 AND tract_to_msa_income_percentage > 179.1 THEN อยู่กลุ่มนี้
- IF property_value > 7.1e+05 AND income > 172.5 AND tract_population ≤ 6049 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 810/276/287 · coverage กฎบน validation 0.0655
- Fidelity F1 0.7770 · precision 0.7977 · recall 0.7572 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9303 · ERM error 0.0592 · FPR 0.8000 · FNR 0.0037
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.1e-14), derived_msa-md (p_adj=8e-12), county_code (p_adj=3e-27), conforming_loan_limit (p_adj=8.1e-263), derived_loan_product_type (p_adj=7.1e-31), loan_type (p_adj=4e-29), loan_amount (p_adj=5.8e-60), property_value (p_adj=4.4e-54), construction_method (p_adj=1.5e-05), income (p_adj=6.5e-28), debt_to_income_ratio (p_adj=2.7e-19), aus-1 (p_adj=6.5e-23), tract_population (p_adj=1.1e-07), ffiec_msa_md_median_family_income (p_adj=2.8e-35), tract_to_msa_income_percentage (p_adj=1.4e-56), tract_one_to_four_family_homes (p_adj=4.3e-10)
- องค์ประกอบ race_eth: Hispanic 3.1% (ทั้งชุด 9.1%), NH Asian 16.0% (ทั้งชุด 6.8%), NH Black 11.5% (ทั้งชุด 22.0%), NH White 47.0% (ทั้งชุด 41.8%), Other 3.8% (ทั้งชุด 2.4%), Unknown 18.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 10.8% (ทั้งชุด 28.3%), Joint 49.5% (ทั้งชุด 30.0%), Male 33.4% (ทั้งชุด 35.3%), Unknown 6.3% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 24.0% (ทั้งชุด 29.9%), 35-44 36.2% (ทั้งชุด 27.0%), 45-54 24.4% (ทั้งชุด 17.5%), 55-64 13.9% (ทั้งชุด 11.8%), 65-74 0.7% (ทั้งชุด 5.2%), <25 0.3% (ทั้งชุด 7.2%), >74 0.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 29 · กลุ่ม 6
- IF tract_owner_occupied_units > 1413 AND ffiec_msa_md_median_family_income ≤ 7.71e+04 AND tract_owner_occupied_units > 1748 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1413 AND ffiec_msa_md_median_family_income > 7.71e+04 AND loan_amount ≤ 6.6e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2664/829/872 · coverage กฎบน validation 0.2010
- Fidelity F1 0.8267 · precision 0.8396 · recall 0.8142 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9197 · ERM error 0.0642 · FPR 0.7286 · FNR 0.0062
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0047), derived_msa-md (p_adj=9.5e-41), county_code (p_adj=2.8e-136), conforming_loan_limit (p_adj=0.0047), derived_loan_product_type (p_adj=0.00042), loan_type (p_adj=0.00053), loan_amount (p_adj=1.5e-13), loan_term (p_adj=8.8e-15), property_value (p_adj=4.5e-08), construction_method (p_adj=2.3e-16), debt_to_income_ratio (p_adj=1.5e-05), aus-1 (p_adj=1.6e-15), tract_population (p_adj=9.2e-256), ffiec_msa_md_median_family_income (p_adj=2.3e-38), tract_to_msa_income_percentage (p_adj=6.7e-34), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=3.5e-266), tract_median_age_of_housing_units (p_adj=1e-131)
- องค์ประกอบ race_eth: Hispanic 6.5% (ทั้งชุด 9.1%), NH Asian 9.9% (ทั้งชุด 6.8%), NH Black 17.1% (ทั้งชุด 22.0%), NH White 43.6% (ทั้งชุด 41.8%), Other 1.6% (ทั้งชุด 2.4%), Unknown 21.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 23.2% (ทั้งชุด 28.3%), Joint 33.6% (ทั้งชุด 30.0%), Male 35.3% (ทั้งชุด 35.3%), Unknown 7.9% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 29.1% (ทั้งชุด 29.9%), 35-44 29.7% (ทั้งชุด 27.0%), 45-54 17.7% (ทั้งชุด 17.5%), 55-64 12.6% (ทั้งชุด 11.8%), 65-74 5.5% (ทั้งชุด 5.2%), <25 4.6% (ทั้งชุด 7.2%), >74 0.7% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 29 · กลุ่ม 7
- IF ffiec_msa_md_median_family_income ≤ 9.11e+04 AND ffiec_msa_md_median_family_income > 8.405e+04 AND tract_one_to_four_family_homes ≤ 1394 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 9.11e+04 AND tract_owner_occupied_units ≤ 1298 AND property_value ≤ 6.7e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3929/1083/1061 · coverage กฎบน validation 0.4065
- Fidelity F1 0.7612 · precision 0.6341 · recall 0.9520 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8897 · ERM error 0.0829 · FPR 0.7265 · FNR 0.0032
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0014), derived_msa-md (p_adj=5.9e-121), county_code (p_adj=5.1e-113), conforming_loan_limit (p_adj=2.1e-05), derived_loan_product_type (p_adj=1.1e-07), loan_type (p_adj=7.2e-06), loan_term (p_adj=5.3e-40), property_value (p_adj=0.00049), construction_method (p_adj=9.7e-19), income (p_adj=0.026), debt_to_income_ratio (p_adj=2e-06), aus-1 (p_adj=8e-27), tract_population (p_adj=5.5e-171), ffiec_msa_md_median_family_income (p_adj=3.8e-293), tract_to_msa_income_percentage (p_adj=8.3e-59), tract_owner_occupied_units (p_adj=2.6e-283), tract_one_to_four_family_homes (p_adj=1.3e-290), tract_median_age_of_housing_units (p_adj=1.3e-16)
- องค์ประกอบ race_eth: Hispanic 11.6% (ทั้งชุด 9.1%), NH Asian 7.4% (ทั้งชุด 6.8%), NH Black 26.0% (ทั้งชุด 22.0%), NH White 36.6% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.4%), Unknown 16.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 32.9% (ทั้งชุด 28.3%), Joint 25.1% (ทั้งชุด 30.0%), Male 36.0% (ทั้งชุด 35.3%), Unknown 6.0% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 34.7% (ทั้งชุด 29.9%), 35-44 24.3% (ทั้งชุด 27.0%), 45-54 16.7% (ทั้งชุด 17.5%), 55-64 10.7% (ทั้งชุด 11.8%), 65-74 4.1% (ทั้งชุด 5.2%), <25 7.2% (ทั้งชุด 7.2%), >74 2.4% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 29 · กลุ่ม 0
- IF debt_to_income_ratio ≤ 52 AND initially_payable_to_institution_3 > 0.5 AND property_value ≤ 4.6e+05 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio ≤ 52 AND initially_payable_to_institution_3 > 0.5 AND property_value > 4.6e+05 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 52 AND loan_term ≤ 324 AND construction_method_1 > 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 52 AND loan_term > 324 AND debt_to_income_ratio ≤ 60 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 52 AND loan_term > 324 AND debt_to_income_ratio > 60 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 857/837/842 · coverage กฎบน validation 0.1722
- Fidelity F1 0.4797 · precision 0.5312 · recall 0.4373 · เงื่อนไขรวม 15 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- **กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี**
- คำอธิบายสำรอง: ตัวแปรที่ต่างจากส่วนที่เหลือมากที่สุด คำนวณบน train เท่านั้น
  - debt_to_income_ratio: SMD 0.722; ค่าเฉลี่ยกลุ่ม 49.71, ส่วนที่เหลือ 40.85
  - property_value: SMD -0.391; ค่าเฉลี่ยกลุ่ม 3.102e+05, ส่วนที่เหลือ 3.946e+05
  - tract_to_msa_income_percentage: SMD -0.387; ค่าเฉลี่ยกลุ่ม 92.42, ส่วนที่เหลือ 108.6
  - income: SMD -0.362; ค่าเฉลี่ยกลุ่ม 83.27, ส่วนที่เหลือ 126.1
  - loan_term: SMD 0.324; ค่าเฉลี่ยกลุ่ม 357.5, ส่วนที่เหลือ 346.7
- อนุมัติจริง 0.8409 · ERM error 0.0926 · FPR 0.5522 · FNR 0.0056
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.7e-25), derived_msa-md (p_adj=1.5e-41), county_code (p_adj=6.8e-53), conforming_loan_limit (p_adj=0.00067), derived_loan_product_type (p_adj=0), loan_type (p_adj=0), lien_status (p_adj=0.0059), loan_amount (p_adj=0.00028), loan_term (p_adj=1.1e-49), property_value (p_adj=2.7e-48), construction_method (p_adj=7.3e-10), income (p_adj=7e-45), debt_to_income_ratio (p_adj=4.1e-82), applicant_credit_score_type (p_adj=1.5e-05), initially_payable_to_institution (p_adj=6.6e-08), aus-1 (p_adj=0), ffiec_msa_md_median_family_income (p_adj=9.4e-88), tract_to_msa_income_percentage (p_adj=3.2e-57), tract_owner_occupied_units (p_adj=1.2e-14), tract_one_to_four_family_homes (p_adj=1.2e-12)
- องค์ประกอบ race_eth: Hispanic 12.0% (ทั้งชุด 9.1%), NH Asian 1.9% (ทั้งชุด 6.8%), NH Black 40.0% (ทั้งชุด 22.0%), NH White 24.2% (ทั้งชุด 41.8%), Other 1.8% (ทั้งชุด 2.4%), Unknown 20.1% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.0% (ทั้งชุด 28.3%), Joint 26.5% (ทั้งชุด 30.0%), Male 32.8% (ทั้งชุด 35.3%), Unknown 6.8% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 30.9% (ทั้งชุด 29.9%), 35-44 27.6% (ทั้งชุด 27.0%), 45-54 18.8% (ทั้งชุด 17.5%), 55-64 10.2% (ทั้งชุด 11.8%), 65-74 3.7% (ทั้งชุด 5.2%), <25 7.2% (ทั้งชุด 7.2%), >74 1.7% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 29 · กลุ่ม 1
- IF construction_method_1 ≤ 0.5 AND aus-1_6 > 0.5 AND tract_population > 1514 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 645/326/319 · coverage กฎบน validation 0.0717
- Fidelity F1 0.8711 · precision 0.9303 · recall 0.8190 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.3605 · ERM error 0.2194 · FPR 0.1765 · FNR 0.2957
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.6e-295), derived_msa-md (p_adj=4.1e-51), county_code (p_adj=6.7e-126), derived_loan_product_type (p_adj=1.3e-82), loan_type (p_adj=6.8e-40), lien_status (p_adj=3.5e-52), loan_amount (p_adj=1.4e-260), loan_term (p_adj=2.7e-58), property_value (p_adj=6.2e-174), construction_method (p_adj=0), income (p_adj=5.3e-86), applicant_credit_score_type (p_adj=2.6e-201), aus-1 (p_adj=0), tract_population (p_adj=7.2e-08), ffiec_msa_md_median_family_income (p_adj=2.9e-31), tract_to_msa_income_percentage (p_adj=7.6e-18), tract_owner_occupied_units (p_adj=0.00011), tract_median_age_of_housing_units (p_adj=2.6e-09)
- องค์ประกอบ race_eth: Hispanic 9.1% (ทั้งชุด 9.1%), NH Asian 0.3% (ทั้งชุด 6.8%), NH Black 24.1% (ทั้งชุด 22.0%), NH White 44.5% (ทั้งชุด 41.8%), Other 2.2% (ทั้งชุด 2.4%), Unknown 19.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 43.3% (ทั้งชุด 28.3%), Joint 27.9% (ทั้งชุด 30.0%), Male 24.5% (ทั้งชุด 35.3%), Unknown 4.4% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 24.8% (ทั้งชุด 29.9%), 35-44 24.5% (ทั้งชุด 27.0%), 45-54 17.2% (ทั้งชุด 17.5%), 55-64 14.1% (ทั้งชุด 11.8%), 65-74 6.6% (ทั้งชุด 5.2%), <25 12.2% (ทั้งชุด 7.2%), >74 0.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 29 · กลุ่ม 2
- IF property_value ≤ 3.3e+05 AND tract_one_to_four_family_homes > 1882 AND debt_to_income_ratio > 60 THEN อยู่กลุ่มนี้
- IF property_value > 3.3e+05 AND loan_type_2 ≤ 0.5 AND initially_payable_to_institution_3 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF property_value > 3.3e+05 AND loan_type_2 ≤ 0.5 AND initially_payable_to_institution_3 > 0.5 THEN อยู่กลุ่มนี้
- IF property_value > 3.3e+05 AND loan_type_2 > 0.5 AND tract_owner_occupied_units > 1853 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 269/380/375 · coverage กฎบน validation 0.4545
- Fidelity F1 0.3203 · precision 0.1936 · recall 0.9263 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- **กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี**
- คำอธิบายสำรอง: ตัวแปรที่ต่างจากส่วนที่เหลือมากที่สุด คำนวณบน train เท่านั้น
  - loan_amount: SMD 0.740; ค่าเฉลี่ยกลุ่ม 4.862e+05, ส่วนที่เหลือ 3.176e+05
  - tract_to_msa_income_percentage: SMD 0.698; ค่าเฉลี่ยกลุ่ม 137.7, ส่วนที่เหลือ 106.8
  - property_value: SMD 0.695; ค่าเฉลี่ยกลุ่ม 6.005e+05, ส่วนที่เหลือ 3.842e+05
  - tract_owner_occupied_units: SMD 0.626; ค่าเฉลี่ยกลุ่ม 1401, ส่วนที่เหลือ 1087
  - tract_population: SMD 0.540; ค่าเฉลี่ยกลุ่ม 5457, ส่วนที่เหลือ 4453
- อนุมัติจริง 0.9253 · ERM error 0.0480 · FPR 0.6429 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.5e-09), county_code (p_adj=4.4e-67), derived_loan_product_type (p_adj=1.1e-28), loan_type (p_adj=2.8e-26), loan_amount (p_adj=1e-46), loan_term (p_adj=6.2e-05), property_value (p_adj=1e-52), construction_method (p_adj=8.5e-06), income (p_adj=1.2e-16), debt_to_income_ratio (p_adj=1.7e-08), submission_of_application (p_adj=0.0015), aus-1 (p_adj=4.2e-19), tract_population (p_adj=3.1e-44), tract_to_msa_income_percentage (p_adj=1.6e-52), tract_owner_occupied_units (p_adj=5.9e-70), tract_one_to_four_family_homes (p_adj=1.7e-48), tract_median_age_of_housing_units (p_adj=4.1e-45)
- องค์ประกอบ race_eth: Hispanic 5.1% (ทั้งชุด 9.1%), NH Asian 14.4% (ทั้งชุด 6.8%), NH Black 8.3% (ทั้งชุด 22.0%), NH White 53.6% (ทั้งชุด 41.8%), Other 0.8% (ทั้งชุด 2.4%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 17.9% (ทั้งชุด 28.3%), Joint 39.2% (ทั้งชุด 30.0%), Male 38.4% (ทั้งชุด 35.3%), Unknown 4.5% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 29.1% (ทั้งชุด 29.9%), 35-44 29.3% (ทั้งชุด 27.0%), 45-54 18.7% (ทั้งชุด 17.5%), 55-64 12.5% (ทั้งชุด 11.8%), 65-74 7.7% (ทั้งชุด 5.2%), <25 1.1% (ทั้งชุด 7.2%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.3% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 29 · กลุ่ม 3
- IF tract_population ≤ 95.5 AND property_value ≤ 3.4e+05 AND income ≤ 69.5 THEN อยู่กลุ่มนี้
- IF tract_population ≤ 95.5 AND property_value ≤ 3.4e+05 AND income > 69.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 189/75/54 · coverage กฎบน validation 0.0138
- Fidelity F1 0.8308 · precision 0.9818 · recall 0.7200 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.0926 · ERM error 0.0741 · FPR 0.0408 · FNR 0.4000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.3e-108), derived_msa-md (p_adj=1.7e-22), county_code (p_adj=3.7e-147), loan_amount (p_adj=5.1e-27), loan_term (p_adj=1.9e-19), property_value (p_adj=4.7e-30), construction_method (p_adj=4.5e-87), income (p_adj=5.8e-17), debt_to_income_ratio (p_adj=0.032), applicant_credit_score_type (p_adj=1.5e-05), aus-1 (p_adj=7.9e-46), tract_population (p_adj=1.7e-35), ffiec_msa_md_median_family_income (p_adj=5.2e-06), tract_to_msa_income_percentage (p_adj=3.3e-17), tract_owner_occupied_units (p_adj=1.8e-35), tract_one_to_four_family_homes (p_adj=8.8e-30), tract_median_age_of_housing_units (p_adj=8.9e-10)
- องค์ประกอบ race_eth: Hispanic 3.7% (ทั้งชุด 9.1%), NH Asian 1.9% (ทั้งชุด 6.8%), NH Black 38.9% (ทั้งชุด 22.0%), NH White 51.9% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.4%), Unknown 1.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 55.6% (ทั้งชุด 28.3%), Joint 22.2% (ทั้งชุด 30.0%), Male 22.2% (ทั้งชุด 35.3%), Unknown 0.0% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 48.1% (ทั้งชุด 29.9%), 35-44 24.1% (ทั้งชุด 27.0%), 45-54 11.1% (ทั้งชุด 17.5%), 55-64 5.6% (ทั้งชุด 11.8%), 65-74 5.6% (ทั้งชุด 5.2%), <25 5.6% (ทั้งชุด 7.2%), >74 0.0% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 29 · กลุ่ม 4
- IF property_value > 6e+05 AND income ≤ 182.5 AND tract_to_msa_income_percentage > 125.2 THEN อยู่กลุ่มนี้
- IF property_value > 6e+05 AND income > 182.5 AND derived_loan_product_type_Conventional:First Lien > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1235/310/327 · coverage กฎบน validation 0.1025
- Fidelity F1 0.7111 · precision 0.6244 · recall 0.8258 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9266 · ERM error 0.0581 · FPR 0.7500 · FNR 0.0033
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1e-17), derived_msa-md (p_adj=6.2e-17), county_code (p_adj=3.3e-53), conforming_loan_limit (p_adj=7.7e-228), derived_loan_product_type (p_adj=2.8e-41), loan_type (p_adj=6.5e-39), loan_amount (p_adj=7.3e-63), property_value (p_adj=2.6e-57), construction_method (p_adj=8.6e-07), income (p_adj=6.4e-32), debt_to_income_ratio (p_adj=1.1e-26), aus-1 (p_adj=2.1e-25), tract_population (p_adj=0.00073), ffiec_msa_md_median_family_income (p_adj=3.4e-49), tract_to_msa_income_percentage (p_adj=4.1e-63), tract_one_to_four_family_homes (p_adj=5e-05)
- องค์ประกอบ race_eth: Hispanic 2.8% (ทั้งชุด 9.1%), NH Asian 16.8% (ทั้งชุด 6.8%), NH Black 10.4% (ทั้งชุด 22.0%), NH White 47.7% (ทั้งชุด 41.8%), Other 4.3% (ทั้งชุด 2.4%), Unknown 18.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 12.2% (ทั้งชุด 28.3%), Joint 48.3% (ทั้งชุด 30.0%), Male 32.1% (ทั้งชุด 35.3%), Unknown 7.3% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 22.3% (ทั้งชุด 29.9%), 35-44 38.2% (ทั้งชุด 27.0%), 45-54 24.2% (ทั้งชุด 17.5%), 55-64 13.8% (ทั้งชุด 11.8%), 65-74 0.6% (ทั้งชุด 5.2%), <25 0.3% (ทั้งชุด 7.2%), >74 0.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 29 · กลุ่ม 5
- IF ffiec_msa_md_median_family_income > 9.58e+04 AND property_value ≤ 6.5e+05 AND debt_to_income_ratio ≤ 60 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4870/1053/1065 · coverage กฎบน validation 0.4960
- Fidelity F1 0.6388 · precision 0.4889 · recall 0.9212 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8977 · ERM error 0.0695 · FPR 0.6697 · FNR 0.0010
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=8.5e-23), derived_msa-md (p_adj=2.3e-154), county_code (p_adj=5.4e-125), conforming_loan_limit (p_adj=4.6e-06), derived_loan_product_type (p_adj=5.4e-146), preapproval (p_adj=0.011), loan_type (p_adj=7.2e-137), loan_term (p_adj=1.7e-16), construction_method (p_adj=5.4e-30), income (p_adj=0.00014), debt_to_income_ratio (p_adj=6e-11), applicant_credit_score_type (p_adj=3.9e-07), aus-1 (p_adj=7.4e-99), ffiec_msa_md_median_family_income (p_adj=0), tract_to_msa_income_percentage (p_adj=4.4e-09), tract_owner_occupied_units (p_adj=0.00071), tract_one_to_four_family_homes (p_adj=3.6e-21)
- องค์ประกอบ race_eth: Hispanic 12.5% (ทั้งชุด 9.1%), NH Asian 10.5% (ทั้งชุด 6.8%), NH Black 17.7% (ทั้งชุด 22.0%), NH White 39.0% (ทั้งชุด 41.8%), Other 2.5% (ทั้งชุด 2.4%), Unknown 17.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 30.1% (ทั้งชุด 28.3%), Joint 26.9% (ทั้งชุด 30.0%), Male 35.8% (ทั้งชุด 35.3%), Unknown 7.1% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 34.0% (ทั้งชุด 29.9%), 35-44 23.9% (ทั้งชุด 27.0%), 45-54 15.8% (ทั้งชุด 17.5%), 55-64 12.1% (ทั้งชุด 11.8%), 65-74 5.6% (ทั้งชุด 5.2%), <25 7.1% (ทั้งชุด 7.2%), >74 1.4% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 29 · กลุ่ม 6
- IF loan_type_3 ≤ 0.5 AND tract_one_to_four_family_homes > 2732 AND tract_population > 8443 THEN อยู่กลุ่มนี้
- IF loan_type_3 > 0.5 AND ffiec_msa_md_median_family_income ≤ 9.58e+04 AND tract_owner_occupied_units ≤ 776.5 THEN อยู่กลุ่มนี้
- IF loan_type_3 > 0.5 AND ffiec_msa_md_median_family_income ≤ 9.58e+04 AND tract_owner_occupied_units > 776.5 THEN อยู่กลุ่มนี้
- IF loan_type_3 > 0.5 AND ffiec_msa_md_median_family_income > 9.58e+04 AND tract_owner_occupied_units > 1054 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1531/415/440 · coverage กฎบน validation 0.1075
- Fidelity F1 0.7882 · precision 0.7744 · recall 0.8024 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9023 · ERM error 0.0886 · FPR 0.8140 · FNR 0.0101
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.3e-93), derived_msa-md (p_adj=1.9e-154), county_code (p_adj=4.2e-136), derived_loan_product_type (p_adj=0), loan_type (p_adj=0), loan_term (p_adj=7.1e-58), property_value (p_adj=3.4e-12), construction_method (p_adj=2.4e-07), income (p_adj=1.7e-09), debt_to_income_ratio (p_adj=5.6e-13), applicant_credit_score_type (p_adj=6.1e-05), submission_of_application (p_adj=2.5e-05), initially_payable_to_institution (p_adj=0.005), aus-1 (p_adj=7.3e-54), tract_population (p_adj=1.7e-20), ffiec_msa_md_median_family_income (p_adj=1.7e-51), tract_to_msa_income_percentage (p_adj=3e-10), tract_owner_occupied_units (p_adj=4.9e-15), tract_one_to_four_family_homes (p_adj=2.8e-24), tract_median_age_of_housing_units (p_adj=1.1e-12)
- องค์ประกอบ race_eth: Hispanic 6.1% (ทั้งชุด 9.1%), NH Asian 2.3% (ทั้งชุด 6.8%), NH Black 26.1% (ทั้งชุด 22.0%), NH White 40.0% (ทั้งชุด 41.8%), Other 3.6% (ทั้งชุด 2.4%), Unknown 21.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 18.0% (ทั้งชุด 28.3%), Joint 28.6% (ทั้งชุด 30.0%), Male 45.0% (ทั้งชุด 35.3%), Unknown 8.4% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.6% (ทั้งชุด 29.9%), 35-44 28.4% (ทั้งชุด 27.0%), 45-54 16.8% (ทั้งชุด 17.5%), 55-64 10.9% (ทั้งชุด 11.8%), 65-74 5.0% (ทั้งชุด 5.2%), <25 8.6% (ทั้งชุด 7.2%), >74 1.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 29 · กลุ่ม 7
- IF ffiec_msa_md_median_family_income ≤ 1.015e+05 AND derived_loan_product_type_VA:First Lien ≤ 0.5 AND tract_median_age_of_housing_units > 16.5 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 1.015e+05 AND loan_amount ≤ 4e+04 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2404/604/578 · coverage กฎบน validation 0.3070
- Fidelity F1 0.6245 · precision 0.4658 · recall 0.9470 · เงื่อนไขรวม 5 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8927 · ERM error 0.0986 · FPR 0.7581 · FNR 0.0194
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.4e-41), derived_msa-md (p_adj=1.8e-229), county_code (p_adj=5.2e-230), derived_loan_product_type (p_adj=5.7e-48), loan_type (p_adj=2.6e-42), lien_status (p_adj=3.9e-05), loan_amount (p_adj=1e-144), property_value (p_adj=4.9e-115), income (p_adj=3.3e-21), debt_to_income_ratio (p_adj=1e-11), applicant_credit_score_type (p_adj=7.5e-35), submission_of_application (p_adj=3.3e-39), initially_payable_to_institution (p_adj=4.1e-46), aus-1 (p_adj=1.2e-61), tract_population (p_adj=2.9e-13), ffiec_msa_md_median_family_income (p_adj=5e-196), tract_owner_occupied_units (p_adj=1.7e-09), tract_median_age_of_housing_units (p_adj=2.4e-41)
- องค์ประกอบ race_eth: Hispanic 7.6% (ทั้งชุด 9.1%), NH Asian 3.6% (ทั้งชุด 6.8%), NH Black 13.0% (ทั้งชุด 22.0%), NH White 60.2% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.4%), Unknown 13.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 29.6% (ทั้งชุด 28.3%), Joint 27.3% (ทั้งชุด 30.0%), Male 37.5% (ทั้งชุด 35.3%), Unknown 5.5% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.2% (ทั้งชุด 29.9%), 35-44 24.2% (ทั้งชุด 27.0%), 45-54 15.7% (ทั้งชุด 17.5%), 55-64 11.8% (ทั้งชุด 11.8%), 65-74 6.9% (ทั้งชุด 5.2%), <25 11.6% (ทั้งชุด 7.2%), >74 1.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 29 · กลุ่ม 0
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio ≤ 52 AND initially_payable_to_institution_3 > 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio > 52 AND lei_549300FGXN1K3HLB1R50 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND debt_to_income_ratio ≤ 60 AND construction_method_1 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND debt_to_income_ratio ≤ 60 AND construction_method_1 > 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND debt_to_income_ratio > 60 AND construction_method_2 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1254/688/622 · coverage กฎบน validation 0.3035
- Fidelity F1 0.5678 · precision 0.4448 · recall 0.7849 · เงื่อนไขรวม 15 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.5836 · ERM error 0.2717 · FPR 0.4479 · FNR 0.1460
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.7e-81), derived_msa-md (p_adj=5.2e-12), county_code (p_adj=9.5e-40), derived_loan_product_type (p_adj=3.2e-05), preapproval (p_adj=6.5e-05), loan_type (p_adj=0.014), loan_amount (p_adj=4.7e-41), loan_term (p_adj=7.7e-24), property_value (p_adj=4.2e-63), construction_method (p_adj=2.4e-112), applicant_credit_score_type (p_adj=4.1e-56), submission_of_application (p_adj=1.1e-07), initially_payable_to_institution (p_adj=6.2e-09), aus-1 (p_adj=2.3e-160), tract_population (p_adj=0.0012), ffiec_msa_md_median_family_income (p_adj=9.6e-05), tract_to_msa_income_percentage (p_adj=2.8e-19), tract_owner_occupied_units (p_adj=5.4e-06)
- องค์ประกอบ race_eth: Hispanic 12.1% (ทั้งชุด 9.1%), NH Asian 3.1% (ทั้งชุด 6.8%), NH Black 31.5% (ทั้งชุด 22.0%), NH White 36.0% (ทั้งชุด 41.8%), Other 1.4% (ทั้งชุด 2.4%), Unknown 15.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.9% (ทั้งชุด 28.3%), Joint 26.5% (ทั้งชุด 30.0%), Male 35.0% (ทั้งชุด 35.3%), Unknown 3.5% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.6% (ทั้งชุด 29.9%), 35-44 27.3% (ทั้งชุด 27.0%), 45-54 16.9% (ทั้งชุด 17.5%), 55-64 11.4% (ทั้งชุด 11.8%), 65-74 5.5% (ทั้งชุด 5.2%), <25 9.0% (ทั้งชุด 7.2%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 29 · กลุ่ม 1
- IF debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 > 0.5 AND debt_to_income_ratio > 37.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND loan_type_3 ≤ 0.5 AND property_value ≤ 3.6e+05 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND loan_type_3 ≤ 0.5 AND property_value > 3.6e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 706/228/210 · coverage กฎบน validation 0.0560
- Fidelity F1 0.8009 · precision 0.8080 · recall 0.7939 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.0143 · ERM error 0.0143 · FPR 0.0000 · FNR 1.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=8.7e-22), derived_msa-md (p_adj=8e-12), county_code (p_adj=7e-35), derived_loan_product_type (p_adj=0.0033), loan_type (p_adj=0.026), loan_amount (p_adj=9e-16), loan_term (p_adj=9.4e-12), property_value (p_adj=3.9e-23), construction_method (p_adj=5.9e-74), income (p_adj=3.2e-72), debt_to_income_ratio (p_adj=7.8e-105), applicant_credit_score_type (p_adj=2.5e-14), initially_payable_to_institution (p_adj=4.4e-136), aus-1 (p_adj=2e-50), tract_population (p_adj=1.2e-05), ffiec_msa_md_median_family_income (p_adj=4.8e-05), tract_to_msa_income_percentage (p_adj=5.5e-15), tract_owner_occupied_units (p_adj=3.2e-06)
- องค์ประกอบ race_eth: Hispanic 6.7% (ทั้งชุด 9.1%), NH Asian 3.8% (ทั้งชุด 6.8%), NH Black 27.1% (ทั้งชุด 22.0%), NH White 38.6% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.4%), Unknown 21.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 46.2% (ทั้งชุด 28.3%), Joint 22.4% (ทั้งชุด 30.0%), Male 25.2% (ทั้งชุด 35.3%), Unknown 6.2% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.6% (ทั้งชุด 29.9%), 35-44 21.4% (ทั้งชุด 27.0%), 45-54 16.2% (ทั้งชุด 17.5%), 55-64 18.6% (ทั้งชุด 11.8%), 65-74 3.3% (ทั้งชุด 5.2%), <25 10.5% (ทั้งชุด 7.2%), >74 1.4% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 29 · กลุ่ม 2
- IF lei_549300FGXN1K3HLB1R50 ≤ 0.5 AND debt_to_income_ratio ≤ 60 AND preapproval_2 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 8243/2520/2610 · coverage กฎบน validation 0.8755
- Fidelity F1 0.8286 · precision 0.7125 · recall 0.9901 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9291 · ERM error 0.0709 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.1e-175), derived_msa-md (p_adj=3.2e-14), county_code (p_adj=7.8e-27), derived_loan_product_type (p_adj=2.8e-05), preapproval (p_adj=6.8e-68), loan_type (p_adj=6.7e-06), loan_amount (p_adj=1.2e-16), loan_term (p_adj=1.7e-32), property_value (p_adj=5.1e-08), construction_method (p_adj=5.9e-99), debt_to_income_ratio (p_adj=0.00025), applicant_credit_score_type (p_adj=7.5e-33), initially_payable_to_institution (p_adj=3e-29), aus-1 (p_adj=1.2e-94), tract_population (p_adj=2.2e-05), ffiec_msa_md_median_family_income (p_adj=6.8e-11), tract_to_msa_income_percentage (p_adj=2.9e-11), tract_owner_occupied_units (p_adj=0.00013)
- องค์ประกอบ race_eth: Hispanic 9.5% (ทั้งชุด 9.1%), NH Asian 7.7% (ทั้งชุด 6.8%), NH Black 20.4% (ทั้งชุด 22.0%), NH White 42.2% (ทั้งชุด 41.8%), Other 2.6% (ทั้งชุด 2.4%), Unknown 17.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 26.5% (ทั้งชุด 28.3%), Joint 31.0% (ทั้งชุด 30.0%), Male 35.9% (ทั้งชุด 35.3%), Unknown 6.6% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 30.8% (ทั้งชุด 29.9%), 35-44 27.4% (ทั้งชุด 27.0%), 45-54 17.6% (ทั้งชุด 17.5%), 55-64 11.0% (ทั้งชุด 11.8%), 65-74 5.1% (ทั้งชุด 5.2%), <25 6.8% (ทั้งชุด 7.2%), >74 1.2% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 29 · กลุ่ม 3
- IF preapproval_1 ≤ 0.5 AND lei_549300FGXN1K3HLB1R50 ≤ 0.5 AND lei_549300MGPZBLQDIL7538 > 0.5 THEN อยู่กลุ่มนี้
- IF preapproval_1 ≤ 0.5 AND lei_549300FGXN1K3HLB1R50 > 0.5 AND initially_payable_to_institution_3 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF preapproval_1 > 0.5 AND tract_to_msa_income_percentage ≤ 73.85 THEN อยู่กลุ่มนี้
- IF preapproval_1 > 0.5 AND tract_to_msa_income_percentage > 73.85 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1797/564/558 · coverage กฎบน validation 0.0968
- Fidelity F1 0.7361 · precision 0.9044 · recall 0.6206 · เงื่อนไขรวม 10 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9964 · ERM error 0.0036 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=8.2e-238), preapproval (p_adj=1.8e-226), construction_method (p_adj=5.1e-07), debt_to_income_ratio (p_adj=1.6e-06), applicant_credit_score_type (p_adj=6.3e-05), initially_payable_to_institution (p_adj=0.0019), aus-1 (p_adj=2.6e-13)
- องค์ประกอบ race_eth: Hispanic 5.0% (ทั้งชุด 9.1%), NH Asian 7.7% (ทั้งชุด 6.8%), NH Black 16.8% (ทั้งชุด 22.0%), NH White 47.1% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.4%), Unknown 21.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 22.6% (ทั้งชุด 28.3%), Joint 31.9% (ทั้งชุด 30.0%), Male 36.4% (ทั้งชุด 35.3%), Unknown 9.1% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 27.8% (ทั้งชุด 29.9%), 35-44 26.7% (ทั้งชุด 27.0%), 45-54 18.3% (ทั้งชุด 17.5%), 55-64 13.3% (ทั้งชุด 11.8%), 65-74 5.9% (ทั้งชุด 5.2%), <25 5.9% (ทั้งชุด 7.2%), >74 2.2% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k2 · c · seed 29 · กลุ่ม 0
- IF tract_owner_occupied_units ≤ 1254 AND property_value ≤ 4.9e+05 AND tract_owner_occupied_units ≤ 985.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units ≤ 1254 AND property_value ≤ 4.9e+05 AND tract_owner_occupied_units > 985.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units ≤ 1254 AND property_value > 4.9e+05 AND tract_owner_occupied_units ≤ 792 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value ≤ 2.6e+05 AND tract_population ≤ 5908 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 7140/2348/2330 · coverage กฎบน validation 0.6322
- Fidelity F1 0.9079 · precision 0.8754 · recall 0.9429 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.7837 · ERM error 0.1069 · FPR 0.3988 · FNR 0.0263
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.8e-15), derived_msa-md (p_adj=1.4e-64), county_code (p_adj=2.7e-115), conforming_loan_limit (p_adj=9.3e-27), derived_loan_product_type (p_adj=1.2e-17), loan_type (p_adj=3.1e-12), lien_status (p_adj=0.01), loan_amount (p_adj=2.7e-153), loan_term (p_adj=2.6e-22), property_value (p_adj=1.9e-128), construction_method (p_adj=3.4e-45), income (p_adj=1.1e-55), debt_to_income_ratio (p_adj=2e-14), applicant_credit_score_type (p_adj=6e-06), aus-1 (p_adj=2.5e-23), tract_population (p_adj=7.3e-265), ffiec_msa_md_median_family_income (p_adj=2.9e-68), tract_to_msa_income_percentage (p_adj=9.5e-167), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=1.9e-216), tract_median_age_of_housing_units (p_adj=1.5e-107)
- องค์ประกอบ race_eth: Hispanic 10.9% (ทั้งชุด 9.1%), NH Asian 4.2% (ทั้งชุด 6.8%), NH Black 24.8% (ทั้งชุด 22.0%), NH White 41.5% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.4%), Unknown 16.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 33.3% (ทั้งชุด 28.3%), Joint 25.8% (ทั้งชุด 30.0%), Male 35.2% (ทั้งชุด 35.3%), Unknown 5.8% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 31.4% (ทั้งชุด 29.9%), 35-44 24.4% (ทั้งชุด 27.0%), 45-54 16.7% (ทั้งชุด 17.5%), 55-64 10.9% (ทั้งชุด 11.8%), 65-74 5.4% (ทั้งชุด 5.2%), <25 9.5% (ทั้งชุด 7.2%), >74 1.7% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k2 · c · seed 29 · กลุ่ม 1
- IF tract_owner_occupied_units ≤ 1254 AND property_value > 4.6e+05 AND tract_owner_occupied_units > 809.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value ≤ 2.6e+05 AND tract_population > 5908 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.6e+05 AND tract_owner_occupied_units ≤ 1416 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.6e+05 AND tract_owner_occupied_units > 1416 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4860/1652/1670 · coverage กฎบน validation 0.3755
- Fidelity F1 0.8580 · precision 0.9008 · recall 0.8190 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9108 · ERM error 0.0659 · FPR 0.6846 · FNR 0.0053
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.8e-15), derived_msa-md (p_adj=1.4e-64), county_code (p_adj=2.7e-115), conforming_loan_limit (p_adj=9.3e-27), derived_loan_product_type (p_adj=1.2e-17), loan_type (p_adj=3.1e-12), lien_status (p_adj=0.01), loan_amount (p_adj=2.7e-153), loan_term (p_adj=2.6e-22), property_value (p_adj=1.9e-128), construction_method (p_adj=3.4e-45), income (p_adj=1.1e-55), debt_to_income_ratio (p_adj=2e-14), applicant_credit_score_type (p_adj=6e-06), aus-1 (p_adj=2.5e-23), tract_population (p_adj=7.3e-265), ffiec_msa_md_median_family_income (p_adj=2.9e-68), tract_to_msa_income_percentage (p_adj=9.5e-167), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=1.9e-216), tract_median_age_of_housing_units (p_adj=1.5e-107)
- องค์ประกอบ race_eth: Hispanic 6.5% (ทั้งชุด 9.1%), NH Asian 10.2% (ทั้งชุด 6.8%), NH Black 18.1% (ทั้งชุด 22.0%), NH White 42.0% (ทั้งชุด 41.8%), Other 2.8% (ทั้งชุด 2.4%), Unknown 20.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 21.4% (ทั้งชุด 28.3%), Joint 35.9% (ทั้งชุด 30.0%), Male 35.4% (ทั้งชุด 35.3%), Unknown 7.4% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.0% (ทั้งชุด 29.9%), 35-44 30.5% (ทั้งชุด 27.0%), 45-54 18.7% (ทั้งชุด 17.5%), 55-64 13.0% (ทั้งชุด 11.8%), 65-74 5.0% (ทั้งชุด 5.2%), <25 4.0% (ทั้งชุด 7.2%), >74 0.8% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · c · seed 29 · กลุ่ม 0
- IF loan_type_3 ≤ 0.5 AND ffiec_msa_md_median_family_income ≤ 9.58e+04 AND property_value > 2e+05 THEN อยู่กลุ่มนี้
- IF loan_type_3 > 0.5 AND derived_msa-md_12060 ≤ 0.5 AND tract_owner_occupied_units ≤ 626.5 THEN อยู่กลุ่มนี้
- IF loan_type_3 > 0.5 AND derived_msa-md_12060 ≤ 0.5 AND tract_owner_occupied_units > 626.5 THEN อยู่กลุ่มนี้
- IF loan_type_3 > 0.5 AND derived_msa-md_12060 > 0.5 AND tract_owner_occupied_units ≤ 868 THEN อยู่กลุ่มนี้
- IF loan_type_3 > 0.5 AND derived_msa-md_12060 > 0.5 AND tract_owner_occupied_units > 868 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2270/732/717 · coverage กฎบน validation 0.3295
- Fidelity F1 0.6712 · precision 0.5220 · recall 0.9399 · เงื่อนไขรวม 15 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9135 · ERM error 0.0725 · FPR 0.7742 · FNR 0.0061
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.2e-63), derived_msa-md (p_adj=6e-225), county_code (p_adj=7.4e-247), conforming_loan_limit (p_adj=0.029), derived_loan_product_type (p_adj=0), loan_type (p_adj=0), lien_status (p_adj=0.05), loan_term (p_adj=2.5e-60), property_value (p_adj=6.2e-11), construction_method (p_adj=1.1e-13), income (p_adj=2.8e-07), debt_to_income_ratio (p_adj=0.016), applicant_credit_score_type (p_adj=0.0041), submission_of_application (p_adj=0.00064), aus-1 (p_adj=2.6e-51), tract_population (p_adj=5.9e-36), ffiec_msa_md_median_family_income (p_adj=2.3e-142), tract_to_msa_income_percentage (p_adj=5.8e-29), tract_owner_occupied_units (p_adj=5.9e-33), tract_one_to_four_family_homes (p_adj=3.7e-53), tract_median_age_of_housing_units (p_adj=1.2e-17)
- องค์ประกอบ race_eth: Hispanic 6.6% (ทั้งชุด 9.1%), NH Asian 2.9% (ทั้งชุด 6.8%), NH Black 20.6% (ทั้งชุด 22.0%), NH White 47.0% (ทั้งชุด 41.8%), Other 2.6% (ทั้งชุด 2.4%), Unknown 20.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 20.6% (ทั้งชุด 28.3%), Joint 31.4% (ทั้งชุด 30.0%), Male 40.4% (ทั้งชุด 35.3%), Unknown 7.5% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.7% (ทั้งชุด 29.9%), 35-44 26.1% (ทั้งชุด 27.0%), 45-54 18.0% (ทั้งชุด 17.5%), 55-64 11.6% (ทั้งชุด 11.8%), 65-74 5.7% (ทั้งชุด 5.2%), <25 8.2% (ทั้งชุด 7.2%), >74 1.5% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · c · seed 29 · กลุ่ม 1
- IF loan_term ≤ 315.5 AND aus-1_6 ≤ 0.5 AND loan_amount ≤ 1.6e+05 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 315.5 AND aus-1_6 > 0.5 AND construction_method_2 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 315.5 AND aus-1_6 > 0.5 AND construction_method_2 > 0.5 THEN อยู่กลุ่มนี้
- IF loan_term > 315.5 AND loan_amount ≤ 1.3e+05 AND loan_type_1 > 0.5 THEN อยู่กลุ่มนี้
- IF loan_term > 315.5 AND loan_amount > 1.3e+05 AND initially_payable_to_institution_1111 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1839/631/607 · coverage กฎบน validation 0.1437
- Fidelity F1 0.8192 · precision 0.8591 · recall 0.7829 · เงื่อนไขรวม 15 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.5420 · ERM error 0.1680 · FPR 0.2050 · FNR 0.1368
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5e-267), derived_msa-md (p_adj=3.1e-166), county_code (p_adj=9.6e-213), derived_loan_product_type (p_adj=4.3e-131), loan_type (p_adj=6.3e-78), lien_status (p_adj=5.3e-67), loan_amount (p_adj=0), loan_term (p_adj=5e-67), property_value (p_adj=9.6e-237), construction_method (p_adj=0), income (p_adj=2.9e-48), applicant_credit_score_type (p_adj=2.5e-155), submission_of_application (p_adj=3.4e-43), initially_payable_to_institution (p_adj=3.2e-41), aus-1 (p_adj=0), tract_population (p_adj=1e-35), ffiec_msa_md_median_family_income (p_adj=7.7e-97), tract_to_msa_income_percentage (p_adj=1.1e-31), tract_owner_occupied_units (p_adj=3.3e-27), tract_one_to_four_family_homes (p_adj=0.012), tract_median_age_of_housing_units (p_adj=9.6e-06)
- องค์ประกอบ race_eth: Hispanic 8.4% (ทั้งชุด 9.1%), NH Asian 2.3% (ทั้งชุด 6.8%), NH Black 21.1% (ทั้งชุด 22.0%), NH White 51.6% (ทั้งชุด 41.8%), Other 1.6% (ทั้งชุด 2.4%), Unknown 15.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 39.4% (ทั้งชุด 28.3%), Joint 26.9% (ทั้งชุด 30.0%), Male 29.5% (ทั้งชุด 35.3%), Unknown 4.3% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 26.4% (ทั้งชุด 29.9%), 35-44 24.2% (ทั้งชุด 27.0%), 45-54 17.5% (ทั้งชุด 17.5%), 55-64 12.5% (ทั้งชุด 11.8%), 65-74 7.4% (ทั้งชุด 5.2%), <25 10.9% (ทั้งชุด 7.2%), >74 1.2% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · c · seed 29 · กลุ่ม 2
- IF ffiec_msa_md_median_family_income ≤ 7.915e+04 AND derived_loan_product_type_FHA:First Lien > 0.5 AND tract_median_age_of_housing_units > 27.5 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 7.915e+04 AND property_value ≤ 5.9e+05 AND loan_term > 344 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 6293/2097/2125 · coverage กฎบน validation 0.5893
- Fidelity F1 0.8639 · precision 0.8163 · recall 0.9175 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8706 · ERM error 0.0828 · FPR 0.6182 · FNR 0.0032
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.3e-60), derived_msa-md (p_adj=5e-194), county_code (p_adj=6.4e-190), conforming_loan_limit (p_adj=4.1e-23), derived_loan_product_type (p_adj=3e-189), loan_type (p_adj=2e-182), lien_status (p_adj=5.6e-10), loan_amount (p_adj=1.5e-10), loan_term (p_adj=8.7e-46), property_value (p_adj=1.2e-19), construction_method (p_adj=1.3e-59), income (p_adj=2.7e-29), debt_to_income_ratio (p_adj=1.9e-08), applicant_credit_score_type (p_adj=6.5e-31), submission_of_application (p_adj=6.2e-10), initially_payable_to_institution (p_adj=1.3e-10), aus-1 (p_adj=2.2e-143), tract_population (p_adj=0.027), ffiec_msa_md_median_family_income (p_adj=7.3e-202), tract_to_msa_income_percentage (p_adj=4.1e-83), tract_owner_occupied_units (p_adj=7.8e-22), tract_one_to_four_family_homes (p_adj=7.9e-28), tract_median_age_of_housing_units (p_adj=0.045)
- องค์ประกอบ race_eth: Hispanic 11.8% (ทั้งชุด 9.1%), NH Asian 6.3% (ทั้งชุด 6.8%), NH Black 25.9% (ทั้งชุด 22.0%), NH White 35.3% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.4%), Unknown 18.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 31.4% (ทั้งชุด 28.3%), Joint 26.9% (ทั้งชุด 30.0%), Male 34.8% (ทั้งชุด 35.3%), Unknown 6.9% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 32.3% (ทั้งชุด 29.9%), 35-44 25.7% (ทั้งชุด 27.0%), 45-54 16.6% (ทั้งชุด 17.5%), 55-64 11.2% (ทั้งชุด 11.8%), 65-74 5.2% (ทั้งชุด 5.2%), <25 7.6% (ทั้งชุด 7.2%), >74 1.5% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · c · seed 29 · กลุ่ม 3
- IF property_value ≤ 5.9e+05 AND property_value > 4.9e+05 AND tract_to_msa_income_percentage > 146.6 THEN อยู่กลุ่มนี้
- IF property_value > 5.9e+05 AND income ≤ 157.5 AND tract_to_msa_income_percentage > 133 THEN อยู่กลุ่มนี้
- IF property_value > 5.9e+05 AND income > 157.5 AND derived_loan_product_type_Conventional:First Lien > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1598/540/551 · coverage กฎบน validation 0.1300
- Fidelity F1 0.7849 · precision 0.8000 · recall 0.7704 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9310 · ERM error 0.0526 · FPR 0.7368 · FNR 0.0019
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=9.5e-26), derived_msa-md (p_adj=3.5e-30), county_code (p_adj=3.3e-105), conforming_loan_limit (p_adj=4.3e-132), derived_loan_product_type (p_adj=2.7e-71), loan_type (p_adj=8.2e-67), loan_amount (p_adj=8.9e-101), property_value (p_adj=4.2e-88), construction_method (p_adj=3.8e-14), income (p_adj=6.3e-47), debt_to_income_ratio (p_adj=2.6e-39), aus-1 (p_adj=2.8e-30), ffiec_msa_md_median_family_income (p_adj=7.2e-70), tract_to_msa_income_percentage (p_adj=4.4e-103), tract_owner_occupied_units (p_adj=3.5e-21)
- องค์ประกอบ race_eth: Hispanic 2.9% (ทั้งชุด 9.1%), NH Asian 18.3% (ทั้งชุด 6.8%), NH Black 9.4% (ทั้งชุด 22.0%), NH White 48.8% (ทั้งชุด 41.8%), Other 3.6% (ทั้งชุด 2.4%), Unknown 16.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 14.2% (ทั้งชุด 28.3%), Joint 43.7% (ทั้งชุด 30.0%), Male 36.7% (ทั้งชุด 35.3%), Unknown 5.4% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 26.5% (ทั้งชุด 29.9%), 35-44 35.9% (ทั้งชุด 27.0%), 45-54 20.7% (ทั้งชุด 17.5%), 55-64 13.4% (ทั้งชุด 11.8%), 65-74 2.2% (ทั้งชุด 5.2%), <25 0.5% (ทั้งชุด 7.2%), >74 0.7% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · c · seed 29 · กลุ่ม 0
- IF lei_549300FGXN1K3HLB1R50 ≤ 0.5 AND preapproval_2 > 0.5 AND lei_549300MGPZBLQDIL7538 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 9439/3181/3189 · coverage กฎบน validation 0.8970
- Fidelity F1 0.9295 · precision 0.8768 · recall 0.9890 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.7984 · ERM error 0.1094 · FPR 0.4557 · FNR 0.0220
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.1e-197), derived_msa-md (p_adj=1.6e-06), county_code (p_adj=5e-10), derived_loan_product_type (p_adj=0.046), preapproval (p_adj=7.3e-144), property_value (p_adj=2.2e-05), construction_method (p_adj=3.5e-13), debt_to_income_ratio (p_adj=5.9e-15), applicant_credit_score_type (p_adj=3.4e-10), submission_of_application (p_adj=0.011), initially_payable_to_institution (p_adj=0.00036), aus-1 (p_adj=4.8e-26), tract_to_msa_income_percentage (p_adj=0.037)
- องค์ประกอบ race_eth: Hispanic 9.9% (ทั้งชุด 9.1%), NH Asian 6.8% (ทั้งชุด 6.8%), NH Black 23.5% (ทั้งชุด 22.0%), NH White 39.9% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.4%), Unknown 17.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 29.6% (ทั้งชุด 28.3%), Joint 29.0% (ทั้งชุด 30.0%), Male 35.6% (ทั้งชุด 35.3%), Unknown 5.8% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 30.6% (ทั้งชุด 29.9%), 35-44 27.1% (ทั้งชุด 27.0%), 45-54 17.3% (ทั้งชุด 17.5%), 55-64 11.3% (ทั้งชุด 11.8%), 65-74 5.0% (ทั้งชุด 5.2%), <25 7.5% (ทั้งชุด 7.2%), >74 1.2% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · c · seed 29 · กลุ่ม 1
- IF lei_549300FGXN1K3HLB1R50 ≤ 0.5 AND preapproval_2 ≤ 0.5 AND tract_one_to_four_family_homes ≤ 1268 THEN อยู่กลุ่มนี้
- IF lei_549300FGXN1K3HLB1R50 ≤ 0.5 AND preapproval_2 ≤ 0.5 AND tract_one_to_four_family_homes > 1268 THEN อยู่กลุ่มนี้
- IF lei_549300FGXN1K3HLB1R50 ≤ 0.5 AND preapproval_2 > 0.5 AND lei_549300MGPZBLQDIL7538 > 0.5 THEN อยู่กลุ่มนี้
- IF lei_549300FGXN1K3HLB1R50 > 0.5 AND debt_to_income_ratio ≤ 52 AND property_value ≤ 2.4e+05 THEN อยู่กลุ่มนี้
- IF lei_549300FGXN1K3HLB1R50 > 0.5 AND debt_to_income_ratio ≤ 52 AND property_value > 2.4e+05 THEN อยู่กลุ่มนี้
- IF lei_549300FGXN1K3HLB1R50 > 0.5 AND debt_to_income_ratio > 52 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2561/819/811 · coverage กฎบน validation 0.1030
- Fidelity F1 0.6125 · precision 0.9150 · recall 0.4603 · เงื่อนไขรวม 17 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9877 · ERM error 0.0123 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.1e-197), derived_msa-md (p_adj=1.6e-06), county_code (p_adj=5e-10), derived_loan_product_type (p_adj=0.046), preapproval (p_adj=7.3e-144), property_value (p_adj=2.2e-05), construction_method (p_adj=3.5e-13), debt_to_income_ratio (p_adj=5.9e-15), applicant_credit_score_type (p_adj=3.4e-10), submission_of_application (p_adj=0.011), initially_payable_to_institution (p_adj=0.00036), aus-1 (p_adj=4.8e-26), tract_to_msa_income_percentage (p_adj=0.037)
- องค์ประกอบ race_eth: Hispanic 5.9% (ทั้งชุด 9.1%), NH Asian 6.7% (ทั้งชุด 6.8%), NH Black 16.2% (ทั้งชุด 22.0%), NH White 48.8% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.4%), Unknown 20.1% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 23.1% (ทั้งชุด 28.3%), Joint 34.0% (ทั้งชุด 30.0%), Male 33.9% (ทั้งชุด 35.3%), Unknown 9.0% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 27.3% (ทั้งชุด 29.9%), 35-44 26.3% (ทั้งชุด 27.0%), 45-54 18.4% (ทั้งชุด 17.5%), 55-64 13.7% (ทั้งชุด 11.8%), 65-74 6.2% (ทั้งชุด 5.2%), <25 6.3% (ทั้งชุด 7.2%), >74 2.0% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 29 · กลุ่ม 0
- IF loan_term ≤ 315.5 AND construction_method_2 > 0.5 AND loan_term > 203.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 902/304/282 · coverage กฎบน validation 0.0770
- Fidelity F1 0.9444 · precision 0.9383 · recall 0.9507 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.2163 · ERM error 0.1773 · FPR 0.0950 · FNR 0.4754
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0), derived_msa-md (p_adj=3.9e-80), county_code (p_adj=2.1e-181), derived_loan_product_type (p_adj=4.2e-34), loan_type (p_adj=2.7e-32), loan_amount (p_adj=5.8e-248), loan_term (p_adj=2e-146), property_value (p_adj=1.8e-280), construction_method (p_adj=0), income (p_adj=3.2e-78), debt_to_income_ratio (p_adj=0.0081), applicant_credit_score_type (p_adj=1.1e-185), initially_payable_to_institution (p_adj=0.04), aus-1 (p_adj=1.3e-307), tract_population (p_adj=1.8e-36), ffiec_msa_md_median_family_income (p_adj=2.2e-41), tract_to_msa_income_percentage (p_adj=1.3e-25), tract_owner_occupied_units (p_adj=2.9e-31), tract_one_to_four_family_homes (p_adj=2.7e-11)
- องค์ประกอบ race_eth: Hispanic 6.7% (ทั้งชุด 9.1%), NH Asian 0.4% (ทั้งชุด 6.8%), NH Black 28.7% (ทั้งชุด 22.0%), NH White 45.7% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.4%), Unknown 16.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 48.2% (ทั้งชุด 28.3%), Joint 28.0% (ทั้งชุด 30.0%), Male 22.0% (ทั้งชุด 35.3%), Unknown 1.8% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 27.0% (ทั้งชุด 29.9%), 35-44 24.8% (ทั้งชุด 27.0%), 45-54 17.7% (ทั้งชุด 17.5%), 55-64 13.8% (ทั้งชุด 11.8%), 65-74 5.3% (ทั้งชุด 5.2%), <25 10.6% (ทั้งชุด 7.2%), >74 0.7% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 29 · กลุ่ม 1
- IF loan_term ≤ 202 AND property_value ≤ 5.5e+05 AND tract_owner_occupied_units ≤ 1570 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 283/99/93 · coverage กฎบน validation 0.0225
- Fidelity F1 0.8783 · precision 0.9222 · recall 0.8384 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8065 · ERM error 0.1720 · FPR 0.8333 · FNR 0.0133
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=8.7e-06), derived_loan_product_type (p_adj=5.7e-196), loan_type (p_adj=3.7e-07), lien_status (p_adj=2.8e-197), loan_amount (p_adj=1.4e-25), loan_term (p_adj=1.7e-54), aus-1 (p_adj=2e-11), tract_owner_occupied_units (p_adj=0.0039)
- องค์ประกอบ race_eth: Hispanic 11.8% (ทั้งชุด 9.1%), NH Asian 12.9% (ทั้งชุด 6.8%), NH Black 17.2% (ทั้งชุด 22.0%), NH White 41.9% (ทั้งชุด 41.8%), Other 2.2% (ทั้งชุด 2.4%), Unknown 14.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 30.1% (ทั้งชุด 28.3%), Joint 23.7% (ทั้งชุด 30.0%), Male 39.8% (ทั้งชุด 35.3%), Unknown 6.5% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 32.3% (ทั้งชุด 29.9%), 35-44 22.6% (ทั้งชุด 27.0%), 45-54 17.2% (ทั้งชุด 17.5%), 55-64 9.7% (ทั้งชุด 11.8%), 65-74 14.0% (ทั้งชุด 5.2%), <25 3.2% (ทั้งชุด 7.2%), >74 1.1% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 29 · กลุ่ม 2
- IF tract_owner_occupied_units ≤ 1254 AND loan_term > 315.5 AND property_value ≤ 4.9e+05 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value ≤ 2.6e+05 AND tract_population ≤ 5598 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 5955/1945/1955 · coverage กฎบน validation 0.5008
- Fidelity F1 0.8723 · precision 0.8597 · recall 0.8853 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8645 · ERM error 0.0936 · FPR 0.6226 · FNR 0.0107
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.7e-17), derived_msa-md (p_adj=5.3e-07), county_code (p_adj=1.2e-62), conforming_loan_limit (p_adj=1.7e-17), derived_loan_product_type (p_adj=1.7e-51), loan_type (p_adj=8.3e-52), loan_amount (p_adj=4.3e-62), loan_term (p_adj=1.2e-68), property_value (p_adj=2.8e-72), construction_method (p_adj=4.1e-23), income (p_adj=1.7e-39), debt_to_income_ratio (p_adj=1.8e-07), applicant_credit_score_type (p_adj=2.6e-13), aus-1 (p_adj=7.8e-59), tract_population (p_adj=4.7e-156), ffiec_msa_md_median_family_income (p_adj=5.4e-08), tract_to_msa_income_percentage (p_adj=1.3e-93), tract_owner_occupied_units (p_adj=1e-283), tract_one_to_four_family_homes (p_adj=2.7e-153), tract_median_age_of_housing_units (p_adj=5.8e-86)
- องค์ประกอบ race_eth: Hispanic 11.5% (ทั้งชุด 9.1%), NH Asian 4.4% (ทั้งชุด 6.8%), NH Black 24.6% (ทั้งชุด 22.0%), NH White 40.9% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.4%), Unknown 16.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 31.3% (ทั้งชุด 28.3%), Joint 25.6% (ทั้งชุด 30.0%), Male 36.9% (ทั้งชุด 35.3%), Unknown 6.3% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 32.0% (ทั้งชุด 29.9%), 35-44 24.5% (ทั้งชุด 27.0%), 45-54 16.5% (ทั้งชุด 17.5%), 55-64 10.5% (ทั้งชุด 11.8%), 65-74 5.0% (ทั้งชุด 5.2%), <25 9.7% (ทั้งชุด 7.2%), >74 1.9% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 29 · กลุ่ม 3
- IF tract_owner_occupied_units ≤ 1254 AND property_value > 4.6e+05 AND tract_owner_occupied_units > 809.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value ≤ 2.6e+05 AND tract_population > 5908 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.6e+05 AND tract_owner_occupied_units ≤ 1416 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.6e+05 AND tract_owner_occupied_units > 1416 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4860/1652/1670 · coverage กฎบน validation 0.3755
- Fidelity F1 0.8580 · precision 0.9008 · recall 0.8190 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9108 · ERM error 0.0659 · FPR 0.6846 · FNR 0.0053
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.8e-15), derived_msa-md (p_adj=1.4e-64), county_code (p_adj=2.7e-115), conforming_loan_limit (p_adj=9.3e-27), derived_loan_product_type (p_adj=1.2e-17), loan_type (p_adj=3.1e-12), lien_status (p_adj=0.01), loan_amount (p_adj=2.7e-153), loan_term (p_adj=2.6e-22), property_value (p_adj=1.9e-128), construction_method (p_adj=3.4e-45), income (p_adj=1.1e-55), debt_to_income_ratio (p_adj=2e-14), applicant_credit_score_type (p_adj=6e-06), aus-1 (p_adj=2.5e-23), tract_population (p_adj=7.3e-265), ffiec_msa_md_median_family_income (p_adj=2.9e-68), tract_to_msa_income_percentage (p_adj=9.5e-167), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=1.9e-216), tract_median_age_of_housing_units (p_adj=1.5e-107)
- องค์ประกอบ race_eth: Hispanic 6.5% (ทั้งชุด 9.1%), NH Asian 10.2% (ทั้งชุด 6.8%), NH Black 18.1% (ทั้งชุด 22.0%), NH White 42.0% (ทั้งชุด 41.8%), Other 2.8% (ทั้งชุด 2.4%), Unknown 20.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 21.4% (ทั้งชุด 28.3%), Joint 35.9% (ทั้งชุด 30.0%), Male 35.4% (ทั้งชุด 35.3%), Unknown 7.4% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.0% (ทั้งชุด 29.9%), 35-44 30.5% (ทั้งชุด 27.0%), 45-54 18.7% (ทั้งชุด 17.5%), 55-64 13.0% (ทั้งชุด 11.8%), 65-74 5.0% (ทั้งชุด 5.2%), <25 4.0% (ทั้งชุด 7.2%), >74 0.8% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 29 · กลุ่ม 0
- IF loan_term ≤ 315.5 AND construction_method_2 > 0.5 AND loan_term > 203.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 902/304/282 · coverage กฎบน validation 0.0770
- Fidelity F1 0.9444 · precision 0.9383 · recall 0.9507 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.2163 · ERM error 0.1773 · FPR 0.0950 · FNR 0.4754
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0), derived_msa-md (p_adj=3.9e-80), county_code (p_adj=2.1e-181), derived_loan_product_type (p_adj=4.2e-34), loan_type (p_adj=2.7e-32), loan_amount (p_adj=5.8e-248), loan_term (p_adj=2e-146), property_value (p_adj=1.8e-280), construction_method (p_adj=0), income (p_adj=3.2e-78), debt_to_income_ratio (p_adj=0.0081), applicant_credit_score_type (p_adj=1.1e-185), initially_payable_to_institution (p_adj=0.04), aus-1 (p_adj=1.3e-307), tract_population (p_adj=1.8e-36), ffiec_msa_md_median_family_income (p_adj=2.2e-41), tract_to_msa_income_percentage (p_adj=1.3e-25), tract_owner_occupied_units (p_adj=2.9e-31), tract_one_to_four_family_homes (p_adj=2.7e-11)
- องค์ประกอบ race_eth: Hispanic 6.7% (ทั้งชุด 9.1%), NH Asian 0.4% (ทั้งชุด 6.8%), NH Black 28.7% (ทั้งชุด 22.0%), NH White 45.7% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.4%), Unknown 16.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 48.2% (ทั้งชุด 28.3%), Joint 28.0% (ทั้งชุด 30.0%), Male 22.0% (ทั้งชุด 35.3%), Unknown 1.8% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 27.0% (ทั้งชุด 29.9%), 35-44 24.8% (ทั้งชุด 27.0%), 45-54 17.7% (ทั้งชุด 17.5%), 55-64 13.8% (ทั้งชุด 11.8%), 65-74 5.3% (ทั้งชุด 5.2%), <25 10.6% (ทั้งชุด 7.2%), >74 0.7% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 29 · กลุ่ม 1
- IF loan_term ≤ 202 AND property_value ≤ 5.5e+05 AND tract_owner_occupied_units ≤ 1570 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 283/99/93 · coverage กฎบน validation 0.0225
- Fidelity F1 0.8783 · precision 0.9222 · recall 0.8384 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8065 · ERM error 0.1720 · FPR 0.8333 · FNR 0.0133
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=8.7e-06), derived_loan_product_type (p_adj=5.7e-196), loan_type (p_adj=3.7e-07), lien_status (p_adj=2.8e-197), loan_amount (p_adj=1.4e-25), loan_term (p_adj=1.7e-54), aus-1 (p_adj=2e-11), tract_owner_occupied_units (p_adj=0.0039)
- องค์ประกอบ race_eth: Hispanic 11.8% (ทั้งชุด 9.1%), NH Asian 12.9% (ทั้งชุด 6.8%), NH Black 17.2% (ทั้งชุด 22.0%), NH White 41.9% (ทั้งชุด 41.8%), Other 2.2% (ทั้งชุด 2.4%), Unknown 14.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 30.1% (ทั้งชุด 28.3%), Joint 23.7% (ทั้งชุด 30.0%), Male 39.8% (ทั้งชุด 35.3%), Unknown 6.5% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 32.3% (ทั้งชุด 29.9%), 35-44 22.6% (ทั้งชุด 27.0%), 45-54 17.2% (ทั้งชุด 17.5%), 55-64 9.7% (ทั้งชุด 11.8%), 65-74 14.0% (ทั้งชุด 5.2%), <25 3.2% (ทั้งชุด 7.2%), >74 1.1% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 29 · กลุ่ม 2
- IF tract_owner_occupied_units ≤ 1254 AND loan_term > 315.5 AND property_value ≤ 4.9e+05 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value ≤ 2.6e+05 AND tract_population ≤ 5598 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 5955/1945/1955 · coverage กฎบน validation 0.5008
- Fidelity F1 0.8723 · precision 0.8597 · recall 0.8853 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8645 · ERM error 0.0936 · FPR 0.6226 · FNR 0.0107
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.7e-17), derived_msa-md (p_adj=5.3e-07), county_code (p_adj=1.2e-62), conforming_loan_limit (p_adj=1.7e-17), derived_loan_product_type (p_adj=1.7e-51), loan_type (p_adj=8.3e-52), loan_amount (p_adj=4.3e-62), loan_term (p_adj=1.2e-68), property_value (p_adj=2.8e-72), construction_method (p_adj=4.1e-23), income (p_adj=1.7e-39), debt_to_income_ratio (p_adj=1.8e-07), applicant_credit_score_type (p_adj=2.6e-13), aus-1 (p_adj=7.8e-59), tract_population (p_adj=4.7e-156), ffiec_msa_md_median_family_income (p_adj=5.4e-08), tract_to_msa_income_percentage (p_adj=1.3e-93), tract_owner_occupied_units (p_adj=1e-283), tract_one_to_four_family_homes (p_adj=2.7e-153), tract_median_age_of_housing_units (p_adj=5.8e-86)
- องค์ประกอบ race_eth: Hispanic 11.5% (ทั้งชุด 9.1%), NH Asian 4.4% (ทั้งชุด 6.8%), NH Black 24.6% (ทั้งชุด 22.0%), NH White 40.9% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.4%), Unknown 16.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 31.3% (ทั้งชุด 28.3%), Joint 25.6% (ทั้งชุด 30.0%), Male 36.9% (ทั้งชุด 35.3%), Unknown 6.3% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 32.0% (ทั้งชุด 29.9%), 35-44 24.5% (ทั้งชุด 27.0%), 45-54 16.5% (ทั้งชุด 17.5%), 55-64 10.5% (ทั้งชุด 11.8%), 65-74 5.0% (ทั้งชุด 5.2%), <25 9.7% (ทั้งชุด 7.2%), >74 1.9% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 29 · กลุ่ม 3
- IF tract_owner_occupied_units ≤ 1254 AND property_value > 4.6e+05 AND tract_owner_occupied_units > 809.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value ≤ 2.6e+05 AND tract_population > 5908 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.6e+05 AND tract_owner_occupied_units ≤ 1416 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.6e+05 AND tract_owner_occupied_units > 1416 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4860/1652/1670 · coverage กฎบน validation 0.3755
- Fidelity F1 0.8580 · precision 0.9008 · recall 0.8190 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9108 · ERM error 0.0659 · FPR 0.6846 · FNR 0.0053
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.8e-15), derived_msa-md (p_adj=1.4e-64), county_code (p_adj=2.7e-115), conforming_loan_limit (p_adj=9.3e-27), derived_loan_product_type (p_adj=1.2e-17), loan_type (p_adj=3.1e-12), lien_status (p_adj=0.01), loan_amount (p_adj=2.7e-153), loan_term (p_adj=2.6e-22), property_value (p_adj=1.9e-128), construction_method (p_adj=3.4e-45), income (p_adj=1.1e-55), debt_to_income_ratio (p_adj=2e-14), applicant_credit_score_type (p_adj=6e-06), aus-1 (p_adj=2.5e-23), tract_population (p_adj=7.3e-265), ffiec_msa_md_median_family_income (p_adj=2.9e-68), tract_to_msa_income_percentage (p_adj=9.5e-167), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=1.9e-216), tract_median_age_of_housing_units (p_adj=1.5e-107)
- องค์ประกอบ race_eth: Hispanic 6.5% (ทั้งชุด 9.1%), NH Asian 10.2% (ทั้งชุด 6.8%), NH Black 18.1% (ทั้งชุด 22.0%), NH White 42.0% (ทั้งชุด 41.8%), Other 2.8% (ทั้งชุด 2.4%), Unknown 20.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 21.4% (ทั้งชุด 28.3%), Joint 35.9% (ทั้งชุด 30.0%), Male 35.4% (ทั้งชุด 35.3%), Unknown 7.4% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.0% (ทั้งชุด 29.9%), 35-44 30.5% (ทั้งชุด 27.0%), 45-54 18.7% (ทั้งชุด 17.5%), 55-64 13.0% (ทั้งชุด 11.8%), 65-74 5.0% (ทั้งชุด 5.2%), <25 4.0% (ทั้งชุด 7.2%), >74 0.8% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 43 · กลุ่ม 0
- IF construction_method_1 ≤ 0.5 AND aus-1_6 > 0.5 AND tract_one_to_four_family_homes > 207.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 703/373/347 · coverage กฎบน validation 0.0767
- Fidelity F1 0.8471 · precision 0.9381 · recall 0.7721 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.3948 · ERM error 0.2046 · FPR 0.1667 · FNR 0.2628
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=6.3e-272), derived_msa-md (p_adj=8.9e-48), county_code (p_adj=1.8e-125), derived_loan_product_type (p_adj=3e-57), loan_type (p_adj=1.3e-40), lien_status (p_adj=1.2e-22), loan_amount (p_adj=1.6e-208), loan_term (p_adj=1.6e-75), property_value (p_adj=5.2e-146), construction_method (p_adj=0), income (p_adj=1.5e-39), applicant_credit_score_type (p_adj=1.2e-177), initially_payable_to_institution (p_adj=0.011), aus-1 (p_adj=0), tract_population (p_adj=1.8e-18), ffiec_msa_md_median_family_income (p_adj=9e-28), tract_to_msa_income_percentage (p_adj=3.3e-16), tract_owner_occupied_units (p_adj=6.2e-17), tract_median_age_of_housing_units (p_adj=3.2e-14)
- องค์ประกอบ race_eth: Hispanic 7.2% (ทั้งชุด 9.1%), NH Asian 2.3% (ทั้งชุด 6.8%), NH Black 23.3% (ทั้งชุด 22.0%), NH White 46.4% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.4%), Unknown 19.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 38.3% (ทั้งชุด 29.8%), Joint 31.1% (ทั้งชุด 30.6%), Male 27.1% (ทั้งชุด 33.0%), Unknown 3.5% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 32.6% (ทั้งชุด 30.9%), 35-44 24.8% (ทั้งชุด 26.5%), 45-54 15.6% (ทั้งชุด 17.8%), 55-64 10.4% (ทั้งชุด 11.2%), 65-74 4.6% (ทั้งชุด 5.2%), <25 9.5% (ทั้งชุด 6.8%), >74 2.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 43 · กลุ่ม 1
- IF tract_one_to_four_family_homes ≤ 58 AND property_value ≤ 3.45e+05 AND construction_method_1 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF tract_one_to_four_family_homes ≤ 58 AND property_value ≤ 3.45e+05 AND construction_method_1 > 0.5 THEN อยู่กลุ่มนี้
- IF tract_one_to_four_family_homes ≤ 58 AND property_value > 3.45e+05 AND applicant_credit_score_type_1 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF tract_one_to_four_family_homes ≤ 58 AND property_value > 3.45e+05 AND applicant_credit_score_type_1 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 164/50/52 · coverage กฎบน validation 0.0130
- Fidelity F1 0.9804 · precision 0.9615 · recall 1.0000 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.1538 · ERM error 0.0577 · FPR 0.0000 · FNR 0.3750
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.7e-70), derived_msa-md (p_adj=3.4e-06), county_code (p_adj=3.5e-132), loan_amount (p_adj=8.7e-13), loan_term (p_adj=1.6e-08), property_value (p_adj=6.8e-14), construction_method (p_adj=9.5e-61), income (p_adj=5.9e-08), applicant_credit_score_type (p_adj=1.8e-08), aus-1 (p_adj=1.1e-36), tract_population (p_adj=9.6e-101), ffiec_msa_md_median_family_income (p_adj=0.0013), tract_to_msa_income_percentage (p_adj=3.2e-70), tract_owner_occupied_units (p_adj=5.8e-124), tract_one_to_four_family_homes (p_adj=1.4e-69), tract_median_age_of_housing_units (p_adj=6.6e-78)
- องค์ประกอบ race_eth: Hispanic 7.7% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 42.3% (ทั้งชุด 22.0%), NH White 40.4% (ทั้งชุด 41.8%), Other 3.8% (ทั้งชุด 2.4%), Unknown 5.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 46.2% (ทั้งชุด 29.8%), Joint 28.8% (ทั้งชุด 30.6%), Male 23.1% (ทั้งชุด 33.0%), Unknown 1.9% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 40.4% (ทั้งชุด 30.9%), 35-44 15.4% (ทั้งชุด 26.5%), 45-54 13.5% (ทั้งชุด 17.8%), 55-64 7.7% (ทั้งชุด 11.2%), 65-74 7.7% (ทั้งชุด 5.2%), <25 11.5% (ทั้งชุด 6.8%), >74 1.9% (ทั้งชุด 1.4%), Unknown 1.9% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 43 · กลุ่ม 2
- IF debt_to_income_ratio ≤ 52 AND initially_payable_to_institution_3 > 0.5 AND submission_of_application_1 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio ≤ 52 AND initially_payable_to_institution_3 > 0.5 AND submission_of_application_1 > 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 52 AND loan_term > 318.5 AND debt_to_income_ratio ≤ 60 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 52 AND loan_term > 318.5 AND debt_to_income_ratio > 60 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1089/696/611 · coverage กฎบน validation 0.1857
- Fidelity F1 0.5003 · precision 0.4845 · recall 0.5172 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8151 · ERM error 0.1015 · FPR 0.4602 · FNR 0.0201
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.00074), derived_msa-md (p_adj=2.8e-46), county_code (p_adj=3.3e-34), derived_loan_product_type (p_adj=1.3e-84), loan_type (p_adj=2.2e-87), loan_term (p_adj=9.8e-63), construction_method (p_adj=1.9e-06), income (p_adj=1.9e-13), debt_to_income_ratio (p_adj=2.3e-131), applicant_credit_score_type (p_adj=0.0046), aus-1 (p_adj=1.3e-52), tract_population (p_adj=5.2e-06), ffiec_msa_md_median_family_income (p_adj=2.7e-119), tract_to_msa_income_percentage (p_adj=0.00014), tract_median_age_of_housing_units (p_adj=0.00077)
- องค์ประกอบ race_eth: Hispanic 11.8% (ทั้งชุด 9.1%), NH Asian 4.4% (ทั้งชุด 6.8%), NH Black 35.0% (ทั้งชุด 22.0%), NH White 29.0% (ทั้งชุด 41.8%), Other 1.8% (ทั้งชุด 2.4%), Unknown 18.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.7% (ทั้งชุด 29.8%), Joint 26.2% (ทั้งชุด 30.6%), Male 32.7% (ทั้งชุด 33.0%), Unknown 6.4% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.9% (ทั้งชุด 30.9%), 35-44 25.7% (ทั้งชุด 26.5%), 45-54 22.4% (ทั้งชุด 17.8%), 55-64 10.1% (ทั้งชุด 11.2%), 65-74 3.8% (ทั้งชุด 5.2%), <25 5.7% (ทั้งชุด 6.8%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 43 · กลุ่ม 3
- IF total_units > 2.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4/0/1 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · precision 0.0000 · recall 0.0000 · เงื่อนไขรวม 1 · สูงสุดต่อเส้นทาง 1
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- **กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี**
- คำอธิบายสำรอง: ตัวแปรที่ต่างจากส่วนที่เหลือมากที่สุด คำนวณบน train เท่านั้น
  - total_units: SMD 7.681; ค่าเฉลี่ยกลุ่ม 3.75, ส่วนที่เหลือ 1.004
  - tract_owner_occupied_units: SMD -1.106; ค่าเฉลี่ยกลุ่ม 638.2, ส่วนที่เหลือ 1095
  - tract_to_msa_income_percentage: SMD -0.758; ค่าเฉลี่ยกลุ่ม 79.67, ส่วนที่เหลือ 108.4
  - derived_loan_product_type = FHA:First Lien: สัดส่วนต่าง +0.508; กลุ่ม 75.0%, ส่วนที่เหลือ 24.2%
  - loan_type = 2: สัดส่วนต่าง +0.508; กลุ่ม 75.0%, ส่วนที่เหลือ 24.2%
- อนุมัติจริง 1.0000 · ERM error 0.0000 · FPR N/A · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: ไม่พบ
- องค์ประกอบ race_eth: Hispanic 0.0% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 0.0% (ทั้งชุด 22.0%), NH White 100.0% (ทั้งชุด 41.8%), Other 0.0% (ทั้งชุด 2.4%), Unknown 0.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 0.0% (ทั้งชุด 29.8%), Joint 0.0% (ทั้งชุด 30.6%), Male 100.0% (ทั้งชุด 33.0%), Unknown 0.0% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 0.0% (ทั้งชุด 30.9%), 35-44 0.0% (ทั้งชุด 26.5%), 45-54 0.0% (ทั้งชุด 17.8%), 55-64 0.0% (ทั้งชุด 11.2%), 65-74 0.0% (ทั้งชุด 5.2%), <25 100.0% (ทั้งชุด 6.8%), >74 0.0% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 43 · กลุ่ม 4
- IF tract_owner_occupied_units ≤ 1413 AND tract_population > 5394 AND tract_owner_occupied_units > 1060 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1413 AND derived_msa-md_99999 ≤ 0.5 AND property_value ≤ 9e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2684/792/843 · coverage กฎบน validation 0.2645
- Fidelity F1 0.8043 · precision 0.7032 · recall 0.9394 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9146 · ERM error 0.0617 · FPR 0.6806 · FNR 0.0039
- ตัวแปรต่างชัดหลัง Bonferroni: derived_msa-md (p_adj=6.1e-44), county_code (p_adj=2.2e-146), derived_loan_product_type (p_adj=1.1e-06), loan_type (p_adj=5e-06), loan_amount (p_adj=7.2e-13), loan_term (p_adj=6.6e-15), property_value (p_adj=1.3e-08), construction_method (p_adj=1.7e-14), debt_to_income_ratio (p_adj=0.005), aus-1 (p_adj=6e-18), tract_population (p_adj=1.1e-257), ffiec_msa_md_median_family_income (p_adj=1.8e-24), tract_to_msa_income_percentage (p_adj=1.9e-44), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=1.6e-263), tract_median_age_of_housing_units (p_adj=2e-121)
- องค์ประกอบ race_eth: Hispanic 6.5% (ทั้งชุด 9.1%), NH Asian 9.7% (ทั้งชุด 6.8%), NH Black 18.9% (ทั้งชุด 22.0%), NH White 43.9% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.4%), Unknown 18.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 24.2% (ทั้งชุด 29.8%), Joint 36.2% (ทั้งชุด 30.6%), Male 33.6% (ทั้งชุด 33.0%), Unknown 6.0% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 31.1% (ทั้งชุด 30.9%), 35-44 29.3% (ทั้งชุด 26.5%), 45-54 17.6% (ทั้งชุด 17.8%), 55-64 11.6% (ทั้งชุด 11.2%), 65-74 4.5% (ทั้งชุด 5.2%), <25 4.6% (ทั้งชุด 6.8%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 43 · กลุ่ม 5
- IF property_value ≤ 8.3e+05 AND tract_to_msa_income_percentage > 242.9 AND income > 156 THEN อยู่กลุ่มนี้
- IF property_value > 8.3e+05 AND income ≤ 222.5 AND tract_to_msa_income_percentage > 185.3 THEN อยู่กลุ่มนี้
- IF property_value > 8.3e+05 AND income > 222.5 AND tract_owner_occupied_units ≤ 1881 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 532/176/162 · coverage กฎบน validation 0.0348
- Fidelity F1 0.8000 · precision 0.9065 · recall 0.7159 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9259 · ERM error 0.0741 · FPR 0.7500 · FNR 0.0200
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.1e-30), derived_msa-md (p_adj=7.1e-05), county_code (p_adj=1.1e-11), conforming_loan_limit (p_adj=0), derived_loan_product_type (p_adj=5.3e-13), loan_type (p_adj=2.8e-13), loan_amount (p_adj=8.8e-37), loan_term (p_adj=3.3e-08), property_value (p_adj=2.2e-35), construction_method (p_adj=0.012), income (p_adj=1.2e-12), debt_to_income_ratio (p_adj=2.6e-17), aus-1 (p_adj=1.2e-21), ffiec_msa_md_median_family_income (p_adj=2.8e-16), tract_to_msa_income_percentage (p_adj=2.1e-30)
- องค์ประกอบ race_eth: Hispanic 1.9% (ทั้งชุด 9.1%), NH Asian 14.2% (ทั้งชุด 6.8%), NH Black 9.3% (ทั้งชุด 22.0%), NH White 50.6% (ทั้งชุด 41.8%), Other 4.3% (ทั้งชุด 2.4%), Unknown 19.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 13.6% (ทั้งชุด 29.8%), Joint 46.9% (ทั้งชุด 30.6%), Male 29.0% (ทั้งชุด 33.0%), Unknown 10.5% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 17.9% (ทั้งชุด 30.9%), 35-44 42.0% (ทั้งชุด 26.5%), 45-54 19.8% (ทั้งชุด 17.8%), 55-64 14.8% (ทั้งชุด 11.2%), 65-74 4.9% (ทั้งชุด 5.2%), <25 0.6% (ทั้งชุด 6.8%), >74 0.0% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 43 · กลุ่ม 6
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND aus-1_6 ≤ 0.5 AND tract_owner_occupied_units ≤ 1781 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2538/808/815 · coverage กฎบน validation 0.1963
- Fidelity F1 0.8826 · precision 0.8955 · recall 0.8700 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8773 · ERM error 0.0920 · FPR 0.6900 · FNR 0.0084
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=6e-25), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.0075), derived_loan_product_type (p_adj=6.6e-39), loan_type (p_adj=3e-41), loan_amount (p_adj=4.1e-76), loan_term (p_adj=3.1e-61), property_value (p_adj=7.5e-83), income (p_adj=1.2e-30), applicant_credit_score_type (p_adj=5e-06), initially_payable_to_institution (p_adj=0.01), aus-1 (p_adj=4.7e-24), tract_population (p_adj=1.4e-29), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=2.2e-32), tract_median_age_of_housing_units (p_adj=2.1e-26)
- องค์ประกอบ race_eth: Hispanic 8.2% (ทั้งชุด 9.1%), NH Asian 2.1% (ทั้งชุด 6.8%), NH Black 14.7% (ทั้งชุด 22.0%), NH White 55.1% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.4%), Unknown 17.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 27.0% (ทั้งชุด 29.8%), Joint 30.4% (ทั้งชุด 30.6%), Male 35.5% (ทั้งชุด 33.0%), Unknown 7.1% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.7% (ทั้งชุด 30.9%), 35-44 22.8% (ทั้งชุด 26.5%), 45-54 16.8% (ทั้งชุด 17.8%), 55-64 11.4% (ทั้งชุด 11.2%), 65-74 6.9% (ทั้งชุด 5.2%), <25 9.9% (ทั้งชุด 6.8%), >74 1.5% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · cy · seed 43 · กลุ่ม 7
- IF ffiec_msa_md_median_family_income > 9.11e+04 AND tract_owner_occupied_units ≤ 1298 AND property_value ≤ 8.6e+05 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 9.11e+04 AND tract_owner_occupied_units > 1298 AND tract_population ≤ 4576 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4286/1105/1169 · coverage กฎบน validation 0.4382
- Fidelity F1 0.7404 · precision 0.6035 · recall 0.9575 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9119 · ERM error 0.0642 · FPR 0.6505 · FNR 0.0075
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.6e-13), derived_msa-md (p_adj=1.2e-155), county_code (p_adj=8.5e-150), conforming_loan_limit (p_adj=0.00021), derived_loan_product_type (p_adj=1.3e-21), loan_type (p_adj=2.7e-23), loan_term (p_adj=4.1e-24), construction_method (p_adj=1.3e-32), debt_to_income_ratio (p_adj=7.6e-25), applicant_credit_score_type (p_adj=0.0094), aus-1 (p_adj=3.8e-29), tract_population (p_adj=8.4e-138), ffiec_msa_md_median_family_income (p_adj=0), tract_to_msa_income_percentage (p_adj=6.8e-24), tract_owner_occupied_units (p_adj=9.5e-223), tract_one_to_four_family_homes (p_adj=1.3e-262), tract_median_age_of_housing_units (p_adj=1.2e-15)
- องค์ประกอบ race_eth: Hispanic 11.8% (ทั้งชุด 9.1%), NH Asian 9.7% (ทั้งชุด 6.8%), NH Black 22.9% (ทั้งชุด 22.0%), NH White 35.0% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.4%), Unknown 18.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 32.1% (ทั้งชุด 29.8%), Joint 26.9% (ทั้งชุด 30.6%), Male 33.8% (ทั้งชุด 33.0%), Unknown 7.3% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 32.0% (ทั้งชุด 30.9%), 35-44 26.4% (ทั้งชุด 26.5%), 45-54 17.0% (ทั้งชุด 17.8%), 55-64 11.4% (ทั้งชุด 11.2%), 65-74 5.4% (ทั้งชุด 5.2%), <25 6.6% (ทั้งชุด 6.8%), >74 1.1% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 43 · กลุ่ม 0
- IF loan_type_2 ≤ 0.5 AND initially_payable_to_institution_3 > 0.5 AND property_value ≤ 2.9e+05 THEN อยู่กลุ่มนี้
- IF loan_type_2 > 0.5 AND debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF loan_type_2 > 0.5 AND debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 > 0.5 THEN อยู่กลุ่มนี้
- IF loan_type_2 > 0.5 AND debt_to_income_ratio > 60 AND tract_to_msa_income_percentage ≤ 64.31 THEN อยู่กลุ่มนี้
- IF loan_type_2 > 0.5 AND debt_to_income_ratio > 60 AND tract_to_msa_income_percentage > 64.31 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 422/338/343 · coverage กฎบน validation 0.2422
- Fidelity F1 0.5142 · precision 0.3467 · recall 0.9941 · เงื่อนไขรวม 15 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8251 · ERM error 0.0700 · FPR 0.3500 · FNR 0.0106
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.2e-28), derived_msa-md (p_adj=1.9e-07), county_code (p_adj=6.2e-21), derived_loan_product_type (p_adj=6.2e-256), loan_type (p_adj=1.2e-258), loan_amount (p_adj=7.6e-36), loan_term (p_adj=1.8e-19), property_value (p_adj=4.6e-80), income (p_adj=9.4e-69), debt_to_income_ratio (p_adj=3e-28), applicant_credit_score_type (p_adj=0.014), submission_of_application (p_adj=2.6e-44), initially_payable_to_institution (p_adj=9.8e-11), aus-1 (p_adj=1.5e-119), tract_population (p_adj=4.2e-05), tract_to_msa_income_percentage (p_adj=4.8e-26), tract_owner_occupied_units (p_adj=6.9e-16), tract_median_age_of_housing_units (p_adj=2.3e-09)
- องค์ประกอบ race_eth: Hispanic 11.1% (ทั้งชุด 9.1%), NH Asian 1.7% (ทั้งชุด 6.8%), NH Black 38.8% (ทั้งชุด 22.0%), NH White 31.5% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.4%), Unknown 15.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 43.1% (ทั้งชุด 29.8%), Joint 19.5% (ทั้งชุด 30.6%), Male 30.0% (ทั้งชุด 33.0%), Unknown 7.3% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.9% (ทั้งชุด 30.9%), 35-44 25.9% (ทั้งชุด 26.5%), 45-54 17.8% (ทั้งชุด 17.8%), 55-64 10.8% (ทั้งชุด 11.2%), 65-74 3.2% (ทั้งชุด 5.2%), <25 10.8% (ทั้งชุด 6.8%), >74 0.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 43 · กลุ่ม 1
- IF construction_method_1 ≤ 0.5 AND aus-1_6 > 0.5 AND tract_population > 1578 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 617/350/338 · coverage กฎบน validation 0.0752
- Fidelity F1 0.8909 · precision 0.9635 · recall 0.8286 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.3728 · ERM error 0.2337 · FPR 0.2075 · FNR 0.2778
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=7.1e-296), derived_msa-md (p_adj=1.8e-46), county_code (p_adj=7.7e-122), derived_loan_product_type (p_adj=5e-94), loan_type (p_adj=1e-40), lien_status (p_adj=2.4e-64), loan_amount (p_adj=1.1e-228), loan_term (p_adj=5.3e-55), property_value (p_adj=5e-214), construction_method (p_adj=0), income (p_adj=1.1e-63), applicant_credit_score_type (p_adj=4.3e-201), initially_payable_to_institution (p_adj=0.013), aus-1 (p_adj=0), tract_population (p_adj=1.2e-10), ffiec_msa_md_median_family_income (p_adj=2.2e-26), tract_to_msa_income_percentage (p_adj=5.3e-20), tract_owner_occupied_units (p_adj=8.2e-07), tract_median_age_of_housing_units (p_adj=6.2e-10)
- องค์ประกอบ race_eth: Hispanic 7.1% (ทั้งชุด 9.1%), NH Asian 0.6% (ทั้งชุด 6.8%), NH Black 24.6% (ทั้งชุด 22.0%), NH White 45.9% (ทั้งชุด 41.8%), Other 1.2% (ทั้งชุด 2.4%), Unknown 20.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 38.8% (ทั้งชุด 29.8%), Joint 30.8% (ทั้งชุด 30.6%), Male 26.9% (ทั้งชุด 33.0%), Unknown 3.6% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 35.2% (ทั้งชุด 30.9%), 35-44 26.0% (ทั้งชุด 26.5%), 45-54 13.9% (ทั้งชุด 17.8%), 55-64 10.1% (ทั้งชุด 11.2%), 65-74 3.8% (ทั้งชุด 5.2%), <25 8.9% (ทั้งชุด 6.8%), >74 2.1% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 43 · กลุ่ม 2
- IF loan_type_2 ≤ 0.5 AND debt_to_income_ratio ≤ 52 AND initially_payable_to_institution_3 > 0.5 THEN อยู่กลุ่มนี้
- IF loan_type_2 ≤ 0.5 AND debt_to_income_ratio > 52 AND construction_method_2 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 728/316/299 · coverage กฎบน validation 0.0865
- Fidelity F1 0.2024 · precision 0.1936 · recall 0.2120 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- **กลุ่มนี้อธิบายด้วยกฎลึก 3 ชั้นได้ไม่ดี**
- คำอธิบายสำรอง: ตัวแปรที่ต่างจากส่วนที่เหลือมากที่สุด คำนวณบน train เท่านั้น
  - debt_to_income_ratio: SMD 0.328; ค่าเฉลี่ยกลุ่ม 45.44, ส่วนที่เหลือ 41.1
  - loan_term: SMD 0.263; ค่าเฉลี่ยกลุ่ม 356.4, ส่วนที่เหลือ 347.3
  - derived_loan_product_type = FHA:First Lien: สัดส่วนต่าง -0.242; กลุ่ม 1.5%, ส่วนที่เหลือ 25.7%
  - loan_type = 2: สัดส่วนต่าง -0.242; กลุ่ม 1.5%, ส่วนที่เหลือ 25.7%
  - initially_payable_to_institution = 1: สัดส่วนต่าง -0.173; กลุ่ม 75.4%, ส่วนที่เหลือ 92.7%
- อนุมัติจริง 0.8863 · ERM error 0.0769 · FPR 0.6176 · FNR 0.0075
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0077), derived_msa-md (p_adj=4.4e-12), county_code (p_adj=2.9e-10), derived_loan_product_type (p_adj=1.3e-34), loan_type (p_adj=5.9e-36), loan_term (p_adj=7.8e-09), construction_method (p_adj=0.00017), income (p_adj=0.016), aus-1 (p_adj=9.9e-19), ffiec_msa_md_median_family_income (p_adj=2.7e-09)
- องค์ประกอบ race_eth: Hispanic 6.0% (ทั้งชุด 9.1%), NH Asian 6.4% (ทั้งชุด 6.8%), NH Black 20.7% (ทั้งชุด 22.0%), NH White 45.8% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.4%), Unknown 19.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 23.1% (ทั้งชุด 29.8%), Joint 35.1% (ทั้งชุด 30.6%), Male 33.8% (ทั้งชุด 33.0%), Unknown 8.0% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 27.8% (ทั้งชุด 30.9%), 35-44 22.1% (ทั้งชุด 26.5%), 45-54 18.4% (ทั้งชุด 17.8%), 55-64 17.7% (ทั้งชุด 11.2%), 65-74 6.0% (ทั้งชุด 5.2%), <25 5.7% (ทั้งชุด 6.8%), >74 2.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 43 · กลุ่ม 3
- IF tract_one_to_four_family_homes ≤ 16.5 AND property_value ≤ 3.45e+05 AND aus-1_6 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF tract_one_to_four_family_homes ≤ 16.5 AND property_value ≤ 3.45e+05 AND aus-1_6 > 0.5 THEN อยู่กลุ่มนี้
- IF tract_one_to_four_family_homes > 16.5 AND lei_549300XQVJ1XBNFA5536 > 0.5 AND tract_one_to_four_family_homes ≤ 671.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 193/66/66 · coverage กฎบน validation 0.0135
- Fidelity F1 0.9000 · precision 1.0000 · recall 0.8182 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.1061 · ERM error 0.0606 · FPR 0.0000 · FNR 0.5714
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.2e-122), derived_msa-md (p_adj=8.3e-16), county_code (p_adj=2.1e-154), derived_loan_product_type (p_adj=0.0064), loan_type (p_adj=0.00093), loan_amount (p_adj=7.9e-24), loan_term (p_adj=7e-14), property_value (p_adj=1.3e-31), construction_method (p_adj=1.4e-95), debt_to_income_ratio (p_adj=0.00052), applicant_credit_score_type (p_adj=1.4e-13), aus-1 (p_adj=1.8e-59), tract_population (p_adj=3.1e-41), ffiec_msa_md_median_family_income (p_adj=7e-07), tract_to_msa_income_percentage (p_adj=1.6e-22), tract_owner_occupied_units (p_adj=1.4e-43), tract_one_to_four_family_homes (p_adj=6.9e-36), tract_median_age_of_housing_units (p_adj=2.1e-11)
- องค์ประกอบ race_eth: Hispanic 9.1% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 42.4% (ทั้งชุด 22.0%), NH White 37.9% (ทั้งชุด 41.8%), Other 4.5% (ทั้งชุด 2.4%), Unknown 6.1% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 51.5% (ทั้งชุด 29.8%), Joint 28.8% (ทั้งชุด 30.6%), Male 16.7% (ทั้งชุด 33.0%), Unknown 3.0% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 40.9% (ทั้งชุด 30.9%), 35-44 15.2% (ทั้งชุด 26.5%), 45-54 13.6% (ทั้งชุด 17.8%), 55-64 7.6% (ทั้งชุด 11.2%), 65-74 7.6% (ทั้งชุด 5.2%), <25 12.1% (ทั้งชุด 6.8%), >74 1.5% (ทั้งชุด 1.4%), Unknown 1.5% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 43 · กลุ่ม 4
- IF ffiec_msa_md_median_family_income ≤ 9.58e+04 AND aus-1_1 ≤ 0.5 AND aus-1_2 > 0.5 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income ≤ 9.58e+04 AND aus-1_1 > 0.5 AND derived_loan_product_type_FHA:First Lien ≤ 0.5 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income ≤ 9.58e+04 AND aus-1_1 > 0.5 AND derived_loan_product_type_FHA:First Lien > 0.5 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 9.58e+04 AND loan_type_3 > 0.5 AND loan_amount ≤ 4.2e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3153/957/969 · coverage กฎบน validation 0.2675
- Fidelity F1 0.7667 · precision 0.7262 · recall 0.8119 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8885 · ERM error 0.0980 · FPR 0.7778 · FNR 0.0128
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.9e-71), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.014), derived_loan_product_type (p_adj=3.3e-193), loan_type (p_adj=1.2e-195), loan_amount (p_adj=2.1e-18), loan_term (p_adj=1.7e-22), property_value (p_adj=4.9e-27), construction_method (p_adj=2.7e-06), income (p_adj=3.8e-11), applicant_credit_score_type (p_adj=2.5e-09), submission_of_application (p_adj=4.9e-17), initially_payable_to_institution (p_adj=0.0038), aus-1 (p_adj=6.2e-66), tract_population (p_adj=0.001), ffiec_msa_md_median_family_income (p_adj=2.5e-265), tract_to_msa_income_percentage (p_adj=8.3e-16), tract_owner_occupied_units (p_adj=0.02), tract_one_to_four_family_homes (p_adj=1.1e-17), tract_median_age_of_housing_units (p_adj=0.00077)
- องค์ประกอบ race_eth: Hispanic 7.7% (ทั้งชุด 9.1%), NH Asian 3.4% (ทั้งชุด 6.8%), NH Black 16.2% (ทั้งชุด 22.0%), NH White 52.4% (ทั้งชุด 41.8%), Other 2.9% (ทั้งชุด 2.4%), Unknown 17.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 23.6% (ทั้งชุด 29.8%), Joint 31.1% (ทั้งชุด 30.6%), Male 38.5% (ทั้งชุด 33.0%), Unknown 6.8% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.2% (ทั้งชุด 30.9%), 35-44 23.6% (ทั้งชุด 26.5%), 45-54 16.4% (ทั้งชุด 17.8%), 55-64 12.3% (ทั้งชุด 11.2%), 65-74 7.9% (ทั้งชุด 5.2%), <25 7.8% (ทั้งชุด 6.8%), >74 1.7% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 43 · กลุ่ม 5
- IF loan_type_2 > 0.5 AND debt_to_income_ratio ≤ 60 AND ffiec_msa_md_median_family_income ≤ 9.58e+04 THEN อยู่กลุ่มนี้
- IF loan_type_2 > 0.5 AND debt_to_income_ratio ≤ 60 AND ffiec_msa_md_median_family_income > 9.58e+04 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2147/485/463 · coverage กฎบน validation 0.2323
- Fidelity F1 0.6775 · precision 0.5156 · recall 0.9876 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9006 · ERM error 0.0778 · FPR 0.6957 · FNR 0.0096
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.1e-12), derived_msa-md (p_adj=2.1e-22), county_code (p_adj=6.6e-12), derived_loan_product_type (p_adj=0), loan_type (p_adj=0), loan_term (p_adj=1.3e-61), property_value (p_adj=0.00013), construction_method (p_adj=2.4e-05), income (p_adj=1.8e-05), debt_to_income_ratio (p_adj=2.2e-32), applicant_credit_score_type (p_adj=0.00011), submission_of_application (p_adj=2.8e-12), initially_payable_to_institution (p_adj=0.0017), aus-1 (p_adj=9.9e-297), tract_population (p_adj=6.5e-08), ffiec_msa_md_median_family_income (p_adj=1.5e-52), tract_to_msa_income_percentage (p_adj=3.2e-06), tract_owner_occupied_units (p_adj=0.0015)
- องค์ประกอบ race_eth: Hispanic 12.1% (ทั้งชุด 9.1%), NH Asian 1.5% (ทั้งชุด 6.8%), NH Black 38.4% (ทั้งชุด 22.0%), NH White 26.3% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.4%), Unknown 19.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 37.4% (ทั้งชุด 29.8%), Joint 28.9% (ทั้งชุด 30.6%), Male 27.0% (ทั้งชุด 33.0%), Unknown 6.7% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.2% (ทั้งชุด 30.9%), 35-44 27.6% (ทั้งชุด 26.5%), 45-54 24.4% (ทั้งชุด 17.8%), 55-64 9.9% (ทั้งชุด 11.2%), 65-74 1.9% (ทั้งชุด 5.2%), <25 5.6% (ทั้งชุด 6.8%), >74 0.2% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 43 · กลุ่ม 6
- IF loan_type_1 > 0.5 AND ffiec_msa_md_median_family_income ≤ 9.58e+04 AND derived_msa-md_16860 > 0.5 THEN อยู่กลุ่มนี้
- IF loan_type_1 > 0.5 AND ffiec_msa_md_median_family_income > 9.58e+04 AND property_value ≤ 4.6e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2483/758/801 · coverage กฎบน validation 0.2512
- Fidelity F1 0.7283 · precision 0.6388 · recall 0.8470 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8864 · ERM error 0.0674 · FPR 0.5385 · FNR 0.0070
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.5e-30), derived_msa-md (p_adj=1e-106), county_code (p_adj=8.3e-81), conforming_loan_limit (p_adj=0.0027), derived_loan_product_type (p_adj=3.4e-113), loan_type (p_adj=2.4e-116), loan_amount (p_adj=7.6e-22), loan_term (p_adj=5e-08), property_value (p_adj=3.8e-11), construction_method (p_adj=3.4e-22), income (p_adj=1.8e-24), debt_to_income_ratio (p_adj=0.0054), applicant_credit_score_type (p_adj=9.1e-06), submission_of_application (p_adj=5.4e-22), initially_payable_to_institution (p_adj=6.1e-11), aus-1 (p_adj=1.9e-101), ffiec_msa_md_median_family_income (p_adj=2.7e-295), tract_to_msa_income_percentage (p_adj=4.7e-41), tract_median_age_of_housing_units (p_adj=2.4e-13)
- องค์ประกอบ race_eth: Hispanic 13.9% (ทั้งชุด 9.1%), NH Asian 11.1% (ทั้งชุด 6.8%), NH Black 19.5% (ทั้งชุด 22.0%), NH White 36.0% (ทั้งชุด 41.8%), Other 1.5% (ทั้งชุด 2.4%), Unknown 18.1% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.5% (ทั้งชุด 29.8%), Joint 26.8% (ทั้งชุด 30.6%), Male 33.2% (ทั้งชุด 33.0%), Unknown 5.5% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 34.8% (ทั้งชุด 30.9%), 35-44 23.3% (ทั้งชุด 26.5%), 45-54 16.7% (ทั้งชุด 17.8%), 55-64 10.1% (ทั้งชุด 11.2%), 65-74 5.2% (ทั้งชุด 5.2%), <25 7.7% (ทั้งชุด 6.8%), >74 1.9% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · cy · seed 43 · กลุ่ม 7
- IF property_value > 5.3e+05 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND ffiec_msa_md_median_family_income > 9.58e+04 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2257/730/721 · coverage กฎบน validation 0.1250
- Fidelity F1 0.7236 · precision 0.8900 · recall 0.6096 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9390 · ERM error 0.0485 · FPR 0.6818 · FNR 0.0074
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.6e-50), derived_msa-md (p_adj=8.6e-76), county_code (p_adj=2.2e-132), conforming_loan_limit (p_adj=4.2e-84), derived_loan_product_type (p_adj=6.1e-103), loan_type (p_adj=1.1e-97), loan_amount (p_adj=2.1e-103), property_value (p_adj=2.1e-96), construction_method (p_adj=3.2e-21), income (p_adj=1e-62), debt_to_income_ratio (p_adj=2.3e-54), aus-1 (p_adj=4.5e-38), ffiec_msa_md_median_family_income (p_adj=9.4e-181), tract_to_msa_income_percentage (p_adj=4.7e-92), tract_owner_occupied_units (p_adj=4.6e-17), tract_median_age_of_housing_units (p_adj=0.00049)
- องค์ประกอบ race_eth: Hispanic 5.0% (ทั้งชุด 9.1%), NH Asian 15.8% (ทั้งชุด 6.8%), NH Black 11.4% (ทั้งชุด 22.0%), NH White 45.4% (ทั้งชุด 41.8%), Other 3.7% (ทั้งชุด 2.4%), Unknown 18.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 18.0% (ทั้งชุด 29.8%), Joint 39.0% (ทั้งชุด 30.6%), Male 34.8% (ทั้งชุด 33.0%), Unknown 8.2% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 26.5% (ทั้งชุด 30.9%), 35-44 36.6% (ทั้งชุด 26.5%), 45-54 18.9% (ทั้งชุด 17.8%), 55-64 10.4% (ทั้งชุด 11.2%), 65-74 4.6% (ทั้งชุด 5.2%), <25 2.4% (ทั้งชุด 6.8%), >74 0.7% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 43 · กลุ่ม 0
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio ≤ 52 AND income ≤ 28.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio > 52 AND derived_loan_product_type_Conventional:First Lien ≤ 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio > 52 AND derived_loan_product_type_Conventional:First Lien > 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND debt_to_income_ratio ≤ 60 AND property_value ≤ 3.4e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1171/639/593 · coverage กฎบน validation 0.2620
- Fidelity F1 0.5347 · precision 0.4303 · recall 0.7058 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.5987 · ERM error 0.2917 · FPR 0.5000 · FNR 0.1521
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.1e-63), derived_msa-md (p_adj=7.8e-06), county_code (p_adj=8.3e-23), derived_loan_product_type (p_adj=2.7e-05), preapproval (p_adj=5.9e-05), loan_type (p_adj=3.8e-06), loan_amount (p_adj=2.6e-09), loan_term (p_adj=1.8e-09), property_value (p_adj=8.9e-13), construction_method (p_adj=6.7e-87), applicant_credit_score_type (p_adj=4.8e-35), initially_payable_to_institution (p_adj=7.9e-06), aus-1 (p_adj=4.9e-138), tract_population (p_adj=1.6e-10), ffiec_msa_md_median_family_income (p_adj=0.00019), tract_to_msa_income_percentage (p_adj=5.2e-08), tract_owner_occupied_units (p_adj=1.8e-07)
- องค์ประกอบ race_eth: Hispanic 8.4% (ทั้งชุด 9.1%), NH Asian 4.6% (ทั้งชุด 6.8%), NH Black 27.0% (ทั้งชุด 22.0%), NH White 38.4% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.4%), Unknown 19.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 32.2% (ทั้งชุด 29.8%), Joint 28.8% (ทั้งชุด 30.6%), Male 32.7% (ทั้งชุด 33.0%), Unknown 6.2% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.7% (ทั้งชุด 30.9%), 35-44 26.6% (ทั้งชุด 26.5%), 45-54 18.7% (ทั้งชุด 17.8%), 55-64 10.1% (ทั้งชุด 11.2%), 65-74 4.2% (ทั้งชุด 5.2%), <25 8.6% (ทั้งชุด 6.8%), >74 0.7% (ทั้งชุด 1.4%), Unknown 0.3% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 43 · กลุ่ม 1
- IF debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 ≤ 0.5 AND tract_one_to_four_family_homes ≤ 16.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 > 0.5 AND lei_549300DD4R4SYK5RAQ92 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND derived_loan_product_type_Conventional:First Lien ≤ 0.5 AND income ≤ 49.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND property_value ≤ 4.4e+05 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND property_value > 4.4e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 789/285/269 · coverage กฎบน validation 0.0638
- Fidelity F1 0.8444 · precision 0.8941 · recall 0.8000 · เงื่อนไขรวม 15 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.0558 · ERM error 0.0558 · FPR 0.0000 · FNR 1.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.4e-88), derived_msa-md (p_adj=1.4e-10), county_code (p_adj=1.7e-43), derived_loan_product_type (p_adj=2.4e-05), loan_type (p_adj=2e-05), loan_amount (p_adj=1.5e-21), loan_term (p_adj=1.5e-24), property_value (p_adj=6.8e-28), construction_method (p_adj=4.8e-137), income (p_adj=1.2e-58), debt_to_income_ratio (p_adj=1e-93), applicant_credit_score_type (p_adj=8.4e-34), initially_payable_to_institution (p_adj=1.1e-125), aus-1 (p_adj=1.3e-98), tract_population (p_adj=1.8e-17), ffiec_msa_md_median_family_income (p_adj=3.4e-06), tract_to_msa_income_percentage (p_adj=5.5e-14), tract_owner_occupied_units (p_adj=7.1e-16), tract_one_to_four_family_homes (p_adj=9.9e-11)
- องค์ประกอบ race_eth: Hispanic 11.9% (ทั้งชุด 9.1%), NH Asian 2.2% (ทั้งชุด 6.8%), NH Black 34.2% (ทั้งชุด 22.0%), NH White 28.6% (ทั้งชุด 41.8%), Other 2.2% (ทั้งชุด 2.4%), Unknown 20.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 45.4% (ทั้งชุด 29.8%), Joint 24.9% (ทั้งชุด 30.6%), Male 22.3% (ทั้งชุด 33.0%), Unknown 7.4% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 29.4% (ทั้งชุด 30.9%), 35-44 24.9% (ทั้งชุด 26.5%), 45-54 17.8% (ทั้งชุด 17.8%), 55-64 13.4% (ทั้งชุด 11.2%), 65-74 5.2% (ทั้งชุด 5.2%), <25 6.7% (ทั้งชุด 6.8%), >74 2.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 43 · กลุ่ม 2
- IF preapproval_2 > 0.5 AND debt_to_income_ratio ≤ 60 AND lei_549300FGXN1K3HLB1R50 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 6731/2000/1990 · coverage กฎบน validation 0.8638
- Fidelity F1 0.7204 · precision 0.5687 · recall 0.9825 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9312 · ERM error 0.0688 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.1e-99), derived_msa-md (p_adj=2.8e-11), county_code (p_adj=1.1e-11), derived_loan_product_type (p_adj=2.3e-33), preapproval (p_adj=1.5e-35), loan_type (p_adj=9.5e-35), loan_amount (p_adj=1.8e-05), loan_term (p_adj=4e-23), construction_method (p_adj=3e-56), applicant_credit_score_type (p_adj=3.1e-19), submission_of_application (p_adj=0.011), initially_payable_to_institution (p_adj=1.5e-21), aus-1 (p_adj=8.7e-49), ffiec_msa_md_median_family_income (p_adj=3.6e-07)
- องค์ประกอบ race_eth: Hispanic 10.1% (ทั้งชุด 9.1%), NH Asian 7.8% (ทั้งชุด 6.8%), NH Black 22.5% (ทั้งชุด 22.0%), NH White 40.3% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.4%), Unknown 17.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 29.0% (ทั้งชุด 29.8%), Joint 30.6% (ทั้งชุด 30.6%), Male 34.5% (ทั้งชุด 33.0%), Unknown 5.9% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 31.3% (ทั้งชุด 30.9%), 35-44 26.7% (ทั้งชุด 26.5%), 45-54 17.3% (ทั้งชุด 17.8%), 55-64 11.0% (ทั้งชุด 11.2%), 65-74 5.3% (ทั้งชุด 5.2%), <25 7.2% (ทั้งชุด 6.8%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · cy · seed 43 · กลุ่ม 3
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio ≤ 47.5 AND preapproval_1 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 ≤ 0.5 AND debt_to_income_ratio ≤ 47.5 AND preapproval_1 > 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND derived_loan_product_type_Conventional:Subordinate Lien > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3309/1076/1148 · coverage กฎบน validation 0.5935
- Fidelity F1 0.5391 · precision 0.3917 · recall 0.8643 · เงื่อนไขรวม 8 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9782 · ERM error 0.0218 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.9e-127), derived_msa-md (p_adj=2.7e-05), county_code (p_adj=1e-24), derived_loan_product_type (p_adj=5.8e-27), preapproval (p_adj=4.4e-93), loan_type (p_adj=1.2e-28), property_value (p_adj=2.2e-08), construction_method (p_adj=1.3e-28), debt_to_income_ratio (p_adj=3.8e-48), applicant_credit_score_type (p_adj=2.8e-10), submission_of_application (p_adj=9.3e-07), initially_payable_to_institution (p_adj=1.9e-10), aus-1 (p_adj=1.3e-83), tract_population (p_adj=4.5e-12), tract_to_msa_income_percentage (p_adj=1.5e-05), tract_owner_occupied_units (p_adj=1.1e-05), tract_one_to_four_family_homes (p_adj=2.2e-05)
- องค์ประกอบ race_eth: Hispanic 7.1% (ทั้งชุด 9.1%), NH Asian 7.1% (ทั้งชุด 6.8%), NH Black 15.6% (ทั้งชุด 22.0%), NH White 49.0% (ทั้งชุด 41.8%), Other 2.8% (ทั้งชุด 2.4%), Unknown 18.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 26.0% (ทั้งชุด 29.8%), Joint 33.1% (ทั้งชุด 30.6%), Male 33.2% (ทั้งชุด 33.0%), Unknown 7.7% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.9% (ทั้งชุด 30.9%), 35-44 26.6% (ทั้งชุด 26.5%), 45-54 18.3% (ทั้งชุด 17.8%), 55-64 11.8% (ทั้งชุด 11.2%), 65-74 5.5% (ทั้งชุด 5.2%), <25 5.3% (ทั้งชุด 6.8%), >74 1.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k2 · c · seed 43 · กลุ่ม 0
- IF tract_owner_occupied_units ≤ 1124 AND property_value ≤ 5.3e+05 AND tract_population ≤ 5370 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units ≤ 1124 AND property_value ≤ 5.3e+05 AND tract_population > 5370 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units ≤ 1124 AND property_value > 5.3e+05 AND tract_owner_occupied_units ≤ 763.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1124 AND property_value ≤ 2.7e+05 AND tract_owner_occupied_units ≤ 1450 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 6983/2394/2344 · coverage กฎบน validation 0.5900
- Fidelity F1 0.9074 · precision 0.9140 · recall 0.9010 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.7833 · ERM error 0.1037 · FPR 0.3681 · FNR 0.0305
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=7.8e-14), derived_msa-md (p_adj=7.5e-67), county_code (p_adj=2.5e-121), conforming_loan_limit (p_adj=5.6e-20), derived_loan_product_type (p_adj=2.5e-13), loan_type (p_adj=4.2e-08), lien_status (p_adj=0.00037), loan_amount (p_adj=6.9e-123), loan_term (p_adj=4.9e-32), property_value (p_adj=5.4e-109), construction_method (p_adj=3.1e-40), income (p_adj=1.6e-37), debt_to_income_ratio (p_adj=3.8e-12), applicant_credit_score_type (p_adj=1.9e-09), aus-1 (p_adj=1.9e-28), tract_population (p_adj=5.7e-302), ffiec_msa_md_median_family_income (p_adj=3.4e-69), tract_to_msa_income_percentage (p_adj=7.6e-141), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=5.1e-240), tract_median_age_of_housing_units (p_adj=2.6e-106)
- องค์ประกอบ race_eth: Hispanic 10.2% (ทั้งชุด 9.1%), NH Asian 4.9% (ทั้งชุด 6.8%), NH Black 24.1% (ทั้งชุด 22.0%), NH White 41.0% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.4%), Unknown 17.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 33.7% (ทั้งชุด 29.8%), Joint 26.7% (ทั้งชุด 30.6%), Male 33.4% (ทั้งชุด 33.0%), Unknown 6.2% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 32.8% (ทั้งชุด 30.9%), 35-44 23.6% (ทั้งชุด 26.5%), 45-54 17.0% (ทั้งชุด 17.8%), 55-64 10.8% (ทั้งชุด 11.2%), 65-74 5.5% (ทั้งชุด 5.2%), <25 8.9% (ทั้งชุด 6.8%), >74 1.4% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k2 · c · seed 43 · กลุ่ม 1
- IF tract_owner_occupied_units ≤ 1114 AND property_value > 5.3e+05 AND tract_owner_occupied_units > 763.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1114 AND property_value ≤ 2.7e+05 AND tract_population > 5150 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1114 AND property_value > 2.7e+05 AND tract_population ≤ 4710 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1114 AND property_value > 2.7e+05 AND tract_population > 4710 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 5017/1606/1656 · coverage กฎบน validation 0.4345
- Fidelity F1 0.8654 · precision 0.8326 · recall 0.9010 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9118 · ERM error 0.0646 · FPR 0.6438 · FNR 0.0086
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=7.8e-14), derived_msa-md (p_adj=7.5e-67), county_code (p_adj=2.5e-121), conforming_loan_limit (p_adj=5.6e-20), derived_loan_product_type (p_adj=2.5e-13), loan_type (p_adj=4.2e-08), lien_status (p_adj=0.00037), loan_amount (p_adj=6.9e-123), loan_term (p_adj=4.9e-32), property_value (p_adj=5.4e-109), construction_method (p_adj=3.1e-40), income (p_adj=1.6e-37), debt_to_income_ratio (p_adj=3.8e-12), applicant_credit_score_type (p_adj=1.9e-09), aus-1 (p_adj=1.9e-28), tract_population (p_adj=5.7e-302), ffiec_msa_md_median_family_income (p_adj=3.4e-69), tract_to_msa_income_percentage (p_adj=7.6e-141), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=5.1e-240), tract_median_age_of_housing_units (p_adj=2.6e-106)
- องค์ประกอบ race_eth: Hispanic 7.5% (ทั้งชุด 9.1%), NH Asian 9.3% (ทั้งชุด 6.8%), NH Black 19.0% (ทั้งชุด 22.0%), NH White 42.9% (ทั้งชุด 41.8%), Other 2.8% (ทั้งชุด 2.4%), Unknown 18.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 24.2% (ทั้งชุด 29.8%), Joint 36.2% (ทั้งชุด 30.6%), Male 32.5% (ทั้งชุด 33.0%), Unknown 7.1% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 28.3% (ทั้งชุด 30.9%), 35-44 30.7% (ทั้งชุด 26.5%), 45-54 19.1% (ทั้งชุด 17.8%), 55-64 12.0% (ทั้งชุด 11.2%), 65-74 4.7% (ทั้งชุด 5.2%), <25 3.9% (ทั้งชุด 6.8%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k2 · c · seed 43 · กลุ่ม 0
- IF loan_term ≤ 307.5 AND aus-1_6 ≤ 0.5 AND loan_amount > 1.3e+05 THEN อยู่กลุ่มนี้
- IF loan_term > 307.5 AND derived_loan_product_type_Conventional:Subordinate Lien ≤ 0.5 AND construction_method_1 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF loan_term > 307.5 AND derived_loan_product_type_Conventional:Subordinate Lien ≤ 0.5 AND construction_method_1 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 10655/3549/3555 · coverage กฎบน validation 0.8920
- Fidelity F1 0.9889 · precision 0.9863 · recall 0.9915 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8951 · ERM error 0.0726 · FPR 0.6113 · FNR 0.0094
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0), derived_msa-md (p_adj=9e-58), county_code (p_adj=3.9e-142), derived_loan_product_type (p_adj=2.1e-128), loan_type (p_adj=1.3e-50), lien_status (p_adj=1.4e-92), loan_amount (p_adj=5.9e-30), loan_term (p_adj=1.9e-65), property_value (p_adj=5.2e-12), construction_method (p_adj=0), debt_to_income_ratio (p_adj=0.00034), applicant_credit_score_type (p_adj=2.6e-182), submission_of_application (p_adj=0.00047), initially_payable_to_institution (p_adj=0.00011), aus-1 (p_adj=0), tract_population (p_adj=4.8e-33), ffiec_msa_md_median_family_income (p_adj=1.4e-31), tract_to_msa_income_percentage (p_adj=2.8e-30), tract_owner_occupied_units (p_adj=2.8e-27), tract_one_to_four_family_homes (p_adj=2.6e-09)
- องค์ประกอบ race_eth: Hispanic 9.3% (ทั้งชุด 9.1%), NH Asian 7.5% (ทั้งชุด 6.8%), NH Black 21.3% (ทั้งชุด 22.0%), NH White 41.7% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.4%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 28.5% (ทั้งชุด 29.8%), Joint 30.7% (ทั้งชุด 30.6%), Male 33.9% (ทั้งชุด 33.0%), Unknown 6.9% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.3% (ทั้งชุด 30.9%), 35-44 26.8% (ทั้งชุด 26.5%), 45-54 18.3% (ทั้งชุด 17.8%), 55-64 11.4% (ทั้งชุด 11.2%), 65-74 5.3% (ทั้งชุด 5.2%), <25 6.6% (ทั้งชุด 6.8%), >74 1.2% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k2 · c · seed 43 · กลุ่ม 1
- IF loan_term ≤ 307.5 AND aus-1_6 ≤ 0.5 AND loan_amount ≤ 1.3e+05 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 307.5 AND aus-1_6 > 0.5 AND construction_method_2 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 307.5 AND aus-1_6 > 0.5 AND construction_method_2 > 0.5 THEN อยู่กลุ่มนี้
- IF loan_term > 307.5 AND derived_loan_product_type_Conventional:Subordinate Lien > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1345/451/445 · coverage กฎบน validation 0.1080
- Fidelity F1 0.9105 · precision 0.9306 · recall 0.8914 · เงื่อนไขรวม 11 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.3685 · ERM error 0.2067 · FPR 0.1886 · FNR 0.2378
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0), derived_msa-md (p_adj=9e-58), county_code (p_adj=3.9e-142), derived_loan_product_type (p_adj=2.1e-128), loan_type (p_adj=1.3e-50), lien_status (p_adj=1.4e-92), loan_amount (p_adj=5.9e-30), loan_term (p_adj=1.9e-65), property_value (p_adj=5.2e-12), construction_method (p_adj=0), debt_to_income_ratio (p_adj=0.00034), applicant_credit_score_type (p_adj=2.6e-182), submission_of_application (p_adj=0.00047), initially_payable_to_institution (p_adj=0.00011), aus-1 (p_adj=0), tract_population (p_adj=4.8e-33), ffiec_msa_md_median_family_income (p_adj=1.4e-31), tract_to_msa_income_percentage (p_adj=2.8e-30), tract_owner_occupied_units (p_adj=2.8e-27), tract_one_to_four_family_homes (p_adj=2.6e-09)
- องค์ประกอบ race_eth: Hispanic 7.6% (ทั้งชุด 9.1%), NH Asian 0.9% (ทั้งชุด 6.8%), NH Black 27.6% (ทั้งชุด 22.0%), NH White 42.5% (ทั้งชุด 41.8%), Other 1.8% (ทั้งชุด 2.4%), Unknown 19.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 40.0% (ทั้งชุด 29.8%), Joint 29.9% (ทั้งชุด 30.6%), Male 26.3% (ทั้งชุด 33.0%), Unknown 3.8% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 36.0% (ทั้งชุด 30.9%), 35-44 24.5% (ทั้งชุด 26.5%), 45-54 13.9% (ทั้งชุด 17.8%), 55-64 9.9% (ทั้งชุด 11.2%), 65-74 4.3% (ทั้งชุด 5.2%), <25 9.0% (ทั้งชุด 6.8%), >74 2.2% (ทั้งชุด 1.4%), Unknown 0.2% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · c · seed 43 · กลุ่ม 0
- IF construction_method_1 ≤ 0.5 AND aus-1_6 ≤ 0.5 AND tract_median_age_of_housing_units ≤ 24.5 THEN อยู่กลุ่มนี้
- IF construction_method_1 ≤ 0.5 AND aus-1_6 ≤ 0.5 AND tract_median_age_of_housing_units > 24.5 THEN อยู่กลุ่มนี้
- IF construction_method_1 > 0.5 AND debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 10251/3412/3449 · coverage กฎบน validation 0.8685
- Fidelity F1 0.9765 · precision 0.9678 · recall 0.9853 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9322 · ERM error 0.0678 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.4e-199), derived_msa-md (p_adj=1.4e-29), county_code (p_adj=1.5e-67), derived_loan_product_type (p_adj=3.5e-09), preapproval (p_adj=0.00023), loan_type (p_adj=2.3e-08), loan_amount (p_adj=1.4e-32), loan_term (p_adj=1.4e-46), property_value (p_adj=9.8e-46), construction_method (p_adj=2.8e-267), income (p_adj=5.1e-54), debt_to_income_ratio (p_adj=5e-55), applicant_credit_score_type (p_adj=3.3e-88), initially_payable_to_institution (p_adj=1.6e-96), aus-1 (p_adj=2.2e-236), tract_population (p_adj=1e-32), ffiec_msa_md_median_family_income (p_adj=5.1e-17), tract_to_msa_income_percentage (p_adj=1.8e-24), tract_owner_occupied_units (p_adj=3.4e-27), tract_one_to_four_family_homes (p_adj=1.1e-11)
- องค์ประกอบ race_eth: Hispanic 8.8% (ทั้งชุด 9.1%), NH Asian 7.4% (ทั้งชุด 6.8%), NH Black 20.6% (ทั้งชุด 22.0%), NH White 43.0% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.4%), Unknown 17.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 28.3% (ทั้งชุด 29.8%), Joint 31.3% (ทั้งชุด 30.6%), Male 33.9% (ทั้งชุด 33.0%), Unknown 6.6% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.8% (ทั้งชุด 30.9%), 35-44 27.0% (ทั้งชุด 26.5%), 45-54 17.9% (ทั้งชุด 17.8%), 55-64 11.4% (ทั้งชุด 11.2%), 65-74 5.1% (ทั้งชุด 5.2%), <25 6.6% (ทั้งชุด 6.8%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · c · seed 43 · กลุ่ม 1
- IF aus-1_6 ≤ 0.5 AND initially_payable_to_institution_3 ≤ 0.5 AND debt_to_income_ratio > 60 THEN อยู่กลุ่มนี้
- IF aus-1_6 ≤ 0.5 AND initially_payable_to_institution_3 > 0.5 AND submission_of_application_2 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 ≤ 0.5 AND initially_payable_to_institution_3 > 0.5 AND submission_of_application_2 > 0.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND construction_method_1 ≤ 0.5 AND loan_term ≤ 301.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND construction_method_1 ≤ 0.5 AND loan_term > 301.5 THEN อยู่กลุ่มนี้
- IF aus-1_6 > 0.5 AND construction_method_1 > 0.5 AND debt_to_income_ratio > 46.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1749/588/551 · coverage กฎบน validation 0.1447
- Fidelity F1 0.8603 · precision 0.8670 · recall 0.8537 · เงื่อนไขรวม 18 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.2377 · ERM error 0.2105 · FPR 0.1119 · FNR 0.5267
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.4e-199), derived_msa-md (p_adj=1.4e-29), county_code (p_adj=1.5e-67), derived_loan_product_type (p_adj=3.5e-09), preapproval (p_adj=0.00023), loan_type (p_adj=2.3e-08), loan_amount (p_adj=1.4e-32), loan_term (p_adj=1.4e-46), property_value (p_adj=9.8e-46), construction_method (p_adj=2.8e-267), income (p_adj=5.1e-54), debt_to_income_ratio (p_adj=5e-55), applicant_credit_score_type (p_adj=3.3e-88), initially_payable_to_institution (p_adj=1.6e-96), aus-1 (p_adj=2.2e-236), tract_population (p_adj=1e-32), ffiec_msa_md_median_family_income (p_adj=5.1e-17), tract_to_msa_income_percentage (p_adj=1.8e-24), tract_owner_occupied_units (p_adj=3.4e-27), tract_one_to_four_family_homes (p_adj=1.1e-11)
- องค์ประกอบ race_eth: Hispanic 10.7% (ทั้งชุด 9.1%), NH Asian 2.7% (ทั้งชุด 6.8%), NH Black 30.9% (ทั้งชุด 22.0%), NH White 33.8% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.4%), Unknown 19.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 39.0% (ทั้งชุด 29.8%), Joint 26.7% (ทั้งชุด 30.6%), Male 27.6% (ทั้งชุด 33.0%), Unknown 6.7% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 31.8% (ทั้งชุด 30.9%), 35-44 23.6% (ทั้งชุด 26.5%), 45-54 17.8% (ทั้งชุด 17.8%), 55-64 10.5% (ทั้งชุด 11.2%), 65-74 6.0% (ทั้งชุด 5.2%), <25 8.3% (ทั้งชุด 6.8%), >74 1.8% (ทั้งชุด 1.4%), Unknown 0.2% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 43 · กลุ่ม 0
- IF loan_term ≤ 301.5 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND tract_owner_occupied_units ≤ 1570 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 301.5 AND ffiec_msa_md_median_family_income > 1.015e+05 AND loan_amount ≤ 9e+04 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1021/345/319 · coverage กฎบน validation 0.0862
- Fidelity F1 0.9130 · precision 0.9130 · recall 0.9130 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.3699 · ERM error 0.1755 · FPR 0.1343 · FNR 0.2458
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.1e-242), derived_msa-md (p_adj=3.3e-72), county_code (p_adj=1.6e-161), derived_loan_product_type (p_adj=1.4e-54), loan_type (p_adj=1.9e-36), lien_status (p_adj=7.4e-24), loan_amount (p_adj=3.9e-187), loan_term (p_adj=1.6e-76), property_value (p_adj=1.8e-121), construction_method (p_adj=0), income (p_adj=5.6e-37), applicant_credit_score_type (p_adj=1e-107), initially_payable_to_institution (p_adj=0.017), aus-1 (p_adj=4.8e-284), tract_population (p_adj=3e-29), ffiec_msa_md_median_family_income (p_adj=5.8e-44), tract_to_msa_income_percentage (p_adj=1.5e-23), tract_owner_occupied_units (p_adj=1.7e-26), tract_one_to_four_family_homes (p_adj=9.3e-06)
- องค์ประกอบ race_eth: Hispanic 5.0% (ทั้งชุด 9.1%), NH Asian 1.9% (ทั้งชุด 6.8%), NH Black 26.6% (ทั้งชุด 22.0%), NH White 46.4% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.4%), Unknown 18.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 39.2% (ทั้งชุด 29.8%), Joint 32.3% (ทั้งชุด 30.6%), Male 24.5% (ทั้งชุด 33.0%), Unknown 4.1% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 34.5% (ทั้งชุด 30.9%), 35-44 22.6% (ทั้งชุด 26.5%), 45-54 14.4% (ทั้งชุด 17.8%), 55-64 10.7% (ทั้งชุด 11.2%), 65-74 5.3% (ทั้งชุด 5.2%), <25 9.7% (ทั้งชุด 6.8%), >74 2.8% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 43 · กลุ่ม 1
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND loan_term > 322 AND tract_owner_occupied_units ≤ 1420 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 8.405e+04 AND ffiec_msa_md_median_family_income ≤ 9.11e+04 AND loan_amount ≤ 2.3e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2102/712/731 · coverage กฎบน validation 0.2162
- Fidelity F1 0.8776 · precision 0.8000 · recall 0.9719 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8550 · ERM error 0.1040 · FPR 0.6321 · FNR 0.0144
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.4e-22), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.01), derived_loan_product_type (p_adj=1.3e-38), loan_type (p_adj=6.8e-41), loan_amount (p_adj=3.7e-100), loan_term (p_adj=2.8e-62), property_value (p_adj=1.2e-110), income (p_adj=8.2e-40), applicant_credit_score_type (p_adj=0.0038), aus-1 (p_adj=3.2e-19), tract_population (p_adj=2.7e-47), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=1.6e-53), tract_median_age_of_housing_units (p_adj=4.8e-24)
- องค์ประกอบ race_eth: Hispanic 7.8% (ทั้งชุด 9.1%), NH Asian 2.1% (ทั้งชุด 6.8%), NH Black 16.1% (ทั้งชุด 22.0%), NH White 53.8% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.4%), Unknown 17.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 29.3% (ทั้งชุด 29.8%), Joint 28.5% (ทั้งชุด 30.6%), Male 35.4% (ทั้งชุด 33.0%), Unknown 6.8% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 31.5% (ทั้งชุด 30.9%), 35-44 21.5% (ทั้งชุด 26.5%), 45-54 17.4% (ทั้งชุด 17.8%), 55-64 11.2% (ทั้งชุด 11.2%), 65-74 7.0% (ทั้งชุด 5.2%), <25 10.0% (ทั้งชุด 6.8%), >74 1.4% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 43 · กลุ่ม 2
- IF ffiec_msa_md_median_family_income > 8.405e+04 AND tract_owner_occupied_units ≤ 1114 AND property_value ≤ 8.1e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3832/1331/1288 · coverage กฎบน validation 0.3543
- Fidelity F1 0.8384 · precision 0.8130 · recall 0.8655 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8439 · ERM error 0.0862 · FPR 0.4627 · FNR 0.0166
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=6.8e-05), derived_msa-md (p_adj=5.6e-155), county_code (p_adj=9e-159), conforming_loan_limit (p_adj=0.0019), derived_loan_product_type (p_adj=5.8e-06), loan_type (p_adj=2.9e-07), loan_amount (p_adj=2.2e-07), loan_term (p_adj=6.9e-15), property_value (p_adj=6.3e-16), construction_method (p_adj=4.2e-13), income (p_adj=6.1e-10), debt_to_income_ratio (p_adj=0.00028), aus-1 (p_adj=1.6e-06), tract_population (p_adj=1.3e-145), ffiec_msa_md_median_family_income (p_adj=6.7e-285), tract_to_msa_income_percentage (p_adj=1.2e-99), tract_owner_occupied_units (p_adj=5.6e-277), tract_one_to_four_family_homes (p_adj=3.5e-249), tract_median_age_of_housing_units (p_adj=2.8e-26)
- องค์ประกอบ race_eth: Hispanic 12.9% (ทั้งชุด 9.1%), NH Asian 7.3% (ทั้งชุด 6.8%), NH Black 28.0% (ทั้งชุด 22.0%), NH White 32.2% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.4%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.9% (ทั้งชุด 29.8%), Joint 24.1% (ทั้งชุด 30.6%), Male 34.5% (ทั้งชุด 33.0%), Unknown 6.4% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 33.2% (ทั้งชุด 30.9%), 35-44 24.9% (ทั้งชุด 26.5%), 45-54 17.5% (ทั้งชุด 17.8%), 55-64 10.6% (ทั้งชุด 11.2%), 65-74 4.8% (ทั้งชุด 5.2%), <25 8.0% (ทั้งชุด 6.8%), >74 1.0% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · cy · seed 43 · กลุ่ม 3
- IF tract_owner_occupied_units ≤ 1114 AND property_value > 5.3e+05 AND tract_owner_occupied_units > 763.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1114 AND property_value ≤ 2.7e+05 AND tract_population > 5150 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1114 AND property_value > 2.7e+05 AND tract_population ≤ 4710 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1114 AND property_value > 2.7e+05 AND tract_population > 4710 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 5045/1612/1662 · coverage กฎบน validation 0.4345
- Fidelity F1 0.8651 · precision 0.8337 · recall 0.8989 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9122 · ERM error 0.0644 · FPR 0.6438 · FNR 0.0086
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=7.8e-14), derived_msa-md (p_adj=6.2e-67), county_code (p_adj=9.5e-121), conforming_loan_limit (p_adj=8e-20), derived_loan_product_type (p_adj=9.6e-14), loan_type (p_adj=2e-08), lien_status (p_adj=0.00032), loan_amount (p_adj=1.6e-123), loan_term (p_adj=3.1e-32), property_value (p_adj=2.3e-109), construction_method (p_adj=5.5e-40), income (p_adj=8e-38), debt_to_income_ratio (p_adj=1.3e-12), applicant_credit_score_type (p_adj=1.1e-09), aus-1 (p_adj=4.1e-29), tract_population (p_adj=9.1e-302), ffiec_msa_md_median_family_income (p_adj=4.9e-69), tract_to_msa_income_percentage (p_adj=2.2e-142), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=3e-239), tract_median_age_of_housing_units (p_adj=3.2e-106)
- องค์ประกอบ race_eth: Hispanic 7.5% (ทั้งชุด 9.1%), NH Asian 9.3% (ทั้งชุด 6.8%), NH Black 19.0% (ทั้งชุด 22.0%), NH White 43.0% (ทั้งชุด 41.8%), Other 2.8% (ทั้งชุด 2.4%), Unknown 18.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 24.1% (ทั้งชุด 29.8%), Joint 36.3% (ทั้งชุด 30.6%), Male 32.5% (ทั้งชุด 33.0%), Unknown 7.0% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 28.3% (ทั้งชุด 30.9%), 35-44 30.7% (ทั้งชุด 26.5%), 45-54 19.0% (ทั้งชุด 17.8%), 55-64 11.9% (ทั้งชุด 11.2%), 65-74 4.7% (ทั้งชุด 5.2%), <25 4.0% (ทั้งชุด 6.8%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 43 · กลุ่ม 0
- IF loan_term ≤ 301.5 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND tract_owner_occupied_units ≤ 1570 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 301.5 AND ffiec_msa_md_median_family_income > 1.015e+05 AND loan_amount ≤ 9e+04 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1021/345/319 · coverage กฎบน validation 0.0862
- Fidelity F1 0.9130 · precision 0.9130 · recall 0.9130 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: unbalanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.3699 · ERM error 0.1755 · FPR 0.1343 · FNR 0.2458
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.1e-242), derived_msa-md (p_adj=3.3e-72), county_code (p_adj=1.6e-161), derived_loan_product_type (p_adj=1.4e-54), loan_type (p_adj=1.9e-36), lien_status (p_adj=7.4e-24), loan_amount (p_adj=3.9e-187), loan_term (p_adj=1.6e-76), property_value (p_adj=1.8e-121), construction_method (p_adj=0), income (p_adj=5.6e-37), applicant_credit_score_type (p_adj=1e-107), initially_payable_to_institution (p_adj=0.017), aus-1 (p_adj=4.8e-284), tract_population (p_adj=3e-29), ffiec_msa_md_median_family_income (p_adj=5.8e-44), tract_to_msa_income_percentage (p_adj=1.5e-23), tract_owner_occupied_units (p_adj=1.7e-26), tract_one_to_four_family_homes (p_adj=9.3e-06)
- องค์ประกอบ race_eth: Hispanic 5.0% (ทั้งชุด 9.1%), NH Asian 1.9% (ทั้งชุด 6.8%), NH Black 26.6% (ทั้งชุด 22.0%), NH White 46.4% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.4%), Unknown 18.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 39.2% (ทั้งชุด 29.8%), Joint 32.3% (ทั้งชุด 30.6%), Male 24.5% (ทั้งชุด 33.0%), Unknown 4.1% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 34.5% (ทั้งชุด 30.9%), 35-44 22.6% (ทั้งชุด 26.5%), 45-54 14.4% (ทั้งชุด 17.8%), 55-64 10.7% (ทั้งชุด 11.2%), 65-74 5.3% (ทั้งชุด 5.2%), <25 9.7% (ทั้งชุด 6.8%), >74 2.8% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 43 · กลุ่ม 1
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND loan_term > 322 AND tract_owner_occupied_units ≤ 1420 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 8.405e+04 AND ffiec_msa_md_median_family_income ≤ 9.11e+04 AND loan_amount ≤ 2.3e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2102/712/731 · coverage กฎบน validation 0.2162
- Fidelity F1 0.8776 · precision 0.8000 · recall 0.9719 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8550 · ERM error 0.1040 · FPR 0.6321 · FNR 0.0144
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.4e-22), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.01), derived_loan_product_type (p_adj=1.3e-38), loan_type (p_adj=6.8e-41), loan_amount (p_adj=3.7e-100), loan_term (p_adj=2.8e-62), property_value (p_adj=1.2e-110), income (p_adj=8.2e-40), applicant_credit_score_type (p_adj=0.0038), aus-1 (p_adj=3.2e-19), tract_population (p_adj=2.7e-47), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=1.6e-53), tract_median_age_of_housing_units (p_adj=4.8e-24)
- องค์ประกอบ race_eth: Hispanic 7.8% (ทั้งชุด 9.1%), NH Asian 2.1% (ทั้งชุด 6.8%), NH Black 16.1% (ทั้งชุด 22.0%), NH White 53.8% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.4%), Unknown 17.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 29.3% (ทั้งชุด 29.8%), Joint 28.5% (ทั้งชุด 30.6%), Male 35.4% (ทั้งชุด 33.0%), Unknown 6.8% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 31.5% (ทั้งชุด 30.9%), 35-44 21.5% (ทั้งชุด 26.5%), 45-54 17.4% (ทั้งชุด 17.8%), 55-64 11.2% (ทั้งชุด 11.2%), 65-74 7.0% (ทั้งชุด 5.2%), <25 10.0% (ทั้งชุด 6.8%), >74 1.4% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 43 · กลุ่ม 2
- IF ffiec_msa_md_median_family_income > 8.405e+04 AND tract_owner_occupied_units ≤ 1114 AND property_value ≤ 8.1e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3832/1331/1288 · coverage กฎบน validation 0.3543
- Fidelity F1 0.8384 · precision 0.8130 · recall 0.8655 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.8439 · ERM error 0.0862 · FPR 0.4627 · FNR 0.0166
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=6.8e-05), derived_msa-md (p_adj=5.6e-155), county_code (p_adj=9e-159), conforming_loan_limit (p_adj=0.0019), derived_loan_product_type (p_adj=5.8e-06), loan_type (p_adj=2.9e-07), loan_amount (p_adj=2.2e-07), loan_term (p_adj=6.9e-15), property_value (p_adj=6.3e-16), construction_method (p_adj=4.2e-13), income (p_adj=6.1e-10), debt_to_income_ratio (p_adj=0.00028), aus-1 (p_adj=1.6e-06), tract_population (p_adj=1.3e-145), ffiec_msa_md_median_family_income (p_adj=6.7e-285), tract_to_msa_income_percentage (p_adj=1.2e-99), tract_owner_occupied_units (p_adj=5.6e-277), tract_one_to_four_family_homes (p_adj=3.5e-249), tract_median_age_of_housing_units (p_adj=2.8e-26)
- องค์ประกอบ race_eth: Hispanic 12.9% (ทั้งชุด 9.1%), NH Asian 7.3% (ทั้งชุด 6.8%), NH Black 28.0% (ทั้งชุด 22.0%), NH White 32.2% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.4%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.9% (ทั้งชุด 29.8%), Joint 24.1% (ทั้งชุด 30.6%), Male 34.5% (ทั้งชุด 33.0%), Unknown 6.4% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 33.2% (ทั้งชุด 30.9%), 35-44 24.9% (ทั้งชุด 26.5%), 45-54 17.5% (ทั้งชุด 17.8%), 55-64 10.6% (ทั้งชุด 11.2%), 65-74 4.8% (ทั้งชุด 5.2%), <25 8.0% (ทั้งชุด 6.8%), >74 1.0% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · c · seed 43 · กลุ่ม 3
- IF tract_owner_occupied_units ≤ 1114 AND property_value > 5.3e+05 AND tract_owner_occupied_units > 763.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1114 AND property_value ≤ 2.7e+05 AND tract_population > 5150 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1114 AND property_value > 2.7e+05 AND tract_population ≤ 4710 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1114 AND property_value > 2.7e+05 AND tract_population > 4710 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 5045/1612/1662 · coverage กฎบน validation 0.4345
- Fidelity F1 0.8651 · precision 0.8337 · recall 0.8989 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- ต้นไม้ที่เลือก: balanced ด้วย F1 validation ของ cluster
- อนุมัติจริง 0.9122 · ERM error 0.0644 · FPR 0.6438 · FNR 0.0086
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=7.8e-14), derived_msa-md (p_adj=6.2e-67), county_code (p_adj=9.5e-121), conforming_loan_limit (p_adj=8e-20), derived_loan_product_type (p_adj=9.6e-14), loan_type (p_adj=2e-08), lien_status (p_adj=0.00032), loan_amount (p_adj=1.6e-123), loan_term (p_adj=3.1e-32), property_value (p_adj=2.3e-109), construction_method (p_adj=5.5e-40), income (p_adj=8e-38), debt_to_income_ratio (p_adj=1.3e-12), applicant_credit_score_type (p_adj=1.1e-09), aus-1 (p_adj=4.1e-29), tract_population (p_adj=9.1e-302), ffiec_msa_md_median_family_income (p_adj=4.9e-69), tract_to_msa_income_percentage (p_adj=2.2e-142), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=3e-239), tract_median_age_of_housing_units (p_adj=3.2e-106)
- องค์ประกอบ race_eth: Hispanic 7.5% (ทั้งชุด 9.1%), NH Asian 9.3% (ทั้งชุด 6.8%), NH Black 19.0% (ทั้งชุด 22.0%), NH White 43.0% (ทั้งชุด 41.8%), Other 2.8% (ทั้งชุด 2.4%), Unknown 18.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 24.1% (ทั้งชุด 29.8%), Joint 36.3% (ทั้งชุด 30.6%), Male 32.5% (ทั้งชุด 33.0%), Unknown 7.0% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 28.3% (ทั้งชุด 30.9%), 35-44 30.7% (ทั้งชุด 26.5%), 45-54 19.0% (ทั้งชุด 17.8%), 55-64 11.9% (ทั้งชุด 11.2%), 65-74 4.7% (ทั้งชุด 5.2%), <25 4.0% (ทั้งชุด 6.8%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation
