import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- 1. ตั้งค่าพื้นฐาน (ต้องอยู่บรรทัดแรกสุดของสคริปต์) ---
st.set_page_config(page_title="Synapse System", layout="wide")

# --- 2. การเชื่อมต่อ Firebase (แก้ไข Syntax Error แล้ว) ---
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            # ดึงข้อมูลจาก Secrets ของ Streamlit Cloud
            cred_dict = dict(st.secrets["firebase_service_account"])
            cred = credentials.Certificate(cred_dict)
            return firebase_admin.initialize_app(cred)
        except Exception as e:
            # หากเกิดข้อผิดพลาด จะแสดงคำเตือนแต่ไม่ทำให้โปรแกรมหยุดทำงาน
            st.error(f"การเชื่อมต่อ Firebase ขัดข้อง: {e}")
            return None
    return None

# เรียกใช้งานการเชื่อมต่อ
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
    
    # YouTube Playlist
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
    if st.button("⬅️ กลับหน้าหลัก"): 
        go_to("home")

    # ส่วนบรรยายห้อง
    st.info("ยินดีต้อนรับสู่พื้นที่สาธารณะ ทุกโพสต์มีความเท่าเทียมกัน ดันฟีดตามเวลาจริง")

    # ส่วนฟอร์มโพสต์
    with st.expander("📝 สร้างโพสต์ใหม่", expanded=False):
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
                    st.toast("โพสต์ของคุณออนไลน์แล้ว!")
                    st.rerun()
                elif not db:
                    st.error("ฐานข้อมูลไม่ได้เชื่อมต่อ")

    st.divider()

    # ส่วนแสดงฟีด
    if db:
        try:
            # ดึงข้อมูล (ลบ order_by ออกก่อนเพื่อป้องกันหน้าแดงเรื่อง Index)
            posts = db.collection('posts_red').limit(15).stream()
            for doc in posts:
                p = doc.to_dict()
                with st.container(border=True):
                    st.markdown(f"**👤 {p.get('user')}**")
                    st.write(p.get('text'))
                    if p.get('media'):
                        m = p.get('media')
                        if "youtube" in m or "youtu.be" in m:
                            st.video(m)
                        else:
                            st.image(m, use_container_width=True)
                    st.button(f"❤️ Like", key=f"lk_{doc.id}")
        except Exception:
            st.write("กำลังรอการเชื่อมต่อฟีด...")

# --- 7. ตัวควบคุมหลัก (Main Logic) ---
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "red":
    render_red_room()
else:
    st.title(f"มิติ {st.session_state.page} กำลังเปิดการเชื่อมต่อ...")
    if st.button("กลับหน้าหลัก"): 
        go_to("home")
