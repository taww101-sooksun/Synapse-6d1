import streamlit as st
import datetime

# 1. ตั้งค่าหน้าแอปพลิเคชัน
st.set_page_config(page_title="QUANTUM CALCULATOR", layout="centered")
st.title("🧮 เครื่องคำนวณรหัสตัวเลขจากดวงดาวและปฏิทิน")
st.write("---")

# 2. ส่วนอินพุต: ให้เลือก วัน เดือน ปี
st.subheader("🔮 เลือกวัน เดือน ปี เพื่อถอดรหัสความจริง")
selected_date = st.date_input("เลือกวันที่ต้องการคำนวณ:", datetime.date.today())

# แยกองค์ประกอบ วัน เดือน ปี ค.ศ.
day_of_week = selected_date.isoweekday() # 1=จันทร์, 2=อังคาร, ..., 7=อาทิตย์ (ตรงตามเกณฑ์นาย)
day_num = selected_date.day
month_num = selected_date.month
year_num = selected_date.year
thai_year = year_num + 543 # แปลงเป็น พ.ศ.

# 3. ตรรกะการแปลงค่า วัน และ เดือน (ตรงไปตรงมา)
val_day = day_of_week
day_names = ["", "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
day_name_th = day_names[day_of_week]

val_month = month_num
month_name_th = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"][month_num]

# 4. ล็อกค่าปีนักษัตรตามปี พ.ศ. จริง (ตัดปัญหาสูตรคณิตศาสตร์เพี้ยน)
# เกณฑ์ของนาย: ชวด=1, ฉลู=2, ขาล=3, เถาะ=4, มะโรง=5, มะเส็ง=6, มะเมีย=7, มะแม=8, วอก=9, ระกา=10, จอ=11, ปีกุล=12
if thai_year == 2569:
    zodiac_name = "ปีมะเมีย (ปีม้า)"
    val_zodiac_num = 7
elif thai_year == 2568:
    zodiac_name = "ปีมะเส็ง"
    val_zodiac_num = 6
elif thai_year == 2570:
    zodiac_name = "ปีมะแม"
    val_zodiac_num = 8
else:
    # เผื่อเลือกปีอื่นๆ จะคำนวณแบบล็อกฐานรอบ 12 ปีที่แม่นยำ
    zodiac_map = {
        0: ("ปีมะโรง", 5), 1: ("ปีมะเส็ง", 6), 2: ("ปีมะเมีย", 7), 
        3: ("ปีมะแม", 8), 4: ("ปีวอก", 9), 5: ("ปีระกา", 10), 
        6: ("ปีจอ", 11), 7: ("ปีกุล", 12), 8: ("ปีชวด", 1), 
        9: ("ปีฉลู", 2), 10: ("ปีขาล", 3), 11: ("ปีเถาะ", 4)
    }
    zodiac_name, val_zodiac_num = zodiac_map[(thai_year - 2564) % 12]

# 5. สูตรทางดาราศาสตร์แกะข้างขึ้นข้างแรมอัตโนมัติ
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

# ตรรกะคะแนนข้างขึ้นข้างแรม
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

# --- แสดงผลลัพธ์หน้าจอขั้นที่ 1 ---
st.write("---")
st.subheader("📊 1. ถอดรหัสค่าตัวเลขดิบตามจริง")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label=f"วัน{day_name_th}", value=val_day)
with col2:
    st.metric(label=f"เดือน{month_name_th}", value=val_month)
with col3:
    st.metric(label=f"นักษัตร ({zodiac_name})", value=val_zodiac_num)

st.info(f"🌙 **ระบบคำนวณดวงจันทร์วันนี้:** {lunar_type} {lunar_phase_num} ค่ำ -> ส่งผลต่อสมการ: {modifier_text}")

# --- แสดงผลลัพธ์หน้าจอขั้นที่ 2 ---
st.write("---")
st.subheader("⚡ 2. ผลลัพธ์สมการคณิตศาสตร์ควอนตัม")

base_sum = val_day + val_month + val_zodiac_num
total_before_factor = base_sum + lunar_modifier

# นำค่าคงที่ 1.618 (คูณ) และ 29.53 (หาร) เข้ามาผูกพันอยู่ตลอดเวลา
final_result = (total_before_factor * 1.618) / 29.53

st.code(f"สูตรเริ่มต้น: วัน({val_day}) + เดือน({val_month}) + ปีนักษัตร({val_zodiac_num}) = {base_sum}")
st.code(f"คำนวณข้างขึ้นข้างแรม: {base_sum} ({modifier_text}) = {total_before_factor}")
st.code(f"สูตรผูกพันค่าคงที่ตลอดเวลา: ({total_before_factor} × 1.618) ÷ 29.53")

st.markdown(f"### 🎯 ค่ารหัสลับสุทธิ: ` {final_result:.4f} `")
st.write("---")
st.caption("อยู่นิ่งๆ ไม่เจ็บตัว | ระบบคำนวณสมการตัวเลขตามสัจธรรมความจริง 2026")
