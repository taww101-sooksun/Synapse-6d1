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
st.set_page_config(page_title="SYNAPSE COMMAND", layout="centered")

if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
    except Exception as e:
        st.error(f"Firebase Error: {e}")

# --- 2. SECURITY GATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: white;'>🔐 SYNAPSE UNLOCK</h1>", unsafe_allow_html=True)
    with st.form("Login"):
        u_id = st.text_input("Enter ID / ใส่ ID ของคุณ")
        u_pw = st.text_input("Password / รหัสผ่าน", type="password")
        if st.form_submit_button("UNLOCK SYSTEM"):
            if u_pw == "synapse2026" and u_id: 
                st.session_state.authenticated = True
                st.session_state.my_id = u_id
                st.rerun()
            else:
                st.error("รหัสผิด หรือยังไม่ได้ใส่ ID")
    st.stop()

my_id = st.session_state.my_id

# --- 3. STYLE (รุ้งนิ่งๆ ไหลช้าๆ 60 วินาที ตามที่นายชอบ) ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp { 
        background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); 
        background-size: 1000% 1000%; 
        animation: RainbowFlow 60s ease infinite; 
    }
    .info-card { background: rgba(0,0,0,0.8); border: 1px solid white; border-radius: 12px; padding: 15px; margin-bottom: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA SYNC (อัปเดตสถานะออนไลน์) ---
try:
    db.reference(f'/users/{my_id}').update({
        'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'online'
    })
    all_users = db.reference('/users').get()
    friend_options = [u for u in all_users.keys() if u != my_id] if all_users else []
except: friend_options = []

# --- 5. SIDEBAR: CALL SYSTEM ---
st.sidebar.title(f"👤 ID: {my_id}")
st.sidebar.write("---")
if friend_options:
    target = st.sidebar.selectbox("เลือกเพื่อนที่จะโทรหา", ["-- เลือก --"] + friend_options)
    if st.sidebar.button("📞 CALL NOW"):
        if target != "-- เลือก --":
            room_id = f"SYN-{uuid.uuid4().hex[:6]}"
            db.reference(f'/calls/{target}').set({'from': my_id, 'room': room_id, 'status': 'calling'})
            st.session_state.active_room = room_id
            st.session_state.call_target = target
            st.sidebar.success(f"กำลังโทรหา {target}...")

# --- 6. HEADER & INCOMING CALL ---
st.markdown("<h1 style='text-align: center; color: white;'>S Y N A P S E</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>'อยู่นิ่งๆ ไม่เจ็บตัว'</p>", unsafe_allow_html=True)

# ตรวจสอบสายเรียกเข้า
incoming_ref = db.reference(f'/calls/{my_id}')
call_data = incoming_ref.get()
if call_data and call_data.get('status') == 'calling':
    st.warning(f"🚨 มีสายเรียกเข้าจาก: {call_data.get('from')}")
    col1, col2 = st.columns(2)
    if col1.button("✅ รับสาย"):
        st.session_state.active_room = call_data.get('room')
        st.session_state.call_target = call_data.get('from')
        incoming_ref.update({'status': 'connected'})
        st.rerun()
    if col2.button("❌ ปฏิเสธ"):
        incoming_ref.delete()
        st.rerun()

# --- 7. CORE DATA: GPS & REAL TIME (ตัดเลข TEMP/WIND ที่ไม่จำเป็นออก) ---
location = get_geolocation()
if location and location.get('coords'):
    coords = location['coords']
    lat, lon = coords['latitude'], coords['longitude']
    
    # บันทึกพิกัดจริง
    db.reference(f'/users/{my_id}/location').update({'lat': lat, 'lon': lon, 'timestamp': datetime.now().isoformat()})
    
    # หาเวลาจริงตามพิกัด
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    now_local = datetime.now(pytz.timezone(tz_name)) if tz_name else datetime.now()
    
    # แสดงข้อมูลแบบ Compact (กล่องเดียวจบ)
    st.markdown(f"""
    <div class="info-card">
        <p style='margin:0;'>📍 พิกัด: <b>{lat:.5f}, {lon:.5f}</b></p>
        <p style='margin:0;'>⏰ เวลาท้องถิ่น: <b style='color:#00ff00;'>{now_local.strftime('%H:%M:%S')}</b></p>
    </div>
    """, unsafe_allow_html=True)

    # --- 8. MAP ---
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Hybrid')
    folium.Marker([lat, lon], popup="You", icon=folium.Icon(color='blue', icon='user', prefix='fa')).add_to(m)
    
    # ถ้ามีการโทร ให้โชว์พิกัดเพื่อนด้วย
    active_target = st.session_state.get('call_target')
    if active_target:
        f_loc = db.reference(f'/users/{active_target}/location').get()
        if f_loc:
            f_lat, f_lon = f_loc.get('lat'), f_loc.get('lon')
            folium.Marker([f_lat, f_lon], popup=active_target, icon=folium.Icon(color='red')).add_to(m)
            folium.PolyLine([[lat, lon], [f_lat, f_lon]], color="white", weight=1, dash_array='5').add_to(m)
    
    st_folium(m, use_container_width=True, height=350)

# --- 9. VIDEO CALL UI ---
if "active_room" in st.session_state:
    st.write("---")
    st.subheader(f"🌐 กำลังคุยกับ: {st.session_state.call_target}")
    st.markdown(f'<iframe src="https://meet.jit.si/{st.session_state.active_room}#config.prejoinPageEnabled=false" allow="camera; microphone; fullscreen" width="100%" height="450" style="border-radius:15px; border: 2px solid white;"></iframe>', unsafe_allow_html=True)
    if st.button("วางสาย (End Call)"):
        db.reference(f'/calls/{my_id}').delete()
        if "active_room" in st.session_state: del st.session_state.active_room
        st.rerun()

# --- 10. MUSIC PLAYER (ย่อขนาดให้เล็กลงตามสั่ง) ---
st.write("---")
st.caption("🎵 Sound Therapy: อยู่นิ่งๆ ไม่เจ็บตัว")
pl_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
st.markdown(f'<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list={pl_id}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

st.caption("SYNAPSE V1.9.8 | 'ความจริงที่ใช้งานได้'")
