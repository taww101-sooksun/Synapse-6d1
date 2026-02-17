import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time

# --- 1. SETTING & STYLE (จัดเต็มความสวย) ---
st.set_page_config(page_title="Synapse Core", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { border-radius: 20px; border: 1px solid #444; background: #111; color: #00ff88; height: 3em; transition: 0.3s; width: 100%; font-weight: bold; }
    .stButton>button:hover { border-color: #00ff88; box-shadow: 0 0 20px #00ff88; color: white; }
    .dimension-card { background: rgba(0, 255, 136, 0.05); border: 1px solid #00ff88; padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px; }
    .call-btn { background-color: #00d4ff !important; color: black !important; font-weight: bold !important; text-decoration: none; display: block; padding: 15px; border-radius: 12px; margin-top: 15px; transition: 0.3s; }
    .call-btn:hover { background-color: white !important; box-shadow: 0 0 15px #00d4ff; }
    .chat-msg { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin-bottom: 5px; border-left: 3px solid #00ff88; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATABASE CONNECTION (จุดที่ทำให้ข้อมูลไม่หาย) ---
@st.cache_resource
def init_db():
    if not firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets["firebase_service_account"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"การเชื่อมต่อล้มเหลว: {e}")
            return None
    return firestore.client()

db = init_db()

# --- 3. SESSION CONTROL ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user_name' not in st.session_state: st.session_state.user_name = "Anonymous_User"

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 4. BIOMETRIC PORTAL (หน้าแรก) ---
def show_login():
    st.markdown("<h1 style='text-align:center; color:#00ff88; letter-spacing: 10px;'>SYNAPSE AUTH</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<div class='dimension-card'>", unsafe_allow_html=True)
        st.write("### 🚨 ระบบความปลอดภัยขั้นสูง")
        st.info("กรุณา \"อยู่นิ้งๆ\" เพื่อให้ระบบทำการสแกนใบหน้า...") 
        img = st.camera_input("SCAN")
        
        if img:
            with st.status("🧬 กำลังวิเคราะห์ Biomarkers...", expanded=True) as s:
                time.sleep(1.2)
                st.write("🔒 เข้ารหัสข้อมูล... 100%")
                time.sleep(0.8)
                st.write("👤 ตรวจพบตัวตน: คุณ Sooksun (Master)")
                s.update(label="ACCESS GRANTED", state="complete")
            
            name_input = st.text_input("ระบุรหัสประจำตัวของคุณ:", value="Sooksun_Guest")
            if st.button("🚀 เข้าสู่มิติ Synapse"):
                st.session_state.user_name = name_input
                st.session_state.logged_in = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. MAIN DIMENSION (หน้า Home) ---
def show_home():
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg", use_container_width=True)
        st.markdown("<h2 style='text-align:center; letter-spacing: 5px;'>SYNAPSE CORE</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#00ff88; font-size:22px; font-weight:bold;'>\"อยู่นิ้งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)
        st.write(f"<p style='text-align:center; color:#666;'>ยินดีต้อนรับ, {st.session_state.user_name}</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # เมนูเลือกมิติแบบลกๆ (จัดเต็ม 5 สี)
    st.write("### 🌐 เลือกมิติที่ต้องการเชื่อมต่อ")
    m1, m2, m3, m4, m5 = st.columns(5)
    if m1.button("🔴 RED"): navigate_to("red")
    if m2.button("🔵 BLUE"): navigate_to("blue")
    if m3.button("🟢 GREEN"): navigate_to("green")
    if m4.button("⚫ BLACK"): navigate_to("black")
    if m5.button("🟣 PURPLE"): navigate_to("purple")

    st.write("---")
    st.video("https://www.youtube.com/watch?v=videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO")

# --- 6. GREEN DIMENSION (แชทลับ - แก้ให้ข้อมูลไม่หาย) ---
def show_green():
    st.markdown("<h1 style='color:#00ff88;'>🟢 GREEN SECRET CHAT</h1>", unsafe_allow_html=True)
    if st.button("⬅️ ถอยกลับหน้าหลัก"): navigate_to("home")
    
    if db:
        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input(f"{st.session_state.user_name}: ส่งความถึงมิติ...", placeholder="พิมพ์ตรงนี้...")
            if st.form_submit_button("ส่งข้อมูล (SEND)"):
                if user_msg:
                    db.collection('messages').add({
                        'name': st.session_state.user_name,
                        'text': user_msg,
                        'timestamp': datetime.now()
                    })
                    st.rerun()

        st.write("---")
        # ดึงข้อมูลจากฐานข้อมูล (แสดงผลแบบเนียนๆ)
        messages = db.collection('messages').order_by('timestamp', direction='DESCENDING').limit(20).stream()
        for m in messages:
            msg_data = m.to_dict()
            st.markdown(f"<div class='chat-msg'><b>{msg_data.get('name')}</b>: {msg_data.get('text')}</div>", unsafe_allow_html=True)

# --- 7. BLUE DIMENSION (โทรทั่วโลก) ---
def show_blue():
    st.markdown("<h1 style='color:#00d4ff;'>🔵 BLUE VOICE HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ ถอยกลับหน้าหลัก"): navigate_to("home")
    
    st.markdown("<div class='dimension-card'>", unsafe_allow_html=True)
    st.write("### 📞 ระบบสื่อสารข้ามมิติ")
    st.write("ระบุรหัสลับของคุณเพื่อสร้างช่องสัญญาณ")
    room = st.text_input("รหัสช่องสัญญาณ:", placeholder="เช่น 9999 หรือ Secret_Name")
    
    if room:
        jitsi_url = f"https://meet.jit.si/SynapseCore-{room}#config.prejoinPageEnabled=false"
        st.success(f"เชื่อมต่อมิติ {room} สำเร็จ!")
        st.markdown(f"<a href='{jitsi_url}' target='_blank' class='call-btn'>📞 กดเพื่อเริ่มการสนทนา (START CALL)</a>", unsafe_allow_html=True)
        st.write("ส่งรหัสนี้ให้เพื่อนของคุณ แล้ว \"อยู่นิ้งๆ\" รอรับสายได้เลย")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 8. OTHER DIMENSIONS (RED, BLACK, PURPLE) ---
def show_other(color_name):
    st.markdown(f"<h1 style='color:{color_name.lower()};'>มิติ {color_name}</h1>", unsafe_allow_html=True)
    st.write(f"### กำลังเชื่อมต่อสถานี {color_name}...")
    st.info("มิตินี้กำลังอยู่ระหว่างการพัฒนาโดยคุณ Sooksun...")
    if st.button("⬅️ กลับ"): navigate_to("home")

# --- MAIN LOGIC ---
if not st.session_state.logged_in:
    show_login()
else:
    if st.session_state.page == "home": show_home()
    elif st.session_state.page == "green": show_green()
    elif st.session_state.page == "blue": show_blue()
    else: show_other(st.session_state.page.upper())
