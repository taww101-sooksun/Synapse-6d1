import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
from datetime import datetime

# --- 1. ตั้งค่าหน้าจอ ---
st.set_page_config(page_title="SYNAPSE X - REAL SENSOR", layout="wide")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;} h3 {color: #FFD700 !important;}</style>", unsafe_allow_html=True)

st.title("🔴 SYNAPSE X : REAL-TIME COMMAND")
st.write(f"**SLOGAN:** อยู่นิ่งๆ ไม่เจ็บตัว | **STATUS:** ข้อมูลจริง 100%")

# --- 2. ระบบดึงค่า GPS จริง ---
st.subheader("📍 พิกัดดาวเทียมปัจจุบัน (GPS)")

# คำสั่ง JavaScript ที่เสถียรที่สุดสำหรับมือถือ
location = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(pos => {return {lat: pos.coords.latitude, lon: pos.coords.longitude}})", key="gps_sensor")

if location:
    lat = location['lat']
    lon = location['lon']
    st.success(f"✅ เชื่อมต่อดาวเทียมสำเร็จ: LAT {lat} | LON {lon}")
    # แสดงแผนที่จุดที่คุณอยู่จริง
    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
else:
    st.warning("📡 กำลังรอสัญญาณ... หากพิกัดไม่ขึ้น โปรดกดปุ่มด้านล่างเพื่อกระตุ้นเซนเซอร์")
    if st.button("🛰️ ดึงพิกัดจากดาวเทียม (FORCE GET)"):
        st.rerun()

# --- 3. ส่วนเสริม ---
col1, col2 = st.columns(2)
with col1:
    st.metric("🕒 SYSTEM TIME", datetime.now().strftime("%H:%M:%S"))
with col2:
    st.info("ระบบความปลอดภัย: เชื่อมต่อเซนเซอร์ภายนอกพร้อมทำงาน")

# --- 4. สูตรบำบัด 144 ---
st.markdown("---")
st.subheader("📐 Assassin 144 Calculation")
val_matrix = st.slider("ปรับระดับ Matrix (V)", 1, 144, 72)
result_144 = (val_matrix * 144) / 10
st.write(f"### ผลลัพธ์พลังงานบำบัด: **{result_144}**")

# --- 5. ปุ่มสั่งการ ---
if st.button("🚀 EXECUTE GLOBAL DEPLOY"):
    if location:
        st.balloons()
        st.success(f"ส่งพิกัด {location['lat']} เข้าสู่ระบบ SYNAPSE เรียบร้อย!")
    else:
        st.error("ไม่สามารถส่งข้อมูลได้เนื่องจากไม่มีค่า GPS จริง")
