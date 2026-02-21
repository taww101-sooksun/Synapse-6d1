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
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/'})
    except: pass

# --- 2. MULTI-LANGUAGE DATA ---
languages = {
    "TH": {
        "welcome": "🔐 ปลดล็อคระบบ SYNAPSE",
        "id_label": "ระบุ ID ของคุณ",
        "pw_label": "รหัสผ่านส่วนตัว",
        "btn_unlock": "ยืนยันเข้าใช้งาน",
        "call_friend": "🔍 ค้นหาเพื่อนเพื่อดูพิกัด (กดเพื่อขยาย)",
        "incoming": "🚨 มีสายเรียกเข้า!",
        "music": "🎵 รวมเพลงสบายๆ..อยู่นิ่งๆไม่เจ็บตัว",
        "status": "'อยู่นิ่งๆ ไม่เจ็บตัว'"
    },
    "EN": {
        "welcome": "🔐 SYNAPSE ACCESS CONTROL",
        "id_label": "Enter your ID",
        "pw_label": "Private Password",
        "btn_unlock": "UNLOCK SYSTEM",
        "call_friend": "🔍 SEARCH FRIENDS (Click to Expand)",
        "incoming": "🚨 Incoming Call!",
        "music": "🎵 Sound Therapy: Stay Still & No Pain",
        "status": "'Stay Still & No Pain'"
    }
}

# --- 3. SECURITY GATE (ปรับให้เช็ค ID รายคน) ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False

if not st.session_state.authenticated:
    sel_lang = st.radio("Language / เลือกภาษา", ["TH", "EN"], horizontal=True)
    lang = languages[sel_lang]
    
    st.markdown(f"<h2 style='text-align: center;'>{lang['welcome']}</h2>", unsafe_allow_html=True)
    with st.form("Login"):
        u_id = st.text_input(lang['id_label'])
        u_pw = st.text_input(lang['pw_label'], type="password")
        if st.form_submit_button(lang['btn_unlock']):
            # [ความจริง] ตรงนี้ถ้าจะให้ล็อครายคน นายต้องกำหนดรหัสไว้ใน Firebase 
            # แต่เบื้องต้นผมปรับให้มันจำ ID ที่กรอกไว้เป็นหลักก่อน
            if u_pw == "synapse2026" and u_id:
                st.session_state.authenticated = True
                st.session_state.my_id = u_id
                st.session_state.lang = sel_lang
                st.rerun()
    st.stop()

my_id = st.session_state.my_id
lang = languages[st.session_state.lang]

# --- 4. STYLE (รุ้งนิ่ง 60s) ---
st.markdown("""
    <style>
    @keyframes Rainbow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); background-size: 1000% 1000%; animation: Rainbow 60s ease infinite; }
    .info-card { background: rgba(0,0,0,0.85); border: 2px solid white; border-radius: 12px; padding: 15px; color: white; }
    /* ปรับปุ่มพับหน้า (Expander) ให้ชัดเจนขึ้น */
    .streamlit-expanderHeader { background-color: rgba(255,255,255,0.2) !important; color: white !important; border-radius: 10px !important; font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGO & HEADER ---
col_l, col_r = st.columns([1, 2])
with col_l:
    if os.path.exists("logo.jpg"): st.image("logo.jpg", width=120)
    else: st.subheader("S Y N A P S E")
with col_r:
    st.markdown(f"**ID:** {my_id}")
    st.write(lang['status'])

# --- 6. CORE DATA ---
location = get_geolocation()
if location and location.get('coords'):
    lat, lon = location['coords']['latitude'], location['coords']['longitude']
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    now = datetime.now(pytz.timezone(tz_name)) if tz_name else datetime.now()
    
    db.reference(f'/users/{my_id}/location').update({'lat': lat, 'lon': lon, 'time': now.isoformat()})

    st.markdown(f"""
    <div class="info-card">
        📍 {lat:.5f}, {lon:.5f} | ⏰ {now.strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Marker([lat, lon], icon=folium.Icon(color='blue')).add_to(m)
    st_folium(m, use_container_width=True, height=350)

# --- 7. CALL SYSTEM (ปุ่มพับที่ชัดเจนขึ้น) ---
with st.expander(lang['call_friend'], expanded=False):
    all_u = db.reference('/users').get()
    friends = [u for u in all_u.keys() if u != my_id] if all_u else []
    target = st.selectbox("Select Friend", ["-- Select --"] + friends)
    if st.button("📞 CALL NOW") and target != "-- Select --":
        room = f"SYN-{uuid.uuid4().hex[:4]}"
        db.reference(f'/calls/{target}').set({'from': my_id, 'room': room, 'status': 'calling'})
        st.session_state.active_room = room

# --- 8. MUSIC PLAYER (กะทัดรัด 200px) ---
st.write("---")
st.caption(lang['music'])
pl_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
st.markdown(f'<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list={pl_id}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

st.caption("SYNAPSE V1.9.9 | NO FAKE DATA")
