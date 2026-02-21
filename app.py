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

# รีเฟรชทุก 15 วินาที
st_autorefresh(interval=15000, key="global_refresh")

if not firebase_admin._apps:
    try:
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

# --- 2. STYLE (แก้จุดที่ String ไม่จบ) ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { background: linear-gradient(270deg, #1a1a1a, #001f3f, #000000); background-size: 400% 400%; animation: RainbowFlow 20s ease infinite; }
    .glossy-card { background: rgba(20, 20, 20, 0.8); border: 1px solid #00f2ff; border-radius: 12px; padding: 15px; color: white; box-shadow: 0 0 10px #00f2ff; margin-bottom: 10px; }
    .stTextInput>div>div>input { background-color: #111; color: white; border: 1px solid #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🛰️ SYNAPSE ONLINE")
    st.info(f"**ID:** {st.session_state.my_id}")
    
    st.markdown("---")
    st.subheader("🎵 SYNAPSE RADIO")
    pid = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    st.components.v1.html(
        f'<iframe width="100%" height="150" src="https://www.youtube.com{pid}" '
        f'frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
        height=160
    )
    
    st.subheader("👥 Online Members")
    try:
        online_ref = db.reference('locations').get()
        if online_ref:
            for uid, data in online_ref.items():
                status = "🟢" if uid == st.session_state.my_id else "🔵"
                st.write(f"{status} {uid} <small>({data.get('last_seen', '??')})</small>", unsafe_allow_html=True)
    except:
        st.write("เชื่อมต่อฐานข้อมูลไม่ได้...")

# --- 4. MAIN CONTENT (GPS & CHAT) ---
col_map, col_chat = st.columns([3, 2])

with col_map:
    st.subheader("📍 Real-time Tactical Map")
    location = get_geolocation()
    if location and 'coords' in location:
        lat, lon = location['coords']['latitude'], location['coords']['longitude']
        now = datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%H:%M:%S')
        
        # อัปเดตตำแหน่งลง Firebase (แก้ไขจุดที่พิมพ์ค้างไว้)
        db.reference(f'locations/{st.session_state.my_id}').set({
            'lat': lat, 
            'lon': lon, 
            'last_seen': now
        })
        
        # แสดงแผนที่ Folium
        m = folium.Map(location=[lat, lon], zoom_start=15, tiles="CartoDB dark_matter")
        folium.Marker([lat, lon], popup="You", icon=folium.Icon(color='blue')).add_to(m)
        st_folium(m, width="100%", height=500)
    else:
        st.warning("📡 กำลังรอสัญญาณ GPS... กรุณากดอนุญาตการเข้าถึงตำแหน่ง")

with col_chat:
    st.subheader("💬 Synapse Comms")
    # ส่วนสำหรับดึงข้อความจาก Firebase
    chat_ref = db.reference('chat').order_by_key().limit_to_last(10).get()
    
    chat_container = st.container(height=400)
    with chat_container:
        if chat_ref:
            for msg_id, msg_data in chat_ref.items():
                with st.chat_message("user" if msg_data['user'] == st.session_state.my_id else "assistant"):
                    st.write(f"**{msg_data['user']}**: {msg_data['text']}")

    # ช่องกรอกข้อความ
    if prompt := st.chat_input("ส่งข้อความถึงทีม..."):
        db.reference('chat').push({
            'user': st.session_state.my_id,
            'text': prompt,
            'timestamp': datetime.now(pytz.timezone('Asia/Bangkok')).isoformat()
        })
        st.rerun()
