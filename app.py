import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- 1. Setup ---
st.set_page_config(page_title="Synapse System", layout="wide")

# --- 2. Firebase Connection (Singleton) ---
@st.cache_resource
def get_db():
    if not firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets["firebase_service_account"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Error connecting to Firebase: {e}")
            return None
    return firestore.client()

db = get_db()

# --- 3. Session State Management ---
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'user' not in st.session_state:
    st.session_state.user = "Synapse_User"

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 4. CSS Center ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; transition: 0.3s; }
    .chat-card { background: rgba(0, 255, 136, 0.1); border-left: 5px solid #00ff88; padding: 10px; margin: 5px 0; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 5. Home Page ---
def render_home():
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        logo_url = "https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg"
        st.image(logo_url, use_container_width=True)
    
    st.divider()
    st.video("https://www.youtube.com/watch?v=videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO")
    
    st.subheader("🌐 เลือกมิติการเข้าถึง")
    cols = st.columns(5)
    labels = ["🔴 RED", "🔵 BLUE", "🟢 GREEN", "⚫ BLACK", "🟣 PURPLE"]
    targets = ["red", "blue", "green", "black", "purple"]
    
    for i in range(5):
        if cols[i].button(labels[i], key=f"nav_{targets[i]}"):
            go_to(targets[i])

# --- 6. Green Room (ฉบับแก้ "ไม่ติด") ---
def render_green_room():
    st.markdown("<h1 style='color:#00ff88; text-align:center;'>🟢 GREEN SECRET CHAT</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับศูนย์บัญชาการ", key="back_green"): go_to("home")
    
    st.info("🤐 ข้อความที่นี่จะถูกส่งเข้าสู่ฐานข้อมูล Synapse โดยตรง")

    if db:
        # ส่วนส่งข้อความ
        with st.container(border=True):
            with st.form("green_msg_form", clear_on_submit=True):
                msg_input = st.text_input("พิมพ์ข้อความลับ...", key="green_input")
                if st.form_submit_button("🚀 ส่งสัญญาณ"):
                    if msg_input:
                        db.collection('messages_green').add({
                            'user': st.session_state.user,
                            'msg': msg_input,
                            'time': datetime.now()
                        })
                        st.rerun()

        st.write("### 💬 บันทึกการสนทนา")
        try:
            docs = db.collection('messages_green').order_by('time', direction='DESCENDING').limit(15).stream()
            for doc in docs:
                data = doc.to_dict()
                st.markdown(f"""
                    <div class="chat-card">
                        <b style="color:#00ff88;">{data.get('user')}</b>: {data.get('msg')}
                    </div>
                """, unsafe_allow_html=True)
        except:
            st.caption("กำลังซิงค์ข้อมูลกับดาวเทียม...")

# --- 7. Black Room (Matrix / Hacker Mode) ---
def render_black_room():
    st.markdown("<h1 style='color:#00ff00; font-family:monospace; text-align:center;'>⚫ SYSTEM TERMINAL</h1>", unsafe_allow_html=True)
    if st.button("⬅️ EXIT TERMINAL", key="back_black"): go_to("home")
    
    st.code("""
    [STATUS] : CONNECTED
    [ENCRYPTION] : AES-256
    [LOG] : User connected to Synapse Core...
    [CMD] : Waiting for input_
    """, language="bash")
    
    st.warning("ห้องนี้ใช้สำหรับผู้ดูแลระบบเท่านั้น (Under Construction)")

# --- 8. Main Controller (หัวใจของการสลับหน้า) ---
if st.session_state.page == "home":
    render_home()
elif st.
