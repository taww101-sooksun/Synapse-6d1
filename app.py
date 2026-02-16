import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
import hashlib
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components
import re

# --- 1. ตั้งค่าการเชื่อมต่อ Firebase ---
if not firebase_admin._apps:
    try:
        # ใช้ข้อมูลจาก Streamlit Secrets
        cred_dict = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'storageBucket': st.secrets["firebase_config"]["storageBucket"]
        })
    except Exception as e:
        st.error(f"❌ เชื่อมต่อฐานข้อมูลไม่สำเร็จ: {e}")
        st.stop()

db = firestore.client()
bucket = storage.bucket()

# --- 2. ฟังก์ชันเสริม (Helper Functions) ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_thai_time():
    return datetime.utcnow() + timedelta(hours=7)

def get_youtube_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- 3. ธีมสุดหรู (Luxury Theme) ---
def set_luxury_theme(room_type):
    themes = {
        "home":  {"bg": "#001219", "text": "#FFD700", "accent": "#D4AF37"},
        "red":   {"bg": "#3d0000", "text": "#FFFFFF", "accent": "#FF4D4D"},
        "blue":  {"bg": "#002147", "text": "#FFFFFF", "accent": "#00A8E8"},
        "green": {"bg": "#0a2910", "text": "#FFFFFF", "accent": "#38B000"},
        "black": {"bg": "#121212", "text": "#FFFFFF", "accent": "#E5E5E5"}
    }
    cfg = themes.get(room_type, themes["home"])
    st.markdown(f"""
        <style>
        .stApp {{ background: {cfg['bg']}; color: {cfg['text']}; }}
        .post-box {{
            border: 1px solid {cfg['accent']};
            background: rgba(255, 255, 255, 0.05);
            padding: 15px; border-radius: 12px; margin-bottom: 10px;
        }}
        .stButton>button {{
            background: {cfg['accent']}; color: black !important;
            font-weight: bold; border-radius: 8px; width: 100%;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. ฟังก์ชันแสดงโพสต์และระบบ Like ---
def render_posts(room_id):
    posts_ref = db.collection(f'posts_{room
