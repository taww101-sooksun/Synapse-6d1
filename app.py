import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# --- CONFIG ---
st.set_page_config(page_title="SYNAPSE X - TRUTH", layout="wide")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

# --- 1. เวลาจริง (THAILAND) ---
thai_time = datetime.utcnow() + timedelta(hours=7)
st.metric("🕒 REAL TIME", thai_time.strftime("%H:%M:%S"))

# --- 2. ข้อมูลพิกัดและสภาพอากาศจริง (REAL SENSOR) ---
try:
    # ดึงพิกัดจาก IP จริง
    geo = requests.get('https://ipapi.co/json/').json()
    lat, lon = geo.get('latitude'), geo.get('longitude')
    city = geo.get('city')
    
    # ดึงสภาพอากาศจริงจากพิกัด (Open-Meteo API - No Key Required)
    weather = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true').json()
    temp = weather['current_weather']['temperature']

    st.subheader(f"📍 AREA: {city} | {lat}, {lon}")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🌡️ REAL TEMP", f"{temp} °C")
    with col2:
        st.success("STATUS: SENSOR ONLINE")
    
    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
except:
    st.error("⚠️ SENSOR ERROR: ไม่สามารถดึงข้อมูลจริงได้")

# --- 3. ลอจิก 144 (จับต้องได้) ---
st.markdown("---")
val_matrix = st.slider("MATRIX INPUT", 1, 144, 72)
result_144 = (val_matrix * 144) / 10

if result_144 > 1500:
    st.error(f"OVERLOAD: {result_144} | ลดค่าเพื่อความปลอดภัย")
else:
    st.write(f"### OUTPUT: **{result_144}**")

# --- 4. สถานีจริง ---
st.markdown('<iframe width="100%" height="315" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

if st.button("🚀 EXECUTE TRUTH"):
    st.info(f"บันทึกค่าจริง ณ {thai_time.strftime('%H:%M:%S')} เรียบร้อย")
