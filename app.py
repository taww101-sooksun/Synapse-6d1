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
import uuid
import os

# --- 1. INITIALIZE FIREBASE ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="centered")

if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/',
            'storageBucket': 'notty-101.firebasestorage.app' 
        })
    except: pass

# --- 2. SECURITY GATE (ยึดตามโค้ดของนาย) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
        <style>
        .login-box { background: rgba(0,0,0,0.9); border: 2px solid #fff; padding: 30px; border-radius: 20px; box-shadow: 0 0 20px #fff; text-align: center; }
        </style>
        """, unsafe_allow_html=True)
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: white;'>🔐 SYNAPSE ACCESS CONTROL</h2>", unsafe_allow_html=True)
    with st.form("Login"):
        u_id = st.text_input("Enter your ID / ใส่ ID ของคุณ (ห้ามเว้นว่าง)")
        u_pw = st.text_input("Password / รหัสผ่าน", type="password")
        if st.form_submit_button("UNLOCK SYSTEM"):
            if u_pw == "synapse2026" and u_id: 
                st.session_state.authenticated = True
                st.session_state.my_id = u_id
                st.rerun()
            else:
                st.error("Unauthorized! / รหัสผิด")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 3. SETTINGS & STYLE ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp { background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); background-size: 1200% 1200%; animation: RainbowFlow 10s ease infinite; }
    
    /* กรอบดำเงาแว้บ ตัวหนังสือขาวแสบตา */
    .glossy-card { 
        background: rgba(0, 0, 0, 0.85); 
        border: 2px solid white; 
        border-radius: 15px; 
        padding: 20px; 
        color: white; 
        box-shadow: 0 0 15px #fff, inset 0 0 10px rgba(255,255,255,0.2);
        text-shadow: 0 0 5px #fff;
        margin-bottom: 15px;
    }
    
    /* ปรับปุ่มพับหน้าจอ (Expander) ให้ใหญ่และชัด */
    .streamlit-expanderHeader { 
        background-color: black !important; 
        color: white !important; 
        font-size: 1.5rem !important; 
        font-weight: bold !important;
        border: 2px solid white !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

my_id = st.session_state.my_id

# --- 4. CORE DATA (GPS, WEATHER, ADDRESS) ---
location = get_geolocation()
if location and location.get('coords'):
    coords = location['coords']
    lat, lon = coords['latitude'], coords['longitude']
    
    # ดึงที่อยู่ละเอียด (ถนน หมู่บ้าน แม่น้ำ)
    try:
        geolocator = Nominatim(user_agent="synapse_final")
        address = geolocator.reverse(f"{lat}, {lon}", language='th').raw['address']
        # ดึงความจริง: หมู่บ้าน/ถนน/แม่น้ำ
        village = address.get('village') or address.get('suburb') or "ไม่ระบุหมู่บ้าน"
        road = address.get('road') or "ไม่ระบุถนน"
        waterway = address.get('waterway') or "ไม่มีแหล่งน้ำใกล้เคียง"
        province = address.get('province') or ""
        full_detail = f"🏠 {village} | 🛣️ {road} | 🌊 {waterway} | 🏙️ {province}"
    except:
        full_detail = f"📍 พิกัด: {lat:.5f}, {lon:.5f}"

    # ดึงสภาพอากาศจริง
    try:
        w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
        temp, wind = w_res['temperature'], w_res['windspeed']
    except: temp, wind = "--", "--"

    # แสดงผลในกรอบดำเงา
    st.markdown(f"""
    <div class="glossy-card">
        <h2 style='text-align: center;'>🛰️ COMMAND CENTER</h2>
        <p style='font-size: 1.2rem; color: #00ff00;'><b>{full_detail}</b></p>
        <hr style='border: 1px solid white;'>
        <div style='display: flex; justify-content: space-around;'>
            <span>🌡️ {temp} °C</span>
            <span>💨 {wind} km/h</span>
            <span>⏰ {datetime.now().strftime('%H:%M:%S')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 5. MAP ---
    m = folium.Map(location=[lat, lon], zoom_start=17, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Hybrid')
    folium.Marker([lat, lon], popup="You", icon=folium.Icon(color='blue', icon='user', prefix='fa')).add_to(m)
    st_folium(m, use_container_width=True, height=450)

# --- 6. ระบบโทร (ปุ่มพับหน้าจอใหญ่พิเศษ) ---
with st.expander("📞 รายชื่อเพื่อนและการติดต่อ (CLICK TO OPEN)", expanded=False):
    st.markdown("<div style='background: black; padding: 10px;'>", unsafe_allow_html=True)
    # ใส่ระบบ Call และรายชื่อเพื่อนของนายที่นี่ (คงเดิมตาม V1.6)
    st.write("เลือกเพื่อนที่จะโทรหาผ่านสัญญาณ SYNAPSE...")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. MUSIC PLAYER ---
st.write("---")
st.markdown("<div class='glossy-card'>🎵 Sound Therapy: อยู่นิ่งๆ ไม่เจ็บตัว</div>", unsafe_allow_html=True)
pid = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
st.markdown(f'<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list={pid}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

st.caption("SYNAPSE V3.1 | REALITY DATA | 'อยู่นิ่งๆ' ไม่เจ็บตัว")
