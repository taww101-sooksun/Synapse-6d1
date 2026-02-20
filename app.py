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

# --- 1. INITIALIZE FIREBASE (Safety First) ---
if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://notty-101-default-rtdb.firebaseio.com/',
            'storageBucket': 'notty-101.firebasestorage.app' 
        })
    except Exception as e:
        st.error(f"Firebase Connection Error: {e}")

# --- 2. SECURITY GATE (หน้าด่านป้องกันไอพีมั่วๆ) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center;'>🔐 SYNAPSE ACCESS CONTROL</h2>", unsafe_allow_html=True)
    with st.form("Login"):
        u_id = st.text_input("Enter your ID / ใส่ ID ของคุณ")
        u_pw = st.text_input("Password / รหัสผ่าน", type="password")
        if st.form_submit_button("UNLOCK SYSTEM"):
            # แก้ไขรหัสผ่านตรงนี้ตามใจชอบเลยเพื่อน
            if u_pw == "synapse2026": 
                st.session_state.authenticated = True
                st.session_state.my_id = u_id
                st.rerun()
            else:
                st.error("Unauthorized! / รหัสผ่านไม่ถูกต้อง")
    st.stop()

# --- 3. SETTING & RAINBOW STYLE (ของเดิมเป๊ะๆ) ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="centered")

languages = {
    "TH": {
        "status_info": "STAY STILL & HEAL : 'อยู่นิ่งๆ ไม่เจ็บตัว'",
        "allow_gps": "💡 โปรดกดยืนยัน 'Allow' เพื่อเข้าสู่ Command Center",
        "connecting": "📡 กำลังเชื่อมต่อสัญญาณ...",
        "temp": "🌡️ อุณหภูมิ",
        "wind": "💨 ลม",
        "time": "⏰ เวลา",
        "map_title": "🗺️ แผนที่พิกัดปัจจุบันของคุณ",
        "music_title": "🎵 Sound Therapy (เล่นอัตโนมัติ)",
        "footer": "SYNAPSE V1.6 | ระบบ 2 ภาษา | 'อยู่นิ่งๆ' ไม่เจ็บตัว",
        "call_btn": "✅ รับสาย", "reject_btn": "❌ ไม่รับ", "call_in": "🚨 มีสายเรียกเข้า!"
    },
    "EN": {
        "status_info": "STAY STILL & HEAL : 'Stay Still & No Pain'",
        "allow_gps": "💡 Please click 'Allow' to enter Command Center",
        "connecting": "📡 Connecting to Satellite...",
        "temp": "🌡️ Temp", "wind": "💨 Wind", "time": "⏰ Time",
        "map_title": "🗺️ Your Current Location Map",
        "music_title": "🎵 Sound Therapy (Autoplay)",
        "footer": "SYNAPSE V1.6 | Dual Language | 'Stay Still' No Pain",
        "call_btn": "✅ Accept", "reject_btn": "❌ Reject", "call_in": "🚨 Incoming Call!"
    }
}

sel_lang = st.sidebar.selectbox("SELECT LANGUAGE / เลือกภาษา", ["TH", "EN"])
t = languages[sel_lang]
my_id = st.session_state.my_id

st.markdown("""
    <style>
    @keyframes RainbowFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff);
        background-size: 1200% 1200%;
        animation: RainbowFlow 10s ease infinite;
        color: #ffffff;
    }
    .stMetric, .stInfo, .stSuccess, .stWarning {
        background-color: rgba(0, 0, 0, 0.6) !important;
        padding: 10px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2);
    }
    h1, h2, h3, p, span { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. HEADER ---
try:
    st.image("logo.jpg", width=300)
except:
    st.markdown("<h1 style='text-align: center;'>S Y N A P S E</h1>", unsafe_allow_html=True)
st.info(t["status_info"])

# --- 5. INCOMING CALL LISTENER ---
try:
    incoming_ref = db.reference(f'/calls/{my_id}')
    call_data = incoming_ref.get()
    if call_data and call_data.get('status') == 'calling':
        st.warning(f"{t['call_in']} จาก: {call_data.get('from')}")
        st.write(f"📍 พิกัดผู้โทร: {call_data.get('location')}")
        btn1, btn2 = st.columns(2)
        if btn1.button(t['call_btn']):
            st.session_state.active_room = call_data.get('room')
            incoming_ref.update({'status': 'connected'})
        if btn2.button(t['reject_btn']):
            incoming_ref.delete()
            st.rerun()
except: pass

# --- 6. CORE LOGIC (GPS, WEATHER & TIME) ---
location = get_geolocation()
if location:
    coords = location.get('coords', {})
    lat, lon = coords.get('latitude'), coords.get('longitude')
    if lat and lon:
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=lon, lat=lat)
        try:
            geolocator = Nominatim(user_agent="synapse_v1")
            loc_th = geolocator.reverse(f"{lat}, {lon}", language='th')
            name_th = loc_th.raw.get('address', {}).get('province') or "พิกัดไทย"
            loc_en = geolocator.reverse(f"{lat}, {lon}", language='en')
            name_en = loc_en.raw.get('address', {}).get('state') or "Location"
            display_loc = f"📍 {name_th} | {name_en}"
        except: display_loc = f"📍 {lat:.4f}, {lon:.4f}"

        # --- DIAL SYSTEM ---
        st.sidebar.write("---")
        target = st.sidebar.text_input("Friend ID to Call")
        if st.sidebar.button("📞 Call Now"):
            room_id = f"SYNAPSE-{uuid.uuid4().hex[:6]}"
            db.reference(f'/calls/{target}').set({
                'from': my_id, 'room': room_id, 'status': 'calling', 'location': display_loc
            })
            st.sidebar.success("Calling...")

        try:
            w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            w_data = requests.get(w_url).json()
            temp = w_data['current_weather']['temperature']
            wind = w_data['current_weather']['windspeed']
        except: temp, wind = "--", "--"
        
        st.success(display_loc)
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(t["temp"], f"{temp} °C")
        with c2: st.metric(t["wind"], f"{wind} km/h")
        with c3:
            if tz_name:
                now_ = datetime.now(pytz.timezone(tz_name))
                st.metric(t["time"], now_.strftime('%H:%M'))

        # --- MAP ---
        st.write("---")
        st.subheader(t["map_title"])
        m = folium.Map(location=[lat, lon], zoom_start=18, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google Satellite')
        folium.Marker([lat, lon], popup=display_loc, icon=folium.Icon(color='red', icon='crosshairs', prefix='fa')).add_to(m)
        st_folium(m, width=700, height=350, returned_objects=[])
    else: st.warning(t["connecting"])
else: st.info(t["allow_gps"])

# --- 7. VIDEO CALL ROOM ---
if "active_room" in st.session_state:
    st.write("---")
    st.subheader("🌐 Private Line Active")
    j_url = f"https://meet.jit.si/{st.session_state.active_room}"
    st.markdown(f'<iframe src="{j_url}" allow="camera; microphone; fullscreen" width="100%" height="450" style="border-radius:15px;"></iframe>', unsafe_allow_html=True)
    if st.button("End Call"):
        del st.session_state.active_room
        st.rerun()

# --- 8. MUSIC ---
st.write("---")
st.subheader(t["music_title"])
pid = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
embed = f'<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list={pid}&autoplay=1&loop=1&playlist={pid}&mute=1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>'
st.markdown(embed, unsafe_allow_html=True)

st.divider()
st.caption(t["footer"])
