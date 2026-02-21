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
from firebase_admin import credentials, db, storage
import uuid

# --- 1. INITIALIZE FIREBASE (ระบบจริง) ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="wide") 

if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/',
            'storageBucket': 'notty-101.firebasestorage.app' 
        })
    except Exception as e:
        st.error(f"Firebase Connection Error: {e}")

# --- 2. SECURITY GATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center;'>🔐 SYNAPSE ACCESS CONTROL</h2>", unsafe_allow_html=True)
    with st.form("Login"):
        u_id = st.text_input("Enter your ID / ใส่ ID ของคุณ")
        u_pw = st.text_input("Password / รหัสผ่าน", type="password")
        if st.form_submit_button("UNLOCK SYSTEM"):
            if u_pw == "synapse2026" and u_id: 
                st.session_state.authenticated = True
                st.session_state.my_id = u_id
                st.rerun()
            else:
                st.error("Unauthorized!")
    st.stop()

# --- 3. SETTINGS & LANGUAGES ---
languages = {
    "TH": {
        "status_info": "STAY STILL & HEAL : 'อยู่นิ่งๆ ไม่เจ็บตัว'",
        "allow_gps": "💡 โปรดกดยืนยัน 'Allow' เพื่อเข้าสู่ Command Center",
        "map_title": "🗺️ แผนที่พิกัดจริง (Hybrid Map - เห็นชื่อสถานที่ชัดเจน)",
        "call_now": "📞 กดโทรหาเพื่อน (CALL NOW)",
        "waiting": "⏳ กำลังรอความจริงจากอีกฝ่าย...",
        "call_in": "🚨 มีสายเรียกเข้า!"
    },
    "EN": {
        "status_info": "STAY STILL & HEAL : 'Stay Still & No Pain'",
        "allow_gps": "💡 Please click 'Allow' to enter",
        "map_title": "🗺️ Real-Time Hybrid Map",
        "call_now": "📞 CALL NOW",
        "waiting": "⏳ Waiting for response...",
        "call_in": "🚨 Incoming Call!"
    }
}

sel_lang = st.sidebar.selectbox("SELECT LANGUAGE", ["TH", "EN"])
t = languages[sel_lang]
my_id = st.session_state.my_id

