import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime, timedelta
import uuid

# --- 1. เชื่อมต่อ Firebase (เหมือนเดิม) ---
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase_service_account"]))
    firebase_admin.initialize_app(cred, {'storageBucket': st.secrets["firebase_config"]["storageBucket"]})
db = firestore.client()
bucket = storage.bucket()

# --- 2. ธีมหน้าจอ: เข้มมาก (Deep Dark Mode) ---
def set_room_theme(room_id):
    themes = {
        "home":  {"bg": "linear-gradient(180deg, #000814, #001d3d, #003566)", "text": "#FFD60A", "accent": "#FFD60A"},
        "red":   {"bg": "#4a0000", "text": "#ffffff", "accent": "#ff0000"},
        "blue":  {"bg": "#001233", "text": "#ffffff", "accent": "#0077b6"},
        "green": {"bg": "#0b190e", "text": "#ffffff", "accent": "#2dc653"},
        "black": {"bg": "#000000", "text": "#ffffff", "accent": "#333333"}
    }
    cfg = themes.get(room_id, themes["home"])
    st.markdown(f"""
        <style>
        .stApp {{ background: {cfg['bg']}; color: {cfg['text']}; }}
        h1, h2, h3, p, label {{ color: {cfg['text']} !important; text-shadow: 2px 2px 4px #000000; }}
        .stButton>button {{ background-color: {cfg['accent']}; color: black !important; border-radius: 10px; font-weight: bold; }}
        /* แก้ปัญหาตัวหนังสือในโพสต์จม */
        .stMarkdown {{ background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px; }}
        </style>
    """, unsafe_allow_html=True)

# --- 3. ฟังก์ชันโพสต์ (ดึงกลับมาให้ใช้งานได้จริง) ---
def render_social_room(room_id, room_name):
    set_room_theme(room_id)
    st.title(f"🚀 {room_name} Room")
    
    with st.expander("➕ สร้างโพสต์ใหม่"):
        with st.form(f"form_{room_id}"):
            msg = st.text_area("เขียนอะไรซักหน่อย...")
            if st.form_submit_button("ส่งโพสต์"):
                db.collection(f'posts_{room_id}').add({
                    'user': st.session_state.user, 'text': msg, 
                    'timestamp': datetime.utcnow() + timedelta(hours=7)
                })
                st.rerun()

    # ดึงข้อมูลมาโชว์ (ไม่งั้นหน้าจอจะโล่ง)
    for doc in db.collection(f'posts_{room_id}').order_by('timestamp', direction='DESCENDING').limit(20).stream():
        p = doc.to_dict()
        st.info(f"👤 {p['user']} : {p['text']}")

# --- 4. หน้าหลัก 5 สี (ฉบับเข้มขลัง) ---
if 'user' not in st.session_state:
    set_room_theme("home")
    st.image("logo.jpg") #
    st.title("Firebase Social 2026")
    u_input = st.text_input("ชื่อของคุณ")
    if st.button("เข้าสู่ระบบ"):
        st.session_state.user = u_input
        st.rerun()
else:
    with st.sidebar:
        menu = st.radio("ไปที่หน้า...", ["หน้าหลัก", "YouTube (Red)", "Facebook (Blue)", "Line (Green)", "X (Black)"])

    if menu == "หน้าหลัก":
        set_room_theme("home")
        st.image("logo.jpg", use_container_width=True) #
        st.title("ยินดีต้อนรับสู่ Synapse")
        
        # เพลย์ลิสต์ YouTube
        st.subheader("🎵 ฟังเพลงไป แชทไป")
        st.video("https://youtube.com/playlist?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO&si=BGiqmOiqhccE7538")
        
        st.markdown("---")
        # คำบรรยายแต่ละห้อง
        st.subheader("📂 รายละเอียดห้องต่างๆ")
        cols = st.columns(2)
        with cols[0]:
            st.markdown("🔴 **YouTube:** ดูคลิปแชร์ไอดี")
            st.markdown("🔵 **Facebook:** โทรฟรี Peer-to-Peer") #
        with cols[1]:
            st.markdown("🟢 **Line:** ส่งรูป ส่งใจ")
            st.markdown("⚫ **X:** ข่าวไว ทันเหตุการณ์")
    else:
        mapping = {"YouTube (Red)": ("red", "YouTube"), "Facebook (Blue)": ("blue", "Facebook"), 
                   "Line (Green)": ("green", "Line"), "X (Black)": ("black", "X")}
        render_social_room(*mapping[menu])
