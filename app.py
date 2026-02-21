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
import random

# --- 1. INITIALIZE (ตั้งค่าหน้าจอ) ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="wide")

# เชื่อมต่อ Firebase
if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
    except:
        st.error("⚠️ ยังไม่ได้เชื่อมต่อ Firebase Secrets")

# --- 2. สร้าง ID อัตโนมัติ (ไม่เจ็บตัว ไม่ต้องพิมพ์) ---
if 'my_id' not in st.session_state:
    st.session_state.my_id = f"USER-{random.randint(1000, 9999)}"

# --- 3. STYLE (รุ้ง + ดำเงา) ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); background-size: 1200% 1200%; animation: RainbowFlow 30s ease infinite; }
    .glossy-card { background: rgba(0, 0, 0, 0.85); border: 2px solid white; border-radius: 15px; padding: 20px; color: white; box-shadow: 0 0 15px #fff; text-shadow: 0 0 5px #fff; margin-bottom: 15px; }
    .streamlit-expanderHeader { background-color: black !important; color: white !important; border: 1px solid white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR (เช็ครายชื่อคนออนไลน์) ---
st.sidebar.title("🛰️ SYNAPSE ONLINE")
st.sidebar.markdown(f"**ID ของคุณ:** `{st.session_state.my_id}`")
st.sidebar.markdown("---")
st.sidebar.subheader("👥 สมาชิกที่ตรวจพบ")

# --- 5. LOGO & HEADER ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo2.jpg", use_container_width=True)
    except:
        st.markdown("<h2 style='text-align: center; color: white;'>🛰️ SYNAPSE</h2>", unsafe_allow_html=True)

st.title("🛰️ COMMAND CENTER")

# --- 6. REALITY CORE (GPS + แผนที่รวม) ---
location = get_geolocation()

if location and location.get('coords'):
    lat = location['coords']['latitude']
    lon = location['coords']['longitude']
    
    # ดึงเวลาและที่อยู่
    now = datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%H:%M:%S')
    
    # 📤 ส่งพิกัดเราขึ้น Firebase
    try:
        ref = db.reference(f'locations/{st.session_state.my_id}')
        ref.set({
            'lat': lat,
            'lon': lon,
            'last_seen': now
        })
    except: pass

    # 🌡️ ข้อมูลอากาศ
    try:
        w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
        temp = w['temperature']
    except: temp = "--"

    st.markdown(f"""
    <div class="glossy-card">
        <div style='display: flex; justify-content: space-around; font-size: 1.2rem;'>
            <span>📍 {lat:.4f}, {lon:.4f}</span>
            <span>🌡️ {temp}°C</span>
            <span style='color: yellow;'>⏰ {now}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 📥 ดึงพิกัดทุกคนมาปักหมุด
    m = folium.Map(location=[lat, lon], zoom_start=15, 
                   tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
                   attr='Google Hybrid')
    
    try:
        all_users = db.reference('locations').get()
        if all_users:
            for uid, data in all_users.items():
                is_me = (uid == st.session_state.my_id)
                # ปักหมุดเพื่อนทุกคน
                folium.Marker(
                    [data['lat'], data['lon']],
                    popup=f"{uid} (เวลา: {data['last_seen']})",
                    icon=folium.Icon(color='red' if is_me else 'blue', icon='user', prefix='fa')
                ).add_to(m)
                # แสดงชื่อใน Sidebar
                st.sidebar.text(f"{'🟢' if is_me else '🔵'} {uid} ({data['last_seen']})")
    except: pass

    st_folium(m, use_container_width=True, height=500, key="global_map")

else:
    st.info("📡 กำลังรอพิกัด GPS... (โปรดอนุญาตให้เข้าถึงตำแหน่งบนบราวเซอร์)")

# --- 7. COMMUNICATION & MUSIC ---
with st.expander("📞 ระบบติดต่อสื่อสาร (CLICK TO OPEN)"):
    call_room = st.text_input("รหัสห้อง (คุยกับเพื่อนต้องใส่เหมือนกัน)", "synapse_free_zone")
    if st.button("🚀 เริ่มการเชื่อมต่อสัญญาณ"):
        st.markdown(f'<iframe src="https://meet.jit.si/SYNAPSE_{call_room}" allow="camera; microphone; fullscreen" width="100%" height="600" style="border: 2px solid white; border-radius: 15px;"></iframe>', unsafe_allow_html=True)

st.markdown(f"<div class='glossy-card' style='text-align: center;'>'อยู่นิ่งๆ ไม่เจ็บตัว'</div>", unsafe_allow_html=True)
st.markdown('<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0"></iframe>', unsafe_allow_html=True)
