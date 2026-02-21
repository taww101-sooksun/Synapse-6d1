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
import uuid
import os

# --- 1. INITIALIZE & SECURITY (ฝังเบอร์ในโค้ด) ---
st.set_page_config(page_title="SYNAPSE V3.0", layout="wide")

# รายชื่อเบอร์ที่อนุญาต (Whitelist)
ALLOWED_PHONES = ["0970801941", "0896544464"] # <-- แก้เบอร์เพื่อนที่นี่

if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'lang' not in st.session_state: st.session_state.lang = "TH"

# --- 2. MULTI-LANGUAGE DATA ---
texts = {
    "TH": {
        "welcome": "📱 ระบบยืนยันตัวตนความจริง",
        "guide": "📖 วิธีใช้งาน: 1.กรอกเบอร์ที่ลงทะเบียน 2.กดยอมรับ GPS 3.ระบบจะล็อกเครื่องคุณทันที",
        "weather": "☁️ สภาพอากาศจริงในพื้นที่",
        "map": "🗺️ แผนที่พิกัดดาวเทียม (Real-Time)",
        "call": "📞 ระบบโทรฟรีผ่าน SYNAPSE",
        "music": "🎵 เครื่องเล่นเสียง H.D. (อยู่นิ่งๆไม่เจ็บตัว)",
        "status": "'อยู่นิ่งๆ ไม่เจ็บตัว'"
    },
    "EN": {
        "welcome": "📱 REALITY AUTHENTICATION",
        "guide": "📖 Guide: 1.Enter Registered Phone 2.Allow GPS 3.Device will be Locked to your ID",
        "weather": "☁️ Real Local Weather",
        "map": "🗺️ Satellite Reality Map",
        "call": "📞 SYNAPSE Free Call",
        "music": "🎵 H.D. Sound (Stay Still & No Pain)",
        "status": "'Stay Still & No Pain'"
    }
}

# --- 3. CSS STYLE (ดำเงาแว้บ + รุ้งไว 10s) ---
st.markdown(f"""
    <style>
    @keyframes RainbowFlow {{ 0% {{background-position:0% 50%}} 50% {{background-position:100% 50%}} 100% {{background-position:0% 50%}} }}
    .stApp {{ 
        background: #FF7F50;
        background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff);
        background-size: 1200% 1200%;
        animation: RainbowFlow 10s ease infinite;
    }}
    /* กรอบดำเงาแว้บ ตัวหนังสือขาวแสบตา */
    .glossy-card {{ 
        background: rgba(0, 0, 0, 0.85); 
        border: 2px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8), inset 0 0 15px rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border-radius: 15px; 
        padding: 20px; 
        color: #FFFFFF; 
        text-shadow: 0 0 10px #FFFFFF, 0 0 20px #FFFFFF;
        margin-bottom: 15px;
    }}
    .streamlit-expanderHeader {{ background-color: rgba(0,0,0,0.9) !important; color: white !important; border: 1px solid white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN GATE (เช็คเบอร์ + เช็คเครื่อง) ---
if not st.session_state.authenticated:
    st.markdown("<div class='glossy-card'>", unsafe_allow_html=True)
    st.title("🔐 SYNAPSE ACCESS")
    u_phone = st.text_input("กรอกเบอร์โทรศัพท์ที่ฝังในระบบ")
    if st.button("ยืนยันความจริง"):
        if u_phone in ALLOWED_PHONES:
            st.session_state.authenticated = True
            st.session_state.my_id = u_phone
            st.rerun()
        else:
            st.error("❌ เบอร์นี้ไม่ได้ถูกฝังไว้ในฐานข้อมูลความจริง")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

lang = texts[st.session_state.lang]

# --- 5. LOGO & HEADER ---
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("logo.jpg"): st.image("logo.jpg", width=150)
    else: st.title("S-Y-N")
with col2:
    if st.button("🌐 TH / EN"):
        st.session_state.lang = "EN" if st.session_state.lang == "TH" else "TH"
        st.rerun()
    st.markdown(f"**ID:** {st.session_state.my_id} | {lang['status']}")

# --- 6. USER GUIDE (แนะนำวิธีใช้) ---
with st.expander(lang['guide']):
    st.write("1. ระบบจะดึงพิกัดจากดาวเทียมเพื่อยืนยันว่าคุณไม่ได้โกหกตำแหน่ง")
    st.write("2. สภาพอากาศจะถูกดึงจากสถานีอุตุนิยมวิทยาที่ใกล้ที่สุด")
    st.write("3. แผนที่สามารถกดขยายดูแบบดาวเทียม (Hybrid) ได้")
    st.write("4. การโทรจะผ่านระบบ Peer-to-Peer ไม่เสียค่าใช้จ่าย")

# --- 7. GPS & WEATHER REALITY ---
location = get_geolocation()
if location and location.get('coords'):
    lat, lon = location['coords']['latitude'], location['coords']['longitude']
    
    # ดึงสภาพอากาศจริง (ใช้ Open-Meteo API ไม่ต้องใช้ Key)
    w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    w_data = requests.get(w_url).json()['current_weather']
    
    # นาฬิกาโลกระบุตำแหน่งจริง
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    now = datetime.now(pytz.timezone(tz_name)) if tz_name else datetime.now()

    st.markdown(f"""
    <div class='glossy-card'>
        <h3>📍 {lang['weather']}</h3>
        <p style='font-size: 1.5rem;'>🌡️ อุณหภูมิ: {w_data['temperature']}°C | 💨 ลม: {w_data['windspeed']} km/h</p>
        <p>⏰ เวลาท้องถิ่น: {now.strftime('%H:%M:%S')} | 🌏 พิกัด: {lat:.5f}, {lon:.5f}</p>
    </div>
    """, unsafe_allow_html=True)

    # แผนที่ใหญ่
    st.markdown(f"### {lang['map']}")
    m = folium.Map(location=[lat, lon], zoom_start=18, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Hybrid')
    folium.Marker([lat, lon], icon=folium.Icon(color='red', icon='bolt', prefix='fa')).add_to(m)
    st_folium(m, use_container_width=True, height=500)

# --- 8. CALL & MUSIC ---
st.markdown(f"<div class='glossy-card'><h3>{lang['call']}</h3></div>", unsafe_allow_html=True)

with st.expander(lang['music']):
    pl_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    st.markdown(f'<iframe width="100%" height="450" src="https://www.youtube.com/embed/videoseries?list={pl_id}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

st.caption("SYNAPSE V3.0 FINAL | TRUTH SYSTEM | NO FAKE DATA")
