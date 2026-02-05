import streamlit as st
from datetime import datetime, timedelta

# --- CONFIG ---
st.set_page_config(page_title="SYNAPSE X - THE 10 TRUTHS", layout="wide")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;} .stMetric {background-color: #111; padding: 10px; border-radius: 5px;}</style>", unsafe_allow_html=True)

st.title("🔴 SYNAPSE X : COMMAND CENTER")
st.write(f"**SLOGAN:** อยู่นิ่งๆ ไม่เจ็บตัว | **MISSION:** บำบัดและควบคุมความจริง")

# --- ข้อมูล 10 อย่าง (The 10 Vital Signals) ---
st.subheader("📊 ข้อมูลวิเคราะห์ระบบ (10 Parameters)")

col1, col2, col3 = st.columns(3)

with col1:
    # 1. เวลาไทยจริง
    thai_time = datetime.utcnow() + timedelta(hours=7)
    st.metric("1. REAL TIME (TH)", thai_time.strftime("%H:%M:%S"))
    
    # 2. พิกัด (ป้อนค่าจริง)
    location_input = st.text_input("2. LOCATION (ระบุพื้นที่จริง)", "สมุทรปราการ")
    
    # 3. สถานะร่างกาย (User Status)
    body_status = st.selectbox("3. BODY STATUS", ["ปกติ", "อ่อนเพลีย", "ต้องการพลังงาน"])

with col2:
    # 4. ค่า Matrix 144
    val_matrix = st.slider("4. MATRIX INPUT (V)", 1, 144, 72)
    
    # 5. พลังงานบำบัด (ผลลัพธ์)
    result_144 = (val_matrix * 144) / 10
    st.metric("5. OUTPUT ENERGY", f"{result_144}")
    
    # 6. อุณหภูมิหน้างาน (ป้อนค่าจริงที่สัมผัสได้)
    temp_input = st.number_input("6. REAL TEMP (°C)", value=32)

with col3:
    # 7. ระดับความปลอดภัย (Safety Level)
    st.metric("7. SAFETY LEVEL", "HIGH" if result_144 <= 1500 else "CRITICAL")
    
    # 8. สถานะเครือข่าย
    st.write("8. NETWORK: **CONNECTED**")
    
    # 9. โหมดการทำงาน
    mode = st.radio("9. SYSTEM MODE", ["บำบัด (Healing)", "เฝ้าระวัง (Monitor)"])
    
    # 10. สโลแกนยืนยันตัวตน
    st.info(f"10. SLOGAN: **อยู่นิ่งๆ ไม่เจ็บตัว**")

# --- ส่วนควบคุมและแสดงผลแผนที่ ---
st.markdown("---")
if st.button("🚀 EXECUTE GLOBAL DEPLOY (บันทึกค่าจริง)"):
    st.success(f"บันทึกข้อมูลทั้ง 10 อย่าง ณ เวลา {thai_time.strftime('%H:%M:%S')} เรียบร้อยแล้ว")
    st.balloons()

# --- สถานีความจริง (S.S.S PRIVATE STATION) ---
st.subheader("📺 S.S.S PRIVATE STATION")
st.markdown('<iframe width="100%" height="400" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
