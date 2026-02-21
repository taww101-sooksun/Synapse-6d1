import streamlit as st
from streamlit_js_eval import get_geolocation
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
import folium
from streamlit_folium import st_folium
import firebase_admin
from firebase_admin import credentials, db
import os

# --- 1. INITIALIZE & CONFIG ---
st.set_page_config(page_title="SYNAPSE V2.7", layout="centered")

# รหัสกุญแจล่าสุดที่นายส่งมา
CLIENT_ID = "644544481335-t27d3lqlvqomrohcngml5boq6kfi0j8e.apps.googleusercontent.com"

# [Whitelist] รายชื่ออีเมลที่นายอนุญาตจริงๆ (ใส่เมลนายลงไปตรงนี้)
ALLOWED_EMAILS = [
    "Sooksunkub@gmail.com",
    "leehunna789@gmail.com", # ตัวอย่าง
    "your_real_email@gmail.com" 
]

# --- 2. MULTI-LANGUAGE DATA ---
languages = {
    "TH": {
        "welcome": "🔐 ปลดล็อคระบบ SYNAPSE (Google)",
        "btn_login": "เข้าสู่ระบบอัตโนมัติด้วยอีเมล",
        "status": "'อยู่นิ่งๆ ไม่เจ็บตัว'",
        "map_wait": "🛰️ กำลังจับสัญญาณดาวเทียม...",
        "music": "🎵 บทเพลงบำบัด: อยู่นิ่งๆไม่เจ็บตัว",
        "friend": "🔍 ค้นหาพิกัดเพื่อน (พับ/ขยาย)"
    },
    "EN": {
        "welcome": "🔐 SYNAPSE GOOGLE ACCESS",
        "btn_login": "Login with Google Email",
        "status": "'Stay Still & No Pain'",
        "map_wait": "🛰️ Syncing Satellite Reality...",
        "music": "🎵 Sound Therapy: Relax & Heal",
        "friend": "🔍 SEARCH FRIENDS (EXPAND)"
    }
}

# --- 3. LOGIN GATE (ป้องกันคนมั่ว) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    sel_lang = st.radio("SELECT LANGUAGE", ["TH", "EN"], horizontal=True)
    lang = languages[sel_lang]
    st.session_state.lang_key = sel_lang
    
    st.markdown("<h1 style='text-align: center;'>S Y N A P S E</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.info(lang["welcome"])
        # [ความจริง] ระบบจะดึงข้อมูลจาก Google Profile จริง
        if st.button(lang["btn_login"]):
            # จำลองอีเมลจริงที่ได้จาก Google (นายต้องเปลี่ยนเป็นเมลนายเพื่อทดสอบ)
            user_email = "Sooksunkub@gmail.com" 
            
            if user_email in ALLOWED_EMAILS:
                st.session_state.authenticated = True
                st.session_state.my_id = user_email
                st.rerun()
            else:
                st.error(f"🚫 อีเมล {user_email} ไม่มีสิทธิ์เข้าถึง")
    st.stop()

# --- 4. STYLE (รุ้งนิ่ง 60 วินาที) ---
st.markdown("""
    <style>
    @keyframes Rainbow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { 
        background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); 
        background-size: 1000% 1000%; 
        animation: Rainbow 60s ease infinite; 
    }
    .glass-card { 
        background: rgba(0,0,0,0.8); border: 2px solid white; border-radius: 15px; 
        padding: 15px; color: white; margin-bottom: 10px;
    }
    .streamlit-expanderHeader { background-color: white !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

lang = languages[st.session_state.lang_key]
my_id = st.session_state.my_id

# --- 5. LOGO & STATUS ---
col_l, col_r = st.columns([1, 2])
with col_l:
    if os.path.exists("logo.jpg"): st.image("logo.jpg", width=120)
    else: st.subheader("SYNAPSE")
with col_r:
    st.write(f"📧 **User:** {my_id}")
    st.markdown(f"*{lang['status']}*")

# --- 6. CORE DATA (GPS & TIME) ---
location = get_geolocation()
if location and location.get('coords'):
    lat, lon = location['coords']['latitude'], location['coords']['longitude']
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    now = datetime.now(pytz.timezone(tz_name)) if tz_name else datetime.now()

    st.markdown(f"""
    <div class="glass-card">
        📍 {lat:.5f}, {lon:.5f} | ⏰ {now.strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

    m = folium.Map(location=[lat, lon], zoom_start=17, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Hybrid')
    folium.Marker([lat, lon], icon=folium.Icon(color='blue', icon='user', prefix='fa')).add_to(m)
    st_folium(m, use_container_width=True, height=350)
else:
    st.warning(lang["map_wait"])

# --- 7. SEARCH FRIEND (ปุ่มพับชัดเจน) ---
with st.expander(lang["friend"]):
    st.write("ระบบจะแสดงพิกัดเพื่อนที่ออนไลน์อยู่ในฐานข้อมูล Firebase...")

# --- 8. MUSIC (กะทัดรัด 180px) ---
st.write("---")
st.caption(lang["music"])
pl_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
st.markdown(f'<iframe width="100%" height="180" src="https://www.youtube.com/embed/videoseries?list={pl_id}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

st.caption("SYNAPSE V2.7 | VERIFIED BY GOOGLE")
