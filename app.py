import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# --- ส่วนที่ 1: การตั้งค่าระบบ (Setup & Firebase) ---
def init_firebase():
    if not firebase_admin._apps:
        try:
            fb_creds = dict(st.secrets["firebase_credentials"])
            cred = credentials.Certificate(fb_creds)
            firebase_admin.initialize_app(cred, {
                'databaseURL': st.secrets["firebase_db_url"]
            })
        except Exception as e:
            st.error(f"Error: {e}")

def save_log(action_details):
    """ฟังก์ชันส่งข้อมูลไปเก็บที่ Firebase"""
    try:
        now = datetime.now()
        date_key = now.strftime("%Y-%m-%d")
        ref = db.reference(f'synapse_logs/{date_key}')
        ref.push({
            'time': now.strftime("%H:%M:%S"),
            'action': action_details,
            'user': 'Ta101'
        })
    except: pass

# --- ส่วนที่ 2: ฟังก์ชันวาดหน้าตา (UI Components) ---
def setup_ui():
    st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle, #001 0%, #000 100%); color: #00f2fe; }
        .neon-header { 
            font-size: 38px; font-weight: 900; text-align: center;
            color: #fff; text-shadow: 0 0 15px #ff1744, 0 0 20px #00f2fe;
            border: 5px double #ff1744; padding: 15px; border-radius: 15px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def draw_box(title, target_level):
    if st.button(title, use_container_width=True):
        st.session_state.nav_level = target_level
        save_log(f"NAVIGATED TO: {title}") # บันทึก Log ทุกครั้งที่กดปุ่ม
        st.rerun()

# --- ส่วนที่ 3: การรันระบบ (Execution) ---
init_firebase()
setup_ui()

if 'nav_level' not in st.session_state:
    st.session_state.nav_level = "HOME"

st.markdown('<div class="neon-header">ศูนย์บัญชาการไซแนปส์</div>', unsafe_allow_html=True)

# สร้างเมนู Tabs ตามรูปของคุณ
main_tabs = st.tabs(["🚀 แกนหลัก", "🛰️ เรดาร์", "💬 การสื่อสาร", "📊 ประวัติ"])

# --- ส่วนที่ 4: เนื้อหาในแต่ละ Tab ---

# [TAB: ประวัติกิจกรรม]
with main_tabs[3]:
    st.markdown("### 📊 ประวัติกิจกรรม")
    today = datetime.now().strftime("%Y-%m-%d")
    logs = db.reference(f'synapse_logs/{today}').get()
    if logs:
        for log_id in reversed(list(logs.keys())):
            item = logs[log_id]
            # แสดงผลเป็นกล่อง Code แบบในรูปที่คุณส่งมา
            st.code(f"[{item['time']}] {item['action']}")
    else:
        st.info("ยังไม่มีบันทึกสำหรับวันนี้")

# [TAB: แกนหลัก (Hierarchy)]
with main_tabs[0]:
    if st.session_state.nav_level != "HOME":
        if st.button("⬅️ BACK"):
            if "." in st.session_state.nav_level:
                st.session_state.nav_level = ".".join(st.session_state.nav_level.split(".")[:-1])
            else:
                st.session_state.nav_level = "HOME"
            save_log(f"BACK TO: {st.session_state.nav_level}")
            st.rerun()

    st.write(f"เส้นทางปัจจุบัน: **{st.session_state.nav_level}**")
    
    # Logic การคุมชั้น (Hierarchy)
    if st.session_state.nav_level == "HOME":
        c1, c2 = st.columns(2)
        with c1: draw_box("กรอบที่ 1", "1")
        with c2: draw_box("กรอบที่ 2", "2")
    elif st.session_state.nav_level == "1":
        draw_box("เจาะลึก 1.1", "1.1")
    # ... เพิ่มเงื่อนไขอื่นๆ ต่อได้ที่นี่ ...
