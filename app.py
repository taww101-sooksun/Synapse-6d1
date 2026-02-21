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
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="wide", page_icon="🛰️")

# ใช้ interval 15 วินาที เพื่อลดภาระเครื่อง และเช็ค Notification
st_autorefresh(interval=15000, key="global_refresh")

if not firebase_admin._apps:
    try:
        # ดึงค่าจาก Secrets โดยตรง (ตรวจสอบให้แน่ใจว่าใน TOML พิมพ์ชื่อตรงกัน)
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': st.secrets["firebase_db_url"]
        })
    except Exception as e:
        st.error(f"⚠️ Firebase Connection Failed: {e}")

if 'my_id' not in st.session_state:
    st.session_state.my_id = f"USER-{random.randint(1000, 9999)}"
if 'last_msg_id' not in st.session_state:
    st.session_state.last_msg_id = None

# --- 2. STYLE ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { background: linear-gradient(270deg, #1a1a1a, #001f3f, #000000); background-size: 400% 400%; animation: RainbowFlow 20s ease infinite; }
    .glossy-card { background: rgba(20, 20, 20, 0.8); border: 1px solid #00f2ff; border-radius: 12px; padding: 15px; color: white; box-shadow: 0 0 10px #00f2ff; margin-bottom: 10px; }
    .stTextInput>div>div>input { background-color: #111; color: white; border: 1px solid #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (เพลงจะไม่โดน Refresh ถ้าเราไม่ขยับส่วนนี้มาก) ---
with st.sidebar:
    st.title("🛰️ SYNAPSE ONLINE")
    st.info(f"**ID:** {st.session_state.my_id}")
    
    st.markdown("---")
    st.subheader("🎵 SYNAPSE RADIO")
    # ใช้ Iframe แบบซ่อนขอบ
    pid = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    st.components.v1.html(
        f'<iframe width="100%" height="150" src="https://www.youtube.com/embed/videoseries?list={pid}" '
        f'frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
        height=160
    )
    
    # แสดงรายชื่อสมาชิกออนไลน์
    st.subheader("👥 Online Members")
    try:
        online_ref = db.reference('locations').get()
        if online_ref:
            for uid, data in online_ref.items():
                status = "🟢" if uid == st.session_state.my_id else "🔵"
                st.write(f"{status} {uid} <small>({data.get('last_seen', '??')})</small>", unsafe_allow_html=True)
    except:
        st.write("เชื่อมต่อฐานข้อมูลไม่ได้...")

# --- 4. GPS & MAP ---
col_map, col_chat = st.columns([3, 2])

with col_map:
    location = get_geolocation()
    if location and 'coords' in location:
        lat, lon = location['coords']['latitude'], location['coords']['longitude']
        now = datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%H:%M:%S')
        
        # อัปเดตตำแหน่งลง Firebase
        db.reference(f'locations/{st.session_state.my_id}').set({
            'lat': lat, 'lon': lon, 'last_seen': now
        })
        
        st.markdown(f"<div class='glossy-card'>📍 Location: {lat:.4f}, {lon:.4f} | ⏰ {now}</div>", unsafe_allow_html=True)
        
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Google Hybrid').add_to(m)
        
        # ดึงทุกคนมาปักหมุด
        all_users = db.reference('locations').get()
        if all_users:
            for uid, data in all_users.items():
                color = 'red' if uid == st.session_state.my_id else 'blue'
                folium.Marker([data['lat'], data['lon']], popup=uid, icon=folium.Icon(color=color)).add_to(m)
        
        st_folium(m, use_container_width=True, height=450, key="main_map")
    else:
        st.warning("📡 กำลังรอสัญญาณ GPS... (กรุณากดอนุญาตสิทธิ์การเข้าถึงตำแหน่ง)")

# --- 5. CHAT SYSTEM ---
with col_chat:
    st.markdown("<div class='glossy-card'>💬 TRANSMISSION</div>", unsafe_allow_html=True)
    
    # ส่วนแสดงข้อความ
    chat_container = st.container(height=350)
    try:
        messages = db.reference('chat').order_by_key().limit_to_last(20).get()
        if messages:
            for m_id, msg in messages.items():
                # ระบบ Notification แจ้งเตือนข้อความใหม่
                if st.session_state.last_msg_id != m_id:
                    if msg['user'] != st.session_state.my_id:
                        st.toast(f"New Msg from {msg['user']}")
                    st.session_state.last_msg_id = m_id
                
                with chat_container:
                    align = "right" if msg['user'] == st.session_state.my_id else "left"
                    st.markdown(f"**{msg['user']}**: {msg['text']} <br><small style='color:gray;'>{msg['time']}</small>", unsafe_allow_html=True)
                    st.markdown("---")
    except:
        st.error("Chat Offline")

    # ส่วนส่งข้อความ
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Message", label_visibility="collapsed")
        submit = st.form_submit_button("📡 SEND")
        if submit and user_input:
            db.reference('chat').push({
                'user': st.session_state.my_id,
                'text': user_input,
                'time': datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%H:%M')
            })
            st.rerun()

# --- 6. FOOTER ---
st.markdown(f"<div class='glossy-card' style='text-align: center; border-color: red;'>สโลแกน: อยู่นิ่งๆ ไม่เจ็บตัว</div>", unsafe_allow_html=True)
