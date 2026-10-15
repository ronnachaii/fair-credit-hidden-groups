# การ์ดอธิบายกลุ่ม HMDA

กฎ one-hot ที่ ≤ 0.5 หมายถึงไม่มีค่านั้น; สถิติต่างกลุ่มเป็นเชิงสำรวจ ไม่ใช่เหตุและผล

### GDRO-raw-k4 · seed 17 · กลุ่ม 0
- IF tract_population ≤ 357.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 151/46/56 · coverage กฎบน validation 0.0110
- Fidelity F1 0.9778 · เงื่อนไขรวม 1 · สูงสุดต่อเส้นทาง 1
- อนุมัติจริง 0.0893 · ERM error 0.0536 · FPR 0.0196 · FNR 0.4000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.7e-121), derived_msa-md (p_adj=4.7e-13), county_code (p_adj=2.6e-112), loan_amount (p_adj=1.5e-12), loan_term (p_adj=1e-13), property_value (p_adj=1.4e-16), construction_method (p_adj=5.6e-71), income (p_adj=2.4e-13), debt_to_income_ratio (p_adj=1.2e-06), applicant_credit_score_type (p_adj=2.6e-06), aus-1 (p_adj=7.8e-41), tract_population (p_adj=0), ffiec_msa_md_median_family_income (p_adj=0.00095), tract_to_msa_income_percentage (p_adj=0), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=0), tract_median_age_of_housing_units (p_adj=0)
- องค์ประกอบ race_eth: Hispanic 3.6% (ทั้งชุด 9.1%), NH Asian 3.6% (ทั้งชุด 6.8%), NH Black 33.9% (ทั้งชุด 22.0%), NH White 42.9% (ทั้งชุด 41.8%), Other 3.6% (ทั้งชุด 2.3%), Unknown 12.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 46.4% (ทั้งชุด 27.1%), Joint 25.0% (ทั้งชุด 30.7%), Male 26.8% (ทั้งชุด 35.6%), Unknown 1.8% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 26.8% (ทั้งชุด 31.4%), 35-44 32.1% (ทั้งชุด 26.6%), 45-54 21.4% (ทั้งชุด 17.5%), 55-64 3.6% (ทั้งชุด 11.7%), 65-74 7.1% (ทั้งชุด 5.5%), <25 7.1% (ทั้งชุด 5.9%), >74 1.8% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 17 · กลุ่ม 1
- IF initially_payable_to_institution_3 ≤ 0.5 AND debt_to_income_ratio > 60 AND construction_method_2 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF initially_payable_to_institution_3 > 0.5 AND loan_type_1 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF initially_payable_to_institution_3 > 0.5 AND loan_type_1 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1087/642/646 · coverage กฎบน validation 0.0445
- Fidelity F1 0.1829 · เงื่อนไขรวม 7 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8142 · ERM error 0.0789 · FPR 0.3417 · FNR 0.0190
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.023), derived_msa-md (p_adj=1.4e-44), county_code (p_adj=7.9e-32), derived_loan_product_type (p_adj=7e-83), loan_type (p_adj=7.2e-85), loan_term (p_adj=5e-58), construction_method (p_adj=1.3e-13), income (p_adj=1.8e-24), debt_to_income_ratio (p_adj=5.4e-146), aus-1 (p_adj=1.1e-45), tract_population (p_adj=2e-06), ffiec_msa_md_median_family_income (p_adj=2.6e-106), tract_owner_occupied_units (p_adj=0.015)
- องค์ประกอบ race_eth: Hispanic 12.1% (ทั้งชุด 9.1%), NH Asian 5.3% (ทั้งชุด 6.8%), NH Black 35.3% (ทั้งชุด 22.0%), NH White 26.0% (ทั้งชุด 41.8%), Other 2.6% (ทั้งชุด 2.3%), Unknown 18.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 35.1% (ทั้งชุด 27.1%), Joint 27.9% (ทั้งชุด 30.7%), Male 30.7% (ทั้งชุด 35.6%), Unknown 6.3% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 29.1% (ทั้งชุด 31.4%), 35-44 28.6% (ทั้งชุด 26.6%), 45-54 19.5% (ทั้งชุด 17.5%), 55-64 10.7% (ทั้งชุด 11.7%), 65-74 5.9% (ทั้งชุด 5.5%), <25 5.0% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 17 · กลุ่ม 2
- IF construction_method_2 > 0.5 AND aus-1_6 > 0.5 AND tract_one_to_four_family_homes > 464 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 712/341/355 · coverage กฎบน validation 0.0717
- Fidelity F1 0.8280 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.4394 · ERM error 0.1972 · FPR 0.0955 · FNR 0.3269
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.3e-234), derived_msa-md (p_adj=1e-48), county_code (p_adj=2.8e-105), derived_loan_product_type (p_adj=5.1e-89), loan_type (p_adj=2.5e-47), lien_status (p_adj=2.4e-52), loan_amount (p_adj=6e-234), loan_term (p_adj=6.8e-77), property_value (p_adj=4.1e-151), construction_method (p_adj=0), income (p_adj=4e-62), applicant_credit_score_type (p_adj=6.4e-179), aus-1 (p_adj=6.9e-293), tract_population (p_adj=1e-13), ffiec_msa_md_median_family_income (p_adj=7.1e-29), tract_to_msa_income_percentage (p_adj=2.6e-17), tract_owner_occupied_units (p_adj=1.4e-09), tract_median_age_of_housing_units (p_adj=3.7e-15)
- องค์ประกอบ race_eth: Hispanic 6.5% (ทั้งชุด 9.1%), NH Asian 2.8% (ทั้งชุด 6.8%), NH Black 24.2% (ทั้งชุด 22.0%), NH White 44.2% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.3%), Unknown 20.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.9% (ทั้งชุด 27.1%), Joint 27.0% (ทั้งชุด 30.7%), Male 32.7% (ทั้งชุด 35.6%), Unknown 5.4% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.1% (ทั้งชุด 31.4%), 35-44 23.9% (ทั้งชุด 26.6%), 45-54 18.0% (ทั้งชุด 17.5%), 55-64 11.8% (ทั้งชุด 11.7%), 65-74 5.6% (ทั้งชุด 5.5%), <25 8.7% (ทั้งชุด 5.9%), >74 1.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 17 · กลุ่ม 3
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 10/11/8 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 0.8750 · ERM error 0.1250 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.8e-74), county_code (p_adj=2.4e-41), applicant_credit_score_type (p_adj=0.015), submission_of_application (p_adj=1.1e-05), initially_payable_to_institution (p_adj=0.00014), aus-1 (p_adj=1.8e-06)
- องค์ประกอบ race_eth: Hispanic 25.0% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 12.5% (ทั้งชุด 22.0%), NH White 37.5% (ทั้งชุด 41.8%), Other 0.0% (ทั้งชุด 2.3%), Unknown 25.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 12.5% (ทั้งชุด 27.1%), Joint 50.0% (ทั้งชุด 30.7%), Male 25.0% (ทั้งชุด 35.6%), Unknown 12.5% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 62.5% (ทั้งชุด 31.4%), 35-44 12.5% (ทั้งชุด 26.6%), 45-54 12.5% (ทั้งชุด 17.5%), 55-64 0.0% (ทั้งชุด 11.7%), 65-74 12.5% (ทั้งชุด 5.5%), <25 0.0% (ทั้งชุด 5.9%), >74 0.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 17 · กลุ่ม 4
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND aus-1_6 ≤ 0.5 AND tract_owner_occupied_units ≤ 1781 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2532/801/759 · coverage กฎบน validation 0.1930
- Fidelity F1 0.8875 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8775 · ERM error 0.0909 · FPR 0.6667 · FNR 0.0105
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=7.9e-29), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.0053), derived_loan_product_type (p_adj=1.9e-32), loan_type (p_adj=9.4e-34), loan_amount (p_adj=4.7e-63), loan_term (p_adj=3e-60), property_value (p_adj=4e-68), income (p_adj=1.6e-23), applicant_credit_score_type (p_adj=9e-15), submission_of_application (p_adj=1.1e-12), initially_payable_to_institution (p_adj=4.8e-13), aus-1 (p_adj=9.8e-33), tract_population (p_adj=3.6e-29), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=1.5e-35), tract_median_age_of_housing_units (p_adj=1.5e-22)
- องค์ประกอบ race_eth: Hispanic 6.7% (ทั้งชุด 9.1%), NH Asian 1.6% (ทั้งชุด 6.8%), NH Black 15.9% (ทั้งชุด 22.0%), NH White 58.0% (ทั้งชุด 41.8%), Other 2.9% (ทั้งชุด 2.3%), Unknown 14.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 22.7% (ทั้งชุด 27.1%), Joint 32.7% (ทั้งชุด 30.7%), Male 37.5% (ทั้งชุด 35.6%), Unknown 7.1% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 31.2% (ทั้งชุด 31.4%), 35-44 21.7% (ทั้งชุด 26.6%), 45-54 14.0% (ทั้งชุด 17.5%), 55-64 14.5% (ทั้งชุด 11.7%), 65-74 6.6% (ทั้งชุด 5.5%), <25 10.1% (ทั้งชุด 5.9%), >74 1.8% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 17 · กลุ่ม 5
- IF ffiec_msa_md_median_family_income ≤ 9.11e+04 AND ffiec_msa_md_median_family_income > 8.405e+04 AND tract_one_to_four_family_homes ≤ 1350 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 9.11e+04 AND tract_owner_occupied_units ≤ 1298 AND property_value ≤ 7.5e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4124/1098/1130 · coverage กฎบน validation 0.4198
- Fidelity F1 0.7555 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9071 · ERM error 0.0681 · FPR 0.6857 · FNR 0.0049
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=9.3e-12), derived_msa-md (p_adj=2e-136), county_code (p_adj=5.9e-131), conforming_loan_limit (p_adj=9.5e-06), derived_loan_product_type (p_adj=4.4e-18), loan_type (p_adj=5.4e-16), loan_term (p_adj=2.4e-29), construction_method (p_adj=3.5e-29), debt_to_income_ratio (p_adj=8.4e-19), applicant_credit_score_type (p_adj=1.1e-05), aus-1 (p_adj=1e-25), tract_population (p_adj=4.6e-147), ffiec_msa_md_median_family_income (p_adj=0), tract_to_msa_income_percentage (p_adj=1.3e-30), tract_owner_occupied_units (p_adj=7.9e-237), tract_one_to_four_family_homes (p_adj=3.2e-270), tract_median_age_of_housing_units (p_adj=2.7e-20)
- องค์ประกอบ race_eth: Hispanic 11.7% (ทั้งชุด 9.1%), NH Asian 9.6% (ทั้งชุด 6.8%), NH Black 22.4% (ทั้งชุด 22.0%), NH White 35.7% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.3%), Unknown 18.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 29.7% (ทั้งชุด 27.1%), Joint 27.8% (ทั้งชุด 30.7%), Male 35.8% (ทั้งชุด 35.6%), Unknown 6.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 36.2% (ทั้งชุด 31.4%), 35-44 25.7% (ทั้งชุด 26.6%), 45-54 16.0% (ทั้งชุด 17.5%), 55-64 11.0% (ทั้งชุด 11.7%), 65-74 5.0% (ทั้งชุด 5.5%), <25 5.1% (ทั้งชุด 5.9%), >74 1.1% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 17 · กลุ่ม 6
- IF property_value > 7.6e+05 AND income ≤ 247.5 AND tract_to_msa_income_percentage > 152.6 THEN อยู่กลุ่มนี้
- IF property_value > 7.6e+05 AND income > 247.5 AND property_value ≤ 9.6e+05 THEN อยู่กลุ่มนี้
- IF property_value > 7.6e+05 AND income > 247.5 AND property_value > 9.6e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 637/231/204 · coverage กฎบน validation 0.0483
- Fidelity F1 0.7830 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9510 · ERM error 0.0392 · FPR 0.7000 · FNR 0.0052
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.7e-16), derived_msa-md (p_adj=0.00015), county_code (p_adj=1.4e-17), conforming_loan_limit (p_adj=0), derived_loan_product_type (p_adj=4.8e-22), loan_type (p_adj=2.3e-21), loan_amount (p_adj=8.1e-43), loan_term (p_adj=6.2e-06), property_value (p_adj=4e-45), construction_method (p_adj=0.00038), income (p_adj=3.2e-23), debt_to_income_ratio (p_adj=3.6e-19), aus-1 (p_adj=2.7e-09), ffiec_msa_md_median_family_income (p_adj=3.2e-18), tract_to_msa_income_percentage (p_adj=3.7e-42), tract_one_to_four_family_homes (p_adj=0.0022)
- องค์ประกอบ race_eth: Hispanic 3.9% (ทั้งชุด 9.1%), NH Asian 15.2% (ทั้งชุด 6.8%), NH Black 5.4% (ทั้งชุด 22.0%), NH White 54.9% (ทั้งชุด 41.8%), Other 2.5% (ทั้งชุด 2.3%), Unknown 18.1% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 12.7% (ทั้งชุด 27.1%), Joint 48.5% (ทั้งชุด 30.7%), Male 32.4% (ทั้งชุด 35.6%), Unknown 6.4% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 23.5% (ทั้งชุด 31.4%), 35-44 39.2% (ทั้งชุด 26.6%), 45-54 22.5% (ทั้งชุด 17.5%), 55-64 12.7% (ทั้งชุด 11.7%), 65-74 1.0% (ทั้งชุด 5.5%), <25 1.0% (ทั้งชุด 5.9%), >74 0.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 17 · กลุ่ม 7
- IF tract_owner_occupied_units > 1374 AND tract_population ≤ 5150 AND tract_median_age_of_housing_units ≤ 30.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1374 AND tract_population > 5150 AND aus-1_6 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2747/830/842 · coverage กฎบน validation 0.2162
- Fidelity F1 0.8224 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9121 · ERM error 0.0582 · FPR 0.5946 · FNR 0.0065
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.00034), derived_msa-md (p_adj=4e-38), county_code (p_adj=5.8e-134), conforming_loan_limit (p_adj=0.046), derived_loan_product_type (p_adj=8.5e-07), loan_type (p_adj=5.7e-07), loan_amount (p_adj=2.4e-10), loan_term (p_adj=2.8e-16), property_value (p_adj=8e-11), construction_method (p_adj=4e-17), debt_to_income_ratio (p_adj=0.0025), aus-1 (p_adj=6.7e-16), tract_population (p_adj=4.7e-242), ffiec_msa_md_median_family_income (p_adj=1.2e-24), tract_to_msa_income_percentage (p_adj=3.8e-36), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=8.1e-254), tract_median_age_of_housing_units (p_adj=3.1e-124)
- องค์ประกอบ race_eth: Hispanic 8.1% (ทั้งชุด 9.1%), NH Asian 8.8% (ทั้งชุด 6.8%), NH Black 19.0% (ทั้งชุด 22.0%), NH White 43.1% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.3%), Unknown 19.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 20.5% (ทั้งชุด 27.1%), Joint 32.4% (ทั้งชุด 30.7%), Male 40.4% (ทั้งชุด 35.6%), Unknown 6.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 29.3% (ทั้งชุด 31.4%), 35-44 28.5% (ทั้งชุด 26.6%), 45-54 19.7% (ทั้งชุด 17.5%), 55-64 11.3% (ทั้งชุด 11.7%), 65-74 5.6% (ทั้งชุด 5.5%), <25 4.0% (ทั้งชุด 5.9%), >74 1.5% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 0
- IF tract_population ≤ 357.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 150/43/57 · coverage กฎบน validation 0.0110
- Fidelity F1 0.9885 · เงื่อนไขรวม 1 · สูงสุดต่อเส้นทาง 1
- อนุมัติจริง 0.1053 · ERM error 0.0526 · FPR 0.0196 · FNR 0.3333
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.9e-137), derived_msa-md (p_adj=1.1e-15), county_code (p_adj=1.2e-120), derived_loan_product_type (p_adj=0.038), loan_type (p_adj=0.014), loan_amount (p_adj=9.7e-08), loan_term (p_adj=6e-15), property_value (p_adj=4.3e-28), construction_method (p_adj=1e-72), income (p_adj=3.1e-06), debt_to_income_ratio (p_adj=2.3e-06), applicant_credit_score_type (p_adj=3.8e-07), aus-1 (p_adj=4.2e-42), tract_population (p_adj=4.1e-86), ffiec_msa_md_median_family_income (p_adj=9.3e-05), tract_to_msa_income_percentage (p_adj=2.9e-36), tract_owner_occupied_units (p_adj=3.1e-100), tract_one_to_four_family_homes (p_adj=2.6e-74), tract_median_age_of_housing_units (p_adj=1.2e-26)
- องค์ประกอบ race_eth: Hispanic 3.5% (ทั้งชุด 9.1%), NH Asian 3.5% (ทั้งชุด 6.8%), NH Black 31.6% (ทั้งชุด 22.0%), NH White 45.6% (ทั้งชุด 41.8%), Other 3.5% (ทั้งชุด 2.3%), Unknown 12.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 47.4% (ทั้งชุด 27.1%), Joint 26.3% (ทั้งชุด 30.7%), Male 24.6% (ทั้งชุด 35.6%), Unknown 1.8% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.1% (ทั้งชุด 31.4%), 35-44 29.8% (ทั้งชุด 26.6%), 45-54 21.1% (ทั้งชุด 17.5%), 55-64 5.3% (ทั้งชุด 11.7%), 65-74 7.0% (ทั้งชุด 5.5%), <25 7.0% (ทั้งชุด 5.9%), >74 1.8% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 1
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 314/273/296 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 0.8311 · ERM error 0.0878 · FPR 0.5200 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: derived_msa-md (p_adj=8.7e-29), county_code (p_adj=1e-22), derived_loan_product_type (p_adj=1.2e-204), loan_type (p_adj=3.6e-207), loan_term (p_adj=1.8e-45), construction_method (p_adj=1.5e-05), income (p_adj=0.0041), debt_to_income_ratio (p_adj=1.8e-26), submission_of_application (p_adj=0.022), aus-1 (p_adj=3.2e-138), tract_population (p_adj=4.6e-18), ffiec_msa_md_median_family_income (p_adj=5.1e-288), tract_to_msa_income_percentage (p_adj=1.3e-06), tract_owner_occupied_units (p_adj=1.6e-22), tract_one_to_four_family_homes (p_adj=1.9e-42)
- องค์ประกอบ race_eth: Hispanic 12.5% (ทั้งชุด 9.1%), NH Asian 3.7% (ทั้งชุด 6.8%), NH Black 49.0% (ทั้งชุด 22.0%), NH White 14.5% (ทั้งชุด 41.8%), Other 0.7% (ทั้งชุด 2.3%), Unknown 19.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 41.2% (ทั้งชุด 27.1%), Joint 24.0% (ทั้งชุด 30.7%), Male 26.0% (ทั้งชุด 35.6%), Unknown 8.8% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.4% (ทั้งชุด 31.4%), 35-44 32.1% (ทั้งชุด 26.6%), 45-54 19.9% (ทั้งชุด 17.5%), 55-64 11.1% (ทั้งชุด 11.7%), 65-74 1.7% (ทั้งชุด 5.5%), <25 4.4% (ทั้งชุด 5.9%), >74 0.3% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 2
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 349/106/100 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 0.8500 · ERM error 0.0700 · FPR 0.3333 · FNR 0.0235
- ตัวแปรต่างชัดหลัง Bonferroni: derived_msa-md (p_adj=2e-43), county_code (p_adj=8.4e-24), derived_loan_product_type (p_adj=1.4e-33), loan_type (p_adj=1.2e-32), loan_amount (p_adj=4e-17), loan_term (p_adj=6.1e-31), property_value (p_adj=2.1e-24), income (p_adj=1e-17), aus-1 (p_adj=5.8e-20), ffiec_msa_md_median_family_income (p_adj=1.4e-08)
- องค์ประกอบ race_eth: Hispanic 5.0% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 28.0% (ทั้งชุด 22.0%), NH White 44.0% (ทั้งชุด 41.8%), Other 5.0% (ทั้งชุด 2.3%), Unknown 18.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 35.0% (ทั้งชุด 27.1%), Joint 24.0% (ทั้งชุด 30.7%), Male 36.0% (ทั้งชุด 35.6%), Unknown 5.0% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.0% (ทั้งชุด 31.4%), 35-44 22.0% (ทั้งชุด 26.6%), 45-54 14.0% (ทั้งชุด 17.5%), 55-64 15.0% (ทั้งชุด 11.7%), 65-74 7.0% (ทั้งชุด 5.5%), <25 8.0% (ทั้งชุด 5.9%), >74 4.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 3
- IF construction_method_2 > 0.5 AND tract_one_to_four_family_homes > 1716 AND loan_term ≤ 328.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 202/92/93 · coverage กฎบน validation 0.0248
- Fidelity F1 0.6911 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.3763 · ERM error 0.1720 · FPR 0.1034 · FNR 0.2857
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.5e-47), derived_msa-md (p_adj=9.8e-60), county_code (p_adj=7.2e-71), derived_loan_product_type (p_adj=6.6e-18), loan_type (p_adj=2.6e-08), lien_status (p_adj=9.6e-11), loan_amount (p_adj=1.3e-43), loan_term (p_adj=1.6e-11), property_value (p_adj=1.5e-29), construction_method (p_adj=5e-96), income (p_adj=2.9e-11), applicant_credit_score_type (p_adj=1.7e-89), submission_of_application (p_adj=0.027), initially_payable_to_institution (p_adj=0.032), aus-1 (p_adj=3e-74), tract_population (p_adj=0.0012), ffiec_msa_md_median_family_income (p_adj=1.2e-14), tract_owner_occupied_units (p_adj=5.7e-10), tract_one_to_four_family_homes (p_adj=1.1e-18)
- องค์ประกอบ race_eth: Hispanic 8.6% (ทั้งชุด 9.1%), NH Asian 1.1% (ทั้งชุด 6.8%), NH Black 19.4% (ทั้งชุด 22.0%), NH White 55.9% (ทั้งชุด 41.8%), Other 4.3% (ทั้งชุด 2.3%), Unknown 10.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 32.3% (ทั้งชุด 27.1%), Joint 37.6% (ทั้งชุด 30.7%), Male 28.0% (ทั้งชุด 35.6%), Unknown 2.2% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.1% (ทั้งชุด 31.4%), 35-44 23.7% (ทั้งชุด 26.6%), 45-54 18.3% (ทั้งชุด 17.5%), 55-64 8.6% (ทั้งชุด 11.7%), 65-74 6.5% (ทั้งชุด 5.5%), <25 10.8% (ทั้งชุด 5.9%), >74 2.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 4
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 147/125/122 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 0.6311 · ERM error 0.2131 · FPR 0.2222 · FNR 0.2078
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.5e-06), derived_msa-md (p_adj=9.1e-07), county_code (p_adj=4.9e-11), derived_loan_product_type (p_adj=3.5e-247), loan_type (p_adj=5.4e-13), lien_status (p_adj=9.2e-245), loan_amount (p_adj=3e-77), loan_term (p_adj=2.6e-15), property_value (p_adj=4.3e-35), construction_method (p_adj=5e-40), income (p_adj=4.6e-21), applicant_credit_score_type (p_adj=1e-15), aus-1 (p_adj=9.5e-94), ffiec_msa_md_median_family_income (p_adj=4.7e-122), tract_to_msa_income_percentage (p_adj=9.2e-11)
- องค์ประกอบ race_eth: Hispanic 8.2% (ทั้งชุด 9.1%), NH Asian 1.6% (ทั้งชุด 6.8%), NH Black 24.6% (ทั้งชุด 22.0%), NH White 36.1% (ทั้งชุด 41.8%), Other 2.5% (ทั้งชุด 2.3%), Unknown 27.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 32.8% (ทั้งชุด 27.1%), Joint 27.9% (ทั้งชุด 30.7%), Male 32.8% (ทั้งชุด 35.6%), Unknown 6.6% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 29.5% (ทั้งชุด 31.4%), 35-44 30.3% (ทั้งชุด 26.6%), 45-54 16.4% (ทั้งชุด 17.5%), 55-64 15.6% (ทั้งชุด 11.7%), 65-74 0.0% (ทั้งชุด 5.5%), <25 7.4% (ทั้งชุด 5.9%), >74 0.8% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 5
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 172/278/298 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 0.9329 · ERM error 0.0537 · FPR 0.7500 · FNR 0.0036
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2e-13), derived_msa-md (p_adj=9.8e-25), county_code (p_adj=2.5e-112), conforming_loan_limit (p_adj=1.8e-07), derived_loan_product_type (p_adj=2.9e-34), loan_type (p_adj=1.3e-32), loan_amount (p_adj=9.8e-75), property_value (p_adj=1.9e-75), construction_method (p_adj=1.3e-06), income (p_adj=4.9e-33), debt_to_income_ratio (p_adj=2.1e-14), initially_payable_to_institution (p_adj=0.013), aus-1 (p_adj=1.7e-12), tract_population (p_adj=8.8e-20), ffiec_msa_md_median_family_income (p_adj=6.2e-136), tract_to_msa_income_percentage (p_adj=8.4e-48), tract_owner_occupied_units (p_adj=9.5e-62), tract_one_to_four_family_homes (p_adj=4.4e-14), tract_median_age_of_housing_units (p_adj=9e-19)
- องค์ประกอบ race_eth: Hispanic 5.4% (ทั้งชุด 9.1%), NH Asian 23.5% (ทั้งชุด 6.8%), NH Black 9.7% (ทั้งชุด 22.0%), NH White 41.9% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.3%), Unknown 17.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 19.8% (ทั้งชุด 27.1%), Joint 40.6% (ทั้งชุด 30.7%), Male 33.2% (ทั้งชุด 35.6%), Unknown 6.4% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 25.8% (ทั้งชุด 31.4%), 35-44 38.6% (ทั้งชุด 26.6%), 45-54 20.8% (ทั้งชุด 17.5%), 55-64 9.1% (ทั้งชุด 11.7%), 65-74 4.7% (ทั้งชุด 5.5%), <25 0.0% (ทั้งชุด 5.9%), >74 1.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 6
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 241/379/397 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 0.8564 · ERM error 0.0680 · FPR 0.4035 · FNR 0.0118
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.001), derived_msa-md (p_adj=1.2e-43), county_code (p_adj=4.8e-47), derived_loan_product_type (p_adj=8.8e-49), loan_type (p_adj=5.4e-46), loan_amount (p_adj=6.5e-17), loan_term (p_adj=1.3e-20), property_value (p_adj=1.4e-21), construction_method (p_adj=6.6e-07), income (p_adj=7.8e-21), aus-1 (p_adj=8.1e-20), tract_population (p_adj=2.9e-36), ffiec_msa_md_median_family_income (p_adj=2.4e-296), tract_to_msa_income_percentage (p_adj=6e-40), tract_owner_occupied_units (p_adj=2.2e-89), tract_one_to_four_family_homes (p_adj=6.2e-63), tract_median_age_of_housing_units (p_adj=4e-16)
- องค์ประกอบ race_eth: Hispanic 17.4% (ทั้งชุด 9.1%), NH Asian 9.1% (ทั้งชุด 6.8%), NH Black 22.2% (ทั้งชุด 22.0%), NH White 31.5% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.3%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 36.8% (ทั้งชุด 27.1%), Joint 19.4% (ทั้งชุด 30.7%), Male 36.0% (ทั้งชุด 35.6%), Unknown 7.8% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 34.5% (ทั้งชุด 31.4%), 35-44 28.7% (ทั้งชุด 26.6%), 45-54 14.6% (ทั้งชุด 17.5%), 55-64 12.3% (ทั้งชุด 11.7%), 65-74 4.5% (ทั้งชุด 5.5%), <25 5.0% (ทั้งชุด 5.9%), >74 0.3% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 7
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 385/171/177 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 0.3785 · ERM error 0.2429 · FPR 0.1545 · FNR 0.3881
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.9e-202), derived_msa-md (p_adj=1.2e-119), county_code (p_adj=1.1e-244), derived_loan_product_type (p_adj=3.5e-21), loan_type (p_adj=1e-20), loan_amount (p_adj=5.7e-58), loan_term (p_adj=9.4e-29), property_value (p_adj=1.6e-153), construction_method (p_adj=4.6e-211), income (p_adj=7.5e-31), applicant_credit_score_type (p_adj=4.5e-142), submission_of_application (p_adj=1e-87), initially_payable_to_institution (p_adj=7.2e-88), aus-1 (p_adj=1.4e-216), tract_population (p_adj=1.4e-37), ffiec_msa_md_median_family_income (p_adj=3.5e-161), tract_to_msa_income_percentage (p_adj=0.0004), tract_owner_occupied_units (p_adj=5e-31), tract_median_age_of_housing_units (p_adj=3.4e-17)
- องค์ประกอบ race_eth: Hispanic 3.4% (ทั้งชุด 9.1%), NH Asian 0.6% (ทั้งชุด 6.8%), NH Black 26.0% (ทั้งชุด 22.0%), NH White 50.3% (ทั้งชุด 41.8%), Other 1.1% (ทั้งชุด 2.3%), Unknown 18.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 33.9% (ทั้งชุด 27.1%), Joint 31.6% (ทั้งชุด 30.7%), Male 30.5% (ทั้งชุด 35.6%), Unknown 4.0% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 29.4% (ทั้งชุด 31.4%), 35-44 20.3% (ทั้งชุด 26.6%), 45-54 17.5% (ทั้งชุด 17.5%), 55-64 14.7% (ทั้งชุด 11.7%), 65-74 5.6% (ทั้งชุด 5.5%), <25 10.7% (ทั้งชุด 5.9%), >74 1.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 8
- IF derived_loan_product_type_FHA:First Lien ≤ 0.5 AND derived_loan_product_type_FSA/RHS:First Lien > 0.5 THEN อยู่กลุ่มนี้
- IF derived_loan_product_type_FHA:First Lien > 0.5 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND ffiec_msa_md_median_family_income ≤ 7.71e+04 THEN อยู่กลุ่มนี้
- IF derived_loan_product_type_FHA:First Lien > 0.5 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND ffiec_msa_md_median_family_income > 7.71e+04 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 951/329/334 · coverage กฎบน validation 0.1030
- Fidelity F1 0.8853 · เงื่อนไขรวม 8 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8563 · ERM error 0.1078 · FPR 0.7292 · FNR 0.0035
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.9e-09), derived_msa-md (p_adj=7.4e-126), county_code (p_adj=1.2e-123), derived_loan_product_type (p_adj=5.3e-231), loan_type (p_adj=4.5e-233), loan_amount (p_adj=2.8e-55), loan_term (p_adj=8.5e-59), property_value (p_adj=3.8e-96), income (p_adj=5.6e-43), aus-1 (p_adj=6.7e-179), ffiec_msa_md_median_family_income (p_adj=1.6e-140), tract_owner_occupied_units (p_adj=0.0084), tract_median_age_of_housing_units (p_adj=2.3e-08)
- องค์ประกอบ race_eth: Hispanic 9.0% (ทั้งชุด 9.1%), NH Asian 0.3% (ทั้งชุด 6.8%), NH Black 24.0% (ทั้งชุด 22.0%), NH White 48.8% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.3%), Unknown 15.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 31.1% (ทั้งชุด 27.1%), Joint 28.7% (ทั้งชุด 30.7%), Male 32.6% (ทั้งชุด 35.6%), Unknown 7.5% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 37.7% (ทั้งชุด 31.4%), 35-44 24.0% (ทั้งชุด 26.6%), 45-54 13.8% (ทั้งชุด 17.5%), 55-64 10.8% (ทั้งชุด 11.7%), 65-74 3.3% (ทั้งชุด 5.5%), <25 10.2% (ทั้งชุด 5.9%), >74 0.3% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 9
- IF ffiec_msa_md_median_family_income > 1.015e+05 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND tract_owner_occupied_units ≤ 1594 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2850/549/545 · coverage กฎบน validation 0.3167
- Fidelity F1 0.5870 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9394 · ERM error 0.0404 · FPR 0.6061 · FNR 0.0039
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.9e-15), derived_msa-md (p_adj=1.2e-74), county_code (p_adj=2.1e-78), derived_loan_product_type (p_adj=8.9e-84), loan_type (p_adj=8.9e-79), loan_amount (p_adj=4.8e-26), property_value (p_adj=4.7e-37), construction_method (p_adj=1.2e-14), income (p_adj=8.1e-17), debt_to_income_ratio (p_adj=7.5e-22), submission_of_application (p_adj=1e-10), initially_payable_to_institution (p_adj=5e-06), aus-1 (p_adj=2.9e-76), tract_population (p_adj=1.1e-09), ffiec_msa_md_median_family_income (p_adj=0), tract_to_msa_income_percentage (p_adj=3.8e-12), tract_owner_occupied_units (p_adj=5.6e-07), tract_one_to_four_family_homes (p_adj=1.1e-42)
- องค์ประกอบ race_eth: Hispanic 8.6% (ทั้งชุด 9.1%), NH Asian 16.1% (ทั้งชุด 6.8%), NH Black 12.5% (ทั้งชุด 22.0%), NH White 44.8% (ทั้งชุด 41.8%), Other 2.9% (ทั้งชุด 2.3%), Unknown 15.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 24.2% (ทั้งชุด 27.1%), Joint 33.4% (ทั้งชุด 30.7%), Male 37.8% (ทั้งชุด 35.6%), Unknown 4.6% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 39.1% (ทั้งชุด 31.4%), 35-44 27.5% (ทั้งชุด 26.6%), 45-54 16.0% (ทั้งชุด 17.5%), 55-64 9.2% (ทั้งชุด 11.7%), 65-74 3.9% (ทั้งชุด 5.5%), <25 3.7% (ทั้งชุด 5.9%), >74 0.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 10
- IF ffiec_msa_md_median_family_income ≤ 1.015e+05 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND construction_method_1 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1216/410/371 · coverage กฎบน validation 0.1580
- Fidelity F1 0.7466 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9407 · ERM error 0.0350 · FPR 0.4545 · FNR 0.0086
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.3e-11), derived_msa-md (p_adj=2.1e-164), county_code (p_adj=9.1e-164), derived_loan_product_type (p_adj=2.2e-53), loan_type (p_adj=1.1e-50), loan_amount (p_adj=2.1e-05), loan_term (p_adj=2.9e-05), construction_method (p_adj=9.8e-05), debt_to_income_ratio (p_adj=4.5e-19), aus-1 (p_adj=4.7e-30), tract_population (p_adj=2.6e-11), ffiec_msa_md_median_family_income (p_adj=2e-112), tract_to_msa_income_percentage (p_adj=9.5e-05)
- องค์ประกอบ race_eth: Hispanic 7.0% (ทั้งชุด 9.1%), NH Asian 3.2% (ทั้งชุด 6.8%), NH Black 4.9% (ทั้งชุด 22.0%), NH White 66.3% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.3%), Unknown 15.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 21.3% (ทั้งชุด 27.1%), Joint 38.0% (ทั้งชุด 30.7%), Male 33.7% (ทั้งชุด 35.6%), Unknown 7.0% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 27.5% (ทั้งชุด 31.4%), 35-44 16.4% (ทั้งชุด 26.6%), 45-54 16.7% (ทั้งชุด 17.5%), 55-64 17.8% (ทั้งชุด 11.7%), 65-74 11.6% (ทั้งชุด 5.5%), <25 7.0% (ทั้งชุด 5.9%), >74 3.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 11
- IF tract_owner_occupied_units > 1583 AND tract_owner_occupied_units > 1839 AND loan_type_1 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1301/358/354 · coverage กฎบน validation 0.0493
- Fidelity F1 0.5477 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9181 · ERM error 0.0593 · FPR 0.6552 · FNR 0.0062
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0015), derived_msa-md (p_adj=2.6e-30), county_code (p_adj=2.1e-117), derived_loan_product_type (p_adj=8.8e-08), loan_type (p_adj=1.8e-07), loan_term (p_adj=0.00079), construction_method (p_adj=6.2e-07), submission_of_application (p_adj=0.018), aus-1 (p_adj=2.7e-11), tract_population (p_adj=4.8e-93), ffiec_msa_md_median_family_income (p_adj=8.1e-13), tract_to_msa_income_percentage (p_adj=7.1e-09), tract_owner_occupied_units (p_adj=2.3e-131), tract_one_to_four_family_homes (p_adj=5.8e-100), tract_median_age_of_housing_units (p_adj=2.8e-80)
- องค์ประกอบ race_eth: Hispanic 9.6% (ทั้งชุด 9.1%), NH Asian 6.8% (ทั้งชุด 6.8%), NH Black 13.8% (ทั้งชุด 22.0%), NH White 45.8% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.3%), Unknown 21.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 18.1% (ทั้งชุด 27.1%), Joint 32.8% (ทั้งชุด 30.7%), Male 41.8% (ทั้งชุด 35.6%), Unknown 7.3% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.2% (ทั้งชุด 31.4%), 35-44 26.8% (ทั้งชุด 26.6%), 45-54 19.2% (ทั้งชุด 17.5%), 55-64 13.6% (ทั้งชุด 11.7%), 65-74 5.6% (ทั้งชุด 5.5%), <25 4.2% (ทั้งชุด 5.9%), >74 2.3% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 12
- IF conforming_loan_limit_C ≤ 0.5 AND income > 309 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 283/99/73 · coverage กฎบน validation 0.0168
- Fidelity F1 0.7470 · เงื่อนไขรวม 2 · สูงสุดต่อเส้นทาง 2
- อนุมัติจริง 0.9452 · ERM error 0.0685 · FPR 1.0000 · FNR 0.0145
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.2e-23), conforming_loan_limit (p_adj=0), derived_loan_product_type (p_adj=1.3e-05), loan_type (p_adj=5e-06), loan_amount (p_adj=1.9e-18), loan_term (p_adj=5.9e-56), property_value (p_adj=1e-19), income (p_adj=6.5e-10), debt_to_income_ratio (p_adj=4.6e-07), aus-1 (p_adj=5e-20), ffiec_msa_md_median_family_income (p_adj=1.1e-05), tract_to_msa_income_percentage (p_adj=2.8e-12)
- องค์ประกอบ race_eth: Hispanic 4.1% (ทั้งชุด 9.1%), NH Asian 12.3% (ทั้งชุด 6.8%), NH Black 5.5% (ทั้งชุด 22.0%), NH White 54.8% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.3%), Unknown 20.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 8.2% (ทั้งชุด 27.1%), Joint 45.2% (ทั้งชุด 30.7%), Male 39.7% (ทั้งชุด 35.6%), Unknown 6.8% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 20.5% (ทั้งชุด 31.4%), 35-44 37.0% (ทั้งชุด 26.6%), 45-54 27.4% (ทั้งชุด 17.5%), 55-64 13.7% (ทั้งชุด 11.7%), 65-74 1.4% (ทั้งชุด 5.5%), <25 0.0% (ทั้งชุด 5.9%), >74 0.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 13
- IF derived_loan_product_type_VA:First Lien > 0.5 AND tract_owner_occupied_units ≤ 1904 AND aus-1_1 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF derived_loan_product_type_VA:First Lien > 0.5 AND tract_owner_occupied_units ≤ 1904 AND aus-1_1 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1338/448/455 · coverage กฎบน validation 0.1075
- Fidelity F1 0.8907 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8901 · ERM error 0.0747 · FPR 0.5600 · FNR 0.0148
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.1e-109), derived_msa-md (p_adj=1.3e-83), county_code (p_adj=2.4e-58), derived_loan_product_type (p_adj=0), loan_type (p_adj=0), loan_term (p_adj=5.4e-69), property_value (p_adj=5.2e-08), construction_method (p_adj=5.5e-07), income (p_adj=6.4e-11), debt_to_income_ratio (p_adj=8.4e-12), applicant_credit_score_type (p_adj=9e-05), aus-1 (p_adj=8.7e-65), ffiec_msa_md_median_family_income (p_adj=1.5e-14), tract_median_age_of_housing_units (p_adj=0.013)
- องค์ประกอบ race_eth: Hispanic 6.4% (ทั้งชุด 9.1%), NH Asian 1.8% (ทั้งชุด 6.8%), NH Black 27.3% (ทั้งชุด 22.0%), NH White 40.0% (ทั้งชุด 41.8%), Other 3.1% (ทั้งชุด 2.3%), Unknown 21.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 13.2% (ทั้งชุด 27.1%), Joint 31.9% (ทั้งชุด 30.7%), Male 48.6% (ทั้งชุด 35.6%), Unknown 6.4% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.8% (ทั้งชุด 31.4%), 35-44 24.2% (ทั้งชุด 26.6%), 45-54 15.8% (ทั้งชุด 17.5%), 55-64 11.4% (ทั้งชุด 11.7%), 65-74 9.7% (ทั้งชุด 5.5%), <25 7.5% (ทั้งชุด 5.9%), >74 2.6% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 14
- IF loan_type_2 > 0.5 AND derived_msa-md_12060 > 0.5 AND income ≤ 50.5 THEN อยู่กลุ่มนี้
- IF loan_type_2 > 0.5 AND derived_msa-md_12060 > 0.5 AND income > 50.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1510/286/285 · coverage กฎบน validation 0.1430
- Fidelity F1 0.6643 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8596 · ERM error 0.0877 · FPR 0.5500 · FNR 0.0122
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=6.2e-11), derived_msa-md (p_adj=1.6e-33), county_code (p_adj=3.3e-59), derived_loan_product_type (p_adj=2.6e-194), loan_type (p_adj=9.1e-197), loan_term (p_adj=6.3e-60), property_value (p_adj=7.3e-22), construction_method (p_adj=0.0024), income (p_adj=8.6e-30), debt_to_income_ratio (p_adj=1.1e-27), applicant_credit_score_type (p_adj=0.00026), aus-1 (p_adj=2.4e-96), tract_population (p_adj=4.2e-17), ffiec_msa_md_median_family_income (p_adj=0), tract_to_msa_income_percentage (p_adj=2.8e-34), tract_owner_occupied_units (p_adj=1.4e-07), tract_one_to_four_family_homes (p_adj=1.8e-11)
- องค์ประกอบ race_eth: Hispanic 13.7% (ทั้งชุด 9.1%), NH Asian 2.1% (ทั้งชุด 6.8%), NH Black 43.5% (ทั้งชุด 22.0%), NH White 21.4% (ทั้งชุด 41.8%), Other 1.1% (ทั้งชุด 2.3%), Unknown 18.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 38.2% (ทั้งชุด 27.1%), Joint 26.0% (ทั้งชุด 30.7%), Male 28.1% (ทั้งชุด 35.6%), Unknown 7.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 29.8% (ทั้งชุด 31.4%), 35-44 26.3% (ทั้งชุด 26.6%), 45-54 23.5% (ทั้งชุด 17.5%), 55-64 8.4% (ทั้งชุด 11.7%), 65-74 3.5% (ทั้งชุด 5.5%), <25 8.4% (ทั้งชุด 5.9%), >74 0.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k8 · seed 17 · กลุ่ม 15
- IF loan_amount ≤ 3e+04 AND tract_population ≤ 4288 THEN อยู่กลุ่มนี้
- IF loan_amount ≤ 3e+04 AND tract_population > 4288 THEN อยู่กลุ่มนี้
- IF loan_amount > 3e+04 AND initially_payable_to_institution_1111 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 591/54/43 · coverage กฎบน validation 0.0382
- Fidelity F1 0.1836 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 2
- อนุมัติจริง 0.5116 · ERM error 0.1860 · FPR 0.2857 · FNR 0.0909
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.8e-24), derived_msa-md (p_adj=8.1e-11), county_code (p_adj=6.5e-12), derived_loan_product_type (p_adj=6.3e-20), lien_status (p_adj=5.7e-20), loan_amount (p_adj=3.7e-16), loan_term (p_adj=0.0032), property_value (p_adj=7.9e-12), construction_method (p_adj=3.1e-10), income (p_adj=1.1e-07), applicant_credit_score_type (p_adj=6.7e-20), aus-1 (p_adj=1.4e-15), tract_population (p_adj=0.0086), ffiec_msa_md_median_family_income (p_adj=4.8e-11)
- องค์ประกอบ race_eth: Hispanic 7.0% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 23.3% (ทั้งชุด 22.0%), NH White 55.8% (ทั้งชุด 41.8%), Other 0.0% (ทั้งชุด 2.3%), Unknown 14.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 27.9% (ทั้งชุด 27.1%), Joint 18.6% (ทั้งชุด 30.7%), Male 44.2% (ทั้งชุด 35.6%), Unknown 9.3% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 41.9% (ทั้งชุด 31.4%), 35-44 18.6% (ทั้งชุด 26.6%), 45-54 16.3% (ทั้งชุด 17.5%), 55-64 4.7% (ทั้งชุด 11.7%), 65-74 9.3% (ทั้งชุด 5.5%), <25 4.7% (ทั้งชุด 5.9%), >74 4.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 17 · กลุ่ม 0
- IF debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 ≤ 0.5 AND tract_population ≤ 796.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND loan_term ≤ 352 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND loan_term > 352 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 695/205/230 · coverage กฎบน validation 0.0370
- Fidelity F1 0.7195 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.0217 · ERM error 0.0217 · FPR 0.0000 · FNR 1.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.1e-73), derived_msa-md (p_adj=8e-11), county_code (p_adj=1.6e-37), derived_loan_product_type (p_adj=5.8e-09), loan_type (p_adj=2.6e-09), loan_amount (p_adj=1.8e-23), loan_term (p_adj=1.7e-20), property_value (p_adj=1.2e-28), construction_method (p_adj=1.5e-123), income (p_adj=3.8e-53), debt_to_income_ratio (p_adj=7.8e-78), applicant_credit_score_type (p_adj=2.7e-40), initially_payable_to_institution (p_adj=8.2e-108), aus-1 (p_adj=1.3e-97), tract_population (p_adj=2e-14), ffiec_msa_md_median_family_income (p_adj=3e-08), tract_to_msa_income_percentage (p_adj=2.6e-18), tract_owner_occupied_units (p_adj=1.7e-14), tract_one_to_four_family_homes (p_adj=1.4e-06)
- องค์ประกอบ race_eth: Hispanic 10.0% (ทั้งชุด 9.1%), NH Asian 4.8% (ทั้งชุด 6.8%), NH Black 30.9% (ทั้งชุด 22.0%), NH White 35.2% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.3%), Unknown 17.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 41.7% (ทั้งชุด 27.1%), Joint 23.5% (ทั้งชุด 30.7%), Male 28.7% (ทั้งชุด 35.6%), Unknown 6.1% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.4% (ทั้งชุด 31.4%), 35-44 26.1% (ทั้งชุด 26.6%), 45-54 20.4% (ทั้งชุด 17.5%), 55-64 10.0% (ทั้งชุด 11.7%), 65-74 5.7% (ทั้งชุด 5.5%), <25 6.5% (ทั้งชุด 5.9%), >74 0.9% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 17 · กลุ่ม 1
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 1265/594/587 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 0.5741 · ERM error 0.2470 · FPR 0.2760 · FNR 0.2255
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=9e-58), derived_msa-md (p_adj=0.003), county_code (p_adj=1.1e-27), preapproval (p_adj=9.4e-05), loan_amount (p_adj=8e-35), loan_term (p_adj=5.3e-14), property_value (p_adj=5e-60), construction_method (p_adj=1.1e-106), income (p_adj=5.3e-37), applicant_credit_score_type (p_adj=3.3e-35), initially_payable_to_institution (p_adj=0.00014), aus-1 (p_adj=1.9e-129), tract_population (p_adj=0.0011), ffiec_msa_md_median_family_income (p_adj=0.00015), tract_to_msa_income_percentage (p_adj=2.2e-19), tract_owner_occupied_units (p_adj=0.00013)
- องค์ประกอบ race_eth: Hispanic 7.8% (ทั้งชุด 9.1%), NH Asian 2.9% (ทั้งชุด 6.8%), NH Black 32.4% (ทั้งชุด 22.0%), NH White 37.0% (ทั้งชุด 41.8%), Other 2.2% (ทั้งชุด 2.3%), Unknown 17.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 33.7% (ทั้งชุด 27.1%), Joint 26.6% (ทั้งชุด 30.7%), Male 33.7% (ทั้งชุด 35.6%), Unknown 6.0% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.7% (ทั้งชุด 31.4%), 35-44 24.7% (ทั้งชุด 26.6%), 45-54 17.5% (ทั้งชุด 17.5%), 55-64 13.1% (ทั้งชุด 11.7%), 65-74 3.7% (ทั้งชุด 5.5%), <25 9.0% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 17 · กลุ่ม 2
- IF preapproval_1 ≤ 0.5 AND debt_to_income_ratio ≤ 60 AND lei_549300FGXN1K3HLB1R50 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 8000/2546/2479 · coverage กฎบน validation 0.8735
- Fidelity F1 0.8354 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9306 · ERM error 0.0694 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=7e-162), derived_msa-md (p_adj=6.7e-13), county_code (p_adj=1.5e-15), derived_loan_product_type (p_adj=5.9e-09), preapproval (p_adj=6.8e-64), loan_type (p_adj=4.8e-09), loan_amount (p_adj=5.5e-06), loan_term (p_adj=3.6e-15), property_value (p_adj=9.4e-06), construction_method (p_adj=5.8e-94), debt_to_income_ratio (p_adj=6.4e-07), applicant_credit_score_type (p_adj=7.1e-39), submission_of_application (p_adj=0.035), initially_payable_to_institution (p_adj=1.6e-34), aus-1 (p_adj=8.6e-82), tract_population (p_adj=0.0019), ffiec_msa_md_median_family_income (p_adj=9.6e-13), tract_to_msa_income_percentage (p_adj=0.03), tract_owner_occupied_units (p_adj=0.014)
- องค์ประกอบ race_eth: Hispanic 10.5% (ทั้งชุด 9.1%), NH Asian 8.0% (ทั้งชุด 6.8%), NH Black 21.0% (ทั้งชุด 22.0%), NH White 40.3% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.3%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 25.9% (ทั้งชุด 27.1%), Joint 31.1% (ทั้งชุด 30.7%), Male 36.9% (ทั้งชุด 35.6%), Unknown 6.1% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 31.9% (ทั้งชุด 31.4%), 35-44 26.5% (ทั้งชุด 26.6%), 45-54 18.0% (ทั้งชุด 17.5%), 55-64 11.3% (ทั้งชุด 11.7%), 65-74 5.7% (ทั้งชุด 5.5%), <25 5.3% (ทั้งชุด 5.9%), >74 1.3% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 17 · กลุ่ม 3
- IF preapproval_1 ≤ 0.5 AND lei_549300MGPZBLQDIL7538 ≤ 0.5 AND lei_549300FGXN1K3HLB1R50 > 0.5 THEN อยู่กลุ่มนี้
- IF preapproval_1 ≤ 0.5 AND lei_549300MGPZBLQDIL7538 > 0.5 AND property_value ≤ 3.3e+05 THEN อยู่กลุ่มนี้
- IF preapproval_1 ≤ 0.5 AND lei_549300MGPZBLQDIL7538 > 0.5 AND property_value > 3.3e+05 THEN อยู่กลุ่มนี้
- IF preapproval_1 > 0.5 AND income ≤ 81.5 THEN อยู่กลุ่มนี้
- IF preapproval_1 > 0.5 AND income > 81.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2040/655/704 · coverage กฎบน validation 0.1040
- Fidelity F1 0.6443 · เงื่อนไขรวม 13 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9915 · ERM error 0.0085 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.9e-194), derived_msa-md (p_adj=0.019), county_code (p_adj=1.7e-12), derived_loan_product_type (p_adj=1e-07), preapproval (p_adj=2.3e-184), loan_type (p_adj=1.8e-07), loan_amount (p_adj=1.9e-05), loan_term (p_adj=1.6e-05), property_value (p_adj=6.7e-09), construction_method (p_adj=8.6e-15), income (p_adj=1.1e-06), debt_to_income_ratio (p_adj=1.3e-20), submission_of_application (p_adj=0.0028), initially_payable_to_institution (p_adj=7e-06), aus-1 (p_adj=3.4e-34), tract_to_msa_income_percentage (p_adj=6.8e-14), tract_owner_occupied_units (p_adj=0.0029)
- องค์ประกอบ race_eth: Hispanic 5.0% (ทั้งชุด 9.1%), NH Asian 6.4% (ทั้งชุด 6.8%), NH Black 13.9% (ทั้งชุด 22.0%), NH White 53.1% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.3%), Unknown 19.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 21.2% (ทั้งชุด 27.1%), Joint 35.2% (ทั้งชุด 30.7%), Male 35.1% (ทั้งชุด 35.6%), Unknown 8.5% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 30.7% (ทั้งชุด 31.4%), 35-44 28.6% (ทั้งชุด 26.6%), 45-54 15.2% (ทั้งชุด 17.5%), 55-64 12.4% (ทั้งชุด 11.7%), 65-74 6.0% (ทั้งชุด 5.5%), <25 5.5% (ทั้งชุด 5.9%), >74 1.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 17 · กลุ่ม 0
- IF loan_term ≤ 306 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND tract_owner_occupied_units ≤ 1372 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 306 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND tract_owner_occupied_units > 1372 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 306 AND ffiec_msa_md_median_family_income > 1.015e+05 AND loan_amount ≤ 8e+04 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 970/296/304 · coverage กฎบน validation 0.0835
- Fidelity F1 0.9143 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.3882 · ERM error 0.1743 · FPR 0.0699 · FNR 0.3390
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=7.3e-213), derived_msa-md (p_adj=8.3e-87), county_code (p_adj=2.3e-148), derived_loan_product_type (p_adj=6.2e-76), loan_type (p_adj=3.1e-39), lien_status (p_adj=5.3e-46), loan_amount (p_adj=2.6e-216), loan_term (p_adj=2.1e-72), property_value (p_adj=1.1e-147), construction_method (p_adj=0), income (p_adj=3.4e-65), applicant_credit_score_type (p_adj=3.6e-118), aus-1 (p_adj=4.4e-258), tract_population (p_adj=2.3e-27), ffiec_msa_md_median_family_income (p_adj=2.9e-52), tract_to_msa_income_percentage (p_adj=4.4e-24), tract_owner_occupied_units (p_adj=1.4e-21), tract_one_to_four_family_homes (p_adj=0.0045)
- องค์ประกอบ race_eth: Hispanic 4.6% (ทั้งชุด 9.1%), NH Asian 1.6% (ทั้งชุด 6.8%), NH Black 28.3% (ทั้งชุด 22.0%), NH White 43.8% (ทั้งชุด 41.8%), Other 1.3% (ทั้งชุด 2.3%), Unknown 20.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 38.8% (ทั้งชุด 27.1%), Joint 27.0% (ทั้งชุด 30.7%), Male 28.9% (ทั้งชุด 35.6%), Unknown 5.3% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 31.2% (ทั้งชุด 31.4%), 35-44 23.7% (ทั้งชุด 26.6%), 45-54 19.1% (ทั้งชุด 17.5%), 55-64 9.9% (ทั้งชุด 11.7%), 65-74 6.2% (ทั้งชุด 5.5%), <25 7.9% (ทั้งชุด 5.9%), >74 2.0% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 17 · กลุ่ม 1
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND loan_term > 334 AND tract_owner_occupied_units ≤ 1420 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2208/766/699 · coverage กฎบน validation 0.1913
- Fidelity F1 0.9001 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8512 · ERM error 0.0916 · FPR 0.5385 · FNR 0.0134
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=8.2e-23), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.016), derived_loan_product_type (p_adj=1.2e-32), loan_type (p_adj=7.3e-34), loan_amount (p_adj=4.5e-89), loan_term (p_adj=1.1e-66), property_value (p_adj=1.2e-101), income (p_adj=1e-44), applicant_credit_score_type (p_adj=7.7e-10), submission_of_application (p_adj=6.5e-10), initially_payable_to_institution (p_adj=8.9e-10), aus-1 (p_adj=6.5e-22), tract_population (p_adj=1.1e-39), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=2.8e-55), tract_median_age_of_housing_units (p_adj=4.3e-23)
- องค์ประกอบ race_eth: Hispanic 7.9% (ทั้งชุด 9.1%), NH Asian 1.3% (ทั้งชุด 6.8%), NH Black 17.6% (ทั้งชุด 22.0%), NH White 55.5% (ทั้งชุด 41.8%), Other 3.0% (ทั้งชุด 2.3%), Unknown 14.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 24.3% (ทั้งชุด 27.1%), Joint 30.0% (ทั้งชุด 30.7%), Male 38.2% (ทั้งชุด 35.6%), Unknown 7.4% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 32.8% (ทั้งชุด 31.4%), 35-44 22.3% (ทั้งชุด 26.6%), 45-54 14.4% (ทั้งชุด 17.5%), 55-64 12.6% (ทั้งชุด 11.7%), 65-74 6.4% (ทั้งชุด 5.5%), <25 9.7% (ทั้งชุด 5.9%), >74 1.7% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 17 · กลุ่ม 2
- IF ffiec_msa_md_median_family_income > 8.405e+04 AND tract_owner_occupied_units ≤ 1112 AND property_value ≤ 5.5e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3992/1319/1353 · coverage กฎบน validation 0.3078
- Fidelity F1 0.8141 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8492 · ERM error 0.0820 · FPR 0.4314 · FNR 0.0200
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0012), derived_msa-md (p_adj=3.1e-166), county_code (p_adj=3.8e-171), conforming_loan_limit (p_adj=7.2e-07), derived_loan_product_type (p_adj=7.2e-09), loan_type (p_adj=1.7e-09), loan_amount (p_adj=6.1e-16), loan_term (p_adj=3.3e-15), property_value (p_adj=1.4e-28), construction_method (p_adj=6.8e-11), income (p_adj=1.1e-23), debt_to_income_ratio (p_adj=2.3e-08), applicant_credit_score_type (p_adj=0.04), aus-1 (p_adj=2.3e-08), tract_population (p_adj=7.2e-133), ffiec_msa_md_median_family_income (p_adj=9.4e-273), tract_to_msa_income_percentage (p_adj=6.2e-108), tract_owner_occupied_units (p_adj=2.6e-261), tract_one_to_four_family_homes (p_adj=6e-228), tract_median_age_of_housing_units (p_adj=2.9e-25)
- องค์ประกอบ race_eth: Hispanic 12.7% (ทั้งชุด 9.1%), NH Asian 7.0% (ทั้งชุด 6.8%), NH Black 26.8% (ทั้งชุด 22.0%), NH White 33.7% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.3%), Unknown 17.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 33.4% (ทั้งชุด 27.1%), Joint 26.1% (ทั้งชุด 30.7%), Male 34.4% (ทั้งชุด 35.6%), Unknown 6.1% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 34.5% (ทั้งชุด 31.4%), 35-44 24.8% (ทั้งชุด 26.6%), 45-54 17.2% (ทั้งชุด 17.5%), 55-64 11.2% (ทั้งชุด 11.7%), 65-74 4.8% (ทั้งชุด 5.5%), <25 6.3% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 17 · กลุ่ม 3
- IF tract_owner_occupied_units ≤ 1254 AND property_value > 4.4e+05 AND tract_owner_occupied_units > 878 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value ≤ 2.6e+05 AND tract_population > 6030 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.6e+05 AND tract_owner_occupied_units ≤ 1416 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.6e+05 AND tract_owner_occupied_units > 1416 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4830/1619/1644 · coverage กฎบน validation 0.3795
- Fidelity F1 0.8479 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9033 · ERM error 0.0608 · FPR 0.5660 · FNR 0.0067
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.1e-16), derived_msa-md (p_adj=3.2e-63), county_code (p_adj=6.7e-121), conforming_loan_limit (p_adj=1e-24), derived_loan_product_type (p_adj=2.2e-16), loan_type (p_adj=1.6e-12), lien_status (p_adj=0.021), loan_amount (p_adj=1.4e-138), loan_term (p_adj=1.4e-21), property_value (p_adj=1.6e-137), construction_method (p_adj=1.6e-49), income (p_adj=5.4e-63), debt_to_income_ratio (p_adj=1.7e-14), applicant_credit_score_type (p_adj=6.2e-06), aus-1 (p_adj=1e-31), tract_population (p_adj=8.4e-269), ffiec_msa_md_median_family_income (p_adj=9.7e-64), tract_to_msa_income_percentage (p_adj=1.6e-158), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=1.5e-213), tract_median_age_of_housing_units (p_adj=3.6e-104)
- องค์ประกอบ race_eth: Hispanic 7.5% (ทั้งชุด 9.1%), NH Asian 9.9% (ทั้งชุด 6.8%), NH Black 18.7% (ทั้งชุด 22.0%), NH White 42.2% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.3%), Unknown 19.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 21.0% (ทั้งชุด 27.1%), Joint 35.5% (ทั้งชุด 30.7%), Male 36.9% (ทั้งชุด 35.6%), Unknown 6.7% (ทั้งชุด 6.5%)
- องค์ประกอบ age: 25-34 28.3% (ทั้งชุด 31.4%), 35-44 30.5% (ทั้งชุด 26.6%), 45-54 18.9% (ทั้งชุด 17.5%), 55-64 12.0% (ทั้งชุด 11.7%), 65-74 5.4% (ทั้งชุด 5.5%), <25 3.7% (ทั้งชุด 5.9%), >74 1.2% (ทั้งชุด 1.4%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 29 · กลุ่ม 0
- IF initially_payable_to_institution_3 ≤ 0.5 AND debt_to_income_ratio > 60 AND construction_method_1 > 0.5 THEN อยู่กลุ่มนี้
- IF initially_payable_to_institution_3 > 0.5 AND tract_to_msa_income_percentage ≤ 99.99 THEN อยู่กลุ่มนี้
- IF initially_payable_to_institution_3 > 0.5 AND tract_to_msa_income_percentage > 99.99 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1129/589/617 · coverage กฎบน validation 0.0430
- Fidelity F1 0.1840 · เงื่อนไขรวม 7 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8023 · ERM error 0.0972 · FPR 0.4590 · FNR 0.0081
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.2e-10), derived_msa-md (p_adj=1e-44), county_code (p_adj=8.3e-31), conforming_loan_limit (p_adj=0.037), derived_loan_product_type (p_adj=1.4e-90), loan_type (p_adj=1.1e-91), loan_term (p_adj=1.5e-62), property_value (p_adj=4.2e-05), construction_method (p_adj=5.9e-10), income (p_adj=3.4e-28), debt_to_income_ratio (p_adj=6.2e-137), aus-1 (p_adj=1.6e-48), tract_population (p_adj=6e-07), ffiec_msa_md_median_family_income (p_adj=6e-107), tract_median_age_of_housing_units (p_adj=0.0023)
- องค์ประกอบ race_eth: Hispanic 12.6% (ทั้งชุด 9.1%), NH Asian 5.0% (ทั้งชุด 6.8%), NH Black 32.7% (ทั้งชุด 22.0%), NH White 24.6% (ทั้งชุด 41.8%), Other 3.1% (ทั้งชุด 2.4%), Unknown 21.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 31.1% (ทั้งชุด 28.3%), Joint 26.4% (ทั้งชุด 30.0%), Male 34.5% (ทั้งชุด 35.3%), Unknown 7.9% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.7% (ทั้งชุด 29.9%), 35-44 29.0% (ทั้งชุด 27.0%), 45-54 18.3% (ทั้งชุด 17.5%), 55-64 11.2% (ทั้งชุด 11.8%), 65-74 6.0% (ทั้งชุด 5.2%), <25 5.3% (ทั้งชุด 7.2%), >74 1.5% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 29 · กลุ่ม 1
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 2/2/6 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 1.0000 · ERM error 0.0000 · FPR N/A · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.8e-134), loan_term (p_adj=3e-67), applicant_credit_score_type (p_adj=0.01), submission_of_application (p_adj=1.5e-06), initially_payable_to_institution (p_adj=7.3e-06), aus-1 (p_adj=3.7e-05)
- องค์ประกอบ race_eth: Hispanic 0.0% (ทั้งชุด 9.1%), NH Asian 16.7% (ทั้งชุด 6.8%), NH Black 33.3% (ทั้งชุด 22.0%), NH White 50.0% (ทั้งชุด 41.8%), Other 0.0% (ทั้งชุด 2.4%), Unknown 0.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 16.7% (ทั้งชุด 28.3%), Joint 50.0% (ทั้งชุด 30.0%), Male 33.3% (ทั้งชุด 35.3%), Unknown 0.0% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 50.0% (ทั้งชุด 29.9%), 35-44 33.3% (ทั้งชุด 27.0%), 45-54 0.0% (ทั้งชุด 17.5%), 55-64 16.7% (ทั้งชุด 11.8%), 65-74 0.0% (ทั้งชุด 5.2%), <25 0.0% (ทั้งชุด 7.2%), >74 0.0% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 29 · กลุ่ม 2
- IF construction_method_1 ≤ 0.5 AND aus-1_6 > 0.5 AND tract_population > 1514 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 684/362/342 · coverage กฎบน validation 0.0717
- Fidelity F1 0.8228 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.3918 · ERM error 0.1871 · FPR 0.1587 · FNR 0.2313
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.2e-243), derived_msa-md (p_adj=7e-61), county_code (p_adj=1.5e-130), derived_loan_product_type (p_adj=2.1e-74), loan_type (p_adj=9.6e-43), lien_status (p_adj=2.7e-40), loan_amount (p_adj=1e-228), loan_term (p_adj=1.7e-82), property_value (p_adj=1.2e-150), construction_method (p_adj=0), income (p_adj=6.2e-64), applicant_credit_score_type (p_adj=8.2e-156), initially_payable_to_institution (p_adj=0.027), aus-1 (p_adj=1.6e-286), tract_population (p_adj=1.9e-18), ffiec_msa_md_median_family_income (p_adj=2.6e-36), tract_to_msa_income_percentage (p_adj=6.8e-17), tract_owner_occupied_units (p_adj=6.6e-16), tract_median_age_of_housing_units (p_adj=8.3e-13)
- องค์ประกอบ race_eth: Hispanic 10.2% (ทั้งชุด 9.1%), NH Asian 2.3% (ทั้งชุด 6.8%), NH Black 22.8% (ทั้งชุด 22.0%), NH White 44.7% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.4%), Unknown 17.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 41.2% (ทั้งชุด 28.3%), Joint 27.5% (ทั้งชุด 30.0%), Male 28.1% (ทั้งชุด 35.3%), Unknown 3.2% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 26.3% (ทั้งชุด 29.9%), 35-44 24.3% (ทั้งชุด 27.0%), 45-54 17.3% (ทั้งชุด 17.5%), 55-64 13.2% (ทั้งชุด 11.8%), 65-74 7.3% (ทั้งชุด 5.2%), <25 10.8% (ทั้งชุด 7.2%), >74 0.9% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 29 · กลุ่ม 3
- IF tract_population ≤ 95.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 145/58/41 · coverage กฎบน validation 0.0145
- Fidelity F1 1.0000 · เงื่อนไขรวม 1 · สูงสุดต่อเส้นทาง 1
- อนุมัติจริง 0.0732 · ERM error 0.0976 · FPR 0.0526 · FNR 0.6667
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.4e-76), derived_msa-md (p_adj=7.8e-09), county_code (p_adj=2.4e-142), loan_amount (p_adj=1.6e-12), loan_term (p_adj=2e-11), property_value (p_adj=6.8e-14), construction_method (p_adj=4e-59), income (p_adj=6.2e-06), applicant_credit_score_type (p_adj=0.0069), aus-1 (p_adj=8.2e-31), tract_population (p_adj=2.9e-182), ffiec_msa_md_median_family_income (p_adj=0.0069), tract_to_msa_income_percentage (p_adj=0), tract_owner_occupied_units (p_adj=9.5e-100), tract_one_to_four_family_homes (p_adj=1.1e-89), tract_median_age_of_housing_units (p_adj=2.9e-50)
- องค์ประกอบ race_eth: Hispanic 0.0% (ทั้งชุด 9.1%), NH Asian 2.4% (ทั้งชุด 6.8%), NH Black 46.3% (ทั้งชุด 22.0%), NH White 48.8% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.4%), Unknown 0.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 53.7% (ทั้งชุด 28.3%), Joint 26.8% (ทั้งชุด 30.0%), Male 19.5% (ทั้งชุด 35.3%), Unknown 0.0% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 41.5% (ทั้งชุด 29.9%), 35-44 26.8% (ทั้งชุด 27.0%), 45-54 12.2% (ทั้งชุด 17.5%), 55-64 7.3% (ทั้งชุด 11.8%), 65-74 4.9% (ทั้งชุด 5.2%), <25 7.3% (ทั้งชุด 7.2%), >74 0.0% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 29 · กลุ่ม 4
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND aus-1_6 ≤ 0.5 AND tract_owner_occupied_units ≤ 1781 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2637/801/774 · coverage กฎบน validation 0.1913
- Fidelity F1 0.8799 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8992 · ERM error 0.0904 · FPR 0.7692 · FNR 0.0144
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.5e-15), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.0018), derived_loan_product_type (p_adj=2.4e-35), loan_type (p_adj=3.3e-36), loan_amount (p_adj=2e-87), loan_term (p_adj=7.2e-65), property_value (p_adj=9.7e-88), income (p_adj=8.3e-33), applicant_credit_score_type (p_adj=2e-05), submission_of_application (p_adj=0.00027), initially_payable_to_institution (p_adj=2.1e-08), aus-1 (p_adj=3e-24), tract_population (p_adj=7.4e-15), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=1.4e-21), tract_one_to_four_family_homes (p_adj=0.0078), tract_median_age_of_housing_units (p_adj=4.4e-29)
- องค์ประกอบ race_eth: Hispanic 8.0% (ทั้งชุด 9.1%), NH Asian 2.3% (ทั้งชุด 6.8%), NH Black 15.5% (ทั้งชุด 22.0%), NH White 56.7% (ทั้งชุด 41.8%), Other 2.5% (ทั้งชุด 2.4%), Unknown 15.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 25.1% (ทั้งชุด 28.3%), Joint 29.5% (ทั้งชุด 30.0%), Male 39.5% (ทั้งชุด 35.3%), Unknown 5.9% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.4% (ทั้งชุด 29.9%), 35-44 23.5% (ทั้งชุด 27.0%), 45-54 15.9% (ทั้งชุด 17.5%), 55-64 11.5% (ทั้งชุด 11.8%), 65-74 6.6% (ทั้งชุด 5.2%), <25 12.8% (ทั้งชุด 7.2%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 29 · กลุ่ม 5
- IF property_value ≤ 7.1e+05 AND property_value > 5.9e+05 AND tract_to_msa_income_percentage > 173.8 THEN อยู่กลุ่มนี้
- IF property_value > 7.1e+05 AND income > 172.5 AND tract_population ≤ 5539 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 810/276/287 · coverage กฎบน validation 0.0578
- Fidelity F1 0.7337 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9303 · ERM error 0.0592 · FPR 0.8000 · FNR 0.0037
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=7.7e-15), derived_msa-md (p_adj=5.4e-12), county_code (p_adj=2.1e-27), conforming_loan_limit (p_adj=5.5e-263), derived_loan_product_type (p_adj=4.8e-31), loan_type (p_adj=2.7e-29), loan_amount (p_adj=3.9e-60), property_value (p_adj=3e-54), construction_method (p_adj=9.9e-06), income (p_adj=4.4e-28), debt_to_income_ratio (p_adj=1.8e-19), aus-1 (p_adj=4.4e-23), tract_population (p_adj=7.5e-08), ffiec_msa_md_median_family_income (p_adj=1.9e-35), tract_to_msa_income_percentage (p_adj=9.2e-57), tract_one_to_four_family_homes (p_adj=2.9e-10)
- องค์ประกอบ race_eth: Hispanic 3.1% (ทั้งชุด 9.1%), NH Asian 16.0% (ทั้งชุด 6.8%), NH Black 11.5% (ทั้งชุด 22.0%), NH White 47.0% (ทั้งชุด 41.8%), Other 3.8% (ทั้งชุด 2.4%), Unknown 18.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 10.8% (ทั้งชุด 28.3%), Joint 49.5% (ทั้งชุด 30.0%), Male 33.4% (ทั้งชุด 35.3%), Unknown 6.3% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 24.0% (ทั้งชุด 29.9%), 35-44 36.2% (ทั้งชุด 27.0%), 45-54 24.4% (ทั้งชุด 17.5%), 55-64 13.9% (ทั้งชุด 11.8%), 65-74 0.7% (ทั้งชุด 5.2%), <25 0.3% (ทั้งชุด 7.2%), >74 0.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 29 · กลุ่ม 6
- IF tract_owner_occupied_units > 1413 AND ffiec_msa_md_median_family_income ≤ 7.71e+04 AND tract_owner_occupied_units > 1748 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1413 AND ffiec_msa_md_median_family_income > 7.71e+04 AND loan_amount ≤ 6.6e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2664/829/872 · coverage กฎบน validation 0.2010
- Fidelity F1 0.8267 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9197 · ERM error 0.0642 · FPR 0.7286 · FNR 0.0062
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0032), derived_msa-md (p_adj=6.4e-41), county_code (p_adj=1.9e-136), conforming_loan_limit (p_adj=0.0032), derived_loan_product_type (p_adj=0.00028), loan_type (p_adj=0.00036), loan_amount (p_adj=1e-13), loan_term (p_adj=6e-15), property_value (p_adj=3e-08), construction_method (p_adj=1.5e-16), debt_to_income_ratio (p_adj=1e-05), aus-1 (p_adj=1.1e-15), tract_population (p_adj=6.2e-256), ffiec_msa_md_median_family_income (p_adj=1.5e-38), tract_to_msa_income_percentage (p_adj=4.6e-34), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=2.4e-266), tract_median_age_of_housing_units (p_adj=7e-132)
- องค์ประกอบ race_eth: Hispanic 6.5% (ทั้งชุด 9.1%), NH Asian 9.9% (ทั้งชุด 6.8%), NH Black 17.1% (ทั้งชุด 22.0%), NH White 43.6% (ทั้งชุด 41.8%), Other 1.6% (ทั้งชุด 2.4%), Unknown 21.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 23.2% (ทั้งชุด 28.3%), Joint 33.6% (ทั้งชุด 30.0%), Male 35.3% (ทั้งชุด 35.3%), Unknown 7.9% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 29.1% (ทั้งชุด 29.9%), 35-44 29.7% (ทั้งชุด 27.0%), 45-54 17.7% (ทั้งชุด 17.5%), 55-64 12.6% (ทั้งชุด 11.8%), 65-74 5.5% (ทั้งชุด 5.2%), <25 4.6% (ทั้งชุด 7.2%), >74 0.7% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 29 · กลุ่ม 7
- IF ffiec_msa_md_median_family_income ≤ 9.11e+04 AND ffiec_msa_md_median_family_income > 8.405e+04 AND tract_one_to_four_family_homes ≤ 1365 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 9.11e+04 AND tract_owner_occupied_units ≤ 1298 AND property_value ≤ 6.7e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3929/1083/1061 · coverage กฎบน validation 0.4055
- Fidelity F1 0.7623 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8897 · ERM error 0.0829 · FPR 0.7265 · FNR 0.0032
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.00096), derived_msa-md (p_adj=4e-121), county_code (p_adj=3.4e-113), conforming_loan_limit (p_adj=1.4e-05), derived_loan_product_type (p_adj=7.6e-08), loan_type (p_adj=4.9e-06), loan_amount (p_adj=0.038), loan_term (p_adj=3.6e-40), property_value (p_adj=0.00033), construction_method (p_adj=6.6e-19), income (p_adj=0.018), debt_to_income_ratio (p_adj=1.3e-06), aus-1 (p_adj=5.4e-27), tract_population (p_adj=3.7e-171), ffiec_msa_md_median_family_income (p_adj=2.6e-293), tract_to_msa_income_percentage (p_adj=5.6e-59), tract_owner_occupied_units (p_adj=1.8e-283), tract_one_to_four_family_homes (p_adj=8.5e-291), tract_median_age_of_housing_units (p_adj=9e-17)
- องค์ประกอบ race_eth: Hispanic 11.6% (ทั้งชุด 9.1%), NH Asian 7.4% (ทั้งชุด 6.8%), NH Black 26.0% (ทั้งชุด 22.0%), NH White 36.6% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.4%), Unknown 16.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 32.9% (ทั้งชุด 28.3%), Joint 25.1% (ทั้งชุด 30.0%), Male 36.0% (ทั้งชุด 35.3%), Unknown 6.0% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 34.7% (ทั้งชุด 29.9%), 35-44 24.3% (ทั้งชุด 27.0%), 45-54 16.7% (ทั้งชุด 17.5%), 55-64 10.7% (ทั้งชุด 11.8%), 65-74 4.1% (ทั้งชุด 5.2%), <25 7.2% (ทั้งชุด 7.2%), >74 2.4% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 29 · กลุ่ม 0
- IF initially_payable_to_institution_3 ≤ 0.5 AND debt_to_income_ratio > 60 AND construction_method_1 > 0.5 THEN อยู่กลุ่มนี้
- IF initially_payable_to_institution_3 > 0.5 AND property_value ≤ 3.4e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 857/837/842 · coverage กฎบน validation 0.0335
- Fidelity F1 0.1092 · เงื่อนไขรวม 5 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8409 · ERM error 0.0926 · FPR 0.5522 · FNR 0.0056
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.1e-25), derived_msa-md (p_adj=9.9e-42), county_code (p_adj=4.6e-53), conforming_loan_limit (p_adj=0.00045), derived_loan_product_type (p_adj=0), loan_type (p_adj=0), lien_status (p_adj=0.004), loan_amount (p_adj=0.00019), loan_term (p_adj=7.4e-50), property_value (p_adj=1.8e-48), construction_method (p_adj=4.9e-10), income (p_adj=4.7e-45), debt_to_income_ratio (p_adj=2.8e-82), applicant_credit_score_type (p_adj=1e-05), initially_payable_to_institution (p_adj=4.4e-08), aus-1 (p_adj=0), ffiec_msa_md_median_family_income (p_adj=6.3e-88), tract_to_msa_income_percentage (p_adj=2.1e-57), tract_owner_occupied_units (p_adj=7.9e-15), tract_one_to_four_family_homes (p_adj=7.8e-13)
- องค์ประกอบ race_eth: Hispanic 12.0% (ทั้งชุด 9.1%), NH Asian 1.9% (ทั้งชุด 6.8%), NH Black 40.0% (ทั้งชุด 22.0%), NH White 24.2% (ทั้งชุด 41.8%), Other 1.8% (ทั้งชุด 2.4%), Unknown 20.1% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.0% (ทั้งชุด 28.3%), Joint 26.5% (ทั้งชุด 30.0%), Male 32.8% (ทั้งชุด 35.3%), Unknown 6.8% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 30.9% (ทั้งชุด 29.9%), 35-44 27.6% (ทั้งชุด 27.0%), 45-54 18.8% (ทั้งชุด 17.5%), 55-64 10.2% (ทั้งชุด 11.8%), 65-74 3.7% (ทั้งชุด 5.2%), <25 7.2% (ทั้งชุด 7.2%), >74 1.7% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 29 · กลุ่ม 1
- IF construction_method_1 ≤ 0.5 AND aus-1_6 > 0.5 AND tract_population > 1514 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 645/326/319 · coverage กฎบน validation 0.0717
- Fidelity F1 0.8711 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.3605 · ERM error 0.2194 · FPR 0.1765 · FNR 0.2957
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.5e-295), derived_msa-md (p_adj=2.8e-51), county_code (p_adj=4.5e-126), derived_loan_product_type (p_adj=8.9e-83), loan_type (p_adj=4.6e-40), lien_status (p_adj=2.4e-52), loan_amount (p_adj=9.7e-261), loan_term (p_adj=1.8e-58), property_value (p_adj=4.2e-174), construction_method (p_adj=0), income (p_adj=3.6e-86), applicant_credit_score_type (p_adj=1.7e-201), aus-1 (p_adj=0), tract_population (p_adj=4.9e-08), ffiec_msa_md_median_family_income (p_adj=2e-31), tract_to_msa_income_percentage (p_adj=5.2e-18), tract_owner_occupied_units (p_adj=7.2e-05), tract_median_age_of_housing_units (p_adj=1.8e-09)
- องค์ประกอบ race_eth: Hispanic 9.1% (ทั้งชุด 9.1%), NH Asian 0.3% (ทั้งชุด 6.8%), NH Black 24.1% (ทั้งชุด 22.0%), NH White 44.5% (ทั้งชุด 41.8%), Other 2.2% (ทั้งชุด 2.4%), Unknown 19.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 43.3% (ทั้งชุด 28.3%), Joint 27.9% (ทั้งชุด 30.0%), Male 24.5% (ทั้งชุด 35.3%), Unknown 4.4% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 24.8% (ทั้งชุด 29.9%), 35-44 24.5% (ทั้งชุด 27.0%), 45-54 17.2% (ทั้งชุด 17.5%), 55-64 14.1% (ทั้งชุด 11.8%), 65-74 6.6% (ทั้งชุด 5.2%), <25 12.2% (ทั้งชุด 7.2%), >74 0.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 29 · กลุ่ม 2
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 269/380/375 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 0.9253 · ERM error 0.0480 · FPR 0.6429 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.3e-09), county_code (p_adj=3e-67), derived_loan_product_type (p_adj=7.8e-29), loan_type (p_adj=1.9e-26), loan_amount (p_adj=7e-47), loan_term (p_adj=4.2e-05), property_value (p_adj=7e-53), construction_method (p_adj=5.8e-06), income (p_adj=8.2e-17), debt_to_income_ratio (p_adj=1.2e-08), submission_of_application (p_adj=0.001), aus-1 (p_adj=2.8e-19), tract_population (p_adj=2.1e-44), tract_to_msa_income_percentage (p_adj=1.1e-52), tract_owner_occupied_units (p_adj=4e-70), tract_one_to_four_family_homes (p_adj=1.1e-48), tract_median_age_of_housing_units (p_adj=2.7e-45)
- องค์ประกอบ race_eth: Hispanic 5.1% (ทั้งชุด 9.1%), NH Asian 14.4% (ทั้งชุด 6.8%), NH Black 8.3% (ทั้งชุด 22.0%), NH White 53.6% (ทั้งชุด 41.8%), Other 0.8% (ทั้งชุด 2.4%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 17.9% (ทั้งชุด 28.3%), Joint 39.2% (ทั้งชุด 30.0%), Male 38.4% (ทั้งชุด 35.3%), Unknown 4.5% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 29.1% (ทั้งชุด 29.9%), 35-44 29.3% (ทั้งชุด 27.0%), 45-54 18.7% (ทั้งชุด 17.5%), 55-64 12.5% (ทั้งชุด 11.8%), 65-74 7.7% (ทั้งชุด 5.2%), <25 1.1% (ทั้งชุด 7.2%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.3% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 29 · กลุ่ม 3
- IF tract_population ≤ 95.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 189/75/54 · coverage กฎบน validation 0.0145
- Fidelity F1 0.8421 · เงื่อนไขรวม 1 · สูงสุดต่อเส้นทาง 1
- อนุมัติจริง 0.0926 · ERM error 0.0741 · FPR 0.0408 · FNR 0.4000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.5e-108), derived_msa-md (p_adj=1.1e-22), county_code (p_adj=2.5e-147), loan_amount (p_adj=3.5e-27), loan_term (p_adj=1.3e-19), property_value (p_adj=3.2e-30), construction_method (p_adj=3e-87), income (p_adj=3.9e-17), debt_to_income_ratio (p_adj=0.022), applicant_credit_score_type (p_adj=1e-05), aus-1 (p_adj=5.4e-46), tract_population (p_adj=1.2e-35), ffiec_msa_md_median_family_income (p_adj=3.6e-06), tract_to_msa_income_percentage (p_adj=2.2e-17), tract_owner_occupied_units (p_adj=1.2e-35), tract_one_to_four_family_homes (p_adj=5.9e-30), tract_median_age_of_housing_units (p_adj=6e-10)
- องค์ประกอบ race_eth: Hispanic 3.7% (ทั้งชุด 9.1%), NH Asian 1.9% (ทั้งชุด 6.8%), NH Black 38.9% (ทั้งชุด 22.0%), NH White 51.9% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.4%), Unknown 1.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 55.6% (ทั้งชุด 28.3%), Joint 22.2% (ทั้งชุด 30.0%), Male 22.2% (ทั้งชุด 35.3%), Unknown 0.0% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 48.1% (ทั้งชุด 29.9%), 35-44 24.1% (ทั้งชุด 27.0%), 45-54 11.1% (ทั้งชุด 17.5%), 55-64 5.6% (ทั้งชุด 11.8%), 65-74 5.6% (ทั้งชุด 5.2%), <25 5.6% (ทั้งชุด 7.2%), >74 0.0% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 29 · กลุ่ม 4
- IF property_value > 6e+05 AND income ≤ 182.5 AND tract_to_msa_income_percentage > 125.2 THEN อยู่กลุ่มนี้
- IF property_value > 6e+05 AND income > 182.5 AND tract_to_msa_income_percentage ≤ 112.5 THEN อยู่กลุ่มนี้
- IF property_value > 6e+05 AND income > 182.5 AND tract_to_msa_income_percentage > 112.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1235/310/327 · coverage กฎบน validation 0.1077
- Fidelity F1 0.7072 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9266 · ERM error 0.0581 · FPR 0.7500 · FNR 0.0033
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=6.8e-18), derived_msa-md (p_adj=4.2e-17), county_code (p_adj=2.3e-53), conforming_loan_limit (p_adj=5.2e-228), derived_loan_product_type (p_adj=1.9e-41), loan_type (p_adj=4.4e-39), loan_amount (p_adj=4.9e-63), property_value (p_adj=1.7e-57), construction_method (p_adj=5.8e-07), income (p_adj=4.3e-32), debt_to_income_ratio (p_adj=7.2e-27), aus-1 (p_adj=1.5e-25), tract_population (p_adj=0.00049), ffiec_msa_md_median_family_income (p_adj=2.3e-49), tract_to_msa_income_percentage (p_adj=2.8e-63), tract_one_to_four_family_homes (p_adj=3.4e-05)
- องค์ประกอบ race_eth: Hispanic 2.8% (ทั้งชุด 9.1%), NH Asian 16.8% (ทั้งชุด 6.8%), NH Black 10.4% (ทั้งชุด 22.0%), NH White 47.7% (ทั้งชุด 41.8%), Other 4.3% (ทั้งชุด 2.4%), Unknown 18.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 12.2% (ทั้งชุด 28.3%), Joint 48.3% (ทั้งชุด 30.0%), Male 32.1% (ทั้งชุด 35.3%), Unknown 7.3% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 22.3% (ทั้งชุด 29.9%), 35-44 38.2% (ทั้งชุด 27.0%), 45-54 24.2% (ทั้งชุด 17.5%), 55-64 13.8% (ทั้งชุด 11.8%), 65-74 0.6% (ทั้งชุด 5.2%), <25 0.3% (ทั้งชุด 7.2%), >74 0.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 29 · กลุ่ม 5
- IF ffiec_msa_md_median_family_income > 9.58e+04 AND property_value ≤ 6.3e+05 AND debt_to_income_ratio ≤ 60 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4870/1053/1065 · coverage กฎบน validation 0.4890
- Fidelity F1 0.6361 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8977 · ERM error 0.0695 · FPR 0.6697 · FNR 0.0010
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.7e-23), derived_msa-md (p_adj=1.5e-154), county_code (p_adj=3.6e-125), conforming_loan_limit (p_adj=3.1e-06), derived_loan_product_type (p_adj=3.7e-146), preapproval (p_adj=0.0072), loan_type (p_adj=4.9e-137), loan_term (p_adj=1.1e-16), construction_method (p_adj=3.7e-30), income (p_adj=9.7e-05), debt_to_income_ratio (p_adj=4.1e-11), applicant_credit_score_type (p_adj=2.7e-07), submission_of_application (p_adj=0.038), aus-1 (p_adj=5e-99), ffiec_msa_md_median_family_income (p_adj=0), tract_to_msa_income_percentage (p_adj=3e-09), tract_owner_occupied_units (p_adj=0.00048), tract_one_to_four_family_homes (p_adj=2.4e-21)
- องค์ประกอบ race_eth: Hispanic 12.5% (ทั้งชุด 9.1%), NH Asian 10.5% (ทั้งชุด 6.8%), NH Black 17.7% (ทั้งชุด 22.0%), NH White 39.0% (ทั้งชุด 41.8%), Other 2.5% (ทั้งชุด 2.4%), Unknown 17.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 30.1% (ทั้งชุด 28.3%), Joint 26.9% (ทั้งชุด 30.0%), Male 35.8% (ทั้งชุด 35.3%), Unknown 7.1% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 34.0% (ทั้งชุด 29.9%), 35-44 23.9% (ทั้งชุด 27.0%), 45-54 15.8% (ทั้งชุด 17.5%), 55-64 12.1% (ทั้งชุด 11.8%), 65-74 5.6% (ทั้งชุด 5.2%), <25 7.1% (ทั้งชุด 7.2%), >74 1.4% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 29 · กลุ่ม 6
- IF loan_type_3 > 0.5 AND ffiec_msa_md_median_family_income ≤ 9.58e+04 AND tract_owner_occupied_units ≤ 776.5 THEN อยู่กลุ่มนี้
- IF loan_type_3 > 0.5 AND ffiec_msa_md_median_family_income ≤ 9.58e+04 AND tract_owner_occupied_units > 776.5 THEN อยู่กลุ่มนี้
- IF loan_type_3 > 0.5 AND ffiec_msa_md_median_family_income > 9.58e+04 AND tract_owner_occupied_units > 1054 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1531/415/440 · coverage กฎบน validation 0.0983
- Fidelity F1 0.8045 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9023 · ERM error 0.0886 · FPR 0.8140 · FNR 0.0101
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=8.7e-94), derived_msa-md (p_adj=1.3e-154), county_code (p_adj=2.8e-136), derived_loan_product_type (p_adj=0), loan_type (p_adj=0), loan_term (p_adj=4.8e-58), property_value (p_adj=2.3e-12), construction_method (p_adj=1.6e-07), income (p_adj=1.1e-09), debt_to_income_ratio (p_adj=3.8e-13), applicant_credit_score_type (p_adj=4.1e-05), submission_of_application (p_adj=1.7e-05), initially_payable_to_institution (p_adj=0.0034), aus-1 (p_adj=4.9e-54), tract_population (p_adj=1.2e-20), ffiec_msa_md_median_family_income (p_adj=1.1e-51), tract_to_msa_income_percentage (p_adj=2e-10), tract_owner_occupied_units (p_adj=3.3e-15), tract_one_to_four_family_homes (p_adj=1.9e-24), tract_median_age_of_housing_units (p_adj=7.4e-13)
- องค์ประกอบ race_eth: Hispanic 6.1% (ทั้งชุด 9.1%), NH Asian 2.3% (ทั้งชุด 6.8%), NH Black 26.1% (ทั้งชุด 22.0%), NH White 40.0% (ทั้งชุด 41.8%), Other 3.6% (ทั้งชุด 2.4%), Unknown 21.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 18.0% (ทั้งชุด 28.3%), Joint 28.6% (ทั้งชุด 30.0%), Male 45.0% (ทั้งชุด 35.3%), Unknown 8.4% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.6% (ทั้งชุด 29.9%), 35-44 28.4% (ทั้งชุด 27.0%), 45-54 16.8% (ทั้งชุด 17.5%), 55-64 10.9% (ทั้งชุด 11.8%), 65-74 5.0% (ทั้งชุด 5.2%), <25 8.6% (ทั้งชุด 7.2%), >74 1.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 29 · กลุ่ม 7
- IF ffiec_msa_md_median_family_income ≤ 1.015e+05 AND derived_loan_product_type_VA:First Lien ≤ 0.5 AND tract_median_age_of_housing_units > 16.5 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 1.015e+05 AND loan_amount ≤ 4e+04 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2404/604/578 · coverage กฎบน validation 0.3070
- Fidelity F1 0.6245 · เงื่อนไขรวม 5 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8927 · ERM error 0.0986 · FPR 0.7581 · FNR 0.0194
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.7e-41), derived_msa-md (p_adj=1.2e-229), county_code (p_adj=3.5e-230), derived_loan_product_type (p_adj=3.9e-48), loan_type (p_adj=1.8e-42), lien_status (p_adj=2.7e-05), loan_amount (p_adj=6.8e-145), property_value (p_adj=3.3e-115), income (p_adj=2.2e-21), debt_to_income_ratio (p_adj=6.8e-12), applicant_credit_score_type (p_adj=5.1e-35), submission_of_application (p_adj=2.2e-39), initially_payable_to_institution (p_adj=2.8e-46), aus-1 (p_adj=7.8e-62), tract_population (p_adj=2e-13), ffiec_msa_md_median_family_income (p_adj=3.4e-196), tract_owner_occupied_units (p_adj=1.2e-09), tract_median_age_of_housing_units (p_adj=1.6e-41)
- องค์ประกอบ race_eth: Hispanic 7.6% (ทั้งชุด 9.1%), NH Asian 3.6% (ทั้งชุด 6.8%), NH Black 13.0% (ทั้งชุด 22.0%), NH White 60.2% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.4%), Unknown 13.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 29.6% (ทั้งชุด 28.3%), Joint 27.3% (ทั้งชุด 30.0%), Male 37.5% (ทั้งชุด 35.3%), Unknown 5.5% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.2% (ทั้งชุด 29.9%), 35-44 24.2% (ทั้งชุด 27.0%), 45-54 15.7% (ทั้งชุด 17.5%), 55-64 11.8% (ทั้งชุด 11.8%), 65-74 6.9% (ทั้งชุด 5.2%), <25 11.6% (ทั้งชุด 7.2%), >74 1.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 29 · กลุ่ม 0
- IF aus-1_6 > 0.5 AND debt_to_income_ratio ≤ 60 AND construction_method_2 > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1254/688/622 · coverage กฎบน validation 0.0648
- Fidelity F1 0.4583 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.5836 · ERM error 0.2717 · FPR 0.4479 · FNR 0.1460
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.2e-81), derived_msa-md (p_adj=3.5e-12), county_code (p_adj=6.4e-40), derived_loan_product_type (p_adj=2.1e-05), preapproval (p_adj=4.4e-05), loan_type (p_adj=0.0096), loan_amount (p_adj=3.1e-41), loan_term (p_adj=5.2e-24), property_value (p_adj=2.9e-63), construction_method (p_adj=1.6e-112), applicant_credit_score_type (p_adj=2.8e-56), submission_of_application (p_adj=7.5e-08), initially_payable_to_institution (p_adj=4.2e-09), aus-1 (p_adj=1.6e-160), tract_population (p_adj=0.00084), ffiec_msa_md_median_family_income (p_adj=6.5e-05), tract_to_msa_income_percentage (p_adj=1.9e-19), tract_owner_occupied_units (p_adj=3.6e-06)
- องค์ประกอบ race_eth: Hispanic 12.1% (ทั้งชุด 9.1%), NH Asian 3.1% (ทั้งชุด 6.8%), NH Black 31.5% (ทั้งชุด 22.0%), NH White 36.0% (ทั้งชุด 41.8%), Other 1.4% (ทั้งชุด 2.4%), Unknown 15.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.9% (ทั้งชุด 28.3%), Joint 26.5% (ทั้งชุด 30.0%), Male 35.0% (ทั้งชุด 35.3%), Unknown 3.5% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.6% (ทั้งชุด 29.9%), 35-44 27.3% (ทั้งชุด 27.0%), 45-54 16.9% (ทั้งชุด 17.5%), 55-64 11.4% (ทั้งชุด 11.8%), 65-74 5.5% (ทั้งชุด 5.2%), <25 9.0% (ทั้งชุด 7.2%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 29 · กลุ่ม 1
- IF debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 > 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND income ≤ 79.5 AND derived_loan_product_type_Conventional:First Lien ≤ 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND income ≤ 79.5 AND derived_loan_product_type_Conventional:First Lien > 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND income > 79.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 706/228/210 · coverage กฎบน validation 0.0648
- Fidelity F1 0.7762 · เงื่อนไขรวม 10 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.0143 · ERM error 0.0143 · FPR 0.0000 · FNR 1.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.9e-22), derived_msa-md (p_adj=5.4e-12), county_code (p_adj=4.8e-35), derived_loan_product_type (p_adj=0.0022), loan_type (p_adj=0.018), loan_amount (p_adj=6.1e-16), loan_term (p_adj=6.4e-12), property_value (p_adj=2.6e-23), construction_method (p_adj=4e-74), income (p_adj=2.2e-72), debt_to_income_ratio (p_adj=5.3e-105), applicant_credit_score_type (p_adj=1.7e-14), initially_payable_to_institution (p_adj=2.9e-136), aus-1 (p_adj=1.3e-50), tract_population (p_adj=8.2e-06), ffiec_msa_md_median_family_income (p_adj=3.2e-05), tract_to_msa_income_percentage (p_adj=3.8e-15), tract_owner_occupied_units (p_adj=2.2e-06)
- องค์ประกอบ race_eth: Hispanic 6.7% (ทั้งชุด 9.1%), NH Asian 3.8% (ทั้งชุด 6.8%), NH Black 27.1% (ทั้งชุด 22.0%), NH White 38.6% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.4%), Unknown 21.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 46.2% (ทั้งชุด 28.3%), Joint 22.4% (ทั้งชุด 30.0%), Male 25.2% (ทั้งชุด 35.3%), Unknown 6.2% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.6% (ทั้งชุด 29.9%), 35-44 21.4% (ทั้งชุด 27.0%), 45-54 16.2% (ทั้งชุด 17.5%), 55-64 18.6% (ทั้งชุด 11.8%), 65-74 3.3% (ทั้งชุด 5.2%), <25 10.5% (ทั้งชุด 7.2%), >74 1.4% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 29 · กลุ่ม 2
- IF lei_549300FGXN1K3HLB1R50 ≤ 0.5 AND debt_to_income_ratio ≤ 60 AND preapproval_1 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 8243/2520/2610 · coverage กฎบน validation 0.8755
- Fidelity F1 0.8286 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9291 · ERM error 0.0709 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.4e-175), derived_msa-md (p_adj=2.1e-14), county_code (p_adj=5.3e-27), derived_loan_product_type (p_adj=1.9e-05), preapproval (p_adj=4.6e-68), loan_type (p_adj=4.5e-06), loan_amount (p_adj=8.4e-17), loan_term (p_adj=1.1e-32), property_value (p_adj=3.4e-08), construction_method (p_adj=4e-99), debt_to_income_ratio (p_adj=0.00017), applicant_credit_score_type (p_adj=5e-33), initially_payable_to_institution (p_adj=2e-29), aus-1 (p_adj=8.3e-95), tract_population (p_adj=1.5e-05), ffiec_msa_md_median_family_income (p_adj=4.6e-11), tract_to_msa_income_percentage (p_adj=2e-11), tract_owner_occupied_units (p_adj=8.7e-05)
- องค์ประกอบ race_eth: Hispanic 9.5% (ทั้งชุด 9.1%), NH Asian 7.7% (ทั้งชุด 6.8%), NH Black 20.4% (ทั้งชุด 22.0%), NH White 42.2% (ทั้งชุด 41.8%), Other 2.6% (ทั้งชุด 2.4%), Unknown 17.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 26.5% (ทั้งชุด 28.3%), Joint 31.0% (ทั้งชุด 30.0%), Male 35.9% (ทั้งชุด 35.3%), Unknown 6.6% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 30.8% (ทั้งชุด 29.9%), 35-44 27.4% (ทั้งชุด 27.0%), 45-54 17.6% (ทั้งชุด 17.5%), 55-64 11.0% (ทั้งชุด 11.8%), 65-74 5.1% (ทั้งชุด 5.2%), <25 6.8% (ทั้งชุด 7.2%), >74 1.2% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 29 · กลุ่ม 3
- IF preapproval_1 ≤ 0.5 AND lei_549300FGXN1K3HLB1R50 ≤ 0.5 AND lei_549300MGPZBLQDIL7538 > 0.5 THEN อยู่กลุ่มนี้
- IF preapproval_1 ≤ 0.5 AND lei_549300FGXN1K3HLB1R50 > 0.5 AND loan_type_2 ≤ 0.5 THEN อยู่กลุ่มนี้
- IF preapproval_1 > 0.5 AND tract_to_msa_income_percentage ≤ 81.29 THEN อยู่กลุ่มนี้
- IF preapproval_1 > 0.5 AND tract_to_msa_income_percentage > 81.29 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1797/564/558 · coverage กฎบน validation 0.0932
- Fidelity F1 0.7215 · เงื่อนไขรวม 10 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9964 · ERM error 0.0036 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.5e-238), preapproval (p_adj=1.2e-226), property_value (p_adj=0.044), construction_method (p_adj=3.5e-07), debt_to_income_ratio (p_adj=1.1e-06), applicant_credit_score_type (p_adj=4.3e-05), initially_payable_to_institution (p_adj=0.0013), aus-1 (p_adj=1.8e-13)
- องค์ประกอบ race_eth: Hispanic 5.0% (ทั้งชุด 9.1%), NH Asian 7.7% (ทั้งชุด 6.8%), NH Black 16.8% (ทั้งชุด 22.0%), NH White 47.1% (ทั้งชุด 41.8%), Other 2.3% (ทั้งชุด 2.4%), Unknown 21.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 22.6% (ทั้งชุด 28.3%), Joint 31.9% (ทั้งชุด 30.0%), Male 36.4% (ทั้งชุด 35.3%), Unknown 9.1% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 27.8% (ทั้งชุด 29.9%), 35-44 26.7% (ทั้งชุด 27.0%), 45-54 18.3% (ทั้งชุด 17.5%), 55-64 13.3% (ทั้งชุด 11.8%), 65-74 5.9% (ทั้งชุด 5.2%), <25 5.9% (ทั้งชุด 7.2%), >74 2.2% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 29 · กลุ่ม 0
- IF loan_term ≤ 315.5 AND construction_method_2 > 0.5 AND loan_term ≤ 242.5 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 315.5 AND construction_method_2 > 0.5 AND loan_term > 242.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 902/304/282 · coverage กฎบน validation 0.0813
- Fidelity F1 0.9253 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.2163 · ERM error 0.1773 · FPR 0.0950 · FNR 0.4754
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0), derived_msa-md (p_adj=2.6e-80), county_code (p_adj=1.4e-181), derived_loan_product_type (p_adj=2.9e-34), loan_type (p_adj=1.8e-32), loan_amount (p_adj=3.9e-248), loan_term (p_adj=1.4e-146), property_value (p_adj=1.2e-280), construction_method (p_adj=0), income (p_adj=2.2e-78), debt_to_income_ratio (p_adj=0.0055), applicant_credit_score_type (p_adj=7.5e-186), initially_payable_to_institution (p_adj=0.027), aus-1 (p_adj=8.7e-308), tract_population (p_adj=1.2e-36), ffiec_msa_md_median_family_income (p_adj=1.5e-41), tract_to_msa_income_percentage (p_adj=9.1e-26), tract_owner_occupied_units (p_adj=1.9e-31), tract_one_to_four_family_homes (p_adj=1.8e-11)
- องค์ประกอบ race_eth: Hispanic 6.7% (ทั้งชุด 9.1%), NH Asian 0.4% (ทั้งชุด 6.8%), NH Black 28.7% (ทั้งชุด 22.0%), NH White 45.7% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.4%), Unknown 16.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 48.2% (ทั้งชุด 28.3%), Joint 28.0% (ทั้งชุด 30.0%), Male 22.0% (ทั้งชุด 35.3%), Unknown 1.8% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 27.0% (ทั้งชุด 29.9%), 35-44 24.8% (ทั้งชุด 27.0%), 45-54 17.7% (ทั้งชุด 17.5%), 55-64 13.8% (ทั้งชุด 11.8%), 65-74 5.3% (ทั้งชุด 5.2%), <25 10.6% (ทั้งชุด 7.2%), >74 0.7% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 29 · กลุ่ม 1
- IF loan_term ≤ 202 AND property_value ≤ 3.8e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 283/99/93 · coverage กฎบน validation 0.0190
- Fidelity F1 0.8000 · เงื่อนไขรวม 2 · สูงสุดต่อเส้นทาง 2
- อนุมัติจริง 0.8065 · ERM error 0.1720 · FPR 0.8333 · FNR 0.0133
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.9e-06), derived_loan_product_type (p_adj=3.9e-196), loan_type (p_adj=2.5e-07), lien_status (p_adj=1.9e-197), loan_amount (p_adj=9.3e-26), loan_term (p_adj=1.1e-54), aus-1 (p_adj=1.3e-11), tract_owner_occupied_units (p_adj=0.0027)
- องค์ประกอบ race_eth: Hispanic 11.8% (ทั้งชุด 9.1%), NH Asian 12.9% (ทั้งชุด 6.8%), NH Black 17.2% (ทั้งชุด 22.0%), NH White 41.9% (ทั้งชุด 41.8%), Other 2.2% (ทั้งชุด 2.4%), Unknown 14.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 30.1% (ทั้งชุด 28.3%), Joint 23.7% (ทั้งชุด 30.0%), Male 39.8% (ทั้งชุด 35.3%), Unknown 6.5% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 32.3% (ทั้งชุด 29.9%), 35-44 22.6% (ทั้งชุด 27.0%), 45-54 17.2% (ทั้งชุด 17.5%), 55-64 9.7% (ทั้งชุด 11.8%), 65-74 14.0% (ทั้งชุด 5.2%), <25 3.2% (ทั้งชุด 7.2%), >74 1.1% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 29 · กลุ่ม 2
- IF tract_owner_occupied_units ≤ 1254 AND loan_term > 315.5 AND property_value ≤ 4.9e+05 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value ≤ 2.6e+05 AND tract_population ≤ 5598 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 5955/1945/1955 · coverage กฎบน validation 0.5008
- Fidelity F1 0.8723 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8645 · ERM error 0.0936 · FPR 0.6226 · FNR 0.0107
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.5e-17), derived_msa-md (p_adj=3.6e-07), county_code (p_adj=8.2e-63), conforming_loan_limit (p_adj=1.2e-17), derived_loan_product_type (p_adj=1.1e-51), loan_type (p_adj=5.6e-52), loan_amount (p_adj=2.9e-62), loan_term (p_adj=8e-69), property_value (p_adj=1.9e-72), construction_method (p_adj=2.8e-23), income (p_adj=1.1e-39), debt_to_income_ratio (p_adj=1.2e-07), applicant_credit_score_type (p_adj=1.8e-13), aus-1 (p_adj=5.3e-59), tract_population (p_adj=3.2e-156), ffiec_msa_md_median_family_income (p_adj=3.6e-08), tract_to_msa_income_percentage (p_adj=8.7e-94), tract_owner_occupied_units (p_adj=7e-284), tract_one_to_four_family_homes (p_adj=1.8e-153), tract_median_age_of_housing_units (p_adj=4e-86)
- องค์ประกอบ race_eth: Hispanic 11.5% (ทั้งชุด 9.1%), NH Asian 4.4% (ทั้งชุด 6.8%), NH Black 24.6% (ทั้งชุด 22.0%), NH White 40.9% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.4%), Unknown 16.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 31.3% (ทั้งชุด 28.3%), Joint 25.6% (ทั้งชุด 30.0%), Male 36.9% (ทั้งชุด 35.3%), Unknown 6.3% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 32.0% (ทั้งชุด 29.9%), 35-44 24.5% (ทั้งชุด 27.0%), 45-54 16.5% (ทั้งชุด 17.5%), 55-64 10.5% (ทั้งชุด 11.8%), 65-74 5.0% (ทั้งชุด 5.2%), <25 9.7% (ทั้งชุด 7.2%), >74 1.9% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 29 · กลุ่ม 3
- IF tract_owner_occupied_units ≤ 1254 AND property_value > 4.9e+05 AND tract_owner_occupied_units > 792 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value ≤ 2.6e+05 AND tract_population > 5908 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.6e+05 AND tract_owner_occupied_units ≤ 1416 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1254 AND property_value > 2.6e+05 AND tract_owner_occupied_units > 1416 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4860/1652/1670 · coverage กฎบน validation 0.3678
- Fidelity F1 0.8562 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9108 · ERM error 0.0659 · FPR 0.6846 · FNR 0.0053
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.6e-15), derived_msa-md (p_adj=9.5e-65), county_code (p_adj=1.8e-115), conforming_loan_limit (p_adj=6.3e-27), derived_loan_product_type (p_adj=7.8e-18), loan_type (p_adj=2.1e-12), lien_status (p_adj=0.0067), loan_amount (p_adj=1.8e-153), loan_term (p_adj=1.8e-22), property_value (p_adj=1.3e-128), construction_method (p_adj=2.3e-45), income (p_adj=7.5e-56), debt_to_income_ratio (p_adj=1.3e-14), applicant_credit_score_type (p_adj=4.1e-06), aus-1 (p_adj=1.7e-23), tract_population (p_adj=4.9e-265), ffiec_msa_md_median_family_income (p_adj=1.9e-68), tract_to_msa_income_percentage (p_adj=6.4e-167), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=1.3e-216), tract_median_age_of_housing_units (p_adj=1e-107)
- องค์ประกอบ race_eth: Hispanic 6.5% (ทั้งชุด 9.1%), NH Asian 10.2% (ทั้งชุด 6.8%), NH Black 18.1% (ทั้งชุด 22.0%), NH White 42.0% (ทั้งชุด 41.8%), Other 2.8% (ทั้งชุด 2.4%), Unknown 20.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 21.4% (ทั้งชุด 28.3%), Joint 35.9% (ทั้งชุด 30.0%), Male 35.4% (ทั้งชุด 35.3%), Unknown 7.4% (ทั้งชุด 6.4%)
- องค์ประกอบ age: 25-34 28.0% (ทั้งชุด 29.9%), 35-44 30.5% (ทั้งชุด 27.0%), 45-54 18.7% (ทั้งชุด 17.5%), 55-64 13.0% (ทั้งชุด 11.8%), 65-74 5.0% (ทั้งชุด 5.2%), <25 4.0% (ทั้งชุด 7.2%), >74 0.8% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.0%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 43 · กลุ่ม 0
- IF construction_method_1 ≤ 0.5 AND aus-1_6 > 0.5 AND tract_one_to_four_family_homes > 207.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 703/373/347 · coverage กฎบน validation 0.0767
- Fidelity F1 0.8471 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.3948 · ERM error 0.2046 · FPR 0.1667 · FNR 0.2628
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.2e-272), derived_msa-md (p_adj=6.1e-48), county_code (p_adj=1.2e-125), derived_loan_product_type (p_adj=2e-57), loan_type (p_adj=8.7e-41), lien_status (p_adj=8e-23), loan_amount (p_adj=1.1e-208), loan_term (p_adj=1.1e-75), property_value (p_adj=3.5e-146), construction_method (p_adj=0), income (p_adj=1e-39), applicant_credit_score_type (p_adj=7.8e-178), initially_payable_to_institution (p_adj=0.0072), aus-1 (p_adj=0), tract_population (p_adj=1.2e-18), ffiec_msa_md_median_family_income (p_adj=6.1e-28), tract_to_msa_income_percentage (p_adj=2.2e-16), tract_owner_occupied_units (p_adj=4.2e-17), tract_median_age_of_housing_units (p_adj=2.2e-14)
- องค์ประกอบ race_eth: Hispanic 7.2% (ทั้งชุด 9.1%), NH Asian 2.3% (ทั้งชุด 6.8%), NH Black 23.3% (ทั้งชุด 22.0%), NH White 46.4% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.4%), Unknown 19.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 38.3% (ทั้งชุด 29.8%), Joint 31.1% (ทั้งชุด 30.6%), Male 27.1% (ทั้งชุด 33.0%), Unknown 3.5% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 32.6% (ทั้งชุด 30.9%), 35-44 24.8% (ทั้งชุด 26.5%), 45-54 15.6% (ทั้งชุด 17.8%), 55-64 10.4% (ทั้งชุด 11.2%), 65-74 4.6% (ทั้งชุด 5.2%), <25 9.5% (ทั้งชุด 6.8%), >74 2.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 43 · กลุ่ม 1
- IF tract_one_to_four_family_homes ≤ 16.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 164/50/52 · coverage กฎบน validation 0.0125
- Fidelity F1 1.0000 · เงื่อนไขรวม 1 · สูงสุดต่อเส้นทาง 1
- อนุมัติจริง 0.1538 · ERM error 0.0577 · FPR 0.0000 · FNR 0.3750
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.5e-70), derived_msa-md (p_adj=2.3e-06), county_code (p_adj=2.4e-132), loan_type (p_adj=0.036), loan_amount (p_adj=5.9e-13), loan_term (p_adj=1.1e-08), property_value (p_adj=4.6e-14), construction_method (p_adj=6.4e-61), income (p_adj=4e-08), applicant_credit_score_type (p_adj=1.2e-08), aus-1 (p_adj=7.2e-37), tract_population (p_adj=6.5e-101), ffiec_msa_md_median_family_income (p_adj=0.00091), tract_to_msa_income_percentage (p_adj=2.1e-70), tract_owner_occupied_units (p_adj=3.9e-124), tract_one_to_four_family_homes (p_adj=9.4e-70), tract_median_age_of_housing_units (p_adj=4.5e-78)
- องค์ประกอบ race_eth: Hispanic 7.7% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 42.3% (ทั้งชุด 22.0%), NH White 40.4% (ทั้งชุด 41.8%), Other 3.8% (ทั้งชุด 2.4%), Unknown 5.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 46.2% (ทั้งชุด 29.8%), Joint 28.8% (ทั้งชุด 30.6%), Male 23.1% (ทั้งชุด 33.0%), Unknown 1.9% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 40.4% (ทั้งชุด 30.9%), 35-44 15.4% (ทั้งชุด 26.5%), 45-54 13.5% (ทั้งชุด 17.8%), 55-64 7.7% (ทั้งชุด 11.2%), 65-74 7.7% (ทั้งชุด 5.2%), <25 11.5% (ทั้งชุด 6.8%), >74 1.9% (ทั้งชุด 1.4%), Unknown 1.9% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 43 · กลุ่ม 2
- IF initially_payable_to_institution_3 ≤ 0.5 AND debt_to_income_ratio > 60 AND construction_method_1 > 0.5 THEN อยู่กลุ่มนี้
- IF initially_payable_to_institution_3 > 0.5 AND debt_to_income_ratio ≤ 47.5 THEN อยู่กลุ่มนี้
- IF initially_payable_to_institution_3 > 0.5 AND debt_to_income_ratio > 47.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1089/696/611 · coverage กฎบน validation 0.0435
- Fidelity F1 0.1885 · เงื่อนไขรวม 7 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8151 · ERM error 0.1015 · FPR 0.4602 · FNR 0.0201
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0005), derived_msa-md (p_adj=1.9e-46), county_code (p_adj=2.2e-34), derived_loan_product_type (p_adj=8.8e-85), loan_type (p_adj=1.5e-87), loan_term (p_adj=6.7e-63), construction_method (p_adj=1.3e-06), income (p_adj=1.3e-13), debt_to_income_ratio (p_adj=1.6e-131), applicant_credit_score_type (p_adj=0.0031), aus-1 (p_adj=8.9e-53), tract_population (p_adj=3.5e-06), ffiec_msa_md_median_family_income (p_adj=1.8e-119), tract_to_msa_income_percentage (p_adj=9.2e-05), tract_owner_occupied_units (p_adj=0.041), tract_median_age_of_housing_units (p_adj=0.00052)
- องค์ประกอบ race_eth: Hispanic 11.8% (ทั้งชุด 9.1%), NH Asian 4.4% (ทั้งชุด 6.8%), NH Black 35.0% (ทั้งชุด 22.0%), NH White 29.0% (ทั้งชุด 41.8%), Other 1.8% (ทั้งชุด 2.4%), Unknown 18.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.7% (ทั้งชุด 29.8%), Joint 26.2% (ทั้งชุด 30.6%), Male 32.7% (ทั้งชุด 33.0%), Unknown 6.4% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.9% (ทั้งชุด 30.9%), 35-44 25.7% (ทั้งชุด 26.5%), 45-54 22.4% (ทั้งชุด 17.8%), 55-64 10.1% (ทั้งชุด 11.2%), 65-74 3.8% (ทั้งชุด 5.2%), <25 5.7% (ทั้งชุด 6.8%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 43 · กลุ่ม 3
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 4/0/1 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 1.0000 · ERM error 0.0000 · FPR N/A · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: ไม่พบ
- องค์ประกอบ race_eth: Hispanic 0.0% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 0.0% (ทั้งชุด 22.0%), NH White 100.0% (ทั้งชุด 41.8%), Other 0.0% (ทั้งชุด 2.4%), Unknown 0.0% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 0.0% (ทั้งชุด 29.8%), Joint 0.0% (ทั้งชุด 30.6%), Male 100.0% (ทั้งชุด 33.0%), Unknown 0.0% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 0.0% (ทั้งชุด 30.9%), 35-44 0.0% (ทั้งชุด 26.5%), 45-54 0.0% (ทั้งชุด 17.8%), 55-64 0.0% (ทั้งชุด 11.2%), 65-74 0.0% (ทั้งชุด 5.2%), <25 100.0% (ทั้งชุด 6.8%), >74 0.0% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 43 · กลุ่ม 4
- IF tract_owner_occupied_units ≤ 1413 AND tract_population > 5394 AND tract_owner_occupied_units > 1060 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1413 AND derived_msa-md_99999 ≤ 0.5 AND property_value ≤ 9.5e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2684/792/843 · coverage กฎบน validation 0.2652
- Fidelity F1 0.8041 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9146 · ERM error 0.0617 · FPR 0.6806 · FNR 0.0039
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.035), derived_msa-md (p_adj=4.2e-44), county_code (p_adj=1.5e-146), derived_loan_product_type (p_adj=7.5e-07), loan_type (p_adj=3.4e-06), loan_amount (p_adj=4.9e-13), loan_term (p_adj=4.4e-15), property_value (p_adj=8.9e-09), construction_method (p_adj=1.1e-14), debt_to_income_ratio (p_adj=0.0034), aus-1 (p_adj=4.1e-18), tract_population (p_adj=7.3e-258), ffiec_msa_md_median_family_income (p_adj=1.2e-24), tract_to_msa_income_percentage (p_adj=1.3e-44), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=1.1e-263), tract_median_age_of_housing_units (p_adj=1.4e-121)
- องค์ประกอบ race_eth: Hispanic 6.5% (ทั้งชุด 9.1%), NH Asian 9.7% (ทั้งชุด 6.8%), NH Black 18.9% (ทั้งชุด 22.0%), NH White 43.9% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.4%), Unknown 18.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 24.2% (ทั้งชุด 29.8%), Joint 36.2% (ทั้งชุด 30.6%), Male 33.6% (ทั้งชุด 33.0%), Unknown 6.0% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 31.1% (ทั้งชุด 30.9%), 35-44 29.3% (ทั้งชุด 26.5%), 45-54 17.6% (ทั้งชุด 17.8%), 55-64 11.6% (ทั้งชุด 11.2%), 65-74 4.5% (ทั้งชุด 5.2%), <25 4.6% (ทั้งชุด 6.8%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 43 · กลุ่ม 5
- IF property_value > 8.3e+05 AND income > 222.5 AND tract_population ≤ 4964 THEN อยู่กลุ่มนี้
- IF property_value > 8.3e+05 AND income > 222.5 AND tract_population > 4964 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 532/176/162 · coverage กฎบน validation 0.0302
- Fidelity F1 0.7542 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9259 · ERM error 0.0741 · FPR 0.7500 · FNR 0.0200
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.4e-30), derived_msa-md (p_adj=4.8e-05), county_code (p_adj=7.4e-12), conforming_loan_limit (p_adj=0), derived_loan_product_type (p_adj=3.6e-13), loan_type (p_adj=1.9e-13), loan_amount (p_adj=6e-37), loan_term (p_adj=2.2e-08), property_value (p_adj=1.5e-35), construction_method (p_adj=0.008), income (p_adj=8.4e-13), debt_to_income_ratio (p_adj=1.7e-17), aus-1 (p_adj=8.4e-22), ffiec_msa_md_median_family_income (p_adj=1.9e-16), tract_to_msa_income_percentage (p_adj=1.4e-30)
- องค์ประกอบ race_eth: Hispanic 1.9% (ทั้งชุด 9.1%), NH Asian 14.2% (ทั้งชุด 6.8%), NH Black 9.3% (ทั้งชุด 22.0%), NH White 50.6% (ทั้งชุด 41.8%), Other 4.3% (ทั้งชุด 2.4%), Unknown 19.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 13.6% (ทั้งชุด 29.8%), Joint 46.9% (ทั้งชุด 30.6%), Male 29.0% (ทั้งชุด 33.0%), Unknown 10.5% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 17.9% (ทั้งชุด 30.9%), 35-44 42.0% (ทั้งชุด 26.5%), 45-54 19.8% (ทั้งชุด 17.8%), 55-64 14.8% (ทั้งชุด 11.2%), 65-74 4.9% (ทั้งชุด 5.2%), <25 0.6% (ทั้งชุด 6.8%), >74 0.0% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 43 · กลุ่ม 6
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND aus-1_6 ≤ 0.5 AND tract_owner_occupied_units ≤ 1781 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2538/808/815 · coverage กฎบน validation 0.1963
- Fidelity F1 0.8826 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8773 · ERM error 0.0920 · FPR 0.6900 · FNR 0.0084
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.1e-25), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.0051), derived_loan_product_type (p_adj=4.4e-39), loan_type (p_adj=2e-41), loan_amount (p_adj=2.8e-76), loan_term (p_adj=2.1e-61), property_value (p_adj=5.1e-83), income (p_adj=8.3e-31), applicant_credit_score_type (p_adj=3.4e-06), initially_payable_to_institution (p_adj=0.007), aus-1 (p_adj=3.2e-24), tract_population (p_adj=9.6e-30), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=1.5e-32), tract_median_age_of_housing_units (p_adj=1.4e-26)
- องค์ประกอบ race_eth: Hispanic 8.2% (ทั้งชุด 9.1%), NH Asian 2.1% (ทั้งชุด 6.8%), NH Black 14.7% (ทั้งชุด 22.0%), NH White 55.1% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.4%), Unknown 17.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 27.0% (ทั้งชุด 29.8%), Joint 30.4% (ทั้งชุด 30.6%), Male 35.5% (ทั้งชุด 33.0%), Unknown 7.1% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.7% (ทั้งชุด 30.9%), 35-44 22.8% (ทั้งชุด 26.5%), 45-54 16.8% (ทั้งชุด 17.8%), 55-64 11.4% (ทั้งชุด 11.2%), 65-74 6.9% (ทั้งชุด 5.2%), <25 9.9% (ทั้งชุด 6.8%), >74 1.5% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-raw-k4 · seed 43 · กลุ่ม 7
- IF ffiec_msa_md_median_family_income > 9.11e+04 AND tract_owner_occupied_units ≤ 1298 AND property_value ≤ 8.6e+05 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 9.11e+04 AND tract_owner_occupied_units > 1298 AND tract_population ≤ 4576 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 4286/1105/1169 · coverage กฎบน validation 0.4382
- Fidelity F1 0.7404 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9119 · ERM error 0.0642 · FPR 0.6505 · FNR 0.0075
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.1e-13), derived_msa-md (p_adj=7.9e-156), county_code (p_adj=5.8e-150), conforming_loan_limit (p_adj=0.00014), derived_loan_product_type (p_adj=8.7e-22), loan_type (p_adj=1.8e-23), loan_term (p_adj=2.8e-24), construction_method (p_adj=9e-33), debt_to_income_ratio (p_adj=5.2e-25), applicant_credit_score_type (p_adj=0.0064), aus-1 (p_adj=2.6e-29), tract_population (p_adj=5.7e-138), ffiec_msa_md_median_family_income (p_adj=0), tract_to_msa_income_percentage (p_adj=4.6e-24), tract_owner_occupied_units (p_adj=6.4e-223), tract_one_to_four_family_homes (p_adj=8.9e-263), tract_median_age_of_housing_units (p_adj=8.2e-16)
- องค์ประกอบ race_eth: Hispanic 11.8% (ทั้งชุด 9.1%), NH Asian 9.7% (ทั้งชุด 6.8%), NH Black 22.9% (ทั้งชุด 22.0%), NH White 35.0% (ทั้งชุด 41.8%), Other 2.0% (ทั้งชุด 2.4%), Unknown 18.6% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 32.1% (ทั้งชุด 29.8%), Joint 26.9% (ทั้งชุด 30.6%), Male 33.8% (ทั้งชุด 33.0%), Unknown 7.3% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 32.0% (ทั้งชุด 30.9%), 35-44 26.4% (ทั้งชุด 26.5%), 45-54 17.0% (ทั้งชุด 17.8%), 55-64 11.4% (ทั้งชุด 11.2%), 65-74 5.4% (ทั้งชุด 5.2%), <25 6.6% (ทั้งชุด 6.8%), >74 1.1% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 43 · กลุ่ม 0
- IF loan_type_2 > 0.5 AND initially_payable_to_institution_1 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 422/338/343 · coverage กฎบน validation 0.0175
- Fidelity F1 0.2549 · เงื่อนไขรวม 2 · สูงสุดต่อเส้นทาง 2
- อนุมัติจริง 0.8251 · ERM error 0.0700 · FPR 0.3500 · FNR 0.0106
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=8.2e-29), derived_msa-md (p_adj=1.3e-07), county_code (p_adj=4.2e-21), derived_loan_product_type (p_adj=4.2e-256), loan_type (p_adj=8.3e-259), loan_amount (p_adj=5.1e-36), loan_term (p_adj=1.2e-19), property_value (p_adj=3.1e-80), income (p_adj=6.4e-69), debt_to_income_ratio (p_adj=2.1e-28), applicant_credit_score_type (p_adj=0.0093), submission_of_application (p_adj=1.8e-44), initially_payable_to_institution (p_adj=6.6e-11), aus-1 (p_adj=9.8e-120), tract_population (p_adj=2.9e-05), tract_to_msa_income_percentage (p_adj=3.2e-26), tract_owner_occupied_units (p_adj=4.6e-16), tract_median_age_of_housing_units (p_adj=1.5e-09)
- องค์ประกอบ race_eth: Hispanic 11.1% (ทั้งชุด 9.1%), NH Asian 1.7% (ทั้งชุด 6.8%), NH Black 38.8% (ทั้งชุด 22.0%), NH White 31.5% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.4%), Unknown 15.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 43.1% (ทั้งชุด 29.8%), Joint 19.5% (ทั้งชุด 30.6%), Male 30.0% (ทั้งชุด 33.0%), Unknown 7.3% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.9% (ทั้งชุด 30.9%), 35-44 25.9% (ทั้งชุด 26.5%), 45-54 17.8% (ทั้งชุด 17.8%), 55-64 10.8% (ทั้งชุด 11.2%), 65-74 3.2% (ทั้งชุด 5.2%), <25 10.8% (ทั้งชุด 6.8%), >74 0.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 43 · กลุ่ม 1
- IF construction_method_1 ≤ 0.5 AND aus-1_6 > 0.5 AND tract_population > 1578 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 617/350/338 · coverage กฎบน validation 0.0752
- Fidelity F1 0.8909 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.3728 · ERM error 0.2337 · FPR 0.2075 · FNR 0.2778
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.8e-296), derived_msa-md (p_adj=1.3e-46), county_code (p_adj=5.2e-122), derived_loan_product_type (p_adj=3.4e-94), loan_type (p_adj=7e-41), lien_status (p_adj=1.6e-64), loan_amount (p_adj=7.4e-229), loan_term (p_adj=3.6e-55), property_value (p_adj=3.4e-214), construction_method (p_adj=0), income (p_adj=7.7e-64), applicant_credit_score_type (p_adj=2.9e-201), submission_of_application (p_adj=0.046), initially_payable_to_institution (p_adj=0.0091), aus-1 (p_adj=0), tract_population (p_adj=7.9e-11), ffiec_msa_md_median_family_income (p_adj=1.5e-26), tract_to_msa_income_percentage (p_adj=3.6e-20), tract_owner_occupied_units (p_adj=5.5e-07), tract_median_age_of_housing_units (p_adj=4.2e-10)
- องค์ประกอบ race_eth: Hispanic 7.1% (ทั้งชุด 9.1%), NH Asian 0.6% (ทั้งชุด 6.8%), NH Black 24.6% (ทั้งชุด 22.0%), NH White 45.9% (ทั้งชุด 41.8%), Other 1.2% (ทั้งชุด 2.4%), Unknown 20.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 38.8% (ทั้งชุด 29.8%), Joint 30.8% (ทั้งชุด 30.6%), Male 26.9% (ทั้งชุด 33.0%), Unknown 3.6% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 35.2% (ทั้งชุด 30.9%), 35-44 26.0% (ทั้งชุด 26.5%), 45-54 13.9% (ทั้งชุด 17.8%), 55-64 10.1% (ทั้งชุด 11.2%), 65-74 3.8% (ทั้งชุด 5.2%), <25 8.9% (ทั้งชุด 6.8%), >74 2.1% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 43 · กลุ่ม 2
- IF initially_payable_to_institution_3 > 0.5 AND derived_loan_product_type_Conventional:First Lien > 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 728/316/299 · coverage กฎบน validation 0.0097
- Fidelity F1 0.0338 · เงื่อนไขรวม 2 · สูงสุดต่อเส้นทาง 2
- อนุมัติจริง 0.8863 · ERM error 0.0769 · FPR 0.6176 · FNR 0.0075
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=0.0052), derived_msa-md (p_adj=3e-12), county_code (p_adj=1.9e-10), derived_loan_product_type (p_adj=8.8e-35), loan_type (p_adj=4e-36), loan_term (p_adj=5.3e-09), construction_method (p_adj=0.00012), income (p_adj=0.011), aus-1 (p_adj=6.7e-19), ffiec_msa_md_median_family_income (p_adj=1.8e-09)
- องค์ประกอบ race_eth: Hispanic 6.0% (ทั้งชุด 9.1%), NH Asian 6.4% (ทั้งชุด 6.8%), NH Black 20.7% (ทั้งชุด 22.0%), NH White 45.8% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.4%), Unknown 19.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 23.1% (ทั้งชุด 29.8%), Joint 35.1% (ทั้งชุด 30.6%), Male 33.8% (ทั้งชุด 33.0%), Unknown 8.0% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 27.8% (ทั้งชุด 30.9%), 35-44 22.1% (ทั้งชุด 26.5%), 45-54 18.4% (ทั้งชุด 17.8%), 55-64 17.7% (ทั้งชุด 11.2%), 65-74 6.0% (ทั้งชุด 5.2%), <25 5.7% (ทั้งชุด 6.8%), >74 2.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 43 · กลุ่ม 3
- IF tract_one_to_four_family_homes ≤ 16.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 193/66/66 · coverage กฎบน validation 0.0125
- Fidelity F1 0.8448 · เงื่อนไขรวม 1 · สูงสุดต่อเส้นทาง 1
- อนุมัติจริง 0.1061 · ERM error 0.0606 · FPR 0.0000 · FNR 0.5714
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.5e-122), derived_msa-md (p_adj=5.6e-16), county_code (p_adj=1.4e-154), derived_loan_product_type (p_adj=0.0043), loan_type (p_adj=0.00063), loan_amount (p_adj=5.4e-24), loan_term (p_adj=4.7e-14), property_value (p_adj=8.9e-32), construction_method (p_adj=9.2e-96), debt_to_income_ratio (p_adj=0.00035), applicant_credit_score_type (p_adj=9.7e-14), aus-1 (p_adj=1.2e-59), tract_population (p_adj=2.1e-41), ffiec_msa_md_median_family_income (p_adj=4.7e-07), tract_to_msa_income_percentage (p_adj=1.1e-22), tract_owner_occupied_units (p_adj=9.2e-44), tract_one_to_four_family_homes (p_adj=4.7e-36), tract_median_age_of_housing_units (p_adj=1.4e-11)
- องค์ประกอบ race_eth: Hispanic 9.1% (ทั้งชุด 9.1%), NH Asian 0.0% (ทั้งชุด 6.8%), NH Black 42.4% (ทั้งชุด 22.0%), NH White 37.9% (ทั้งชุด 41.8%), Other 4.5% (ทั้งชุด 2.4%), Unknown 6.1% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 51.5% (ทั้งชุด 29.8%), Joint 28.8% (ทั้งชุด 30.6%), Male 16.7% (ทั้งชุด 33.0%), Unknown 3.0% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 40.9% (ทั้งชุด 30.9%), 35-44 15.2% (ทั้งชุด 26.5%), 45-54 13.6% (ทั้งชุด 17.8%), 55-64 7.6% (ทั้งชุด 11.2%), 65-74 7.6% (ทั้งชุด 5.2%), <25 12.1% (ทั้งชุด 6.8%), >74 1.5% (ทั้งชุด 1.4%), Unknown 1.5% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 43 · กลุ่ม 4
- IF ffiec_msa_md_median_family_income ≤ 9.58e+04 AND aus-1_1 ≤ 0.5 AND aus-1_2 > 0.5 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income ≤ 9.58e+04 AND aus-1_1 > 0.5 AND derived_loan_product_type_FHA:First Lien ≤ 0.5 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income ≤ 9.58e+04 AND aus-1_1 > 0.5 AND derived_loan_product_type_FHA:First Lien > 0.5 THEN อยู่กลุ่มนี้
- IF ffiec_msa_md_median_family_income > 9.58e+04 AND loan_type_3 > 0.5 AND submission_of_application_2 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3153/957/969 · coverage กฎบน validation 0.2762
- Fidelity F1 0.7711 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8885 · ERM error 0.0980 · FPR 0.7778 · FNR 0.0128
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.3e-71), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.0096), derived_loan_product_type (p_adj=2.2e-193), loan_type (p_adj=8e-196), loan_amount (p_adj=1.4e-18), loan_term (p_adj=1.2e-22), property_value (p_adj=3.3e-27), construction_method (p_adj=1.8e-06), income (p_adj=2.6e-11), applicant_credit_score_type (p_adj=1.7e-09), submission_of_application (p_adj=3.3e-17), initially_payable_to_institution (p_adj=0.0026), aus-1 (p_adj=4.2e-66), tract_population (p_adj=0.00069), ffiec_msa_md_median_family_income (p_adj=1.7e-265), tract_to_msa_income_percentage (p_adj=5.6e-16), tract_owner_occupied_units (p_adj=0.014), tract_one_to_four_family_homes (p_adj=7.3e-18), tract_median_age_of_housing_units (p_adj=0.00052)
- องค์ประกอบ race_eth: Hispanic 7.7% (ทั้งชุด 9.1%), NH Asian 3.4% (ทั้งชุด 6.8%), NH Black 16.2% (ทั้งชุด 22.0%), NH White 52.4% (ทั้งชุด 41.8%), Other 2.9% (ทั้งชุด 2.4%), Unknown 17.3% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 23.6% (ทั้งชุด 29.8%), Joint 31.1% (ทั้งชุด 30.6%), Male 38.5% (ทั้งชุด 33.0%), Unknown 6.8% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.2% (ทั้งชุด 30.9%), 35-44 23.6% (ทั้งชุด 26.5%), 45-54 16.4% (ทั้งชุด 17.8%), 55-64 12.3% (ทั้งชุด 11.2%), 65-74 7.9% (ทั้งชุด 5.2%), <25 7.8% (ทั้งชุด 6.8%), >74 1.7% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 43 · กลุ่ม 5
- IF loan_type_2 > 0.5 AND ffiec_msa_md_median_family_income ≤ 9.58e+04 AND aus-1_3 > 0.5 THEN อยู่กลุ่มนี้
- IF loan_type_2 > 0.5 AND ffiec_msa_md_median_family_income > 9.58e+04 AND income ≤ 51.5 THEN อยู่กลุ่มนี้
- IF loan_type_2 > 0.5 AND ffiec_msa_md_median_family_income > 9.58e+04 AND income > 51.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2147/485/463 · coverage กฎบน validation 0.2008
- Fidelity F1 0.7407 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9006 · ERM error 0.0778 · FPR 0.6957 · FNR 0.0096
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.4e-12), derived_msa-md (p_adj=1.4e-22), county_code (p_adj=4.5e-12), derived_loan_product_type (p_adj=0), loan_type (p_adj=0), loan_term (p_adj=9.1e-62), property_value (p_adj=9e-05), construction_method (p_adj=1.6e-05), income (p_adj=1.2e-05), debt_to_income_ratio (p_adj=1.5e-32), applicant_credit_score_type (p_adj=7.7e-05), submission_of_application (p_adj=1.9e-12), initially_payable_to_institution (p_adj=0.0012), aus-1 (p_adj=6.7e-297), tract_population (p_adj=4.4e-08), ffiec_msa_md_median_family_income (p_adj=1e-52), tract_to_msa_income_percentage (p_adj=2.1e-06), tract_owner_occupied_units (p_adj=0.001)
- องค์ประกอบ race_eth: Hispanic 12.1% (ทั้งชุด 9.1%), NH Asian 1.5% (ทั้งชุด 6.8%), NH Black 38.4% (ทั้งชุด 22.0%), NH White 26.3% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.4%), Unknown 19.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 37.4% (ทั้งชุด 29.8%), Joint 28.9% (ทั้งชุด 30.6%), Male 27.0% (ทั้งชุด 33.0%), Unknown 6.7% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.2% (ทั้งชุด 30.9%), 35-44 27.6% (ทั้งชุด 26.5%), 45-54 24.4% (ทั้งชุด 17.8%), 55-64 9.9% (ทั้งชุด 11.2%), 65-74 1.9% (ทั้งชุด 5.2%), <25 5.6% (ทั้งชุด 6.8%), >74 0.2% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 43 · กลุ่ม 6
- IF loan_type_1 > 0.5 AND ffiec_msa_md_median_family_income ≤ 9.58e+04 AND derived_msa-md_16860 > 0.5 THEN อยู่กลุ่มนี้
- IF loan_type_1 > 0.5 AND ffiec_msa_md_median_family_income > 9.58e+04 AND property_value ≤ 4.6e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2483/758/801 · coverage กฎบน validation 0.2512
- Fidelity F1 0.7283 · เงื่อนไขรวม 6 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8864 · ERM error 0.0674 · FPR 0.5385 · FNR 0.0070
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3e-30), derived_msa-md (p_adj=6.8e-107), county_code (p_adj=5.6e-81), conforming_loan_limit (p_adj=0.0018), derived_loan_product_type (p_adj=2.3e-113), loan_type (p_adj=1.6e-116), loan_amount (p_adj=5.2e-22), loan_term (p_adj=3.4e-08), property_value (p_adj=2.5e-11), construction_method (p_adj=2.3e-22), income (p_adj=1.2e-24), debt_to_income_ratio (p_adj=0.0037), applicant_credit_score_type (p_adj=6.1e-06), submission_of_application (p_adj=3.7e-22), initially_payable_to_institution (p_adj=4.2e-11), aus-1 (p_adj=1.3e-101), ffiec_msa_md_median_family_income (p_adj=1.8e-295), tract_to_msa_income_percentage (p_adj=3.2e-41), tract_median_age_of_housing_units (p_adj=1.6e-13)
- องค์ประกอบ race_eth: Hispanic 13.9% (ทั้งชุด 9.1%), NH Asian 11.1% (ทั้งชุด 6.8%), NH Black 19.5% (ทั้งชุด 22.0%), NH White 36.0% (ทั้งชุด 41.8%), Other 1.5% (ทั้งชุด 2.4%), Unknown 18.1% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.5% (ทั้งชุด 29.8%), Joint 26.8% (ทั้งชุด 30.6%), Male 33.2% (ทั้งชุด 33.0%), Unknown 5.5% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 34.8% (ทั้งชุด 30.9%), 35-44 23.3% (ทั้งชุด 26.5%), 45-54 16.7% (ทั้งชุด 17.8%), 55-64 10.1% (ทั้งชุด 11.2%), 65-74 5.2% (ทั้งชุด 5.2%), <25 7.7% (ทั้งชุด 6.8%), >74 1.9% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GDRO-scarf-k4 · seed 43 · กลุ่ม 7
- IF property_value > 5.3e+05 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND ffiec_msa_md_median_family_income > 9.58e+04 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2257/730/721 · coverage กฎบน validation 0.1250
- Fidelity F1 0.7236 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9390 · ERM error 0.0485 · FPR 0.6818 · FNR 0.0074
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.7e-50), derived_msa-md (p_adj=5.8e-76), county_code (p_adj=1.5e-132), conforming_loan_limit (p_adj=2.8e-84), derived_loan_product_type (p_adj=4.1e-103), loan_type (p_adj=7.6e-98), loan_amount (p_adj=1.4e-103), property_value (p_adj=1.4e-96), construction_method (p_adj=2.2e-21), income (p_adj=6.9e-63), debt_to_income_ratio (p_adj=1.6e-54), aus-1 (p_adj=3e-38), ffiec_msa_md_median_family_income (p_adj=6.3e-181), tract_to_msa_income_percentage (p_adj=3.2e-92), tract_owner_occupied_units (p_adj=3.1e-17), tract_median_age_of_housing_units (p_adj=0.00033)
- องค์ประกอบ race_eth: Hispanic 5.0% (ทั้งชุด 9.1%), NH Asian 15.8% (ทั้งชุด 6.8%), NH Black 11.4% (ทั้งชุด 22.0%), NH White 45.4% (ทั้งชุด 41.8%), Other 3.7% (ทั้งชุด 2.4%), Unknown 18.7% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 18.0% (ทั้งชุด 29.8%), Joint 39.0% (ทั้งชุด 30.6%), Male 34.8% (ทั้งชุด 33.0%), Unknown 8.2% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 26.5% (ทั้งชุด 30.9%), 35-44 36.6% (ทั้งชุด 26.5%), 45-54 18.9% (ทั้งชุด 17.8%), 55-64 10.4% (ทั้งชุด 11.2%), 65-74 4.6% (ทั้งชุด 5.2%), <25 2.4% (ทั้งชุด 6.8%), >74 0.7% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 43 · กลุ่ม 0
- ไม่มีใบที่ทำนายว่าอยู่กลุ่มนี้ (อ่าน F1 ควบคู่)
- ขนาด train/validation/test: 1171/639/593 · coverage กฎบน validation 0.0000
- Fidelity F1 0.0000 · เงื่อนไขรวม 0 · สูงสุดต่อเส้นทาง 0
- อนุมัติจริง 0.5987 · ERM error 0.2917 · FPR 0.5000 · FNR 0.1521
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3.4e-63), derived_msa-md (p_adj=5.3e-06), county_code (p_adj=5.6e-23), derived_loan_product_type (p_adj=1.8e-05), preapproval (p_adj=4e-05), loan_type (p_adj=2.5e-06), loan_amount (p_adj=1.7e-09), loan_term (p_adj=1.2e-09), property_value (p_adj=6e-13), construction_method (p_adj=4.5e-87), applicant_credit_score_type (p_adj=3.2e-35), initially_payable_to_institution (p_adj=5.3e-06), aus-1 (p_adj=3.3e-138), tract_population (p_adj=1.1e-10), ffiec_msa_md_median_family_income (p_adj=0.00013), tract_to_msa_income_percentage (p_adj=3.6e-08), tract_owner_occupied_units (p_adj=1.2e-07)
- องค์ประกอบ race_eth: Hispanic 8.4% (ทั้งชุด 9.1%), NH Asian 4.6% (ทั้งชุด 6.8%), NH Black 27.0% (ทั้งชุด 22.0%), NH White 38.4% (ทั้งชุด 41.8%), Other 2.4% (ทั้งชุด 2.4%), Unknown 19.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 32.2% (ทั้งชุด 29.8%), Joint 28.8% (ทั้งชุด 30.6%), Male 32.7% (ทั้งชุด 33.0%), Unknown 6.2% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.7% (ทั้งชุด 30.9%), 35-44 26.6% (ทั้งชุด 26.5%), 45-54 18.7% (ทั้งชุด 17.8%), 55-64 10.1% (ทั้งชุด 11.2%), 65-74 4.2% (ทั้งชุด 5.2%), <25 8.6% (ทั้งชุด 6.8%), >74 0.7% (ทั้งชุด 1.4%), Unknown 0.3% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 43 · กลุ่ม 1
- IF debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 ≤ 0.5 AND tract_one_to_four_family_homes ≤ 58 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio ≤ 60 AND initially_payable_to_institution_3 > 0.5 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND property_value ≤ 2.5e+05 THEN อยู่กลุ่มนี้
- IF debt_to_income_ratio > 60 AND derived_loan_product_type_Conventional:First Lien > 0.5 AND property_value > 2.5e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 789/285/269 · coverage กฎบน validation 0.0643
- Fidelity F1 0.7970 · เงื่อนไขรวม 11 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.0558 · ERM error 0.0558 · FPR 0.0000 · FNR 1.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=3e-88), derived_msa-md (p_adj=9.5e-11), county_code (p_adj=1.2e-43), derived_loan_product_type (p_adj=1.7e-05), loan_type (p_adj=1.3e-05), loan_amount (p_adj=1e-21), loan_term (p_adj=1e-24), property_value (p_adj=4.6e-28), construction_method (p_adj=3.3e-137), income (p_adj=7.8e-59), debt_to_income_ratio (p_adj=7.1e-94), applicant_credit_score_type (p_adj=5.7e-34), initially_payable_to_institution (p_adj=7.2e-126), aus-1 (p_adj=9.1e-99), tract_population (p_adj=1.2e-17), ffiec_msa_md_median_family_income (p_adj=2.3e-06), tract_to_msa_income_percentage (p_adj=3.7e-14), tract_owner_occupied_units (p_adj=4.8e-16), tract_one_to_four_family_homes (p_adj=6.7e-11)
- องค์ประกอบ race_eth: Hispanic 11.9% (ทั้งชุด 9.1%), NH Asian 2.2% (ทั้งชุด 6.8%), NH Black 34.2% (ทั้งชุด 22.0%), NH White 28.6% (ทั้งชุด 41.8%), Other 2.2% (ทั้งชุด 2.4%), Unknown 20.8% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 45.4% (ทั้งชุด 29.8%), Joint 24.9% (ทั้งชุด 30.6%), Male 22.3% (ทั้งชุด 33.0%), Unknown 7.4% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 29.4% (ทั้งชุด 30.9%), 35-44 24.9% (ทั้งชุด 26.5%), 45-54 17.8% (ทั้งชุด 17.8%), 55-64 13.4% (ทั้งชุด 11.2%), 65-74 5.2% (ทั้งชุด 5.2%), <25 6.7% (ทั้งชุด 6.8%), >74 2.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 43 · กลุ่ม 2
- IF preapproval_2 > 0.5 AND debt_to_income_ratio ≤ 60 AND lei_549300FGXN1K3HLB1R50 ≤ 0.5 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 6731/2000/1990 · coverage กฎบน validation 0.8638
- Fidelity F1 0.7204 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9312 · ERM error 0.0688 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=2.1e-99), derived_msa-md (p_adj=1.9e-11), county_code (p_adj=7.3e-12), derived_loan_product_type (p_adj=1.6e-33), preapproval (p_adj=9.8e-36), loan_type (p_adj=6.4e-35), loan_amount (p_adj=1.2e-05), loan_term (p_adj=2.7e-23), construction_method (p_adj=2e-56), applicant_credit_score_type (p_adj=2.1e-19), submission_of_application (p_adj=0.0074), initially_payable_to_institution (p_adj=1e-21), aus-1 (p_adj=5.9e-49), ffiec_msa_md_median_family_income (p_adj=2.4e-07)
- องค์ประกอบ race_eth: Hispanic 10.1% (ทั้งชุด 9.1%), NH Asian 7.8% (ทั้งชุด 6.8%), NH Black 22.5% (ทั้งชุด 22.0%), NH White 40.3% (ทั้งชุด 41.8%), Other 2.1% (ทั้งชุด 2.4%), Unknown 17.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 29.0% (ทั้งชุด 29.8%), Joint 30.6% (ทั้งชุด 30.6%), Male 34.5% (ทั้งชุด 33.0%), Unknown 5.9% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 31.3% (ทั้งชุด 30.9%), 35-44 26.7% (ทั้งชุด 26.5%), 45-54 17.3% (ทั้งชุด 17.8%), 55-64 11.0% (ทั้งชุด 11.2%), 65-74 5.3% (ทั้งชุด 5.2%), <25 7.2% (ทั้งชุด 6.8%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### GEORGE · seed 43 · กลุ่ม 3
- IF preapproval_2 ≤ 0.5 AND ffiec_msa_md_median_family_income ≤ 8.98e+04 THEN อยู่กลุ่มนี้
- IF preapproval_2 ≤ 0.5 AND ffiec_msa_md_median_family_income > 8.98e+04 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3309/1076/1148 · coverage กฎบน validation 0.0405
- Fidelity F1 0.2601 · เงื่อนไขรวม 4 · สูงสุดต่อเส้นทาง 2
- อนุมัติจริง 0.9782 · ERM error 0.0218 · FPR 1.0000 · FNR 0.0000
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.3e-127), derived_msa-md (p_adj=1.8e-05), county_code (p_adj=6.8e-25), derived_loan_product_type (p_adj=3.9e-27), preapproval (p_adj=3e-93), loan_type (p_adj=8.4e-29), property_value (p_adj=1.5e-08), construction_method (p_adj=8.5e-29), debt_to_income_ratio (p_adj=2.6e-48), applicant_credit_score_type (p_adj=1.9e-10), submission_of_application (p_adj=6.3e-07), initially_payable_to_institution (p_adj=1.3e-10), aus-1 (p_adj=8.5e-84), tract_population (p_adj=3.1e-12), tract_to_msa_income_percentage (p_adj=1e-05), tract_owner_occupied_units (p_adj=7.4e-06), tract_one_to_four_family_homes (p_adj=1.5e-05)
- องค์ประกอบ race_eth: Hispanic 7.1% (ทั้งชุด 9.1%), NH Asian 7.1% (ทั้งชุด 6.8%), NH Black 15.6% (ทั้งชุด 22.0%), NH White 49.0% (ทั้งชุด 41.8%), Other 2.8% (ทั้งชุด 2.4%), Unknown 18.4% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 26.0% (ทั้งชุด 29.8%), Joint 33.1% (ทั้งชุด 30.6%), Male 33.2% (ทั้งชุด 33.0%), Unknown 7.7% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 30.9% (ทั้งชุด 30.9%), 35-44 26.6% (ทั้งชุด 26.5%), 45-54 18.3% (ทั้งชุด 17.8%), 55-64 11.8% (ทั้งชุด 11.2%), 65-74 5.5% (ทั้งชุด 5.2%), <25 5.3% (ทั้งชุด 6.8%), >74 1.6% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 43 · กลุ่ม 0
- IF loan_term ≤ 301.5 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND tract_owner_occupied_units ≤ 1340 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 301.5 AND ffiec_msa_md_median_family_income ≤ 1.015e+05 AND tract_owner_occupied_units > 1340 THEN อยู่กลุ่มนี้
- IF loan_term ≤ 301.5 AND ffiec_msa_md_median_family_income > 1.015e+05 AND loan_amount ≤ 9e+04 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 1021/345/319 · coverage กฎบน validation 0.0920
- Fidelity F1 0.8976 · เงื่อนไขรวม 9 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.3699 · ERM error 0.1755 · FPR 0.1343 · FNR 0.2458
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=1.4e-242), derived_msa-md (p_adj=2.2e-72), county_code (p_adj=1e-161), derived_loan_product_type (p_adj=9.6e-55), loan_type (p_adj=1.3e-36), lien_status (p_adj=5e-24), loan_amount (p_adj=2.6e-187), loan_term (p_adj=1.1e-76), property_value (p_adj=1.2e-121), construction_method (p_adj=0), income (p_adj=3.8e-37), applicant_credit_score_type (p_adj=7.1e-108), initially_payable_to_institution (p_adj=0.011), aus-1 (p_adj=3.3e-284), tract_population (p_adj=2e-29), ffiec_msa_md_median_family_income (p_adj=3.9e-44), tract_to_msa_income_percentage (p_adj=1e-23), tract_owner_occupied_units (p_adj=1.1e-26), tract_one_to_four_family_homes (p_adj=6.3e-06)
- องค์ประกอบ race_eth: Hispanic 5.0% (ทั้งชุด 9.1%), NH Asian 1.9% (ทั้งชุด 6.8%), NH Black 26.6% (ทั้งชุด 22.0%), NH White 46.4% (ทั้งชุด 41.8%), Other 1.9% (ทั้งชุด 2.4%), Unknown 18.2% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 39.2% (ทั้งชุด 29.8%), Joint 32.3% (ทั้งชุด 30.6%), Male 24.5% (ทั้งชุด 33.0%), Unknown 4.1% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 34.5% (ทั้งชุด 30.9%), 35-44 22.6% (ทั้งชุด 26.5%), 45-54 14.4% (ทั้งชุด 17.8%), 55-64 10.7% (ทั้งชุด 11.2%), 65-74 5.3% (ทั้งชุด 5.2%), <25 9.7% (ทั้งชุด 6.8%), >74 2.8% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 43 · กลุ่ม 1
- IF ffiec_msa_md_median_family_income ≤ 8.405e+04 AND loan_term > 339.5 AND tract_owner_occupied_units ≤ 1258 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 2102/712/731 · coverage กฎบน validation 0.1680
- Fidelity F1 0.8743 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8550 · ERM error 0.1040 · FPR 0.6321 · FNR 0.0144
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=9.5e-23), derived_msa-md (p_adj=0), county_code (p_adj=0), conforming_loan_limit (p_adj=0.0069), derived_loan_product_type (p_adj=8.9e-39), loan_type (p_adj=4.6e-41), loan_amount (p_adj=2.5e-100), loan_term (p_adj=1.9e-62), property_value (p_adj=8.1e-111), income (p_adj=5.6e-40), applicant_credit_score_type (p_adj=0.0026), aus-1 (p_adj=2.2e-19), tract_population (p_adj=1.9e-47), ffiec_msa_md_median_family_income (p_adj=0), tract_owner_occupied_units (p_adj=1.1e-53), tract_median_age_of_housing_units (p_adj=3.3e-24)
- องค์ประกอบ race_eth: Hispanic 7.8% (ทั้งชุด 9.1%), NH Asian 2.1% (ทั้งชุด 6.8%), NH Black 16.1% (ทั้งชุด 22.0%), NH White 53.8% (ทั้งชุด 41.8%), Other 2.7% (ทั้งชุด 2.4%), Unknown 17.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 29.3% (ทั้งชุด 29.8%), Joint 28.5% (ทั้งชุด 30.6%), Male 35.4% (ทั้งชุด 33.0%), Unknown 6.8% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 31.5% (ทั้งชุด 30.9%), 35-44 21.5% (ทั้งชุด 26.5%), 45-54 17.4% (ทั้งชุด 17.8%), 55-64 11.2% (ทั้งชุด 11.2%), 65-74 7.0% (ทั้งชุด 5.2%), <25 10.0% (ทั้งชุด 6.8%), >74 1.4% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 43 · กลุ่ม 2
- IF tract_owner_occupied_units ≤ 1114 AND ffiec_msa_md_median_family_income > 8.405e+04 AND property_value ≤ 5.3e+05 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 3832/1331/1288 · coverage กฎบน validation 0.3055
- Fidelity F1 0.8249 · เงื่อนไขรวม 3 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.8439 · ERM error 0.0862 · FPR 0.4627 · FNR 0.0166
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=4.6e-05), derived_msa-md (p_adj=3.8e-155), county_code (p_adj=6.1e-159), conforming_loan_limit (p_adj=0.0013), derived_loan_product_type (p_adj=3.9e-06), loan_type (p_adj=1.9e-07), loan_amount (p_adj=1.5e-07), loan_term (p_adj=4.7e-15), property_value (p_adj=4.3e-16), construction_method (p_adj=2.8e-13), income (p_adj=4.2e-10), debt_to_income_ratio (p_adj=0.00019), aus-1 (p_adj=1.1e-06), tract_population (p_adj=8.7e-146), ffiec_msa_md_median_family_income (p_adj=4.6e-285), tract_to_msa_income_percentage (p_adj=8.2e-100), tract_owner_occupied_units (p_adj=3.8e-277), tract_one_to_four_family_homes (p_adj=2.4e-249), tract_median_age_of_housing_units (p_adj=1.9e-26)
- องค์ประกอบ race_eth: Hispanic 12.9% (ทั้งชุด 9.1%), NH Asian 7.3% (ทั้งชุด 6.8%), NH Black 28.0% (ทั้งชุด 22.0%), NH White 32.2% (ทั้งชุด 41.8%), Other 1.7% (ทั้งชุด 2.4%), Unknown 17.9% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 34.9% (ทั้งชุด 29.8%), Joint 24.1% (ทั้งชุด 30.6%), Male 34.5% (ทั้งชุด 33.0%), Unknown 6.4% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 33.2% (ทั้งชุด 30.9%), 35-44 24.9% (ทั้งชุด 26.5%), 45-54 17.5% (ทั้งชุด 17.8%), 55-64 10.6% (ทั้งชุด 11.2%), 65-74 4.8% (ทั้งชุด 5.2%), <25 8.0% (ทั้งชุด 6.8%), >74 1.0% (ทั้งชุด 1.4%), Unknown 0.1% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation

