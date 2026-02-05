import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# --- 1. ตั้งค่าหน้าจอ (สไตล์ดำ-ทอง) ---
st.set_page_config(page_title="SYNAPSE X - MASTERPIECE", layout="wide")
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #FFD700;}
    h1, h2, h3 {color: #FFD700 !important;}
    .stButton>button {background-color: #FFD700; color: black; border-radius: 10px; width: 100%;}
    </style>
    """, unsafe_allow_html=True)

st.title("🔴 SYNAPSE X : REAL-TIME COMMAND")
st.write(f"**SLOGAN:** อยู่นิ่งๆ ไม่เจ็บตัว | **STATUS:** ระบบตรวจจับ IP อัตโนมัติ")

# --- 2. ระบบนาฬิกาไทย (UTC+7) ---
thai_time = datetime.utcnow() + timedelta(hours=7)
st.metric("🕒 SYSTEM TIME (THAILAND)", thai_time.strftime("%H:%M:%S"))

# --- 3. ระบบดึงพิกัดจาก IP (ไม้ตายสุดท้าย ไม่ต้องรอ Permission) ---
st.subheader("📍 พิกัดพื้นที่ปัจจุบัน (ตรวจจับจาก IP)")

try:
    # ดึงข้อมูลจาก API ภายนอกเพื่อหาพิกัด
    response = requests.get('https://ipapi.co/json/').json()
    lat = response.get('latitude')
    lon = response.get('longitude')
    city = response.get('city')
    region = response.get('region')

    if lat and lon:
        st.success(f"✅ ตรวจพบพื้นที่: {city}, {region} | LAT: {lat} | LON: {lon}")
        # แสดงแผนที่
        map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(map_data)
    else:
        st.error("❌ ไม่สามารถดึงพิกัดจาก IP ได้ในขณะนี้")
except:
    st.error("⚠️ ระบบตรวจจับสัญญาณขัดข้อง")

# --- 4. ส่วนสูตรบำบัด 144 ---
st.markdown("---")
st.subheader("📐 Assassin 144 Logic")
val_matrix = st.slider("ปรับระดับ Matrix (V)", 1, 144, 110)
result_144 = (val_matrix * 144) / 10
st.write(f"### ผลลัพธ์พลังงาน: **{result_144}**")

# --- 5. ยูทูป (S.S.S PRIVATE STATION) ---
st.markdown("---")
st.subheader("📺 S.S.S PRIVATE STATION")
st.markdown('<iframe width="100%" height="450" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)

# --- 6. ปุ่มสั่งการสุดท้าย ---
if st.button("🚀 EXECUTE GLOBAL DEPLOY"):
    st.balloons()
    st.success(f"บันทึกข้อมูลเวลา {thai_time.strftime('%H:%M:%S')} เข้าสู่ระบบสำเร็จ!")
