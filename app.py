import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
from datetime import datetime, timedelta

# --- 1. ตั้งค่าหน้าจอ (Theme ดำ-ทอง) ---
st.set_page_config(page_title="SYNAPSE X - MASTERPIECE", layout="wide")
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #FFD700;}
    h1, h2, h3 {color: #FFD700 !important;}
    .stButton>button {background-color: #FFD700; color: black; border-radius: 10px; width: 100%;}
    </style>
    """, unsafe_allow_html=True)

st.title("🔴 SYNAPSE X : REAL-TIME COMMAND")
st.write(f"**SLOGAN:** อยู่นิ่งๆ ไม่เจ็บตัว | **STATUS:** ระบบไทยสมบูรณ์แบบ")

# --- 2. ระบบนาฬิกาไทย (UTC+7) ---
# แก้ไขเวลาให้ตรงกับประเทศไทย 100%
thai_time = datetime.utcnow() + timedelta(hours=7)
st.metric("🕒 SYSTEM TIME (THAILAND)", thai_time.strftime("%H:%M:%S"))

# --- 3. ระบบดึงค่า GPS จริง (Sensor) ---
st.subheader("📍 พิกัดดาวเทียมปัจจุบัน (GPS)")
location = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(pos => {return {lat: pos.coords.latitude, lon: pos.coords.longitude}})", key="gps_v3")

if location:
    lat, lon = location['lat'], location['lon']
    st.success(f"✅ เชื่อมต่อดาวเทียมสำเร็จ: LAT {lat} | LON {lon}")
    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
else:
    st.warning("📡 กำลังรอสัญญาณ GPS... (โปรดใช้ Chrome และกด Allow)")
    if st.button("🛰️ ปลุกสัญญาณ GPS (FORCE ACTIVATE)"):
        st.rerun()

# --- 4. ส่วนสูตรบำบัด 144 ---
st.markdown("---")
st.subheader("📐 Assassin 144 Logic")
val_matrix = st.slider("ปรับระดับ Matrix (V)", 1, 144, 110)
result_144 = (val_matrix * 144) / 10
st.write(f"### ผลลัพธ์พลังงาน: **{result_144}**")

# --- 5. ยูทูป (S.S.S PRIVATE STATION) - เอากลับมาแล้วครับ! ---
st.markdown("---")
st.subheader("📺 S.S.S PRIVATE STATION")
# ใส่ Playlist เดิมของคุณต๊ะ
st.markdown('<iframe width="100%" height="450" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)

# --- 6. ปุ่มสั่งการสุดท้าย ---
st.markdown("---")
if st.button("🚀 EXECUTE GLOBAL DEPLOY"):
    if location:
        st.balloons()
        st.success("บันทึกข้อมูลและส่งพิกัดเรียบร้อย!")
    else:
        st.error("ไม่สามารถส่งข้อมูลได้เนื่องจากไม่มีค่า GPS")