# --- 4. STYLE (เน้นความชัดเจน) ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp { background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); background-size: 1200% 1200%; animation: RainbowFlow 15s ease infinite; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3.5em; font-weight: bold; border: 3px solid white !important; font-size: 20px !important; }
    .stMetric, .stInfo, .stSuccess, .stWarning { background-color: rgba(0, 0, 0, 0.8) !important; padding: 15px; border-radius: 15px; border: 1px solid white; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. REGISTER STATUS ---
try:
    db.reference(f'/users/{my_id}').update({
        'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'online'
    })
    all_users = db.reference('/users').get()
    friend_options = [u for u in all_users.keys() if u != my_id] if all_users else []
except: friend_options = []

# --- 6. HEADER ---
st.markdown(f"<h1 style='text-align: center;'>SYNAPSE REAL-TIME COMMAND</h1>", unsafe_allow_html=True)
st.info(f"👤 USER ID: {my_id} | {t['status_info']}")

# --- 7. SEARCH & CALL (ของจริง) ---
st.subheader("🔍 ค้นหาเพื่อนเพื่อยืนยันพิกัด")
col_search, col_call = st.columns([2, 1])
with col_search:
    target = st.selectbox("พิมพ์ชื่อ ID เพื่อนเพื่อค้นหาความจริง", ["-- เลือกชื่อเพื่อน --"] + friend_options)
with col_call:
    st.write(" ")
    if st.button(t["call_now"]):
        if target != "-- เลือกชื่อเพื่อน --":
            room_id = f"SYNAPSE-{uuid.uuid4().hex[:6]}"
            db.reference(f'/calls/{target}').set({'from': my_id, 'room': room_id, 'status': 'calling'})
            st.session_state.active_room = room_id
            st.session_state.call_target = target
            st.success(f"📡 กำลังส่งสัญญาณไปที่ {target}")

# --- 8. INCOMING CALL ---
try:
    call_data = db.reference(f'/calls/{my_id}').get()
    if call_data and call_data.get('status') == 'calling':
        st.warning(f"{t['call_in']} จาก: {call_data.get('from')}")
        cb1, cb2 = st.columns(2)
        if cb1.button("✅ ยอมรับความจริง (ACCEPT)"):
            st.session_state.active_room = call_data.get('room')
            st.session_state.call_target = call_data.get('from')
            db.reference(f'/calls/{my_id}').update({'status': 'connected'})
            st.rerun()
        if cb2.button("❌ ปฏิเสธ (REJECT)"):
            db.reference(f'/calls/{my_id}').delete()
            st.rerun()
except: pass

# --- 9. MAP & DATA (ความจริงปรากฏชัดเจน) ---
location = get_geolocation()
if location:
    coords = location.get('coords', {})
    lat, lon = coords.get('latitude'), coords.get('longitude')
    if lat and lon:
        # บันทึกพิกัดจริงเข้าสู่ระบบ
        db.reference(f'/users/{my_id}/location').update({'lat': lat, 'lon': lon, 'time': datetime.now().isoformat()})

        # แสดงผลสภาพอากาศจริง
        w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("🌡️ TEMP", f"{w_res['temperature']} °C")
        m_col2.metric("💨 WIND", f"{w_res['windspeed']} km/h")
        m_col3.metric("⏰ TIME", datetime.now().strftime('%H:%M'))

        st.subheader(t["map_title"])
        # แผนที่ Hybrid (เห็นถนน หมู่บ้าน จังหวัด แม่น้ำ ชัดเจน)
        m = folium.Map(location=[lat, lon], zoom_start=17, 
                       tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
                       attr='Google Hybrid Labels')
        
        folium.Marker([lat, lon], popup="ตำแหน่งจริงของคุณ", icon=folium.Icon(color='blue', icon='user', prefix='fa')).add_to(m)

        # ดึงพิกัดจริงของเพื่อน (ถ้ามีการเลือก)
        active_target = st.session_state.get('call_target') or (target if target != "-- เลือกชื่อเพื่อน --" else None)
        if active_target:
            f_data = db.reference(f'/users/{active_target}/location').get()
            if f_data:
                folium.Marker([f_data['lat'], f_data['lon']], popup=f"พิกัดจริงของ {active_target}", 
                              icon=folium.Icon(color='red', icon='eye', prefix='fa')).add_to(m)
                folium.PolyLine([[lat, lon], [f_data['lat'], f_data['lon']]], color="white", weight=3).add_to(m)

        # ปรับแผนที่ให้ใหญ่สะใจ (Responsive & Large)
        st_folium(m, use_container_width=True, height=700)
    else: st.warning("กำลังค้นหาดาวเทียม...")
else: st.info(t["allow_gps"])

# --- 10. CALL ACTIVE ---
if "active_room" in st.session_state:
    st.divider()
    st.subheader(f"🌐 สายตรงความจริง: {st.session_state.call_target}")
    st.markdown(f'<iframe src="https://meet.jit.si/{st.session_state.active_room}" allow="camera; microphone; fullscreen" width="100%" height="600" style="border: 5px solid white; border-radius: 20px;"></iframe>', unsafe_allow_html=True)
    if st.button("❌ วางสายและจบการเชื่อมต่อ"):
        db.reference(f'/calls/{st.session_state.call_target}').delete()
        del st.session_state.active_room
        del st.session_state.call_target
        st.rerun()

st.caption("SYNAPSE V1.8 | REALITY ENGINE | อยู่นิ่งๆ ไม่เจ็บตัว")
