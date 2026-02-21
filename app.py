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

# --- 1. INITIALIZE ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="centered")

if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/'})
    except: pass

# --- 2. MULTI-LANGUAGE ---
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

# --- 3. STYLE (ดำเงาแว้บ + รุ้ง 10s) ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); background-size: 1200% 1200%; animation: RainbowFlow 10s ease infinite; }
    .glossy-card { background: rgba(0, 0, 0, 0.9); border: 2px solid white; border-radius: 15px; padding: 20px; color: white; box-shadow: 0 0 15px #fff; text-shadow: 0 0 5px #fff; margin-bottom: 15px; }
    /* ปุ่มพับหน้าจอใหญ่พิเศษ */
    .streamlit-expanderHeader { background-color: black !important; color: white !important; font-size: 1.5rem !important; border: 2px solid white !important; border-radius: 10px !important; padding: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SECURITY GATE ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if not st.session_state.authenticated:
    st.markdown("<div class='glossy-card'>", unsafe_allow_html=True)
    st.subheader("🔐 SYNAPSE ACCESS")
    u_id = st.text_input("ID")
    u_pw = st.text_input("Password", type="password")
    if st.button("UNLOCK"):
        if u_pw == "synapse2026" and u_id:
            st.session_state.authenticated = True
            st.session_state.my_id = u_id
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. HEADER & LANG ---
c1, c2 = st.columns([4, 1])
with c1: st.title("🛰️ COMMAND CENTER")
with c2: 
    if st.button("🌐 TH/EN"):
        st.session_state.lang = "EN" if st.session_state.lang == "TH" else "TH"
        st.rerun()

# --- 6. REALITY CORE (LOCATION & TIME) ---
location = get_geolocation()
if location and location.get('coords'):
    lat, lon = location['coords']['latitude'], location['coords']['longitude']
    
    # ดึงเวลาตามตำแหน่งจริง (เพื่อนนายอยู่อังกฤษก็ได้เวลาอังกฤษ)
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    if tz_name:
        local_tz = pytz.timezone(tz_name)
        now = datetime.now(local_tz).strftime('%H:%M:%S')
    else:
        now = datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%H:%M:%S')

    # ดึงที่อยู่ (ถนน หมู่บ้าน แม่น้ำ)
    try:
        geo = Nominatim(user_agent="synapse_v3")
        addr = geo.reverse(f"{lat}, {lon}", language='th' if st.session_state.lang == "TH" else 'en').raw['address']
        detail = f"🏠 {addr.get('village', addr.get('suburb', '---'))} | 🛣️ {addr.get('road', '---')} | 🏙️ {addr.get('province', '')}"
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
        <div style='display: flex; justify-content: space-around; font-size: 1.2rem;'>
            <span>{t['weather']}: {temp}°C</span>
            <span>{t['wind']}: {wind}km/h</span>
            <span style='color: yellow;'>{t['time_label']}: {now}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # MAP
    m = folium.Map(location=[lat, lon], zoom_start=17, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Hybrid')
    folium.Marker([lat, lon], icon=folium.Icon(color='blue')).add_to(m)
    st_folium(m, use_container_width=True, height=400)

# --- 7. ระบบโทร JITSI (ใน Expander ใหญ่) ---
with st.expander(t["call_h"], expanded=False):
    st.markdown("<div style='background: black;
