import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- 1. ตั้งค่าพื้นฐาน ---
st.set_page_config(page_title="Synapse System", layout="centered")

# --- 2. การเชื่อมต่อ Firebase (กันหน้าจอขาว) ---
if not firebase_admin._apps:
    try:
        cred_dict = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"⚠️ การเชื่อมต่อล้มเหลว: {e}")
        st.stop()

db = firestore.client()

# --- 3. ฟังก์ชันหน้าหลัก (Home) ---
def render_home():
    st.markdown("""
        <style>
        .logo-box { display: flex; justify-content: center; padding: 20px; }
        .stButton>button { width: 100%; height: 60px; border-radius: 12px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="logo-box">', unsafe_allow_html=True)
    logo_url = "https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg"
    st.image(logo_url, width=280)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    # YouTube Playlist
    st.video("https://www.youtube.com/watch?v=videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO")
    
    st.write("---")
    st.subheader("🌐 เลือกเข้าสู่มิติ")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔴 RED"): st.session_state.page = "red"; st.rerun()
    with col2:
        if st.button("🔵 BLUE"): st.session_state.page = "blue"; st.rerun()
    with col3:
        if st.button("🟢 GREEN"): st.session_state.page = "green"; st.rerun()

# --- 4. ฟังก์ชันห้องสีแดง (Red Room) ---
def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D; text-align:center;'>🔴 RED PUBLIC FEED</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก"):
        st.session_state.page = "home"; st.rerun()

    with st.expander("📝 สร้างโพสต์ใหม่"):
        with st.form("red_post", clear_on_submit=True):
            msg = st.text_area("ข้อความของคุณ")
            media = st.text_input("ลิงก์รูป/วิดีโอ")
            if st.form_submit_button("🚀 POST"):
                if msg or media:
                    db.collection('posts_red').add({
                        'user': st.session_state.user,
                        'text': msg,
                        'media': media,
                        'likes': [],
                        'time': datetime.now()
                    })
                    st.rerun()

    st.divider()
    
    # ดึงข้อมูลโพสต์ (แบบ Safe Mode ไม่เรียงลำดับป้องกัน Index Error)
    try:
        posts = db.collection('posts_red').limit(20).stream()
        for doc in posts:
            p = doc.to_dict()
            st.markdown(f"**👤 {p.get('user')}**")
            st.write(p.get('text'))
            if p.get('media'):
                if "youtube" in p.get('media'): st.video(p.get('media'))
                else: st.image(p.get('media'), use_container_width=True)
            st.write("---")
    except:
        st.write("รอข้อมูลสักครู่...")

# --- 5. ระบบควบคุมหน้าจอ (Main Logic) ---
if 'user' not in st.session_state:
    st.session_state.user = "Synapse_User" # ข้าม Login ไปก่อนเพื่อรันดูผล

if 'page' not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "red":
    render_red_room()
