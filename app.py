import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import time

# --- 1. SETUP & CONFIGURATION ---
def init_firebase():
    if not firebase_admin._apps:
        try:
            fb_creds = dict(st.secrets["firebase_credentials"])
            cred = credentials.Certificate(fb_creds)
            firebase_admin.initialize_app(cred, {
                'databaseURL': st.secrets["firebase_db_url"]
            })
        except Exception as e:
            st.error(f"Firebase Error: {e}")

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

# --- 2. CORE FUNCTIONS (Audio, Log, Chat) ---
def play_audio():
    link = "https://docs.google.com/uc?export=download&id=1AhClqXudsgLtFj7CofAUqPqfX8YW1T7a"
    st.components.v1.html(f"""
        <audio id="synapse-audio" loop autoplay style="display:none;"><source src="{link}" type="audio/mpeg"></audio>
        <script>
            var audio = document.getElementById("synapse-audio");
            window.parent.document.addEventListener('click', function() {{ audio.play(); }}, {{ once: true }});
        </script>
    """, height=0)

def save_log(action_details):
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

def private_chat_logic(my_name, target_name, p_msg=None):
    pair = sorted([my_name, target_name])
    room_id = f"priv_{pair[0]}_{pair[1]}"
    if p_msg:
        db.reference(f'private_rooms/{room_id}').push({
            'name': my_name, 'msg': p_msg, 'ts': time.time()
        })
    try:
        raw_p_msgs = db.reference(f'private_rooms/{room_id}').get()
        if raw_p_msgs:
            return sorted(raw_p_msgs.values(), key=lambda x: x.get('ts', 0))[-10:]
    except: pass
    return []

def draw_box(title, target_level):
    if st.button(title, use_container_width=True):
        st.session_state.nav_level = target_level
        save_log(f"NAVIGATED TO: {title}")
        st.rerun()

# --- 3. EXECUTION ---
init_firebase()
setup_ui()
play_audio()

if 'nav_level' not in st.session_state:
    st.session_state.nav_level = "HOME"

st.markdown('<div class="neon-header">ศูนย์บัญชาการไซแนปส์</div>', unsafe_allow_html=True)
main_tabs = st.tabs(["🚀 แกนหลัก", "🛰️ เรดาร์", "💬 การสื่อสาร", "📊 ประวัติ"])

# --- TAB: แกนหลัก ---
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
    if st.session_state.nav_level == "HOME":
        c1, c2 = st.columns(2)
        with c1: draw_box("กรอบที่ 1", "1")
        with c2: draw_box("กรอบที่ 2", "2")
    elif st.session_state.nav_level == "1":
        draw_box("เจาะลึก 1.1", "1.1")
    elif st.session_state.nav_level == "1.1":
        st.success("ACCESS GRANTED: LEVEL 1.1")

# --- TAB: การสื่อสาร ---
with main_tabs[2]:
    st.subheader("🛰️ PRIVATE COMMUNICATION")
    my_id, target_id = "Ta101", "System_Admin"
    chat_input = st.text_input("ระบุข้อความสัญญาณ...", key="chat_in")
    if st.button("SEND SIGNAL"):
        if chat_input:
            private_chat_logic(my_id, target_id, p_msg=chat_input)
            st.rerun()
    messages = private_chat_logic(my_id, target_id)
    for m in messages:
        color = "🟢" if m['name'] == my_id else "⚪"
        st.markdown(f"{color} **{m['name']}:** {m['msg']}")

# --- TAB: ประวัติ ---
with main_tabs[3]:
    st.markdown("### 📊 ประวัติกิจกรรม")
    today = datetime.now().strftime("%Y-%m-%d")
    logs = db.reference(f'synapse_logs/{today}').get()
    if logs:
        for log_id in reversed(list(logs.keys())):
            item = logs[log_id]
            st.code(f"[{item['time']}] {item['action']}")
