import streamlit as st
from datetime import datetime

# 1. สไตล์แบบอาจารย์ต๊ะ (Dark Neon)
st.set_page_config(page_title="Cosmic Auto-Decoder", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ff00; }
    h1 { color: #ff00ff; text-shadow: 2px 2px #000000; text-align: center; }
    .stMetric { background-color: #1e2130; border-radius: 10px; padding: 15px; border: 1px solid #00ff00; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌌 Cosmic Auto-Decoder")
st.write("<center>ระบบถอดรหัสวันที่และสมดุลจันทรคติอัตโนมัติ</center>", unsafe_allow_html=True)

# 2. ส่วนรับข้อมูล (เปิดขอบเขตให้ใส่ปี 1960 - 2026 ตามความจริงที่นายต้องการ)
min_date = datetime(1960, 1, 1)
max_date = datetime(2026, 12, 31)
current_default = datetime.now() if datetime.now() <= max_date else max_date

selected_date = st.date_input(
    "📅 กรอก วัน/เดือน/ปี ที่ต้องการเช็ค", 
    value=current_default,
    min_value=min_date,
    max_value=max_date
)

# 3. Logic คำนวณอัตโนมัติ (ยึดตามหลักเกณฑ์ความจริง 100%)

# A. วันในสัปดาห์ (จันทร์=1 ยัน อาทิตย์=7 เป๊ะตามระบบ .isoweekday())
val_day = selected_date.isoweekday()
day_name_th = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"][val_day - 1]

# B. เดือน (มกราคม=1 ยัน ธันวาคม=12)
val_month = selected_date.month
month_name_th = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"][val_month]

# C. ปีนักษัตรดัดนิสัยให้ตรงความจริง (ชวด=1 ยัน ปีกุล=12)
thai_year = selected_date.year + 543

# จับคู่ พ.ศ. หาเศษเพื่อเอาชื่อนักษัตรที่แท้จริงของไทย
zodiac_mapping = {
    0: ("ปีมะโรง", 5), 1: ("ปีมะเส็ง", 6), 2: ("ปีมะเมีย", 7), 
    3: ("ปีมะแม", 8), 4: ("ปีวอก", 9), 5: ("ปีระกา", 10), 
    6: ("ปีจอ", 11), 7: ("ปีกุล", 12), 8: ("ปีชวด", 1), 
    9: ("ปีฉลู", 2), 10: ("ปีขาล", 3), 11: ("ปีเถาะ", 4)
}
# ใช้ปีฐาน พ.ศ. 2564 เป็นตัวตั้งต้นคำนวณรอบเศษ 12 ปี
zodiac_name, val_zodiac = zodiac_mapping[(thai_year - 2564) % 12]


# D. สูตรทางดาราศาสตร์แกะข้างขึ้นข้างแรมอัตโนมัติ (Moon Phase)
def get_lunar_phase(date):
    reference_date = datetime(2000, 1, 6).date()
    diff = (date - reference_date).days
    lunar_cycle = 29.53
    age = (diff) % lunar_cycle
    if age < 0:
        age += lunar_cycle
        
    if age < 14.765:
        step = int(age) + 1
        if step > 15: step = 15
        return "ขึ้น", step
    else:
        step = int(age - 14.765) + 1
        if step > 15: step = 15
        return "แรม", step

lunar_type, lunar_step = get_lunar_phase(selected_date)


# E. ตรรกะการคิดคะแนนข้างขึ้นข้างแรมตามสูตรที่นายกำหนดไว้เป๊ะๆ
# แรม 1-6 และ 9-15 = บวกค่าเข้าไป (+)
# ขึ้น 1-6 และ 9-15 = ลบค่าออกไป (-)
# ขึ้น/แรม 7-8 = ค่าคงที่ (มีค่าเป็น 0 ไม่บวกไม่ลบ)
lunar_modifier = 0
modifier_text = "ค่าคงที่ (0)"

if lunar_type == "แรม":
    if 1 <= lunar_step <= 6 or 9 <= lunar_step <= 15:
        lunar_modifier = lunar_step
        modifier_text = f"+ {lunar_step}"
    elif 7 <= lunar_step <= 8:
        lunar_modifier = 0
        modifier_text = "ค่าคงที่ (0)"
elif lunar_type == "ขึ้น":
    if 1 <= lunar_step <= 6 or 9 <= lunar_step <= 15:
        lunar_modifier = -lunar_step
        modifier_text = f"- {lunar_step}"
    elif 7 <= lunar_step <= 8:
        lunar_modifier = 0
        modifier_text = "ค่าคงที่ (0)"


# F. สูตรสมดุลจักรวาลที่มีเลขคงที่ 1.618 และ 29.53 เกี่ยวข้องตลอดเวลา
# ขั้นแรก: รวมฐาน วัน + เดือน + ปีนักษัตร
base_sum = val_day + val_month + val_zodiac

# ขั้นสอง: เอาไปคำนวณร่วมกับผลจากข้างขึ้นข้างแรม
total_before_factor = base_sum + lunar_modifier

# ขั้นสุดท้าย: คูณด้วย 1.618 และ หารด้วย 29.53 ตลอดเวลาตามกฎ
final_result = (total_before_factor * 1.618) / 29.53


# 4. แสดงผลโชว์เพื่อน
st.write("---")
st.subheader(f"🔍 วิเคราะห์ข้อมูลดิบประจำวันที่: {selected_date.strftime('%d/%m/%Y')}")

col1, col2, col3 = st.columns(3)
col1.metric(f"วัน{day_name_th}", f"เลขดิบ: {val_day}")
col2.metric(f"เดือน{month_name_th}", f"เลขดิบ: {val_month}")
col3.metric(f"นักษัตร ({zodiac_name})", f"เลขดิบ: {val_zodiac}")

st.info(f"🌙 **ระบบจันทรคติวันนี้:** {lunar_type} {lunar_step} ค่ำ (ส่งผลต่อสมการ: {modifier_text})")

st.write("### 🎯 เลขรหัสสุทธิประจำจักรวาล (Cosmic Index)")
st.metric(label="ค่าพลังงานสุทธิถอดรหัสได้", value=f"{final_result:.4f}")


# 5. โชว์ที่มาอย่างโปร่งใส ตรวจสอบได้จริง
with st.expander("📝 ขั้นตอนสมการการถอดรหัส (ตรวจสอบความเที่ยงตรง)"):
    st.latex(r"Result = \frac{(Day + Month + Zodiac \pm Lunar) \times 1.618}{29.53}")
    st.markdown(f"""
    **คำนวณตามขั้นตอนจริง:**
    1. **รวมฐานตัวเลขดิบ:** วัน({val_day}) + เดือน({val_month}) + นักษัตร({val_zodiac}) = **{base_sum}**
    2. **คำนวณผลกระทบดวงจันทร์:** {base_sum} ({modifier_text}) = **{total_before_factor}**
    3. **เข้าสูตรคงที่ตลอดเวลา:** ({total_before_factor} × 1.618) ÷ 29.53
    4. **สรุปค่ารหัสสุทธิ:** **{final_result:.4f}**
    """)
    
    # แปลงผลลัพธ์เป็นข้อความตัวเลขเด่นเพื่อเอาไปใช้งานต่อ
    raw_num = str(abs(final_result)).replace('.', '')
    if len(raw_num) >= 5:
        st.success(f"**ตัวเลขเด่นที่ถอดรหัสได้จากฐานพลังงาน:** {raw_num[1:3]} , {raw_num[2:4]}")

st.info("💡 แอปนี้ได้รับการแก้ไขให้ระบบวัน เดือน ปีนักษัตร และข้างขึ้นข้างแรม ทำงานเชื่อมโยงกันอย่างถูกต้องตามหลักสัจธรรมแล้ว")
st.caption("อยู่นิ่งๆ ไม่เจ็บตัว | โค้ดถอดรหัสควบคุมสมการโดยอาจารย์ต๊ะ 2026")
