import streamlit as st
import requests
from streamlit_js_eval import get_geolocation
from datetime import datetime
import pytz
import folium
from streamlit_folium import st_folium
import firebase_admin
from firebase_admin import credentials, db
import random
from streamlit_autorefresh import st_autorefresh 

# --- 1. INITIALIZE ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="wide")

# รีเฟรชแอปทุก 10 วินาที (ปรับเพิ่มจาก 5 เป็น 10 เพื่อให้เพลงมีช่วงเล่นยาวขึ้นนิดนึง)
st_autorefresh(interval=10000, key="notify_check")

if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': st.secrets["firebase_db_url"]
        })
    except Exception as e:
        st.error(f"⚠️ Firebase Error: {e}")

if 'my_id' not in st.session_state:
    st.session_state.my_id = f"USER-{random.randint(1000, 9999)}"
if 'last_msg_id' not in st.session_state:
    st.session_state.last_msg_id = None
if 'last_user_count' not in st.session_state:
    st.session_state.last_user_count = 0

# --- 2. STYLE ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); background-size: 1200% 1200%; animation: RainbowFlow 30s ease infinite; }
    .glossy-card { background: rgba(0, 0, 0, 0.85); border: 2px solid white; border-radius: 15px; padding: 20px; color: white; box-shadow: 0 0 15px #fff; text-shadow: 0 0 5px #fff; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. NOTIFICATION LOGIC ---
def check_notifications():
    try:
        msgs = db.reference('chat').order_by_key().limit_to_last(1).get()
        if msgs:
            msg_id = list(msgs.keys())[0]
            msg_data = msgs[msg_id]
            if st.session_state.last_msg_id != msg_id:
                if msg_data['user'] != st.session_state.my_id:
                    st.toast(f"💬 {msg_data['user']}: {msg_data['text']}", icon="🔔")
                st.session_state.last_msg_id = msg_id
        
        users = db.reference('locations').get()
        if users and len(users) > st.session_state.last_user_count:
            st.toast("🛰️ ตรวจพบสัญญาณใหม่!", icon="🛰️")
            st.session_state.last_user_count = len(users)
    except: pass

check_notifications()

# --- 4. SIDEBAR & MUSIC ---
st.sidebar.title("🛰️ SYNAPSE ONLINE")
st.sidebar.markdown(f"**ID:** `{st.session_state.my_id}`")

# --- ส่วนเล่นเพลง (ใส่ใน Sidebar เพื่อความเป็นระเบียบ) ---
st.sidebar.markdown("---")
st.sidebar.subheader("🎵 SYNAPSE RADIO")
pid = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
st.sidebar.markdown(
    f'<iframe width="100%" height="180" src="https://www.youtube.com/embed/videoseries?list={pid}&autoplay=1" '
    f'frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', 
    unsafe_allow_html=True
)
st.sidebar.markdown("---")

# --- 5. GPS & MAP ---
location = get_geolocation()
if location and 'coords' in location:
    lat, lon = location['coords']['latitude'], location['coords']['longitude']
    now = datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%H:%M:%S')
    try:
        db.reference(f'locations/{st.session_state.my_id}').set({'lat': lat, 'lon': lon, 'last_seen': now})
    except: pass
    
    st.markdown(f"<div class='glossy-card' style='display: flex; justify-content: space-around;'><span>📍 {lat:.4f}, {lon:.4f}</span><span style='color: yellow;'>⏰ {now}</span></div>", unsafe_allow_html=True)
    
    m = folium.Map(location=[lat, lon], zoom_start=15)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Google Hybrid').add_to(m)
    
    try:
        all_users = db.reference('locations').get()
        if all_users:
            st.sidebar.subheader("👥 สมาชิกที่ออนไลน์")
            for uid, data in all_users.items():
                is_me = (uid == st.session_state.my_id)
                folium.Marker([data['lat'], data['lon']], popup=uid, icon=folium.Icon(color='red' if is_me else 'blue')).add_to(m)
                st.sidebar.write(f"{'🟢' if is_me else '🔵'} {uid} ({data['last_seen']})")
    except: pass
    st_folium(m, use_container_width=True, height=400)
else:
    st.info("📡 รอสัญญาณ GPS...")

# --- 6. CHAT SYSTEM ---
st.markdown("<div class='glossy-card'>", unsafe_allow_html=True)
st.subheader("💬 SYNAPSE TRANSMISSION")
chat_box = st.container(height=200)
try:
    messages = db.reference('chat').order_by_key().limit_to_last(15).get()
    with chat_box:
        if messages:
            for _, msg in messages.items():
                st.markdown(f"**[{msg['user']}]**: {msg['text']} <small style='color:gray;'>({msg['time']})</small>", unsafe_allow_html=True)
except: st.write("กำลังเชื่อมต่อแชต...")

with st.form("send_msg", clear_on_submit=True):
    col_msg, col_btn = st.columns([4, 1])
    txt = col_msg.text_input("", placeholder="พิมพ์ข้อความที่นี่...")
    if col_btn.form_submit_button("📡 ส่ง") and txt:
        db.reference('chat').push({
            'user': st.session_state.my_id,
            'text': txt,
            'time': datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%H:%M')
        })
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# --- 7. FOOTER ---
st.markdown(f"<div class='glossy-card' style='text-align: center;'>'อยู่นิ่งๆ ไม่เจ็บตัว'</div>", unsafe_allow_html=True)
