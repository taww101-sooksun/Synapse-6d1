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
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="wide")

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
        u_id = st.text_input("Enter your ID / ใส่ ID ของคุณ (ห้ามเว้นว่าง)")
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

# --- 3. STYLE & UI ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp { background: linear-gradient(270deg, #0f0c29, #302b63, #24243e); background-size: 400% 400%; animation: RainbowFlow 15s ease infinite; color: white; }
    .chat-container { background: rgba(0, 0, 0, 0.4); padding: 20px; border-radius: 15px; border: 1px solid rgba(0, 210, 255, 0.3); margin-bottom: 10px; }
    .bubble-me { background: #0078ff; color: white; padding: 8px 12px; border-radius: 15px 15px 0 15px; margin: 5px 0; text-align: right; width: fit-content; margin-left: auto; }
    .bubble-them { background: #444; color: white; padding: 8px 12px; border-radius: 15px 15px 15px 0; margin: 5px 0; text-align: left; width: fit-content; }
    .msg-time { font-size: 0.7em; opacity: 0.6; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA OPS ---
# บันทึกสถานะ Online
db.reference(f'/users/{my_id}').update({
    'last_seen': datetime.now().strftime('%H:%M:%S'),
    'status': 'online'
})

# --- 5. MAIN INTERFACE ---
col1, col2 = st.columns([1, 2])

with col1:
    st.title("🛰️ CORE")
    st.write(f"USER: **{my_id}**")
    
    # ดึงรายชื่อเพื่อน
    all_users = db.reference('/users').get()
    friend_list = [u for u in all_users.keys() if u != my_id] if all_users else []
    target_chat = st.selectbox("💬 สนทนากับ:", ["-- เลือกเพื่อน --"] + friend_list)

    # GPS Data
    location = get_geolocation()
    if location:
        coords = location.get('coords', {})
        lat, lon = coords.get('latitude'), coords.get('longitude')
        if lat and lon:
            st.success(f"📍 GPS Active: {lat:.4f}, {lon:.4f}")
            m = folium.Map(location=[lat, lon], zoom_start=15, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
            folium.Marker([lat, lon]).add_to(m)
            st_folium(m, width=300, height=250)

with col2:
    if target_chat != "-- เลือกเพื่อน --":
        st.subheader(f"💬 Chatting with: {target_chat}")
        
        # ห้องแชต (Sort ID เพื่อให้เป็นห้องเดียวกัน)
        chat_room_id = "_".join(sorted([my_id, target_chat]))
        chat_ref = db.reference(f'/chats/{chat_room_id}')
        
        # ดึงข้อความ (20 ข้อความล่าสุด)
        msgs = chat_ref.order_by_child('timestamp').limit_to_last(20).get()
        
        # แสดงผลแชต
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        if msgs:
            for m_id in msgs:
                m = msgs[m_id]
                cls = "bubble-me" if m['sender'] == my_id else "bubble-them"
                st.markdown(f'<div class="{cls}">{m["text"]}<span class="msg-time">{m["time"]}</span></div>', unsafe_allow_html=True)
        else:
            st.caption("No messages yet. Start the conversation!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ช่องส่งข้อความ
        with st.form("msg_form", clear_on_submit=True):
            input_msg = st.text_input("Message", placeholder="พิมพ์ข้อความที่นี่...")
            if st.form_submit_button("SEND 🚀"):
                if input_msg:
                    chat_ref.push({
                        'sender': my_id,
                        'text': input_msg,
                        'timestamp': datetime.now().timestamp(),
                        'time': datetime.now().strftime('%H:%M')
                    })
                    st.rerun()
        
        if st.button("🔄 Refresh Chat"):
            st.rerun()
    else:
        st.info("👈 กรุณาเลือกเพื่อนจากแถบด้านซ้ายเพื่อเริ่มการแชต")

# --- 6. FOOTER & SOUND ---
st.write("---")
with st.expander("🎵 Music Therapy & System Info"):
    pid = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    st.markdown(f'<iframe width="100%" height="150" src="https://www.youtube.com/embed/videoseries?list={pid}" frameborder="0" allow="autoplay; encrypted-media"></iframe>', unsafe_allow_html=True)
    st.caption("SYNAPSE V1.7 | Secure Messenger Mode")
