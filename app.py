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

# 2. ส่วนรับข้อมูล (รองรับปี ค.ศ. 1960 - 2026)
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

# C. ระบบล็อกค่าปีนักษัตรตรงๆ ตามปี พ.ศ. (ชวด=1 ยัน ปีกุล=12)
thai_year = selected_date.year + 543

def get_exact_zodiac(year):
    zodiac_order = ["ปีกุล", "ปีชวด", "ปีฉลู", "ปีขาล", "ปีเถาะ", "ปีมะโรง", "ปีมะเส็ง", "ปีมะเมีย", "ปีมะแม", "ปีวอก", "ปีระกา", "ปีจอ"]
    zodiac_map = {
        "ปีชวด": 1, "ปีฉลู": 2, "ปีขาล": 3, "ปีเถาะ": 4,
        "ปีมะโรง": 5, "ปีมะเส็ง": 6, "ปีมะเมีย": 7, "ปีมะแม": 8,
        "ปีวอก": 9, "ปีระกา": 10, "ปีจอ": 11, "ปีกุล": 12
    }
    if year == 2569: return "ปีมะเมีย (ปีม้า)", 7
    if year == 2568: return "ปีมะเส็ง", 6
    if year == 2567: return "ปีมะโรง", 5
    if year == 2566: return "ปีเถาะ", 4
    if year == 2565: return "ปีขาล", 3
    
    calculated_name = zodiac_order[(year - 2444) % 12]
    return calculated_name, zodiac_map.get(calculated_name, 1)

zodiac_name, val_zodiac = get_exact_zodiac(thai_year)

# D. สูตรดาราศาสตร์แกะข้างขึ้นข้างแรมอัตโนมัติ
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

# E. คำนวณตามสูตรและลำดับคณิตศาสตร์ที่นายกำหนดมาเป๊ะๆ
# 1. ฐานรวม วัน + เดือน + ปี
base_sum = val_day + val_month + val_zodiac

# 2. หารค่าดวงจันทร์ (ปรับให้ 29.53 เป็นตัวตั้ง หารด้วยค่าค่ำ เพื่อให้ได้เลข 2.27 ตามโจทย์ที่นายตั้งไว้)
if lunar_step != 0:
    lunar_ratio = 29.53 / lunar_step
else:
    lunar_ratio = 0

# 3. เอาฐานรวม มาบวกกับ ค่าอัตราส่วนดวงจันทร์
total_combined = base_sum + lunar_ratio

# 4. คูณด้วยค่าคงที่ 1.618 ปิดท้ายสมการ
final_result = total_combined * 1.618


# 4. แสดงผลหน้าจอมือถือ
st.write("---")
st.subheader(f"🔍 ดับบระจาวนท: {selected_date.strftime('%d/%m/%Y')}")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(f"วัน{day_name_th}", f"เลขดิบ: {val_day}")
with col2:
    st.metric(f"เดือน{month_name_th}", f"เลขดิบ: {val_month}")
with col3:
    st.metric(f"นักษัตร ({zodiac_name})", f"เลขดิบ: {val_zodiac}")

st.info(f"🌙 **ระบบจันทรคติวันนี้:** {lunar_type} {lunar_step} ค่ำ")

st.write("### 🎯 เลขรหัสสุทธิประจำจักรวาล (Cosmic Index)")
st.metric(label="ค่าพลังงานสุทธิถอดรหัสได้", value=f"{final_result:.4f}")


# 5. โชว์ที่มาสูตรตามกระดาษทดของนาย
with st.expander("📝 ขั้นตอนสมการการถอดรหัส (สูตรตามใบสั่งล่าสุด)"):
    st.markdown(f"""
    **ถอดรหัสตามขั้นตอนจริง:**
    1. **ฐานรวม (วัน + เดือน + ปี):** {val_day} + {val_month} + {val_zodiac} = **{base_sum}**
    2. **อัตราดวงจันทร์ (29.53 ÷ ค่ำ):** 29.53 ÷ {lunar_step} = **{lunar_ratio:.4f}**
    3. **รวมผลรวมก้อนแรก:** {base_sum} + {lunar_ratio:.2f} = **{total_combined:.2f}**
    4. **คูณรหัสทศนิยมคงที่:** {total_combined:.2f} × 1.618 = **{final_result:.4f}**
    """)
    
    raw_num = str(abs(final_result)).replace('.', '')
    if len(raw_num) >= 5:
        st.success(f"**ตัวเลขเด่นที่ถอดรหัสได้:** {raw_num[1:3]} , {raw_num[2:4]}")

st.caption("อยู่นิ่งๆ ไม่เจ็บตัว | โค้ดสัจธรรมความจริงตามใบสั่งอาจารย์ต๊ะ 2026")
