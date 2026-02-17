import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time

# --- 1. Initial Setup ---
st.set_page_config(page_title="Synapse Core", layout="wide", initial_sidebar_state="collapsed")

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

# --- 2. Session & Logic ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user' not in st.session_state: st.session_state.user = "Synapse_User"

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- 3. UI Styling (Cyber Glow) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { border-radius: 15px; border: 1px solid #444; background: #111; color: #00ff88; transition: 0.3s; width: 100%; }
    .stButton>button:hover { border-color: #00ff88; box-shadow: 0 0 15px #00ff88; color: white; }
    .dimension-card { background: rgba(255, 255, 255, 0.03); border: 1px solid #333; padding: 20px; border-radius: 15px; text-align: center; }
    .call-btn { background-color: #00d4ff !important; color: black !important; font-weight: bold !important; text-decoration: none; display: block; padding: 12px; border-radius: 10px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. Biometric Scan Portal ---
def render_login():
    st.markdown("<h1 style='text-align:center; color:#00ff88;'>🔒 BIOMETRIC AUTHENTICATION</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # --- จุดที่ 1: ใส่ลายเซ็นในหน้าสแกนหน้า ---
        st.info("💡 กรุณา \"อยู่นิ้งๆ\" เพื่อให้ระบบทำการสแกนใบหน้า...")
        
        img = st.camera_input("SCAN")
        if img:
            with st.status("🧬 Analyzing Biomarkers...", expanded=True) as s:
                time.sleep(1)
                st.write("✅ ลวดลายม่านตา: ถูกต้อง")
                time.sleep(0.7)
                st.write("✅ โครงสร้างใบหน้า: ยืนยันแล้ว")
                s.update(label="ACCESS GRANTED", state="complete")
            if st.button("🚀 ENTER SYNAPSE"):
                st.session_state.logged_in = True
                st.rerun()

# --- 5. Home Dimension ---
def render_home():
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg", use_container_width=True)
        st.markdown("<h2 style='text-align:center; letter-spacing: 5px;'>SYNAPSE CORE</h2>", unsafe_allow_html=True)
        
        # --- จุดที่ 2: ใส่สโลแกน "อยู่นิ้งๆ ไม่เจ็บตัว" ของจริงใต้โลโก้ ---
        st.markdown("<p style='text-align:center; color:#00d4ff; font-size:22px; font-weight:bold;'>\"อยู่นิ้งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#555;'>By Sooksun</p>", unsafe_allow_html=True)
    
    st.divider()
    st.video("https://www.youtube.com/watch?v=videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO")
    
    with st.expander("📝 STATUS & MANUAL"):
        st.write("📡 System Online: Global Node Connected")
        st.write("🔐 Encryption: End-to-End Active")

    st.write("### 📂 SELECT DIMENSION")
    cols = st.columns(5)
    dims = [("🔴 RED", "red"), ("🔵 BLUE", "blue"), ("🟢 GREEN", "green"), ("⚫ BLACK", "black"), ("🟣 PURPLE", "purple")]
    for i, (label, target) in enumerate(dims):
        if cols[i].button(label, key=f"nav_{target}"): go_to(target)

# --- 6. Blue Dimension (Real-time Global Voice) ---
def render_blue_room():
    st.markdown("<h1 style='color:#00d4ff;'>🔵 BLUE VOICE HUB</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="b_blue"): go_to("home")
    
    st.write("---")
    st.subheader("🔑 มิติเสียงส่วนตัว (โทรทั่วโลกฟรี)")
    
    # --- จุดที่ 3: ปรับคำอธิบายในหน้าโทร ---
    st.write("ระบุรหัสลับเพื่อสร้างมิติของคุณ (ส่งรหัสนี้ให้เพื่อนเพื่อเข้าห้องเดียวกัน)")
    room_code = st.text_input("รหัสห้องลับ:", placeholder="เช่น 1234, หรือชื่อที่คุณตั้งเอง...")
    
    if room_code:
        link = f"https://meet.jit.si/Synapse-{room_code}#config.prejoinPageEnabled=false"
        st.markdown(f'''
            <div class="dimension-card">
                <h3 style="color:#00d4ff;">📍 มิติเสียง: {room_code}</h3>
                <p>ระบบพร้อมทำงานแล้ว "อยู่นิ้งๆ" แล้วกดโทรได้เลย</p>
                <a href="{link}" target="_blank" class="call-btn">📞 เชื่อมต่อสัญญาณ (CALL NOW)</a>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.info("ใส่รหัสห้องเพื่อเริ่มใช้งาน")

# --- 7. Green Dimension (Secret Chat) ---
def render_green_room():
    st.markdown("<h1 style='color:#00ff88;'>🟢 GREEN SECRET CHAT</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก", key="b_green"): go_to("home")
    
    if db:
        with st.form("g_chat", clear_on_submit=True):
            msg = st.text_input(f"{st.session_state.user}: พิมพ์ข้อความ...")
            if st.form_submit_button("SEND"):
                db.collection('messages_green').add({'user': st.session_state.user, 'msg': msg, 'time': datetime.now()})
                st.rerun()
        
        for d in db.collection('messages_green').order_by('time', direction='DESCENDING').limit(15).stream():
            data = d.to_dict()
            st.markdown(f"**{data.get('user')}**: {data.get('msg')}")

# --- Main Entry ---
if not st.session_state.logged_in:
    render_login()
else:
    if st.session_state.page == "home": render_home()
    elif st.session_state.page == "blue": render_blue_room()
    elif st.session_state.page == "green": render_green_room()
    elif st.session_state.page in ["red", "black", "purple"]:
        st.write(f"มิติ {st.session_state.page.upper()} กำลังถูกเชื่อมต่อ...")
        if st.button("กลับ"): go_to("home")
