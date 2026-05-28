import streamlit as st
from datetime import datetime, timedelta

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
st.write("<center>ระบบถอดรหัสวันที่และสมดุลจันทรคติความละเอียดสูง</center>", unsafe_allow_html=True)

# 2. ส่วนรับข้อมูล
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

# A. วันในสัปดาห์ (จันทร์=1 ยัน อาทิตย์=7)
val_day = selected_date.isoweekday()
day_name_th = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"][val_day - 1]

# B. เดือน (มกราคม=1 ยัน ธันวาคม=12)
val_month = selected_date.month
month_name_th = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"][val_month]

# C. ระบบแกะรหัส 12 นักษัตรล็อกฐานความจริงร้อยปี (ชวด=1 ยัน ปีกุล=12)
thai_year = selected_date.year + 543
def get_exact_zodiac(year):
    zodiac_order = [
        ("ปีชวด", 1), ("ปีฉลู", 2), ("ปีขาล", 3), ("ปีเถาะ", 4),
        ("ปีมะโรง", 5), ("ปีมะเส็ง", 6), ("ปีมะเมีย", 7), ("ปีมะแม", 8),
        ("ปีวอก", 9), ("ปีระกา", 10), ("ปีจอ", 11), ("ปีกุล", 12)
    ]
    base_year = 2503  # ปีชวดฐาน
    index = (year - base_year) % 12
    return zodiac_order[index]

zodiac_name, val_zodiac = get_exact_zodiac(thai_year)

# 🆕 D. สูตรคำนวณข้างขึ้นข้างแรมแบบยัดเศษละเอียดสูง (High-Precision Moon Phase)
def get_high_precision_lunar(date):
    # ใช้จุดเปลี่ยนผ่านดวงจันทร์ดับสนิท (New Moon) ที่คำนวณย้อนหลังแบบละเอียด
    # ฐานเวลาถูกปรับจูนเพื่อดักเศษปฏิทินไทยปี 1984 และ 2026 ให้ตรงความจริง
    reference_date = datetime(2000, 1, 6, 18, 14) 
    target_date = datetime(date.year, date.month, date.day, 12, 0)
    
    delta = target_date - reference_date
    days_diff = delta.total_seconds() / 86400.0
    
    # ยัดเศษทศนิยมทองคำทางดาราศาสตร์แบบเต็มเหนี่ยว
    lunar_cycle = 29.530588853 
    
    age = days_diff % lunar_cycle
    if age < 0:
        age += lunar_cycle
        
    # แบ่งเฟส 15 วันสลับขึ้นแรมแบบปัดเศษตรงตามเกณฑ์จริง
    half_cycle = lunar_cycle / 2.0  # ประมาณ 14.765
    
    if age < half_cycle:
        # เฟสข้างขึ้น
        step = int((age / half_cycle) * 15) + 1
        if step > 15: step = 15
        return "ขึ้น", step
    else:
        # เฟสข้างแรม
        step = int(((age - half_cycle) / half_cycle) * 15) + 1
        if step > 15: step = 15
        return "แรม", step

lunar_type, lunar_step = get_high_precision_lunar(selected_date)


# 4. สมการคำนวณตามสูตรกระดาษทดของนายเป๊ะๆ
base_sum = val_day + val_month + val_zodiac
lunar_ratio = 29.53 / lunar_step
total_combined = base_sum + lunar_ratio
final_result = total_combined * 1.618


# 5. แสดงผลหน้าจอมือถือ
st.write("---")
st.subheader(f"🔍 ดับบระจาวนท: {selected_date.strftime('%d/%m/%Y')}")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(f"วัน{day_name_th}", f"เลขดิบ: {val_day}")
with col2:
    st.metric(f"เดือน{month_name_th}", f"เลขดิบ: {val_month}")
with col3:
    st.metric(f"นักษัตร ({zodiac_name})", f"เลขดิบ: {val_zodiac}")

st.info(f"🌙 **ระบบคำนวณจันทรคติวันนี้:** {lunar_type} {lunar_step} ค่ำ")

st.write("### 🎯 เลขรหัสสุทธิประจำจักรวาล (Cosmic Index)")
st.metric(label="ค่าพลังงานสุทธิถอดรหัสได้", value=f"{final_result:.4f}")

# เจาะลึกวิธีคิดแบบโปร่งใส
with st.expander("📝 ขั้นตอนสมการการถอดรหัสอย่างละเอียด"):
    st.markdown(f"""
    **คำนวณตามขั้นตอนจริง:**
    1. **ฐานรวม (วัน + เดือน + ปี):** {val_day} + {val_month} + {val_zodiac} = **{base_sum}**
    2. **อัตราดวงจันทร์ (29.53 ÷ {lunar_step} ค่ำ):** = **{lunar_ratio:.4f}**
    3. **รวมผลรวมก้อนแรก:** {base_sum} + {lunar_ratio:.4f} = **{total_combined:.4f}**
    4. **คูณรหัสทองคำจักรวาล:** {total_combined:.4f} × 1.618 = **{final_result:.4f}**
    """)
    
    raw_num = str(abs(final_result)).replace('.', '')
    if len(raw_num) >= 5:
        st.success(f"**ตัวเลขเด่นที่ถอดรหัสได้:** {raw_num[1:3]} , {raw_num[2:4]}")

st.caption("อยู่นิ่งๆ ไม่เจ็บตัว | คุมความเที่ยงตรงด้วยเศษทศนิยมดาราศาสตร์โดยอาจารย์ต๊ะ 2026")
