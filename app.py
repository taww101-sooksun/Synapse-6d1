import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time

# --- 1. Init & Config ---
st.set_page_config(page_title="Synapse Core", layout="wide", initial_sidebar_state="collapsed")

@st.cache_resource
def init_db():
    if not firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets["firebase_service_account"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except: return None
    return firestore.client()

db = init_db()

# --- 2. Styling (Neon Theme) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'JetBrains Mono', monospace; }
    .stButton>button { border-radius: 20px; border: 1px solid #444; background: #111; color: white; transition: 0.3s; }
    .stButton>button:hover { border-color: #FFD700; box-shadow: 0 0 10px #FFD700; }
    .chat-bubble { background: rgba(0, 255, 136, 0.05); border: 1px solid #00ff88; padding: 12px; border-radius: 10px; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. Navigation Logic ---
if 'page' not in st.session_state: st.session_state.page = "home"
def go_to(p): 
    st.session_state.page = p
    st.rerun()

# --- 4. มิติสีม่วง (PURPLE - มิติแห่งอนาคต) ---
def render_purple_room():
    st.markdown("<h1 style='color:#BC13FE; text-align:center;'>🟣 PURPLE DIMENSION</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="back_p"): go_to("home")
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔮 Synapse AI Prediction")
        st.write("ระบบกำลังคำนวณคลื่นความถี่ทางอารมณ์ของคุณ...")
        st.progress(75)
        st.caption("ความพร้อมในการเข้าสู่สภาวะสงบ: 75%")
    with col2:
        st.subheader("🌌 มิติคู่ขนาน")
        st.warning("มิตินี้ใช้สำหรับรับฟังเสียงจากอนาคต (Coming Soon)")

# --- 5. ปรับปรุงหน้า Black (Hacker Style) ---
def render_black_room():
    st.markdown("<h1 style='color:#00ff00; text-align:center; font-family:monospace;'>[ SYSTEM TERMINAL ]</h1>", unsafe_allow_html=True)
    if st.button("⬅️ EXIT_SESSION", key="back_b"): go_to("home")
    
    # เอฟเฟกต์ Terminal
    terminal_box = st.empty()
    logs = [
        "> Initializing Synapse Protocol...",
        "> Bypassing Firewall...",
        "> Connection Secure: AES-256 Enabled",
        "> Scanning dimension stability...",
        "> Ready for Command."
    ]
    current_log = ""
    for line in logs:
        current_log += line + "\n"
        terminal_box.code(current_log, language="bash")
        time.sleep(0.1)

    st.text_input("ENTER COMMAND:", placeholder="system_override --force")

# --- 6. Main Controller ---
if st.session_state.page == "home":
    # หน้าหลักเดิมของคุณ (ที่โชว์โลโก้และวิดีโอ)
    # ก๊อปปี้ render_home() เดิมมาวางตรงนี้ได้เลยครับ
    st.title("Synapse Home")
    cols = st.columns(5)
    p = ["red", "blue", "green", "black", "purple"]
    l = ["🔴", "🔵", "🟢", "⚫", "🟣"]
    for i in range(5):
        if cols[i].button(l[i], key=f"btn_{p[i]}", use_container_width=True): go_to(p[i])

elif st.session_state.page == "red": render_red_room() # ใช้ฟังก์ชันเดิมที่คุณมี
elif st.session_state.page == "blue": render_blue_room() # ใช้ฟังก์ชันเดิมที่คุณมี
elif st.session_state.page == "green": render_green_room() # ใช้ฟังก์ชันเดิมที่คุณมี
elif st.session_state.page == "black": render_black_room()
elif st.session_state.page == "purple": render_purple_room()
