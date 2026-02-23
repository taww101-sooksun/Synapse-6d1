import streamlit as st
import requests
from streamlit_js_eval import get_geolocation
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
import folium
from streamlit_folium import st_folium
import firebase_admin
from firebase_admin import credentials, db
import os

# --- 1. INITIALIZE FIREBASE ---
if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
    except Exception as e:
        st.error(f"Firebase Error: {e}")

# --- 2. STYLE & RAINBOW (60s) ---
st.set_page_config(page_title="SYNAPSE COMMAND", layout="wide")
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp { background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); background-size: 1200% 1200%; animation: RainbowFlow 60s ease infinite; }
    .info-box { background: rgba(0,0,0,0.8); padding: 10px; border-radius: 5px; border: 1px solid #00ff00; color: white; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGO (บังคับหาไฟล์ logo2.jpg ตามภาพที่ส่งมา) ---
logo_path = "logo2.jpg" 
if os.path.exists(logo_path):
    st.image(logo_path, width=300)
else:
    # ถ้าหาไฟล์ในโฟลเดอร์ไม่เจอ ให้ลองดึงผ่าน URL ของนายเอง (GitHub Raw)
    st.image("https://raw.githubusercontent.com/taww101/สี-app/main/logo2.jpg", width=300)

# --- 4. LOGIN SYSTEM ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.form("Login"):
        u_id = st.text_input("ID / ไอดี")
        u_pw = st.text_input("Password", type="password")
        if st.form_submit_button("UNLOCK"):
            if u_pw == "9999999" and u_id:
                st.session_state.authenticated = True
                st.session_state.my_id = u_id
                st.rerun()
    st.stop()

my_id = st.session_state.my_id
all_users = db.reference('/users').get() or {}

# --- 5. TACTICAL RADAR & GLOBAL TIME ---
st.subheader("📡 RADAR SYSTEM / ระบบเรดาร์")
location = get_geolocation()

if location:
    coords = location.get('coords', {})
    lat, lon = coords.get('latitude'), coords.get('longitude')
    
    if lat and lon:
        # คำนวณเวลา (Time Calculation)
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=lon, lat=lat)
        local_tz = pytz.timezone(tz_name)
        time_local = datetime.now(local_tz).strftime('%H:%M:%S')
        time_global = datetime.now(pytz.utc).strftime('%H:%M:%S UTC') # เวลาสากลให้เพื่อน

        # อัปเดตขึ้น Firebase
        db.reference(f'/users/{my_id}/location').update({
            'lat': lat, 'lon': lon,
            'time': f"{time_local} ({tz_name})",
            'utc': time_global
        })

        # แสดงกล่องข้อมูลด้านบนแผนที่เพื่อให้เห็นชัดๆ
        st.markdown(f"""
        <div class="info-box">
            <b>Your Location:</b> {lat:.4f}, {lon:.4f}<br>
            <b>Local Time (TH):</b> {time_local}<br>
            <b>Global Time (UK/UTC):</b> {time_global}
        </div>
        """, unsafe_allow_html=True)

        # แผนที่ (Map 500px)
        m = folium.Map(location=[lat, lon], zoom_start=17, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Hybrid')
        
        for user_id, user_data in all_users.items():
            loc = user_data.get('location', {})
            u_lat, u_lon = loc.get('lat'), loc.get('lon')
            if u_lat and u_lon:
                is_me = (user_id == my_id)
                color = 'red' if is_me else 'blue'
                
                # รายละเอียดในมุด (Popup)
                popup_text = f"ID: {user_id}<br>Time: {loc.get('time')}<br>UTC: {loc.get('utc')}"
                
                folium.Marker(
                    [u_lat, u_lon],
                    popup=folium.Popup(popup_text, max_width=200),
                    tooltip=user_id,
                    icon=folium.Icon(color=color, icon='user', prefix='fa')
                ).add_to(m)

                # ชื่อลอย (Floating Name)
                folium.map.Marker(
                    [u_lat, u_lon],
                    icon=folium.features.DivIcon(
                        icon_size=(150,36),
                        html=f'<div style="font-size: 12pt; color: {color}; font-weight: bold; text-shadow: 2px 2px black;">{user_id}</div>',
                    )
                ).add_to(m)

        st_folium(m, use_container_width=True, height=500, key="radar_v27")
    else:
        st.warning("🛰️ Waiting for GPS Signal... / รอพิกัด...")
else:
    st.info("💡 Please Allow GPS Access / โปรดอนุญาต GPS")

# --- 6. MESSENGER & YOUTUBE ---
st.write("---")
friend_list = [u for u in all_users.keys() if u != my_id]
target = st.selectbox("💬 Select Friend / เลือกเพื่อน", ["-- Select --"] + friend_list)

if target != "-- Select --":
    st.success(f"Connected to: {target}")
    # ส่วนแชทเดิม (ตัดเพื่อความสั้นในการรัน) ...

# YouTube 150px ตามสั่ง
st.write("---")
yt_url = "https://www.youtube.com/embed?listType=playlist&list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO&autoplay=1&mute=1"
st.markdown(f'<iframe width="100%" height="150" src="{yt_url}" frameborder="0" allow="autoplay; encrypted-media"></iframe>', unsafe_allow_html=True)

st.caption("SYNAPSE V2.7 | GLOBAL SYNC | NO LIES")
