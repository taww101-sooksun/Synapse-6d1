import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time

# --- 1. ระบบจัดการเบื้องต้น ---
st.set_page_config(page_title="Synapse Core", layout="wide")

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

# --- 2. การจัดการสถานะ (Login & Navigation) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user' not in st.session_state: st.session_state.user = "Synapse_User"

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- 3. ตกแต่ง UI (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .stButton>button { border-radius: 25px; font-weight: bold; transition: 0.3s; }
    .scan-line { width: 100%; height: 3px; background-color: #00ff88; position: relative; animation: move 2s infinite; }
    @keyframes move { 0% { top: 0; } 100% { top: 300px; } }
    </style>
""", unsafe_allow_html=True)

# --- 4. หน้าแรก: ระบบสแกนใบหน้า (Face Scan Portal) ---
def render_login():
    st.markdown("<h1 style='text-align:center; color:#00ff88;'>🔒 BIOMETRIC SCAN</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # จำลองเส้นสแกนวิ่งผ่านกล้อง
        st.markdown('<div class="scan-line"></div>', unsafe_allow_html=True)
        img = st.camera_input("สแกนใบหน้าเพื่อเข้าสู่มิติ Synapse")
        
        if img:
            with st.status("🧬 กำลังวิเคราะห์ข้อมูลชีวภาพ...", expanded=True) as status:
                time.sleep(1.5)
                st.write("✅ ตรวจสอบโครงสร้างใบหน้าสำเร็จ")
                time.sleep(1)
                st.write("✅ ยืนยันพิกัดตำแหน่งดวงตา")
                status.update(label="ยืนยันตัวตนสำเร็จ!", state="complete")
            
            st.success(f"ยินดีต้อนรับคุณ {st.session_state.user}")
            if st.button("🚀 เข้าสู่ระบบ (ACCESS GRANTED)", use_container_width=True):
                st.session_state.logged_in = True
                st.rerun()

# --- 5. มิติต่างๆ (Dimensions) ---

def render_home():
    # Logo & Playlist
    c_l, c_m, c_r = st.columns([1, 2, 1])
    with c_m:
        st.image("https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg", use_container_width=True)
        st.markdown("<h2 style='text-align:center;'>SYNAPSE COMMAND CENTER</h2>", unsafe_allow_html=True)
        st.caption("<p style='text-align:center;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)
    
    st.divider()
    st.video("https://www.youtube.com/watch?v=videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO")
    
    # คำบรรยาย
    with st.expander("📖 วิธีใช้งานระบบ"):
        st.write("กดเลือกมิติด้านล่างเพื่อเข้าถึงฟังก์ชันต่างๆ ของระบบ Synapse Core")

    # ปุ่มนำทาง (แยก Key ชัดเจนกันไม่ติด)
    st.write("### 🌐 เลือกมิติ")
    c = st.columns(5)
    if c[0].button("🔴 RED", key="btn_red_home", use_container_width=True): go_to("red")
    if c[1].button("🔵 BLUE", key="btn_blue_home", use_container_width=True): go_to("blue")
    if c[2].button("🟢 GREEN", key="btn_green_home", use_container_width=True): go_to("green")
    if c[3].button("⚫ BLACK", key="btn_black_home", use_container_width=True): go_to("black")
    if c[4].button("🟣 PURPLE", key="btn_purple_home", use_container_width=True): go_to("purple")

def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D;'>🔴 RED MEDIA HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="back_from_red"): go_to("home")
    
    with st.form("form_red", clear_on_submit=True):
        msg = st.text_area("โพสต์ข้อความ...")
        media = st.text_input("ลิงก์รูป/วิดีโอ")
        if st.form_submit_button("POST"):
            if db and (msg or media):
                db.collection('posts_red').add({'user': st.session_state.user, 'text': msg, 'media': media, 'time': datetime.now()})
                st.rerun()
    
    if db:
        posts = db.collection('posts_red').order_by('time', direction='DESCENDING').limit(5).stream()
        for p in posts:
            data = p.to_dict()
            with st.container(border=True):
                st.write(f"👤 **{data.get('user')}**")
                st.write(data.get('text'))

def render_blue_room():
    st.markdown("<h1 style='color:#00d4ff;'>🔵 BLUE VOICE HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="back_from_blue"): go_to("home")
    
    names = ["System Admin", "User_01", "Member_X"]
    for n in names:
        col_name, col_btn = st.columns([3, 1])
        col_name.info(f"🟢 {n}")
        if col_btn.button("📞 CALL", key=f"call_btn_{n}"): # ใส่ key เฉพาะตัว
            st.toast(f"กำลังเชื่อมต่อกับ {n}...")

# --- 6. Main Controller ---
if not st.session_state.logged_in:
    render_login()
else:
    if st.session_state.page == "home": render_home()
    elif st.session_state.page == "red": render_red_room()
    elif st.session_state.page == "blue": render_blue_room()
    elif st.session_state.page == "green": 
        # เรียกฟังก์ชัน Green Room เดิมของคุณ
        st.markdown("🟢 GREEN CHAT")
        if st.button("Back", key="bg"): go_to("home")
    elif st.session_state.page == "black": 
        st.markdown("⚫ SYSTEM TERMINAL")
        if st.button("Back", key="bb"): go_to("home")
    elif st.session_state.page == "purple": 
        st.markdown("🟣 SETTINGS")
        if st.button("Back", key="bp"): go_to("home")
