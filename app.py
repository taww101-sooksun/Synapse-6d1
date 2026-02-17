import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- 1. ตั้งค่าพื้นฐาน (ป้องกันหน้าจอขาว) ---
st.set_page_config(page_title="Synapse System", layout="centered")

# --- 2. การเชื่อมต่อ Firebase แบบปลอดภัย ---
# ถ้าเชื่อมต่อไม่ได้ ระบบจะแจ้งเตือนแต่ไม่ทำหน้าจอแดงค้าง
if not firebase_admin._apps:
    try:
        if "firebase_service_account" in st.secrets:
            cred_dict = dict(st.secrets["firebase_service_account"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        else:
            st.warning("⚠️ ยังไม่ได้ตั้งค่า Firebase Secrets ในระบบ")
    except Exception as e:
        st.error(f"❌ Firebase Error: {e}")

# สร้างตัวแปรฐานข้อมูล (ถ้าเชื่อมต่อสำเร็จ)
try:
    db = firestore.client()
except:
    db = None

# --- 3. จัดการสถานะผู้ใช้ ---
if 'user' not in st.session_state:
    st.session_state.user = "Synapse_User" # ชื่อจำลอง
if 'page' not in st.session_state:
    st.session_state.page = "home"

# --- 4. ส่วนการแสดงผล CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001219 0%, #000000 100%); color: white; }
    .logo-box { display: flex; justify-content: center; padding: 20px; }
    .stButton>button { width: 100%; height: 60px; border-radius: 12px; font-weight: bold; background: #1a1a1a; color: #D4AF37; border: 1px solid #D4AF37; }
    </style>
""", unsafe_allow_html=True)

# --- 5. ฟังก์ชันหน้าหลัก (Home) ---
def render_home():
    st.markdown('<div class="logo-box">', unsafe_allow_html=True)
    # ดึงรูปจาก GitHub ของคุณโดยตรง
    logo_url = "https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg"
    st.image(logo_url, width=280)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("🎬 Synapse Playlist")
    st.video("https://www.youtube.com/watch?v=videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO")
    
    st.write("---")
    st.subheader("🌐 เลือกเข้าสู่มิติ")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔴 RED (Media)"):
            st.session_state.page = "red"; st.rerun()
    with col2:
        if st.button("🔵 BLUE (Voice)"):
            st.info("กำลังพัฒนา..."); 
    with col3:
        if st.button("🟢 GREEN (Chat)"):
            st.info("กำลังพัฒนา..."); 

# --- 6. ฟังก์ชันห้องสีแดง (Red Room) ---
def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D; text-align:center;'>🔴 RED PUBLIC FEED</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก"):
        st.session_state.page = "home"; st.rerun()

    # ส่วนสร้างโพสต์
    with st.expander("📝 สร้างโพสต์ใหม่"):
        with st.form("red_post"):
            msg = st.text_area("ข้อความของคุณ")
            media = st.text_input("ลิงก์รูป/วิดีโอ")
            if st.form_submit_button("🚀 POST"):
                if db and (msg or media):
                    db.collection('posts_red').add({
                        'user': st.session_state.user,
                        'text': msg,
                        'media': media,
                        'time': datetime.now()
                    })
                    st.success("โพสต์เรียบร้อย!")
                    st.rerun()
                elif not db:
                    st.error("ไม่ได้เชื่อมต่อฐานข้อมูล")

    st.divider()
    
    # ดึงข้อมูลมาโชว์ (แบบกันพัง)
    if db:
        try:
            posts = db.collection('posts_red').limit(10).stream()
            for doc in posts:
                p = doc.to_dict()
                st.write(f"👤 **{p.get('user')}**")
                st.write(p.get('text'))
                if p.get('media'):
                    st.caption(f"สื่อ: {p.get('media')}")
                st.divider()
        except Exception as e:
            st.write("กำลังรอข้อมูลใหม่...")

# --- 7. ตัวควบคุมหลัก ---
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "red":
    render_red_room()
