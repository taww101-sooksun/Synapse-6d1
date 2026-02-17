import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- 1. การตั้งค่าเริ่มต้นที่ต้องไว้บนสุดเสมอ ---
st.set_page_config(page_title="Synapse System", layout="wide")

# --- 2. การเชื่อมต่อ Firebase (แบบ Singleton ป้องกันการต่อซ้ำ) ---
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets["firebase_service_account"])
            cred = credentials.Certificate(cred_dict)
            return firebase_admin.initialize_app(cred)
    return None

init_firebase()
db = firestore.client()

# --- 3. จัดการ Session State (สมองของแอป) ---
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'user' not in st.session_state:
    st.session_state.user = "Synapse_User"

# --- 4. ฟังก์ชันย่อยสำหรับแต่ละหน้า ---

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

def render_home():
    # ส่วนหัวและโลโก้
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        logo_url = "https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg"
        st.image(logo_url, use_container_width=True)
        st.markdown("<h2 style='text-align:center;'>ศูนย์บัญชาการ Synapse</h2>", unsafe_allow_html=True)

    st.divider()
    
    # ส่วนเนื้อหา (YouTube)
    st.video("https://www.youtube.com/watch?v=videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO")

    # ปุ่มทางเข้า 5 ห้อง (จัด Layout ใหม่ให้กดง่ายขึ้น)
    st.write("### 📂 เลือกมิติการเข้าถึง")
    cols = st.columns(5)
    rooms = [("🔴 RED", "red"), ("🔵 BLUE", "blue"), ("🟢 GREEN", "green"), ("⚫ BLACK", "black"), ("🟣 PURPLE", "purple")]
    
    for i, (label, target) in enumerate(rooms):
        if cols[i].button(label, key=f"btn_{target}", use_container_width=True):
            go_to(target)

def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D;'>🔴 RED MEDIA HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก"): go_to("home")

    # ส่วนโพสต์ (ใช้ Form เพื่อลดการ Rerun พร่ำเพรื่อ)
    with st.expander("📝 สร้างโพสต์ใหม่", expanded=False):
        with st.form("post_form", clear_on_submit=True):
            msg = st.text_area("เขียนข้อความ...")
            url = st.text_input("ลิงก์สื่อ (YouTube/Image)")
            if st.form_submit_button("🚀 ปล่อยโพสต์"):
                if msg or url:
                    db.collection('posts_red').add({
                        'user': st.session_state.user,
                        'text': msg,
                        'media': url,
                        'time': datetime.now()
                    })
                    st.toast("โพสต์สำเร็จแล้ว!")
                    st.rerun()

    st.divider()

    # ส่วนแสดงฟีด (จำกัดจำนวนเพื่อความลื่น)
    posts = db.collection('posts_red').order_by('time', direction='DESCENDING').limit(15).stream()
    for doc in posts:
        p = doc.to_dict()
        with st.container(border=True):
            st.markdown(f"**👤 {p.get('user')}**")
            st.write(p.get('text'))
            if p.get('media'):
                if "youtube" in p.get('media'): st.video(p.get('media'))
                else: st.image(p.get('media'), use_container_width=True)
            
            # แถบ Like (จำลอง)
            st.button(f"❤️ Like", key=f"like_{doc.id}")

# --- 5. Main Switch (ตัวสลับหน้าจอ) ---
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "red":
    render_red_room()
else:
    st.title(f"ห้อง {st.session_state.page} กำลังพัฒนา")
    if st.button("กลับหน้าหลัก"): go_to("home")
