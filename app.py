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

# --- 1. INITIALIZE ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="wide")

if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': st.secrets["firebase_db_url"]
        })
    except:
        st.error("⚠️ กรุณาตรวจสอบการตั้งค่า Firebase ใน Secrets")

if 'my_id' not in st.session_state:
    st.session_state.my_id = f"USER-{random.randint(1000, 9999)}"

# --- 2. STYLE ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff); background-size: 1200% 1200%; animation: RainbowFlow 30s ease infinite; }
    .glossy-card { background: rgba(0, 0, 0, 0.85); border: 2px solid white; border-radius: 15px; padding: 20px; color: white; box-shadow: 0 0 15px #fff; text-shadow: 0 0 5px #fff; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR & ONLINE USERS ---
st.sidebar.title("🛰️ SYNAPSE ONLINE")
st.sidebar.markdown(f"**ID:** `{st.session_state.my_id}`")
st.sidebar.markdown("---")

# --- 4. GPS & GLOBAL MAP (เหมือนเดิมทุกประการ) ---
location = get_geolocation()

if location and 'coords' in location:
    lat, lon = location['coords']['latitude'], location['coords']['longitude']
    now = datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%H:%M:%S')

    # อัปเดตพิกัดขึ้น Firebase
    try:
        db.reference(f'locations/{st.session_state.my_id}').set({'lat': lat, 'lon': lon, 'last_seen': now})
    except: pass

    # แสดงพิกัดและอากาศ
    st.markdown(f"<div class='glossy-card' style='display: flex; justify-content: space-around;'><span>📍 {lat:.4f}, {lon:.4f}</span><span style='color: yellow;'>⏰ {now}</span></div>", unsafe_allow_html=True)

    # วาดแผนที่
    m = folium.Map(location=[lat, lon], zoom_start=15)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Google Hybrid').add_to(m)

    # ปักหมุดทุกคน
    try:
        users = db.reference('locations').get()
        if users:
            st.sidebar.subheader("👥 สมาชิกที่ออนไลน์")
            for uid, data in users.items():
                is_me = (uid == st.session_state.my_id)
                folium.Marker([data['lat'], data['lon']], popup=uid, icon=folium.Icon(color='red' if is_me else 'blue')).add_to(m)
                st.sidebar.write(f"{'🟢' if is_me else '🔵'} {uid} ({data['last_seen']})")
    except: pass

    st_folium(m, use_container_width=True, height=450)
else:
    st.info("📡 รอสัญญาณ GPS...")

# --- 5. ระบบแชตใหม่ (แทนที่ระบบโทร) ---
st.markdown("<div class='glossy-card'>", unsafe_allow_html=True)
st.subheader("💬 SYNAPSE TRANSMISSION")

# พื้นที่แสดงข้อความ
chat_box = st.container(height=250)
try:
    messages = db.reference('chat').order_by_key().limit_to_last(15).get()
    with chat_box:
        if messages:
            for _, msg in messages.items():
                st.markdown(f"**[{msg['user']}]**: {msg['text']} <small style='color:gray;'>({msg['time']})</small>", unsafe_allow_html=True)

    # ช่องส่งข้อความ
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
import streamlit as st
# --- เพิ่มไลบรารีสำหรับควบคุมเวลาการรีเฟรช ---
from streamlit_autorefresh import st_autorefresh 

# 1. ตั้งค่าให้แอป Refresh ตัวเองทุก 5 วินาที (เพื่อให้เห็นแจ้งเตือนแบบ Real-time)
# คีย์ 'notify_check' เพื่อให้ระบบรู้ว่าเป็นการรันเพื่อเช็คข้อมูล
st_autorefresh(interval=5000, key="notify_check")

# --- ส่วนของ Logic แจ้งเตือน (เอาไว้บนสุดของแอปหรือต่อจากจุดเชื่อมต่อ Firebase) ---

if 'last_msg_id' not in st.session_state:
    st.session_state.last_msg_id = None
if 'last_user_count' not in st.session_state:
    st.session_state.last_user_count = 0

def check_notifications():
    try:
        # 🔔 เช็คข้อความแชตใหม่
        msgs = db.reference('chat').order_by_key().limit_to_last(1).get()
        if msgs:
            msg_id = list(msgs.keys())[0]
            msg_data = msgs[msg_id]
            # ถ้าเป็นข้อความใหม่ และไม่ใช่เราเป็นคนส่งเอง
            if st.session_state.last_msg_id != msg_id:
                if msg_data['user'] != st.session_state.my_id:
                    st.toast(f"💬 ข้อความใหม่จาก {msg_data['user']}: {msg_data['text']}", icon="🔔")
                st.session_state.last_msg_id = msg_id

        # 👥 เช็คเพื่อนใหม่ที่ออนไลน์
        users = db.reference('locations').get()
        if users:
            current_user_count = len(users)
            if current_user_count > st.session_state.last_user_count:
                # หา ID ล่าสุดที่เพิ่มเข้ามา (ถ้าไม่ใช่ตัวเรา)
                new_user = list(users.keys())[-1]
                if new_user != st.session_state.my_id:
                    st.toast(f"🛰️ ตรวจพบสัญญาณใหม่: {new_user} กำลังออนไลน์", icon="🛰️")
            st.session_state.last_user_count = current_user_count
    except:
        pass

# เรียกใช้งานฟังก์ชันแจ้งเตือน
check_notifications()

# --- ต่อด้วยโค้ด GPS, แผนที่ และแชตเดิมของคุณ ---
       
except:
    st.write("ระบบแแชตกำลังเชื่อมต่อ...")
st.markdown("</div>", unsafe_allow_html=True)

# --- 6. FOOTER ---
st.markdown(f"<div class='glossy-card' style='text-align: center;'>'อยู่นิ่งๆ ไม่เจ็บตัว'</div>", unsafe_allow_html=True)
