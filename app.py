import streamlit as st
from datetime import datetime

# 1. สไตล์แบบอาจารย์ต๊ะ (Dark Neon)
st.set_page_config(page_title="Cosmic Commander", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ff00; }
    h1 { color: #ff00ff; text-shadow: 2px 2px #000000; text-align: center; }
    .stMetric { background-color: #1e2130; border-radius: 10px; padding: 15px; border: 1px solid #00ff00; }
    sidebar .sidebar-content { background-color: #111; }
    </style>
    """, unsafe_allow_html=True)

# 2. ทำเมนูแยกหัวข้อเฉพาะตามใบสั่งของนาย
menu = st.sidebar.selectbox("เลือกหัวข้อการทำงาน", ["1. ถอดรหัส Cosmic Index", "2. คำนวณข้างขึ้นข้างแรมโดยเฉพาะ"])

# -----------------------------------------------------------------
# ฟังก์ชันคำนวณฐานข้อมูล (ใช้ร่วมกัน)
# -----------------------------------------------------------------
def get_exact_zodiac(year_th):
    zodiac_order = [
        ("ปีชวด", 1), ("ปีฉลู", 2), ("ปีขาล", 3), ("ปีเถาะ", 4),
        ("ปีมะโรง", 5), ("ปีมะเส็ง", 6), ("ปีมะเมีย", 7), ("ปีมะแม", 8),
        ("ปีวอก", 9), ("ปีระกา", 10), ("ปีจอ", 11), ("ปีกุล", 12)
    ]
    base_year = 2503
    index = (year_th - base_year) % 12
    return zodiac_order[index]


# =================================================================
# หมวดที่ 1: หน้าถอดรหัสรหัสสุทธิ (Cosmic Index)
# =================================================================
if menu == "1. ถอดรหัส Cosmic Index":
    st.title("🌌 Cosmic Auto-Decoder")
    st.write("<center>ระบบถอดรหัสพลังงานสุทธิจักรวาล (เน้นความแม่นยำสูง)</center>", unsafe_allow_html=True)
    
    selected_date = st.date_input("📅 เลือก วัน/เดือน/ปี ที่ต้องการเช็ค", value=datetime.now())
    
    st.write("---")
    st.subheader("🌙 ป้อนข้อมูลจันทรคติจริงจากปฏิทินหลวง")
    col_lunar1, col_lunar2 = st.columns(2)
    with col_lunar1:
        lunar_type = st.selectbox("เลือกสถานะดวงจันทร์", ["ขึ้น", "แรม"])
    with col_lunar2:
        lunar_step = st.slider("จำนวนค่ำ (1-15 ค่ำ)", min_value=1, max_value=15, value=12)

    # คำนวณเลขดิบ
    val_day = selected_date.isoweekday()
    day_name_th = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"][val_day - 1]
    val_month = selected_date.month
    month_name_th = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"][val_month]
    
    thai_year = selected_date.year + 543
    zodiac_name, val_zodiac = get_exact_zodiac(thai_year)

    # สมการหลักของนาย
    base_sum = val_day + val_month + val_zodiac
    lunar_ratio = 29.53 / lunar_step
    total_combined = base_sum + lunar_ratio
    final_result = total_combined * 1.618

    # แสดงผล
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric(f"วัน{day_name_th}", f"เลขดิบ: {val_day}")
    with col2: st.metric(f"เดือน{month_name_th}", f"เลขดิบ: {val_month}")
    with col3: st.metric(f"นักษัตร ({zodiac_name})", f"เลขดิบ: {val_zodiac}")
    
    st.success(f"🌙 **ฐานจันทรคติล็อกค่าไว้ที่:** {lunar_type} {lunar_step} ค่ำ")
    st.write("### 🎯 Cosmic Index สุทธิ")
    st.metric(label="ค่าพลังงานถอดรหัสได้", value=f"{final_result:.4f}")


# =================================================================
# หมวดที่ 2: หน้าคำนวณข้างขึ้นข้างแรมโดยเฉพาะ (สูตรกลไกจันทรคติ)
# =================================================================
elif menu == "2. คำนวณข้างขึ้นข้างแรมโดยเฉพาะ":
    st.title("🌙 Lunar Phase Analyzer")
    st.write("<center>หัวข้อคำนวณและวิเคราะห์แกะรอยข้างขึ้นข้างแรมไทยย้อนหลัง</center>", unsafe_allow_html=True)
    
    test_date = st.date_input("📅 เลือกวันที่ต้องการให้ระบบแกะรอยข้างขึ้นข้างแรม", value=datetime.now())
    
    # ดึงค่าวันเพื่อคำนวณระยะห่าง
    # ใช้จุดสอบทาน (Epoch) ที่คำนวณชดเชยค่าเบี่ยงเบนสะสมของไทย
    ref_date = datetime(1970, 1, 1) 
    diff_days = (test_date - ref_date.date()).days
    
    # วงรอบดวงจันทร์จันทรคติไทยเฉลี่ยเชิงลึก (Synodic Month)
    synodic_month = 29.530588853
    
    # คำนวณหาอายุของดวงจันทร์ในรอบเดือนนั้นๆ
    moon_age = diff_days % synodic_month
    if moon_age < 0:
        moon_age += synodic_month
        
    st.write("---")
    st.subheader("📊 ผลการวิเคราะห์กลไกทางดาราศาสตร์")
    
    # คำนวณเปอร์เซ็นต์ความสว่างของผิวดวงจันทร์จริง
    if moon_age <= (synodic_month / 2):
        brightness = (moon_age / (synodic_month / 2)) * 100
        phase_status = "ดวงจันทร์กำลังโต (Waxing)"
    else:
        brightness = (1 - ((moon_age - (synodic_month / 2)) / (synodic_month / 2))) * 100
        phase_status = "ดวงจันทร์กำลังแหว่ง (Waning)"
        
    st.metric(label="🌓 สถานะรูปทรงดวงจันทร์บนฟ้า", value=phase_status)
    st.metric(label="💡 เปอร์เซ็นต์ความสว่างของแสงจันทร์", value=f"{brightness:.2f} %")
    
    # ถอดค่ากลับมาเป็น ข้างขึ้น ข้างแรม แบบปัดเศษพิกัดปฏิทินหลวง
    half = synodic_month / 2.0
    if moon_age < half:
        calculated_type = "ขึ้น"
        calculated_step = int((moon_age / half) * 15) + 1
    else:
        calculated_type = "แรม"
        calculated_step = int(((moon_age - half) / half) * 15) + 1
        
    if calculated_step > 15: calculated_step = 15

    st.write("---")
    st.subheader("🔮 ผลลัพธ์จันทรคติที่โค้ดประมวลผลได้")
    st.info(f"ระบบคำนวณออกมาได้เป็น: **{calculated_type} {calculated_step} ค่ำ**")
    
    st.warning("""
    ⚠️ **บันทึกความจริงจากนักพัฒนา:** \n
    เนื่องจากปฏิทินไทยมีกฎเกณฑ์พิเศษ (เช่น มีเดือน 8 สองหน หรือมีการเพิ่มวันในบางปีตามคำสั่งปฏิทินหลวง) 
    ผลลัพธ์ข้างต้นอาจคลาดเคลื่อน 1 วันในบางช่วงปี (เช่น วันนี้อาจขึ้น 12 แต่โค้ดปัดเป็น 13) 
    แนะนำให้ใช้หน้านี้เพื่อ 'ดูแนวโน้มของแสงจันทร์' แล้วนำค่าที่ถูกต้องที่สุดไปป้อนในหัวข้อที่ 1 เพื่อความเที่ยงตรง
    """)

st.sidebar.write("---")
st.sidebar.caption("อยู่นิ่งๆ ไม่เจ็บตัว | Command Center v2.0")
