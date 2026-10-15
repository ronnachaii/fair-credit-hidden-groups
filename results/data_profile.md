# ข้อมูล HMDA หลังคัดกรอง

| stage | n |
| --- | --- |
| 1–4 หน่วย | 139963.0000 |
| Single Family | 139963.0000 |
| ข้อมูลต้นทาง | 307343.0000 |
| ซื้อที่อยู่อาศัย | 158596.0000 |
| ผลอนุมัติ/ปฏิเสธที่กำหนด | 139963.0000 |
| อยู่เอง | 141941.0000 |
| ไม่ใช่ open-end | 139963.0000 |
| ไม่ใช่ reverse mortgage | 141688.0000 |
| ไม่ใช่ธุรกิจ | 141728.0000 |

Unknown คงไว้ฝึก แต่ตัดจาก fairness เฉพาะมิติที่ไม่ทราบ และตัดกลุ่มเล็กตาม min_fair_group ใน CSV ผลทดลอง

| dimension | group | n | approval_rate | denial_rate |
| --- | --- | --- | --- | --- |
| age | 25-34 | 42763.0000 | 0.8521 | 0.1479 |
| age | 35-44 | 36993.0000 | 0.8325 | 0.1675 |
| age | 45-54 | 25324.0000 | 0.8237 | 0.1763 |
| age | 55-64 | 16455.0000 | 0.8340 | 0.1660 |
| age | 65-74 | 7486.0000 | 0.8524 | 0.1476 |
| age | <25 | 8724.0000 | 0.8034 | 0.1966 |
| age | >74 | 2180.0000 | 0.8569 | 0.1431 |
| age | Unknown | 38.0000 | 0.5000 | 0.5000 |
| intersection | Hispanic × Female | 3814.0000 | 0.7973 | 0.2027 |
| intersection | Hispanic × Joint | 2743.0000 | 0.8418 | 0.1582 |
| intersection | Hispanic × Male | 6096.0000 | 0.8469 | 0.1531 |
| intersection | NH Asian × Female | 2066.0000 | 0.8887 | 0.1113 |
| intersection | NH Asian × Joint | 2506.0000 | 0.9018 | 0.0982 |
| intersection | NH Asian × Male | 4856.0000 | 0.9018 | 0.0982 |
| intersection | NH Black × Female | 14396.0000 | 0.7515 | 0.2485 |
| intersection | NH Black × Joint | 6308.0000 | 0.7689 | 0.2311 |
| intersection | NH Black × Male | 9924.0000 | 0.7849 | 0.2151 |
| intersection | NH White × Female | 13279.0000 | 0.8366 | 0.1634 |
| intersection | NH White × Joint | 23880.0000 | 0.8925 | 0.1075 |
| intersection | NH White × Male | 21087.0000 | 0.8728 | 0.1272 |
| intersection | Other × Female | 426.0000 | 0.7559 | 0.2441 |
| intersection | Other × Joint | 2389.0000 | 0.8707 | 0.1293 |
| intersection | Other × Male | 447.0000 | 0.7919 | 0.2081 |
| intersection | Unknown | 25746.0000 | 0.8181 | 0.1819 |
| race_eth | Hispanic | 12723.0000 | 0.8302 | 0.1698 |
| race_eth | NH Asian | 9459.0000 | 0.8988 | 0.1012 |
| race_eth | NH Black | 30750.0000 | 0.7656 | 0.2344 |
| race_eth | NH White | 58444.0000 | 0.8723 | 0.1277 |
| race_eth | Other | 3277.0000 | 0.8435 | 0.1565 |
| race_eth | Unknown | 25310.0000 | 0.8196 | 0.1804 |
| sex | Female | 39199.0000 | 0.7930 | 0.2070 |
| sex | Joint | 42760.0000 | 0.8645 | 0.1355 |
| sex | Male | 48851.0000 | 0.8459 | 0.1541 |
| sex | Unknown | 9153.0000 | 0.8437 | 0.1563 |