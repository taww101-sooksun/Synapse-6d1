import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# --- 1. INITIALIZE FIREBASE (ส่วนเชื่อมต่อฐานข้อมูล) ---
def init_firebase():
    if not firebase_admin._apps:
        try:
            # ดึงข้อมูลจาก Secrets ที่คุณตั้งค่าไว้ใน Streamlit Cloud
            fb_creds = dict(st.secrets["firebase_credentials"])
            cred = credentials.Certificate(fb_creds)
            firebase_admin.initialize_app(cred, {
                'databaseURL': st.secrets["firebase_db_url"]
            })
        except Exception as e:
            st.error(f"⚠️ Firebase Connection Error: {e}")

# --- 2. LOGGING SYSTEM (ฟังก์ชันบันทึกประวัติ) ---
def save_log(action_details):
    try:
        now = datetime.now()
        date_key = now.strftime("%Y-%m-%d")
        time_stamp = now.strftime("%H:%M:%S")
        
        # บันทึกลง Path: synapse_logs/วันที่/รายการ
        ref = db.reference(f'synapse_logs/{date_key}')
        ref.push({
            'time': time_stamp,
            'action': action_details,
            'user': 'Ta101'
        })
    except:
        pass # ป้องกันแอปค้างถ้าเน็ตหลุด

# --- 3. UI & NAVIGATION (ส่วนจัดการหน้าตา) ---
def setup_ui():
    st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle, #001 0%, #000 100%); color: #00f2fe; }
        .neon-header { 
            font-size: 40px; font-weight: 900; text-align: center;
            color: #fff; text-shadow: 0 0 15px #ff1744, 0 0 20px #00f2fe;
            border: 10px double #ff1744; padding: 20px; border-radius: 20px;
            margin-bottom: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

def draw_box(title, target_level):
    if st.button(title, use_container_width=True):
        st.session_state.nav_level = target_level
        # บันทึกประวัติการกดลง Firebase ทันที
        save_log(f"NAVIGATED TO: {title} ({target_level})")
        st.rerun()

# --- 4. EXECUTION (เริ่มรันระบบ) ---
init_firebase()
setup_ui()

# ตรวจสอบสถานะหน้าปัจจุบัน
if 'nav_level' not in st.session_state:
    st.session_state.nav_level = "HOME"

# แสดงส่วนหัว
st.markdown('<div class="neon-header">SYNAPSE COMMAND CENTER</div>', unsafe_allow_html=True)

# สร้าง Tabs
main_tabs = st.tabs(["🚀 CORE", "🛰️ RADAR", "💬 COMMS", "📊 LOG", "🔐 SEC", "📺 MEDIA", "🧹 SYS"])

# --- Tab 4: LOG (แสดงประวัติการใช้งาน) ---
with main_tabs[3]:
    st.subheader("📊 ACTIVITY HISTORY")
    today = datetime.now().strftime("%Y-%m-%d")
    logs_ref = db.reference(f'synapse_logs/{today}')
    logs = logs_ref.get()

    if logs:
        for log_id in reversed(list(logs.keys())):
            item = logs[log_id]
            st.code(f"[{item['time']}] {item['action']}")
    else:
        st.info("No activity recorded for today.")

# --- Tab 1: CORE (ระบบ Hierarchy เดิมของคุณ) ---
with main_tabs[0]:
    # ปุ่มย้อนกลับ
    if st.session_state.nav_level != "HOME":
        if st.button("⬅️ BACK"):
            if "." in st.session_state.nav_level:
                st.session_state.nav_level = ".".join(st.session_state.nav_level.split(".")[:-1])
            else:
                st.session_state.nav_level = "HOME"
            save_log(f"BACK TO: {st.session_state.nav_level}")
            st.rerun()

    st.write(f"CURRENT PATH: **{st.session_state.nav_level}**")
    st.markdown("---")

    # Navigation Logic (ยกมาจากที่คุณเขียน)
    if st.session_state.nav_level == "HOME":
        c1, c2 = st.columns(2)
        with c1: draw_box("กรอบที่ 1", "1")
        with c2: draw_box("กรอบที่ 2", "2")
    
    elif st.session_state.nav_level == "1":
        c1, c2 = st.columns(2)
        with c1: draw_box("กรอบที่ 1.1", "1.1")
        with c2: draw_box("กรอบที่ 1.2", "1.2")

    elif st.session_state.nav_level == "1.1":
        st.success("Welcome to Deep Core 1.1")
        draw_box("เจาะลึก 1.1.1", "1.1.1")

    else:
        st.warning(f"System {st.session_state.nav_level} is under construction...")

