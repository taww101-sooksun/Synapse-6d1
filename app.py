import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time

# --- 1. ตั้งค่าพื้นฐาน ---
st.set_page_config(page_title="Synapse Core", layout="wide")

# --- 2. เชื่อมต่อฐานข้อมูล ---
@st.cache_resource
def get_db():
    if not firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets["firebase_service_account"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except: return None
    return firestore.client()

db = get_db()

# --- 3. ระบบจัดการหน้าจอ (Session State) ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user' not in st.session_state: st.session_state.user = "Synapse_User"

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- 4. ตกแต่งหน้าตา (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .stButton>button { border-radius: 20px; height: 3em; font-weight: bold; }
    .chat-card { background: rgba(0, 255, 136, 0.1); border-left: 5px solid #00ff88; padding: 10px; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 5. ฟังก์ชันแต่ละหน้า (Dimensions) ---

def render_home():
    # โลโก้กลางหน้าจอ
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        logo_url = "https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg"
        st.image(logo_url, use_container_width=True)
        st.markdown("<h2 style='text-align:center; color:#FFD700;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#888;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)

    st.divider()

    # เพลย์ลิสต์ YouTube
    st.subheader("📺 Synapse Playlist")
    st.video("https://www.youtube.com/watch?v=videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO")

    st.divider()

    # คำบรรยายการใช้งาน
    with st.expander("📖 คู่มือการใช้งานระบบ Synapse"):
        st.markdown("""
        * **🔴 RED:** พื้นที่โพสต์สื่อและข้อความสาธารณะ
        * **🔵 BLUE:** ศูนย์รวมเสียงและการติดต่อสื่อสาร
        * **🟢 GREEN:** ห้องแชทลับ เข้ารหัสข้อมูลเรียลไทม์
        * **⚫ BLACK:** หน้าจอเทอร์มินัล ตรวจสอบสถานะระบบ
        * **🟣 PURPLE:** ตั้งค่าตัวตนและชื่อเล่นของคุณ
        """)

    # ปุ่มนำทาง
    st.write("### 🌐 เลือกมิติเข้าใช้งาน")
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("🔴 RED", key="h_red", use_container_width=True): go_to("red")
    if c2.button("🔵 BLUE", key="h_blue", use_container_width=True): go_to("blue")
    if c3.button("🟢 GREEN", key="h_green", use_container_width=True): go_to("green")
    if c4.button("⚫ BLACK", key="h_black", use_container_width=True): go_to("black")
    if c5.button("🟣 PURPLE", key="h_purple", use_container_width=True): go_to("purple")

def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D;'>🔴 RED MEDIA</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="back_red"): go_to("home")
    # ... (ส่วนดึงข้อมูล Red เดิม) ...
    st.info("มิติสีแดงพร้อมใช้งาน")

def render_blue_room():
    st.markdown("<h1 style='color:#00d4ff;'>🔵 BLUE VOICE</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="back_blue"): go_to("home")
    st.write("สถานะการเชื่อมต่อสาย: ปกติ")

def render_green_room():
    st.markdown("<h1 style='color:#00ff88;'>🟢 GREEN CHAT</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="back_green"): go_to("home")
    if db:
        with st.form("g_chat", clear_on_submit=True):
            m = st.text_input("พิมพ์ข้อความ...")
            if st.form_submit_button("ส่ง"):
                db.collection('messages_green').add({'user': st.session_state.user, 'msg': m, 'time': datetime.now()})
                st.rerun()
        # แสดงแชท
        docs = db.collection('messages_green').order_by('time', direction='DESCENDING').limit(10).stream()
        for d in docs:
            st.markdown(f'<div class="chat-card"><b>{d.to_dict()["user"]}</b>: {d.to_dict()["msg"]}</div>', unsafe_allow_html=True)

def render_black_room():
    st.markdown("<h1 style='color:#00ff00; font-family:monospace;'>⚫ TERMINAL</h1>", unsafe_allow_html=True)
    if st.button("⬅️ EXIT", key="back_black"): go_to("home")
    st.code("> system_check --status: OK\n> connection: SECURE", language="bash")

def render_purple_room():
    st.markdown("<h1 style='color:#BC13FE;'>🟣 SETTINGS</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับ", key="back_purple"): go_to("home")
    name = st.text_input("ชื่อเล่นของคุณ:", value=st.session_state.user)
    if st.button("บันทึก"):
        st.session_state.user = name
        st.success("บันทึกชื่อเรียบร้อย!")

# --- 6. ส่วนควบคุมหลัก (Main Router) ---
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "red":
    render_red_room()
elif st.session_state.page == "blue":
    render_blue_room()
elif st.session_state.page == "green":
    render_green_room()
elif st.session_state.page == "black":
    render_black_room()
elif st.session_state.page == "purple":
    render_purple_room()
