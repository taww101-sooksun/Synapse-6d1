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
from firebase_admin import credentials, db
import uuid

# --- 1. INITIALIZE FIREBASE ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="centered")

if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/'
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
                st.session_state.my_id = u_id.strip()
                st.rerun()
            else:
                st.error("Unauthorized or ID Empty!")
    st.stop()

my_id = st.session_state.my_id

# --- 3. LANGUAGES ---
languages = {
    "TH": {
        "chat_title": "💬 ห้องสนทนาไร้สาย", "send": "ส่ง", "placeholder": "พิมพ์ข้อความ...",
        "status_info": "STAY STILL & HEAL : 'อยู่นิ่งๆ ไม่เจ็บตัว'",
        "temp": "🌡️ อุณหภูมิ", "time": "⏰ เวลา", "map_title": "🗺️ พิกัดดาวเทียม"
    },
    "EN": {
        "chat_title": "💬 Wireless Chat", "send": "Send", "placeholder": "Type a message...",
        "status_info": "STAY STILL & HEAL",
        "temp": "🌡️ Temp", "time": "⏰ Time", "map_title": "🗺️ Satellite Map"
    }
}
sel_lang = st.sidebar.selectbox("LANGUAGE", ["TH", "EN"])
t = languages[sel_lang]

# --- 4. STYLE (Rainbow) ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp { background: linear-gradient(270deg, #121212, #1a1a2e, #16213e); background-size: 400% 400%; animation: RainbowFlow 15s ease infinite; color: white; }
    .chat-box { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; height: 300px; overflow-y: auto; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.1); }
    .msg-user { color: #00d2ff; font-weight: bold; }
    .msg-text { color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. REGISTER USER STATUS ---
db.reference(f'/users/{my_id}').update({'last_seen': datetime.now().strftime('%H:%M:%S'), 'status': 'online'})

# --- 6. CHAT SYSTEM (Replacement for Calling) ---
st.sidebar.title(f"👤 ID: {my_id}")
all_users = db.reference('/users').get()
friend_list = [u for u in all_users.keys() if u != my_id] if all_users else []
target_chat = st.sidebar.selectbox("💬 เลือกคนที่จะแชตด้วย", ["-- เลือกเพื่อน --"] + friend_list)

if target_chat != "-- เลือกเพื่อน --":
    st.subheader(f"{t['chat_title']} ⮕ {target_chat}")
    
    # สร้าง Chat ID (เอา ID มาเรียงกันเพื่อให้ทั้งคู่เห็นห้องเดียวกัน)
    chat_room_id = "_".join(sorted([my_id, target_chat]))
    chat_ref = db.reference(f'/chats/{chat_room_id}')

    # แสดงข้อความ
    messages = chat_ref.order_by_child('timestamp').limit_to_last(20).get()
    
    chat_html = '<div class="chat-box">'
    if messages:
        for m_id in messages:
            m = messages[m_id]
            chat_html += f'<p><span class="msg-user">{m["sender"]}:</span> <span class="msg-text">{m["text"]}</span> <small style="opacity:0.5;">({m["time"]})</small></p>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # ส่วนการส่งข้อความ
    with st.container():
        msg_input = st.text_input("", placeholder=t["placeholder"], key="chat_input")
        if st.button(t["send"]):
            if msg_input:
                chat_ref.push({
                    'sender': my_id,
                    'text': msg_input,
                    'timestamp': datetime.now().timestamp(),
                    'time': datetime.now().strftime('%H:%M')
                })
                st.rerun()

st.divider()

# --- 7. GPS & MAP (เหมือนเดิม) ---
location = get_geolocation()
if location:
    coords = location.get('coords', {})
    lat, lon = coords.get('latitude'), coords.get('longitude')
    if lat and lon:
        st.write(f"📍 พิกัดปัจจุบัน: {lat:.4f}, {lon:.4f}")
        m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
        folium.Marker([lat, lon]).add_to(m)
        st_folium(m, width=700, height=300)

# --- 8. MUSIC ---
st.write("---")
st.subheader("🎵 Therapy Sound")
pid = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
st.markdown(f'<iframe width="100%" height="150" src="https://www.youtube.com/embed/videoseries?list={pid}" frameborder="0" allow="autoplay; encrypted-media"></iframe>', unsafe_allow_html=True)
