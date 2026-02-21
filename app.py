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

# --- 1. INITIALIZE FIREBASE ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="centered")

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
        u_id = st.text_input("Enter your ID / ใส่ ID ของคุณ (ห้ามเว้นว่าง)")
        u_pw = st.text_input("Password / รหัสผ่าน", type="password")
        if st.form_submit_button("UNLOCK SYSTEM"):
            if u_pw == "synapse2026" and u_id: 
                st.session_state.authenticated = True
                st.session_state.my_id = u_id
                st.rerun()
            else:
                st.error("Unauthorized or ID Empty! / รหัสผิด หรือยังไม่ได้ใส่ ID")
    st.stop()

# --- 3. SETTINGS & LANGUAGES ---
languages = {
    "TH": {
        "status_info": "STAY STILL & HEAL : 'อยู่นิ่งๆ ไม่เจ็บตัว'",
        "allow_gps": "💡 โปรดกดยืนยัน 'Allow' เพื่อเข้าสู่ Command Center",
        "connecting": "📡 กำลังเชื่อมต่อสัญญาณ...",
        "temp": "🌡️ อุณหภูมิ", "wind": "💨 ลม", "time": "⏰ เวลา",
        "map_title": "🗺️ แผนที่พิกัด (น้ำเงิน: คุณ | แดง: เพื่อน)",
        "music_title": "🎵 Sound Therapy (เล่นอัตโนมัติ)",
        "footer": "SYNAPSE V1.6 | ระบบ 2 ภาษา | 'อยู่นิ่งๆ' ไม่เจ็บตัว",
        "call_btn": "✅ รับสาย", "reject_btn": "❌ ไม่รับ", "call_in": "🚨 มีสายเรียกเข้า!",
        "waiting": "⏳ กำลังรออีกฝ่ายรับสาย..."
    },
    "EN": {
        "status_info": "STAY STILL & HEAL : 'Stay Still & No Pain'",
        "allow_gps": "💡 Please click 'Allow' to enter Command Center",
        "connecting": "📡 Connecting to Satellite...",
        "temp": "🌡️ Temp", "wind": "💨 Wind", "time": "⏰ Time",
        "map_title": "🗺️ Location Map (Blue: You | Red: Friend)",
        "music_title": "🎵 Sound Therapy (Autoplay)",
        "footer": "SYNAPSE V1.6 | Dual Language | 'Stay Still' No Pain",
        "call_btn": "✅ Accept", "reject_btn": "❌ Reject", "call_in": "🚨 Incoming Call!",
        "waiting": "⏳ Waiting for answer..."
    }
}

sel_lang = st.sidebar.selectbox("SELECT LANGUAGE / เลือกภาษา", ["TH", "EN"])
t = languages[sel_lang]
my_id = st.session_state.my_id

