import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time

# --- 1. System Config ---
st.set_page_config(page_title="Synapse Core", layout="wide")

# --- 2. Firebase Connection (Safe & Fast) ---
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

# --- 3. Session Management ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user' not in st.session_state: st.session_state.user = "Synapse_User"

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- 4. Global Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .stButton>button { border-radius: 25px; transition: 0.3s; height: 3em; }
    .chat-bubble { background: rgba(0, 255, 136, 0.1); border-left: 4px solid #00ff88; padding: 10px; margin-bottom: 8px; border-radius: 5px; }
    .blue-card { background: rgba(0, 212, 255, 0.1); border-radius: 15px; padding: 20px; margin-bottom: 10px; border: 1px solid #00d4ff; }
    </style>
""", unsafe_allow_html=True)

# --- 5. Dimension Handlers ---

def render_home():
    st.markdown("<h1 style='text-align:center;'>Synapse Home</h1>", unsafe_allow_html=True)
    st.divider()
    # ปรับปุ่มให้เป็นแถวเดียวเท่ๆ ตามรูปของคุณ
    dims = [("🔴", "red"), ("🔵", "blue"), ("🟢", "green"), ("⚫", "black"), ("🟣", "purple")]
    for icon, target in dims:
        if st.button(f"{icon} เข้าสู่มิติ {target.upper()}", key=f"nav_{target}", use_container_width=True):
            go_to(target)

def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D;'>🔴 RED MEDIA HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="b_red"): go_to("home")
    with st.expander("📝 สร้างโพสต์ใหม่"):
        with st.form("red_form", clear_on_submit=True):
            m = st.text_area("ข้อความ")
            u = st.text_input("ลิงก์สื่อ")
            if st.form_submit_button("🚀 POST"):
                if db and (m or u):
                    db.collection('posts_red').add({'user': st.session_state.user, 'text': m, 'media': u, 'time': datetime.now()})
                    st.rerun()
    if db:
        for d in db.collection('posts_red').order_by('time', direction='DESCENDING').limit(10).stream():
            p = d.to_dict()
            with st.container(border=True):
                st.write(f"👤 **{p.get('user')}**")
                st.write(p.get('text'))
                if p.get('media'): st.caption(f"Media Attached: {p.get('media')}")

def render_blue_room():
    st.markdown("<h1 style='color:#00d4ff;'>🔵 BLUE VOICE HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="b_blue"): go_to("home")
    for name in ["System Admin", "User_01", "Member_X"]:
        st.markdown(f'<div class="blue-card">🟢 {name}</div>', unsafe_allow_html=True)
        if st.button(f"📞 CALL {name}", key=f"c_{name}"):
            st.toast(f"Connecting to {name}...")

def render_green_room():
    st.markdown("<h1 style='color:#00ff88;'>🟢 GREEN SECRET CHAT</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="b_green"): go_to("home")
    st.info(f"คุณกำลังคุยในชื่อ: **{st.session_state.user}** (เปลี่ยนได้ที่มิติสีม่วง)")
    with st.form("g_form", clear_on_submit=True):
        msg = st.text_input("พิมพ์ข้อความลับ...")
        if st.form_submit_button("ส่ง"):
            if db and msg:
                db.collection('messages_green').add({'user': st.session_state.user, 'msg': msg, 'time': datetime.now()})
                st.rerun()
    if db:
        for d in db.collection('messages_green').order_by('time', direction='DESCENDING').limit(15).stream():
            c = d.to_dict()
            st.markdown(f'<div class="chat-bubble"><b>{c.get("user")}</b>: {c.get("msg")}</div>', unsafe_allow_html=True)

def render_black_room():
    st.markdown("<h1 style='color:#00ff00; font-family:monospace;'>⚫ SYSTEM TERMINAL</h1>", unsafe_allow_html=True)
    if st.button("⬅️ EXIT TERMINAL", key="b_black"): go_to("home")
    st.code(f"[USER]: {st.session_state.user}\n[STATUS]: ONLINE\n[LOG]: Accessing core...", language="bash")
    st.write("มิตินี้ใช้สำหรับตรวจสอบการทำงานของระบบ")

def render_purple_room():
    st.markdown("<h1 style='color:#BC13FE;'>🟣 PURPLE SETTINGS</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="b_purple"): go_to("home")
    st.subheader("👤 ตั้งค่าตัวตนของคุณ")
    new_name = st.text_input("ระบุชื่อเล่นใหม่:", value=st.session_state.user)
    if st.button("💾 บันทึกชื่อเล่น"):
        st.session_state.user = new_name
        st.success(f"เปลี่ยนชื่อเป็น {new_name} เรียบร้อย!")
        time.sleep(1)
        go_to("home")

# --- 6. Main Router ---
if st.session_state.page == "home": render_home()
elif st.session_state.page == "red": render_red_room()
elif st.session_state.page == "blue": render_blue_room()
elif st.session_state.page == "green": render_green_room()
elif st.session_state.page == "black": render_black_room()
elif st.session_state.page == "purple": render_purple_room()
