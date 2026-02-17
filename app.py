import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- 1. ตั้งค่าพื้นฐาน ---
st.set_page_config(page_title="Synapse System", layout="wide")

# --- 2. การเชื่อมต่อ Firebase (Singleton) ---
@st.cache_resource
def get_db():
    if not firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets["firebase_service_account"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"การเชื่อมต่อฐานข้อมูลขัดข้อง: {e}")
            return None
    return firestore.client()

db = get_db()

# --- 3. จัดการ Session State ---
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'user' not in st.session_state:
    st.session_state.user = "Synapse_User"

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 4. ฟังก์ชันหน้าหลัก (Home) ---
def render_home():
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        logo_url = "https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg"
        st.image(logo_url, use_container_width=True)
    
    st.divider()
    st.video("https://www.youtube.com/watch?v=videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO")
    
    st.write("### 🌐 เลือกเข้าสู่มิติ")
    cols = st.columns(5)
    rooms = [("🔴 RED", "red"), ("🔵 BLUE", "blue"), ("🟢 GREEN", "green"), ("⚫ BLACK", "black"), ("🟣 PURPLE", "purple")]
    
    for i, (label, target) in enumerate(rooms):
        if cols[i].button(label, key=f"nav_{target}", use_container_width=True):
            go_to(target)

# --- 5. ห้องสีแดง (Red - Media Hub) ---
def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D;'>🔴 RED MEDIA HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="back_red"): go_to("home")

    with st.expander("📝 สร้างโพสต์ใหม่"):
        with st.form("post_form_red", clear_on_submit=True):
            msg = st.text_area("เขียนข้อความ...")
            url = st.text_input("ลิงก์ YouTube หรือ รูปภาพ")
            if st.form_submit_button("🚀 POST"):
                if db and (msg or url):
                    db.collection('posts_red').add({'user': st.session_state.user, 'text': msg, 'media': url, 'time': datetime.now()})
                    st.toast("โพสต์ออนไลน์แล้ว!")
                    st.rerun()

    if db:
        posts = db.collection('posts_red').limit(10).stream()
        for doc in posts:
            p = doc.to_dict()
            with st.container(border=True):
                st.write(f"👤 **{p.get('user')}**")
                st.write(p.get('text'))
                if p.get('media'):
                    if "youtube" in p.get('media'): st.video(p.get('media'))
                    else: st.image(p.get('media'), use_container_width=True)

# --- 6. ห้องสีน้ำเงิน (Blue - Voice/Call) ---
def render_blue_room():
    st.markdown("<h1 style='color:#00d4ff;'>🔵 BLUE VOICE HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="back_blue"): go_to("home")
    
    contacts = ["System Admin", "User_01", "Member_X"]
    for name in contacts:
        col_n, col_c = st.columns([3, 1])
        with col_n: st.markdown(f'<div style="padding:15px; background:rgba(0,212,255,0.1); border-radius:10px; margin-bottom:5px;">🟢 {name}</div>', unsafe_allow_html=True)
        with col_c: 
            if st.button(f"📞 CALL", key=f"call_{name}"):
                st.toast(f"กำลังเชื่อมต่อสายไปยัง {name}...")

# --- 7. ห้องสีเขียว (Green - Secret Chat) ---
def render_green_room():
    st.markdown("<h1 style='color:#00ff88;'>🟢 GREEN SECRET CHAT</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="back_green"): go_to("home")
    
    if db:
        with st.form("chat_green", clear_on_submit=True):
            msg = st.text_input("พิมพ์ข้อความลับ...")
            if st.form_submit_button("ส่ง"):
                if msg:
                    db.collection('messages_green').add({'user': st.session_state.user, 'msg': msg, 'time': datetime.now()})
                    st.rerun()
        
        chats = db.collection('messages_green').order_by('time', direction='DESCENDING').limit(15).stream()
        for chat in chats:
            c = chat.to_dict()
            st.markdown(f'<div style="background:rgba(0,255,136,0.1); padding:10px; border-left:4px solid #00ff88; margin-bottom:5px;"><b>{c.get("user")}</b>: {c.get("msg")}</div>', unsafe_allow_html=True)

# --- 8. ห้องสีดำ (Black - System Terminal) ---
def render_black_room():
    st.markdown("<h1 style='color:#00ff00; font-family:monospace; text-align:center;'>⚫ SYSTEM TERMINAL</h1>", unsafe_allow_html=True)
    if st.button("⬅️ EXIT TERMINAL", key="back_black"): go_to("home")
    
    st.code("""
    [STATUS] : CONNECTED
    [ENCRYPTION] : AES-256
    [LOG] : User connected to Synapse Core...
    [CMD] : system_check --run
    """, language="bash")
    st.warning("มิตินี้กำลังอยู่ในการปรับจูนสัญญาณขั้นสูง...")

# --- 9. ตัวควบคุมหลัก (Main Controller) ---
if st.session_state.page == "home": render_home()
elif st.session_state.page == "red": render_red_room()
elif st.session_state.page == "blue": render_blue_room()
elif st.session_state.page == "green": render_green_room()
elif st.session_state.page == "black": render_black_room()
else:
    st.title(f"มิติ {st.session_state.page} กำลังพัฒนา")
    if st.button("กลับหน้าหลัก"): go_to("home")
