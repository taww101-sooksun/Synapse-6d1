import streamlit as st
from datetime import datetime

# 1. สไตล์ Dark Neon อาจารย์ต๊ะ
st.set_page_config(page_title="Cosmic Truth-Center", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ff00; }
    h1 { color: #ff00ff; text-shadow: 2px 2px #000000; text-align: center; }
    .stMetric { background-color: #1e2130; border-radius: 10px; padding: 15px; border: 1px solid #00ff00; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌌 Cosmic Commander")
st.write("<center>ระบบถอดรหัสรหัสสุทธิ บนฐานความจริง 100%</center>", unsafe_allow_html=True)

# 2. ป้อนวัน เดือน ปี สากล
selected_date = st.date_input("📅 กรอก วัน/เดือน/ปี ที่ต้องการเช็ค", value=datetime.now())

# 🆕 3. คลังคลังฐานข้อมูลความจริงแท้ (นายอยากเพิ่มวันไหนให้แม่นยำ 100% เอามาเติมตรงนี้ได้ตลอด)
truth_table = {
    "18/05/1984": {"type": "แรม", "step": 3},  # ล็อกค่าตามรูปปฏิทินจริงของนาย
    "17/08/1996": {"type": "ขึ้น", "step": 4},  # ล็อกค่าตามปฏิทินหลวงจริง
    "28/05/2026": {"type": "ขึ้น", "step": 12}, # ล็อกค่าของวันนี้เป๊ะๆ
}

date_str = selected_date.strftime("%d/%m/%Y")

st.write("---")
st.subheader("🌙 ตรวจสอบระบบจันทรคติ")

# เช็คว่าวันที่กรอก อยู่ในคลังความจริงของเราไหม
if date_str in truth_table:
    st.success(f"🎯 ค้นพบข้อมูลในคลังความจริงสากล! (ล็อกค่าปฏิทินหลวงอัตโนมัติ)")
    lunar_type = truth_table[date_str]["type"]
    lunar_step = truth_table[date_str]["step"]
    st.info(f"ระบบดึงค่าความจริงตรงจากปฏิทิน: **{lunar_type} {lunar_step} ค่ำ**")
else:
    # วันอื่นๆ ที่ระบบไม่รู้ ให้สไลเดอร์โผล่มาให้นายควบคุมความจริงด้วยตัวเอง
    st.warning("⚠️ วันนี้ไม่อยู่ในคลังความจริงด่วน กรุณาเลือกข้างขึ้นแรมตามปฏิทินจริง")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        lunar_type = st.selectbox("เลือกสถานะดวงจันทร์", ["ขึ้น", "แรม"])
    with col_l2:
        lunar_step = st.slider("จำนวนค่ำ (1-15 ค่ำ)", min_value=1, max_value=15, value=1)


# 4. ถอดรหัสเลขดิบ (ส่วนนี้คอมพิวเตอร์ทำถูกชัวร์ 100%)
val_day = selected_date.isoweekday()
day_name_th = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"][val_day - 1]

val_month = selected_date.month
month_name_th = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"][val_month]

thai_year = selected_date.year + 543
def get_exact_zodiac(year):
    zodiac_order = [
        ("ปีชวด", 1), ("ปีฉลู", 2), ("ปีขาล", 3), ("ปีเถาะ", 4),
        ("ปีมะโรง", 5), ("ปีมะเส็ง", 6), ("ปีมะเมีย", 7), ("ปีมะแม", 8),
        ("ปีวอก", 9), ("ปีระกา", 10), ("ปีจอ", 11), ("ปีกุล", 12)
    ]
    base_year = 2503
    index = (year - base_year) % 12
    return zodiac_order[index]

zodiac_name, val_zodiac = get_exact_zodiac(thai_year)


# 5. สมการทองคำของนาย
base_sum = val_day + val_month + val_zodiac
lunar_ratio = 29.53 / lunar_step
total_combined = base_sum + lunar_ratio
final_result = total_combined * 1.618


# 6. แสดงหน้าจอผลลัพธ์
st.write("---")
col1, col2, col3 = st.columns(3)
with col1: st.metric(f"วัน{day_name_th}", f"เลขดิบ: {val_day}")
with col2: st.metric(f"เดือน{month_name_th}", f"เลขดิบ: {val_month}")
with col3: st.metric(f"นักษัตร ({zodiac_name})", f"เลขดิบ: {val_zodiac}")

st.write("### 🎯 เลขรหัสสุทธิประจำจักรวาล (Cosmic Index)")
st.metric(label="ค่าพลังงานสุทธิถอดรหัสได้", value=f"{final_result:.4f}")

with st.expander("📝 เจาะลึกสมการกระดาษทด"):
    st.markdown(f"""
    1. **ฐานรวม:** {val_day} + {val_month} + {val_zodiac} = **{base_sum}**
    2. **อัตราดวงจันทร์ (29.53 ÷ {lunar_step}):** = **{lunar_ratio:.4f}**
    3. **รวมก้อนแรก:** {base_sum} + {lunar_ratio:.4f} = **{total_combined:.4f}**
    4. **คูณรหัสทองคำ:** {total_combined:.4f} × 1.618 = **{final_result:.4f}**
    """)

st.caption("อยู่นิ่งๆ ไม่เจ็บตัว | ล็อกเป้าความเที่ยงตรง 100% โดยอาจารย์ต๊ะ 2026")