### HBAC · seed 43 · กลุ่ม 3
- IF tract_owner_occupied_units ≤ 1124 AND property_value > 5.3e+05 AND tract_owner_occupied_units > 763.5 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1124 AND property_value ≤ 2.7e+05 AND tract_owner_occupied_units > 1450 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1124 AND property_value > 2.7e+05 AND tract_population ≤ 4710 THEN อยู่กลุ่มนี้
- IF tract_owner_occupied_units > 1124 AND property_value > 2.7e+05 AND tract_population > 4710 THEN อยู่กลุ่มนี้
- ขนาด train/validation/test: 5045/1612/1662 · coverage กฎบน validation 0.4100
- Fidelity F1 0.8641 · เงื่อนไขรวม 12 · สูงสุดต่อเส้นทาง 3
- อนุมัติจริง 0.9122 · ERM error 0.0644 · FPR 0.6438 · FNR 0.0086
- ตัวแปรต่างชัดหลัง Bonferroni: lei (p_adj=5.3e-14), derived_msa-md (p_adj=4.2e-67), county_code (p_adj=6.4e-121), conforming_loan_limit (p_adj=5.4e-20), derived_loan_product_type (p_adj=6.5e-14), loan_type (p_adj=1.3e-08), lien_status (p_adj=0.00022), loan_amount (p_adj=1.1e-123), loan_term (p_adj=2.1e-32), property_value (p_adj=1.6e-109), construction_method (p_adj=3.7e-40), income (p_adj=5.4e-38), debt_to_income_ratio (p_adj=8.8e-13), applicant_credit_score_type (p_adj=7.7e-10), aus-1 (p_adj=2.8e-29), tract_population (p_adj=6.2e-302), ffiec_msa_md_median_family_income (p_adj=3.3e-69), tract_to_msa_income_percentage (p_adj=1.5e-142), tract_owner_occupied_units (p_adj=0), tract_one_to_four_family_homes (p_adj=2e-239), tract_median_age_of_housing_units (p_adj=2.2e-106)
- องค์ประกอบ race_eth: Hispanic 7.5% (ทั้งชุด 9.1%), NH Asian 9.3% (ทั้งชุด 6.8%), NH Black 19.0% (ทั้งชุด 22.0%), NH White 43.0% (ทั้งชุด 41.8%), Other 2.8% (ทั้งชุด 2.4%), Unknown 18.5% (ทั้งชุด 18.1%)
- องค์ประกอบ sex: Female 24.1% (ทั้งชุด 29.8%), Joint 36.3% (ทั้งชุด 30.6%), Male 32.5% (ทั้งชุด 33.0%), Unknown 7.0% (ทั้งชุด 6.6%)
- องค์ประกอบ age: 25-34 28.3% (ทั้งชุด 30.9%), 35-44 30.7% (ทั้งชุด 26.5%), 45-54 19.0% (ทั้งชุด 17.8%), 55-64 11.9% (ทั้งชุด 11.2%), 65-74 4.7% (ทั้งชุด 5.2%), <25 4.0% (ทั้งชุด 6.8%), >74 1.3% (ทั้งชุด 1.4%), Unknown 0.0% (ทั้งชุด 0.1%)
- สถิติและการทดสอบใช้ test เท่านั้น; กฎ fit train และวัด fidelity บน validation