# --- 4. STYLE ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp { background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); background-size: 1200% 1200%; animation: RainbowFlow 10s ease infinite; color: #ffffff; }
    .stMetric, .stInfo, .stSuccess, .stWarning { background-color: rgba(0, 0, 0, 0.6) !important; padding: 10px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2); }
    h1, h2, h3, p, span { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. REGISTER & FRIEND LIST ---
try:
    db.reference(f'/users/{my_id}').update({
        'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'online'
    })
    all_users = db.reference('/users').get()
    friend_options = [u for u in all_users.keys() if u != my_id] if all_users else []
except: friend_options = []

# --- 6. SIDEBAR: CALL SYSTEM ---
st.sidebar.title(f"👤 ID: {my_id}")
st.sidebar.write("---")
st.sidebar.subheader("👥 Friend List")

if friend_options:
    target = st.sidebar.selectbox("Select Friend to Call", ["-- Select --"] + friend_options)
else:
    target = st.sidebar.text_input("Target ID (No one online)", placeholder="Waiting for friends...")

if st.sidebar.button("📞 Call Now"):
    if target and target != "-- Select --":
        room_id = f"SYNAPSE-{uuid.uuid4().hex[:6]}"
        db.reference(f'/calls/{target}').set({
            'from': my_id, 'room': room_id, 'status': 'calling'
        })
        st.session_state.active_room = room_id
        st.session_state.call_target = target
        st.sidebar.success(f"Calling {target}...")
    else:
        st.sidebar.error("Select a target first!")

# --- 7. HEADER ---
try:
    st.image("logo.jpg", width=300)
except:
    st.markdown("<h1 style='text-align: center;'>S Y N A P S E</h1>", unsafe_allow_html=True)
st.info(t["status_info"])

# --- 8. INCOMING CALL LISTENER ---
try:
    incoming_ref = db.reference(f'/calls/{my_id}')
    call_data = incoming_ref.get()
    if call_data and call_data.get('status') == 'calling':
        st.warning(f"{t['call_in']} จาก: {call_data.get('from')}")
        b1, b2 = st.columns(2)
        if b1.button(t['call_btn']):
            st.session_state.active_room = call_data.get('room')
            st.session_state.call_target = call_data.get('from')
            incoming_ref.update({'status': 'connected'})
            st.rerun()
        if b2.button(t['reject_btn']):
            incoming_ref.delete()
            st.rerun()
except: pass

# --- 9. CORE DATA (GPS, WEATHER, MAP) ---
location = get_geolocation()
if location:
    coords = location.get('coords', {})
    lat, lon = coords.get('latitude'), coords.get('longitude')
    if lat and lon:
        # อัปเดตพิกัดเราลงที่ /users/ เพื่อให้คนอื่นเห็น (สำคัญมาก)
        try: 
            db.reference(f'/users/{my_id}/location').update({
                'lat': lat, 'lon': lon, 'timestamp': datetime.now().isoformat()
            })
        except: pass

        # ข้อมูลสถานที่ & อากาศ
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=lon, lat=lat)
        try:
            geo = Nominatim(user_agent="synapse_v1")
            loc_th = geo.reverse(f"{lat}, {lon}", language='th').raw.get('address', {}).get('province', 'พิกัดไทย')
            loc_en = geo.reverse(f"{lat}, {lon}", language='en').raw.get('address', {}).get('state', 'Location')
            display_loc = f"📍 {loc_th} | {loc_en}"
        except: display_loc = f"📍 {lat:.4f}, {lon:.4f}"

        try:
            w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
            temp, wind = w_res['temperature'], w_res['windspeed']
        except: temp, wind = "--", "--"
        
        st.success(display_loc)
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(t["temp"], f"{temp} °C")
        with c2: st.metric(t["wind"], f"{wind} km/h")
        with c3:
            now_t = datetime.now(pytz.timezone(tz_name)) if tz_name else datetime.now()
            st.metric(t["time"], now_t.strftime('%H:%M'))

        st.write("---")
        st.subheader(t["map_title"])
        
        # สร้างแผนที่
        m = folium.Map(location=[lat, lon], zoom_start=15, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google Satellite')
        folium.Marker([lat, lon], popup="You", icon=folium.Icon(color='blue', icon='user', prefix='fa')).add_to(m)

        # ดึงพิกัดเพื่อนมาโชว์ถ้ามีการกดเลือกชื่อ หรือกำลังโทร
        active_target = st.session_state.get('call_target') or (target if target != "-- Select --" else None)
        if active_target:
            f_loc = db.reference(f'/users/{active_target}/location').get()
            if f_loc:
                f_lat, f_lon = f_loc.get('lat'), f_loc.get('lon')
                folium.Marker([f_lat, f_lon], popup=active_target, icon=folium.Icon(color='red', icon='eye', prefix='fa')).add_to(m)
                folium.PolyLine([[lat, lon], [f_lat, f_lon]], color="white", weight=1, opacity=0.6, dash_array='5').add_to(m)

        st_folium(m, width=700, height=350)
    else: st.warning(t["connecting"])
else: st.info(t["allow_gps"])

# --- 10. ACTIVE CALL & MUSIC ---
if "active_room" in st.session_state:
    st.divider()
    # ตรวจสอบว่าอีกฝ่ายรับหรือยัง
    check_call = db.reference(f'/calls/{st.session_state.call_target}').get()
    if check_call and check_call.get('status') == 'calling':
        st.warning(t["waiting"])
    
    st.subheader(f"🌐 Line Active: {st.session_state.call_target}")
    st.markdown(f'<iframe src="https://meet.jit.si/{st.session_state.active_room}" allow="camera; microphone; fullscreen" width="100%" height="450" style="border-radius:15px;"></iframe>', unsafe_allow_html=True)
    
    if st.button("End Call"):
        db.reference(f'/calls/{st.session_state.call_target}').delete()
        if "active_room" in st.session_state: del st.session_state.active_room
        if "call_target" in st.session_state: del st.session_state.call_target
        st.rerun()

st.write("---")
st.subheader(t["music_title"])
pid = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
st.markdown(f'<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list={pid}&autoplay=1&mute=1" frameborder="0" allow="autoplay; encrypted-media"></iframe>', unsafe_allow_html=True)

st.divider()
st.caption(t["footer"])
