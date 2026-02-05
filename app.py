import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import requests
from datetime import datetime, timedelta

# --- CONFIG ---
st.set_page_config(page_title="SYNAPSE X - THE TRUTH", layout="wide")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.title("🔴 SYNAPSE X : REAL-TIME TRUTH")
st.write(f"**SLOGAN:** อยู่นิ่งๆ ไม่เจ็บตัว | **STATUS:** ข้อมูลจากเซนเซอร์มือถือโดยตรง")

# --- 1. เวลาไทยที่แท้จริง ---
thai_time = datetime.utcnow() + timedelta(hours=7)
st.metric("🕒 เวลาไทยปัจจุบัน", thai_time.strftime("%H:%M:%S"))

# --- 2. ดึงพิกัดจาก "เซนเซอร์มือถือคุณต๊ะ" เท่านั้น (ไม่เอาค่า Server) ---
st.subheader("📍 จุดพิกัดที่คุณยืนอยู่จริง")
location = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(pos => { return {lat: pos.coords.latitude, lon: pos.coords.longitude} })", key="real_sensor_gps")

if location:
    lat = location['lat']
    lon = location['lon']
    
    # เมื่อได้พิกัดจริงแล้ว ค่อยไปดึงสภาพอากาศจากจุดนั้น
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_data = requests.get(weather_url).json()
    temp_real = weather_data['current_weather']['temperature']

    st.success(f"✅ ตรวจพบเซนเซอร์จริง: LAT {lat} | LON {lon}")
    st.metric("🌡️ อุณหภูมิหน้างานจริง", f"{temp_real} °C")
    
    # แสดงแผนที่จุดที่อยู่จริง
    st.map({"lat": [lat], "lon": [lon]})
else:
    st.warning("⚠️ รอการตอบรับจากเซนเซอร์ GPS... (โปรดกด 'อนุญาต' บนหน้าจอเพื่อยืนยันตัวตนจริง)")

# --- 3. ลอจิก 144 ---
st.markdown("---")
val_matrix = st.slider("MATRIX INPUT", 1, 144, 72)
result_144 = (val_matrix * 144) / 10
st.write(f"### OUTPUT: **{result_144}**")

# --- 4. สถานีบันเทิง ---
st.markdown('<iframe width="100%" height="315" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
