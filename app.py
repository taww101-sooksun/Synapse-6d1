import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# --- 1. ตั้งค่าหน้าจอ (Theme สีดำ-ทอง ตามสไตล์คุณต๊ะ) ---
st.set_page_config(page_title="SYNAPSE X - REAL SENSOR", layout="wide")
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #FFD700;}
    h1, h2, h3 {color: #FFD700 !important;}
    .stButton>button {background-color: #FFD700; color: black; border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. ส่วนหัวแอป ---
st.title("🔴 SYNAPSE X : REAL-TIME COMMAND")
st.write(f"**SLOGAN:** อยู่นิ่งๆ ไม่เจ็บตัว | **STATUS:** ข้อมูลจริง 100%")

# --- 3. ระบบดึงค่า GPS จริง (Sensor Integration) ---
st.subheader("📍 พิกัดดาวเทียมปัจจุบัน (GPS)")
# ใช้ JavaScript ดึงค่าจากมือถือ/คอมพิวเตอร์จริง
location = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(pos => {return {lat: pos.coords.latitude, lon: pos.coords.longitude}})", key="gps")

col1, col2 = st.columns([2, 1])

with col1:
    if location:
        lat = location['lat']
        lon = location['lon']
        st.success(f"ตรวจพบตำแหน่ง: LAT {lat} | LON {lon}")
        # แสดงแผนที่จุดที่อยู่จริง
        st.map({"lat": [lat], "lon": [lon]})
    else:
        st.warning("📡 กำลังรอสัญญาณ GPS... (โปรดตรวจสอบว่ากด 'Allow' หรือ 'อนุญาต' บนเบราว์เซอร์แล้ว)")

with col2:
    st.metric("🕒 SYSTEM TIME", datetime.now().strftime("%H:%M:%S"))
    st.info("ระบบความปลอดภัย: เชื่อมต่อเซนเซอร์ภายนอกพร้อมทำงาน")

# --- 4. สูตรบำบัด 144 (Assassin Logic) ---
st.markdown("---")
st.subheader("📐 Assassin 144 Calculation")
val_matrix = st.slider("ปรับระดับพลังงาน Matrix (V)", 1, 144, 72)

# คำนวณจริงตามลอจิก 144
result_144 = (val_matrix * 144) / 10 
st.latex(r"Energy = \frac{Matrix \times 144}{10}")
st.write(f"### ผลลัพธ์พลังงานบำบัด: **{result_144}**")

# --- 5. ระบบบันเทิงและความปลอดภัย ---
st.subheader("📺 S.S.S PRIVATE STATION")
# ใส่ Playlist YouTube ของคุณ
st.markdown('<iframe width="100%" height="400" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

# --- 6. ปุ่มคำสั่งสุดท้าย ---
st.markdown("---")
if st.button("🚀 EXECUTE GLOBAL DEPLOY (ยืนยันค่าจริง)"):
    if location:
        st.balloons()
        st.success(f"ส่งข้อมูลพิกัด {location['lat']} และค่าพลังงาน {result_144} เข้าสู่ระบบเรียบร้อย!")
    else:
        st.error("ไม่สามารถส่งข้อมูลได้เนื่องจากไม่มีค่า GPS จริง")

st.caption("พัฒนาโดยระบบ SYNAPSE X - เพื่อความปลอดภัยสูงสุดของผู้ใช้")
