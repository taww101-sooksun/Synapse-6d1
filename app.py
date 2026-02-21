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

# รีเฟรชหน้าจออัตโนมัติ
st_autorefresh(interval=15000, key="global_refresh")

# ฟังก์ชันเชื่อมต่อ Firebase เพื่อความเป็นระเบียบ
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            fb_creds = dict(st.secrets["firebase_service_account"])
            cred = credentials.Certificate(fb_creds)
            firebase_admin.initialize_app(cred, {
                'databaseURL': st.secrets["firebase_db_url"]
            })
            return True
        except Exception as e:
            st.error(f"⚠️ Firebase Connection Failed: {e}")
            return False
    return True

init_firebase()

if 'my_id' not in st.session_state:
    st.session_state.my_id = f"USER-{random.randint(1000, 9999)}"
if 'last_msg_id' not in st.session_state:
    st.session_state.last_msg_id = None

# --- 2. FETCH DATA ONCE (Optimization) ---
# ดึงข้อมูลมาครั้งเดียวเพื่อใช้ทั้งหน้า
try:
    all_users_data = db.reference('locations').get() or {}
    chat_messages = db.reference('chat').order_by_key().limit_to_last(20).get() or {}
except Exception as e:
    all_users_data = {}
    chat_messages = {}
    st.sidebar.warning("Database connection issues.")

# --- 3. STYLE (CSS) ---
st.markdown("""
    <style>
    @keyframes RainbowFlow { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    .stApp { background: linear-gradient(270deg, #1a1a1a, #001f3f, #000000); background-size: 400% 400%; animation: RainbowFlow 20s ease infinite; }
    .glossy-card { background: rgba(20, 20, 20, 0.8); border: 1px solid #00f2ff; border-radius: 12px; padding: 15px; color: white; box-shadow: 0
# บรรทัดที่ 53
st.markdown("""
    เนื้อหาที่คุณต้องการแสดง...
    สามารถเขียนได้หลายบรรทัด
""") # <--- ต้องมีเครื่องหมายคำพูด 3 อันปิดท้ายแบบนี้เสมอ
