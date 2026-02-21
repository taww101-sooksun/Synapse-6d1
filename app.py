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

# --- 1. INITIALIZE ---
st.set_page_config(page_title="SYNAPSE COMMAND", layout="wide")

if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/'})
    except: pass

# --- 2. SECURITY ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center;'>🔐 SYNAPSE UNLOCK</h2>", unsafe_allow_html=True)
    with st.form("Login"):
        u_id = st.text_input("ID")
        u_pw = st.text_input("Password", type="password")
        if st.form_submit_button("UNLOCK"):
            if u_pw == "synapse2026" and u_id:
                st.session_state.authenticated = True
                st.session_state.my_id = u_id
                st.rerun()
    st.stop()

my_id = st.session_state.my_id

# --- 3. STYLE (Rainbow Flow) ---
st.markdown("""
    <style>
    @keyframes Rainbow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab); background-size: 400% 400%; animation: Rainbow 15s ease infinite; }
    .info-box { background: rgba(0,0,0,0.8); border: 2px solid #fff; border-radius: 15px; padding: 15px; color: white; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. HEADER ---
if os.path.exists("logo.jpg"): 
    st.image("logo.jpg", width=150)
else: 
    st.markdown("<h1 style='color: white; text-align: center;'>SYNAPSE REAL-TIME</h1>", unsafe_allow_html=True)

# --- 5. LOCATION & REAL TIME (ความจริงที่คลาดเคลื่อนไม่ได้) ---
location = get_geolocation()
if location and location.get('coords'):
    lat = location['coords'].get('latitude')
    lon = location['coords'].get('longitude')
    
    # หา Timezone จริงจากพิกัดเพื่อเวลาที่ถูกต้องที่สุด
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    
    if tz_name:
        local_tz = pytz.timezone(tz_name)
        now = datetime.now(local_tz)
        current_time = now.strftime('%H:%M:%S')
        date_str = now.strftime('%d/%m/%Y')
        
        # บันทึกพิกัดเข้าฐานข้อมูล
        db.reference(f'/users/{my_id}/location').update({'lat': lat, 'lon': lon, 'time': now.isoformat()})
        
        # แสดงผลแบบเน้นๆ เฉพาะสิ่งที่จริง
        st.markdown(f"""
        <div class="info-box">
            <h3 style='margin:0;'>👤 ID: {my_id}</h3>
            <p style='margin:5px 0;'>🌍 พิกัดปัจจุบัน: <b>{lat:.5f}, {lon:.5f}</b></p>
            <p style='margin:5px 0;'>⏰ เวลาท้องถิ่น ({tz_name}): <b style='color:#00ff00; font-size:1.5rem;'>{current_time}</b></p>
            <p style='margin:0; font-size:0.8rem;'>วันที่: {date_str}</p>
        </div>
        """, unsafe_allow_html=True)

        # --- 6. HYBRID MAP (เต็มพื้นที่) ---
        m = folium.Map(location=[lat, lon], zoom_start=17, tiles='https://mt1.google.com/vt/lyrs=y&x={{x}}&y={{y}}&z={{z}}', attr='Google Hybrid')
        folium.Marker([lat, lon], icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
        st_folium(m, use_container_width=True, height=500)
else:
    st.warning("⚠️ กำลังรอการยืนยันพิกัด GPS เพื่อแสดงความจริง...")

# --- 7. SEARCH & CALL ---
with st.expander("🔍 ค้นหาเพื่อนเพื่อดูพิกัดจริง", expanded=False):
    all_u = db.reference('/users').get()
    friends = [u for u in all_u.keys() if u != my_id] if all_u else []
    target = st.selectbox("เลือก ID เพื่อน", ["-- เลือก --"] + friends)
    if st.button("📞 เริ่มการสื่อสาร (CALL)") and target != "-- เลือก --":
        room = f"SYN-{uuid.uuid4().hex[:4]}"
        db.reference(f'/calls/{target}').set({'from': my_id, 'room': room, 'status': 'calling'})
        st.session_state.active_room = room
        st.session_state.call_target = target

# --- 8. MUSIC THERAPY (คลังเพลงรวมของนาย) ---
st.write("---")
st.subheader("🎵 รวมเพลงสบายๆ..อยู่นิ่งๆไม่เจ็บตัว")
pl_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
st.markdown(f'''
    <div style="border: 4px solid white; border-radius: 20px; overflow: hidden;">
        <iframe width="100%" height="450" 
        src="https://www.youtube.com/embed/videoseries?list={pl_id}" 
        frameborder="0" allowfullscreen></iframe>
    </div>
    ''', unsafe_allow_html=True)

st.caption("SYNAPSE V1.9.7 | FOCUS ON REALITY")
