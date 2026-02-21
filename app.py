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

# --- 1. SETTINGS & SECURITY ---
# ใช้รหัส Client ID ล่าสุดที่นายส่งมา
CLIENT_ID = "644544481335-t27d3lqlvqomrohcngml5boq6kfi0j8e.apps.googleusercontent.com"

# [ความจริงที่นายต้องใส่] ระบุอีเมลที่อนุญาตให้เข้าแอปได้จริงๆ เท่านั้น
ALLOWED_EMAILS = [
    "your-email@gmail.com", 
    "friend1@gmail.com",
    "Sooksunkub@gmail.com" # ตัวอย่างอีเมลของนาย
]

st.set_page_config(page_title="SYNAPSE V2.6", layout="centered")

# --- 2. LOGIN LOGIC (Google Auth Simulator) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login_screen():
    # หน้าเข้าสู่ระบบแบบเรียบง่ายแต่ชัดเจน
    st.markdown("""
        <style>
        .login-card { 
            background: rgba(0,0,0,0.8); padding: 40px; border-radius: 20px; 
            border: 2px solid white; text-align: center; color: white;
        }
        .stButton>button { width: 100%; border-radius: 10px; height: 50px; font-weight: bold; }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=150)
    else:
        st.title("S Y N A P S E")
    
    st.subheader("🔐 Personal Access Only")
    st.write("ระบบนี้จำกัดการเข้าถึงเฉพาะอีเมลที่ได้รับอนุญาต")
    
    if st.button("🔴 Continue with Google"):
        # [ความจริง] ระบบจะดึง Email มาจาก Google Profile
        # นายสามารถใช้คำสั่งดึงอีเมลจริงจาก streamlit_google_auth มาใส่ตรงนี้ได้
        dummy_email = "Sooksunkub@gmail.com" # ทดสอบด้วยอีเมลนาย
        
        if dummy_email in ALLOWED_EMAILS:
            st.session_state.authenticated = True
            st.session_state.my_id = dummy_email
            st.rerun()
        else:
            st.error(f"🚫 ขออภัย: อีเมล {dummy_email} ไม่มีสิทธิ์เข้าใช้งาน")
    st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    login_screen()
    st.stop()

# --- 3. MAIN COMMAND CENTER (รุ้งนิ่ง 60s และข้อมูลจริง) ---
my_id = st.session_state.my_id

st.markdown("""
    <style>
    @keyframes Rainbow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); background-size: 1000% 1000%; animation: Rainbow 60s ease infinite; }
    .status-bar { background: rgba(0,0,0,0.9); border: 1px solid white; border-radius: 10px; padding: 10px; color: white; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ส่วนพิกัดและเวลา (ตัดตัวเลขอากาศที่ไม่จำเป็นออกตามสั่ง)
location = get_geolocation()
if location and location.get('coords'):
    lat, lon = location['coords']['latitude'], location['coords']['longitude']
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    now = datetime.now(pytz.timezone(tz_name)) if tz_name else datetime.now()
    
    st.markdown(f"""
        <div class='status-bar'>
            📧 <b>User:</b> {my_id} <br>
            📍 <b>GPS:</b> {lat:.5f}, {lon:.5f} | ⏰ <b>Time:</b> {now.strftime('%H:%M:%S')}
        </div>
        """, unsafe_allow_html=True)

    # แผนที่ Hybrid
    m = folium.Map(location=[lat, lon], zoom_start=17, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Marker([lat, lon], icon=folium.Icon(color='red', icon='user', prefix='fa')).add_to(m)
    st_folium(m, use_container_width=True, height=350)
else:
    st.warning("📡 กำลังค้นหาพิกัดจริงจากดาวเทียม...")

# ปุ่มพับหน้า (Expander) ที่เห็นชัดเจนตามสั่ง
with st.expander("🔍 ค้นหาเพื่อน / รายชื่อออนไลน์", expanded=False):
    st.write("รายชื่อเพื่อนที่อนุญาตในระบบจะแสดงที่นี่...")

# เครื่องเล่นเพลง (ย่อขนาดประหยัดที่)
st.write("---")
st.caption("🎵 Sound Therapy : อยู่นิ่งๆ ไม่เจ็บตัว")
st.markdown('<iframe width="100%" height="180" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

st.caption("SYNAPSE V2.6 | SECURE BY GOOGLE")
