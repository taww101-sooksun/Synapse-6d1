import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- 1. ตั้งค่าพื้นฐาน ---
st.set_page_config(page_title="Synapse System", layout="wide")

# --- 2. การเชื่อมต่อ Firebase ---
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets["firebase_service_account"])
            cred = credentials.Certificate(cred_dict)
            return firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"การเชื่อมต่อ Firebase ขัดข้อง: {e}")
            return None
    return None

init_firebase()
try:
    db = firestore.client()
except Exception:
    db = None

# --- 3. จัดการ Session State ---
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'user' not in st.session_state:
    st.session_state.user = "Synapse_User"

# --- 4. ฟังก์ชันเปลี่ยนหน้าจอ ---
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 5. หน้าหลัก (Home) ---
def render_home():
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        logo_url = "https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg"
        st.image(logo_url, use_container_width=True)
        st.markdown("<h2 style='text-align:center; color:#FFD700;'>COMMAND CENTER</h2>", unsafe_allow_html=True)

    st.divider()
    st.video("https://www.youtube.com/watch?v=videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO")

    st.write("### 📂 เลือกเข้าสู่มิติ")
    cols = st.columns(5)
    rooms = [("🔴 RED", "red"), ("🔵 BLUE", "blue"), ("🟢 GREEN", "green"), ("⚫ BLACK", "black"), ("🟣 PURPLE", "purple")]
    
    for i, (label, target) in enumerate(rooms):
        if cols[i].button(label, key=f"btn_{target}", use_container_width=True):
            go_to(target)

# --- 6. ห้องสีแดง (Red Room) ---
def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D;'>🔴 RED MEDIA HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="back_red"): 
        go_to("home")

    st.info("ยินดีต้อนรับสู่พื้นที่สาธารณะ ทุกโพสต์มีความเท่าเทียมกัน")

    with st.expander("📝 สร้างโพสต์ใหม่"):
        with st.form("post_form", clear_on_submit=True):
            msg = st.text_area("เขียนข้อความ...")
            url = st.text_input("ลิงก์ YouTube หรือ รูปภาพ")
            if st.form_submit_button("🚀 ปล่อยโพสต์"):
                if db and (msg or url):
                    db.collection('posts_red').add({
                        'user': st.session_state.user,
                        'text': msg,
                        'media': url,
                        'time': datetime.now()
                    })
                    st.toast("โพสต์ออนไลน์แล้ว!")
                    st.rerun()

    st.divider()
    if db:
        try:
            posts = db.collection('posts_red').limit(15).stream()
            for doc in posts:
                p = doc.to_dict()
                with st.container(border=True):
                    st.markdown(f"**👤 {p.get('user')}**")
                    st.write(p.get('text'))
                    if p.get('media'):
                        m = p.get('media')
                        if "youtube" in m or "youtu.be" in m: st.video(m)
                        else: st.image(m, use_container_width=True)
                    st.button(f"❤️ Like", key=f"lk_{doc.id}")
        except Exception:
            st.write("กำลังรอการเชื่อมต่อฟีด...")

# --- 7. ห้องสีน้ำเงิน (Blue Room) ---
def render_blue_room():
    st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle, #001a33 0%, #000000 100%); }
        .blue-title { color: #00d4ff; text-align: center; font-weight: bold; text-shadow: 0 0 15px rgba(0, 212, 255, 0.6); }
        .contact-card { background: rgba(0, 212, 255, 0.05); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 15px; padding: 15px; margin-bottom: 10px; }
        .status-dot { height: 10px; width: 10px; background-color: #00ff00; border-radius: 50%; display: inline-block; margin-right: 5px; box-shadow: 0 0 10px #00ff00; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='blue-title'>🔵 BLUE VOICE HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="back_blue"): go_to("home")

    st.divider()
    st.subheader("👥 ผู้ติดต่อออนไลน์")
    contacts = ["System Admin", "User_01", "Member_X"]
    
    for name in contacts:
        col_name, col_call = st.columns([3, 1])
        with col_name:
            st.markdown(f'<div class="contact-card"><span class="status-dot"></span> {name}</div>', unsafe_allow_html=True)
        with col_call:
            if st.button(f"📞 CALL", key=f"call_{name}"):
                st.toast(f"กำลังเชื่อมต่อสายไปยัง {name}...")
                st.balloons()

    st.divider()
    st.subheader("🎵 Synapse Sound Therapy")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# --- 8. ตัวควบคุมหลัก (Main Logic) ---
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "red":
    render_red_room()
elif st.session_state.page == "blue":
    render_blue_room()
else:
    st.title(f"มิติ {st.session_state.page} กำลังเปิดการเชื่อมต่อ...")
    if st.button("กลับหน้าหลัก"): 
        go_to("home")
