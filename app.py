import streamlit as st
import datetime

# 1. ตั้งค่าหน้าแอปพลิเคชัน
st.set_page_config(page_title="QUANTUM CALCULATOR", layout="centered")
st.title("🧮 เครื่องคำนวณรหัสตัวเลขจากดวงดาวและปฏิทิน")
st.write("---")

# 2. ส่วนอินพุต: ให้เลือก วัน เดือน ปี ที่ต้องการคำนวณ
st.subheader("🔮 เลือกวัน เดือน ปี เพื่อถอดรหัสความจริง")
selected_date = st.date_input("เลือกวันที่ต้องการคำนวณ:", datetime.date.today())

# แยกองค์ประกอบ วัน เดือน ปี ค.ศ. จากตัวเลือกข้างบน
day_of_week = selected_date.isoweekday() # ระบบสากล: 1=จันทร์, 2=อังคาร ..., 7=อาทิตย์ เป๊ะตามเกณฑ์ของนาย
day_num = selected_date.day
month_num = selected_date.month
year_num = selected_date.year

# 3. ตรรกะการแปลงค่า วัน เดือน ปีนักษัตร ตามกฎความจริง
# วัน: จันทร์=1, พุธ=3, พฤหัสบดี=4, อาทิตย์=7
val_day = day_of_week
day_names = ["", "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
day_name_th = day_names[day_of_week]

# เดือน: มกราคม=1 ยัน ธันวาคม=12
val_month = month_num
month_name_th = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"][month_num]

# ปีนักษัตร: ชวด=1 ยัน ปีกุล=12
zodiac_animals = ["ปีกุล", "ปีชวด", "ปีฉลู", "ปีขาล", "ปีเถาะ", "ปีมะโรง", "ปีมะเส็ง", "ปีมะเมีย", "ปีมะแม", "ปีวอก", "ปีระกา", "ปีจอ"]
val_zodiac = ((year_num + 543) - 2444) % 12
if val_zodiac == 0:
    val_zodiac = 12
zodiac_name = zodiac_animals[(year_num + 543) % 12]

# 4. สูตรทางดาราศาสตร์แกะข้างขึ้นข้างแรมอัตโนมัติ (คำนวณตามอายุของดวงจันทร์)
ts = (year_num - 2000) * 365.25 + (month_num * 30.6) + day_num
lunar_cycle = 29.53
age = (ts - 4.1) % lunar_cycle

if age < 14.765:
    lunar_type = "ขึ้น"
    lunar_phase_num = int(age) + 1
    if lunar_phase_num > 15: lunar_phase_num = 15
else:
    lunar_type = "แรม"
    lunar_phase_num = int(age - 14.765) + 1
    if lunar_phase_num > 15: lunar_phase_num = 15

# ตรรกะคะแนนข้างขึ้นข้างแรมตามเงื่อนไขของนาย:
# แรม 1-6 และ 9-15 = บวกค่าเข้าไป (+)
# ขึ้น 1-6 และ 9-15 = ลบค่าออกไป (-)
# ขึ้น/แรม 7-8 = ค่าคงที่ (มีค่าเป็น 0)
lunar_modifier = 0
modifier_text = "ค่าคงที่ (0)"

if lunar_type == "แรม":
    if 1 <= lunar_phase_num <= 6 or 9 <= lunar_phase_num <= 15:
        lunar_modifier = lunar_phase_num
        modifier_text = f"+ {lunar_phase_num}"
    elif 7 <= lunar_phase_num <= 8:
        lunar_modifier = 0
        modifier_text = "ค่าคงที่ (0)"
elif lunar_type == "ขึ้น":
    if 1 <= lunar_phase_num <= 6 or 9 <= lunar_phase_num <= 15:
        lunar_modifier = -lunar_phase_num
        modifier_text = f"- {lunar_phase_num}"
    elif 7 <= lunar_phase_num <= 8:
        lunar_modifier = 0
        modifier_text = "ค่าคงที่ (0)"

# --- แสดงผลลัพธ์หน้าจอขั้นที่ 1: ตัวเลขดิบตามจริง ---
st.write("---")
st.subheader("📊 1. ถอดรหัสค่าตัวเลขดิบตามจริง")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label=f"วัน{day_name_th}", value=val_day)
with col2:
    st.metric(label=f"เดือน{month_name_th}", value=val_month)
with col3:
    st.metric(label=f"นักษัตร ({zodiac_name})", value=val_zodiac)

st.info(f"🌙 **ระบบคำนวณดวงจันทร์วันนี้:** {lunar_type} {lunar_phase_num} ค่ำ -> ส่งผลต่อสมการ: {modifier_text}")

# --- แสดงผลลัพธ์หน้าจอขั้นที่ 2: การคำนวณร่วมกับค่าคงที่คงทนตลอดเวลา ---
st.write("---")
st.subheader("⚡ 2. ผลลัพธ์สมการคณิตศาสตร์คณิตศาตรา")

# สูตรคณิตศาสตร์ที่นายกำหนดไว้:
base_sum = val_day + val_month + val_zodiac
total_before_factor = base_sum + lunar_modifier

# นำค่าคงที่ 1.618 (คูณ) และ 29.53 (หาร) เข้ามาผูกพันอยู่ตลอดเวลา
final_result = (total_before_factor * 1.618) / 29.53

st.code(f"สูตรเริ่มต้น: วัน({val_day}) + เดือน({val_month}) + ปีนักษัตร({val_zodiac}) = {base_sum}")
st.code(f"คำนวณข้างขึ้นข้างแรม: {base_sum} ({modifier_text}) = {total_before_factor}")
st.code(f"สูตรผูกพันค่าคงที่ตลอดเวลา: ({total_before_factor} × 1.618) ÷ 29.53")

st.markdown(f"### 🎯 ค่ารหัสลับสุทธิ: ` {final_result:.4f} `")
st.write("---")
st.caption("อยู่นิ่งๆ ไม่เจ็บตัว | ระบบคำนวณสมการตัวเลขตามสัจธรรมความจริง 2026")
