import streamlit as st
import requests
from streamlit_js_eval import get_geolocation
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
import firebase_admin
from firebase_admin import credentials, db
import os

# --- 1. INITIALIZE (ตั้งค่าหน้าจอ) ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="centered")

# เชื่อมต่อ Firebase (ถ้าต้องการเก็บ Log เงียบๆ ไว้ดูเอง)
if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/'})
    except: pass

# --- 2. DICTIONARY ---
texts = {
    "TH": {
        "call_h": "📞 ระบบติดต่อสื่อสาร (CLICK TO OPEN)",
        "call_btn": "🚀 เริ่มการเชื่อมต่อสัญญาณ",
        "status": "'อยู่นิ่งๆ ไม่เจ็บตัว'",
        "time_label": "⏰ เวลาตำแหน่งจริง",
        "weather": "🌡️ อุณหภูมิ", "wind": "💨 ลม"
    },
    "EN": {
        "call_h": "📞 COMMUNICATION SYSTEM (CLICK TO OPEN)",
        "call_btn": "🚀 START CONNECTION",
        "status": "'Stay Still & No Pain'",
        "time_label": "⏰ Local Time",
        "weather": "🌡️ Temp", "wind": "💨 Wind"
    }
}

if 'lang' not in st.session_state: st.session_state.lang = "TH"
t = texts[st.session_state.lang]

# --- 3. STYLE (รุ้ง + ดำเงา) ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); background-size: 1200% 1200%; animation: RainbowFlow 10s ease infinite; }
    .glossy-card { background: rgba(0, 0, 0, 0.85); border: 2px solid white; border-radius: 15px; padding: 20px; color: white; box-shadow: 0 0 15px #fff; text-shadow: 0 0 5px #fff; margin-bottom: 15px; }
    .streamlit-expanderHeader { background-color: black !important; color: white !important; font-size: 1.5rem !important; border: 2px solid white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGO & HEADER ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo2.jpg", use_container_width=True)
    except:
        st.markdown("<h2 style='text-align: center; color: white;'>🛰️ SYNAPSE</h2>", unsafe_allow_html=True)

c1, c2 = st.columns([4, 1])
with c1: st.title("🛰️ COMMAND CENTER")
with c2: 
    if st.button("🌐 TH/EN"):
        st.session_state.lang = "EN" if st.session_state.lang == "TH" else "TH"
        st.rerun()

# --- 5. REALITY CORE (GPS + แผนที่) ---
location = get_geolocation()

if location and location.get('coords'):
    lat, lon = location['coords']['latitude'], location['coords']['longitude']
    
    # ดึงเวลา
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    now = datetime.now(pytz.timezone(tz_name if tz_name else 'Asia/Bangkok')).strftime('%H:%M:%S')

    # ดึงที่อยู่
    try:
        geo = Nominatim(user_agent="synapse_v3_free")
        addr = geo.reverse(f"{lat}, {lon}", timeout=10).raw['address']
        detail = f"🏠 {addr.get('village', addr.get('suburb', '---'))} | 🏙️ {addr.get('province', '')}"
    except: detail = f"📍 {lat:.4f}, {lon:.4f}"

    # สภาพอากาศ
    try:
        w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
        temp, wind = w['temperature'], w['windspeed']
    except: temp, wind = "--", "--"

    st.markdown(f"""
    <div class="glossy-card">
        <p style='color: #00ff00; font-weight: bold; font-size: 1.2rem;'>{detail}</p>
        <hr>
        <div style='display: flex; justify-content: space-around; font-size: 1.1rem;'>
            <span>{t['weather']}: {temp}°C</span>
            <span>{t['wind']}: {wind}km/h</span>
            <span style='color: yellow;'>{t['time_label']}: {now}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # แผนที่
    m = folium.Map(location=[lat, lon], zoom_start=17, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Hybrid')
    folium.Marker([lat, lon], icon=folium.Icon(color='red')).add_to(m)
    st_folium(m, use_container_width=True, height=400, key="map_no_auth")
else:
    st.info("📡 กรุณากด 'Allow Location' เพื่อเปิดระบบแผนที่")

# --- 6. COMMUNICATION & FOOTER ---
with st.expander(t["call_h"]):
    call_room = st.text_input("รหัสห้อง", "synapse_free_zone")
    if st.button(t["call_btn"]):
        st.markdown(f'<iframe src="https://meet.jit.si/SYNAPSE_{call_room}" allow="camera; microphone; fullscreen" width="100%" height="600" style="border: 2px solid white; border-radius: 15px;"></iframe>', unsafe_allow_html=True)

st.markdown(f"<div class='glossy-card'>{t['status']}</div>", unsafe_allow_html=True)
st.markdown('<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0"></iframe>', unsafe_allow_html=True)
