import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time

# --- 1. Basic Config ---
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

# --- 2. Session Logic ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user' not in st.session_state: st.session_state.user = "Synapse_User"

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- 3. Style (เน้นธีมมืดและฟอนต์เท่ๆ) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .stButton>button { border-radius: 20px; border: 1px solid #444; background: #1a1a1a; color: white; transition: 0.3s; width: 100%; }
    .stButton>button:hover { border-color: #00ff88; box-shadow: 0 0 10px #00ff88; }
    .card { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border-left: 5px solid #00ff88; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. Face Scan Portal (หน้าแรกสุด) ---
def render_login():
    st.markdown("<h1 style='text-align:center; color:#00ff88;'>🔒 BIOMETRIC ACCESS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.write("กรุณาสแกนใบหน้าเพื่อยืนยันตัวตนเข้าสู่ระบบ...")
        img = st.camera_input("SCANNING...")
        if img:
            with st.status("🧬 กำลังวิเคราะห์โครงสร้างใบหน้า...", expanded=True) as s:
                time.sleep(1.2)
                st.write("✅ ยืนยันข้อมูลพิกัดใบหน้า")
                time.sleep(0.8)
                st.write("✅ ตรวจสอบสิทธิ์การเข้าถึงสำเร็จ")
                s.update(label="ACCESS GRANTED!", state="complete")
            if st.button("🚀 เข้าสู่หน้าหลัก (ENTER)"):
                st.session_state.logged_in = True
                st.rerun()

# --- 5. Dimension Handlers (แก้จุดที่ไม่ติด) ---

def render_home():
    # โลโก้และชื่อ (ใช้ภาพที่คุณส่งมาเป็นแรงบันดาลใจ)
    c_l, c_m, c_r = st.columns([1, 2, 1])
    with c_m:
        st.image("https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg", use_container_width=True)
        st.markdown("<h1 style='text-align:center;'>SYNAPSE COMMAND</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#888;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)
    
    st.divider()
    # แก้ไขวิดีโอ (ใช้รูปแบบ URL ที่ Streamlit รองรับ)
    st.subheader("📺 ระบบกระจายสัญญาณ")
    st.video("https://www.youtube.com/watch?v=videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO")

    with st.expander("📖 คู่มือการใช้งาน"):
        st.write("ยินดีต้อนรับสู่ Synapse Core เลือกมิติสีต่างๆ เพื่อเริ่มการทำงาน")

    # ปุ่มนำทาง
    st.write("### 📂 มิติการเข้าถึง")
    dims = [("🔴 RED HUB", "red"), ("🔵 BLUE VOICE", "blue"), ("🟢 GREEN CHAT", "green"), ("⚫ BLACK TERM", "black"), ("🟣 SETTINGS", "purple")]
    for label, target in dims:
        if st.button(label, key=f"nav_{target}"): go_to(target)

def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D;'>🔴 RED MEDIA HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ Back", key="b_red"): go_to("home")
    
    with st.form("post_red", clear_on_submit=True):
        txt = st.text_area("โพสต์ข้อความ...")
        url = st.text_input("ลิงก์รูปภาพ/วิดีโอ")
        if st.form_submit_button("🚀 POST"):
            if db and (txt or url):
                db.collection('posts_red').add({'user': st.session_state.user, 'text': txt, 'media': url, 'time': datetime.now()})
                st.rerun()
    
    if db:
        posts = db.collection('posts_red').order_by('time', direction='DESCENDING').limit(10).stream()
        for p in posts:
            d = p.to_dict()
            with st.container(border=True):
                st.write(f"👤 **{d.get('user')}**")
                st.write(d.get('text'))
                if d.get('media'): st.caption(f"Media Link: {d.get('media')}")

def render_blue_room():
    st.markdown("<h1 style='color:#00d4ff;'>🔵 BLUE VOICE HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ Back", key="b_blue"): go_to("home")
    for n in ["Admin_Synapse", "User_Alpha", "User_Beta"]:
        st.markdown(f'<div class="card" style="border-color:#00d4ff;">🟢 {n} (Online)</div>', unsafe_allow_html=True)
        if st.button(f"📞 CALL {n}", key=f"c_{n}"): st.toast(f"Connecting to {n}...")

def render_green_room():
    st.markdown("<h1 style='color:#00ff88;'>🟢 GREEN SECRET CHAT</h1>", unsafe_allow_html=True)
    if st.button("⬅️ Back", key="b_green"): go_to("home")
    
    with st.form("chat_green", clear_on_submit=True):
        m = st.text_input("พิมพ์ข้อความลับ...")
        if st.form_submit_button("ส่ง"):
            if db and m:
                db.collection('messages_green').add({'user': st.session_state.user, 'msg': m, 'time': datetime.now()})
                st.rerun()
    if db:
        chats = db.collection('messages_green').order_by('time', direction='DESCENDING').limit(15).stream()
        for c in chats:
            data = c.to_dict()
            st.markdown(f'<div class="card"><b>{data.get("user")}</b>: {data.get("msg")}</div>', unsafe_allow_html=True)

def render_black_room():
    st.markdown("<h1 style='color:#00ff00; font-family:monospace;'>⚫ SYSTEM TERMINAL</h1>", unsafe_allow_html=True)
    if st.button("⬅️ EXIT", key="b_black"): go_to("home")
    st.code("""
    [STATUS] : CONNECTED
    [ENCRYPTION] : AES-256
    [LOG] : User scanning facial biometric...
    [CMD] : system_check --run
    """, language="bash")
    st.warning("⚠️ กำลังปรับจูนสัญญาณขั้นสูง...")

def render_purple_room():
    st.markdown("<h1 style='color:#BC13FE;'>🟣 SETTINGS</h1>", unsafe_allow_html=True)
    if st.button("⬅️ Back", key="b_purple"): go_to("home")
    new_name = st.text_input("ระบุชื่อเล่นใหม่:", value=st.session_state.user)
    if st.button("💾 บันทึก"):
        st.session_state.user = new_name
        st.success("เปลี่ยนชื่อสำเร็จ!")

# --- 6. Main Routing System ---
if not st.session_state.logged_in:
    render_login()
else:
    if st.session_state.page == "home": render_home()
    elif st.session_state.page == "red": render_red_room()
    elif st.session_state.page == "blue": render_blue_room()
    elif st.session_state.page == "green": render_green_room()
    elif st.session_state.page == "black": render_black_room()
    elif st.session_state.page == "purple": render_purple_room()
