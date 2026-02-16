import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
import hashlib
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components

# --- 1. เชื่อมต่อ Firebase ---
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase_service_account"]))
    firebase_admin.initialize_app(cred, {'storageBucket': st.secrets["firebase_config"]["storageBucket"]})
db = firestore.client()
bucket = storage.bucket()

# --- 2. ฟังก์ชันเสริม ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_thai_time():
    return datetime.utcnow() + timedelta(hours=7)

# --- 3. ธีมสี (ปรับให้สว่างขึ้นนิดนึงเพื่อให้ดูออกว่าเป็นสีอะไร) ---
def set_luxury_theme(room_id):
    themes = {
        "home":  {"bg": "#001219", "text": "#FFD700", "accent": "#D4AF37"},
        "red":   {"bg": "#3d0000", "text": "#FFFFFF", "accent": "#FF4D4D"}, # แดงเข้มแต่ดูออก
        "blue":  {"bg": "#002147", "text": "#FFFFFF", "accent": "#00A8E8"}, # น้ำเงินเข้มชัดเจน
        "green": {"bg": "#0a2910", "text": "#FFFFFF", "accent": "#38B000"}, # เขียวเข้มสะอาดตา
        "black": {"bg": "#121212", "text": "#FFFFFF", "accent": "#E5E5E5"}  # ดำเท่ๆ
    }
    cfg = themes.get(room_id, themes["home"])
    st.markdown(f"""
        <style>
        .stApp {{ background: {cfg['bg']}; color: {cfg['text']}; }}
        h1, h2, h3, p, label {{ color: {cfg['text']} !important; }}
        .post-box {{
            border: 2px solid #D4AF37;
            background: rgba(255, 255, 255, 0.05);
            padding: 20px; border-radius: 15px; margin-bottom: 20px;
            color: white !important;
        }}
        .stButton>button {{
            background: {cfg['accent']}; color: black !important;
            font-weight: bold; border-radius: 12px; width: 100%;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. ฟังก์ชันลูกเล่นการโพสต์ (รูป/วิดีโอ/ไลค์/คอมเมนต์) ---
def render_social_logic(room_id):
    # ส่วนสร้างโพสต์
    with st.expander("📝 สร้างโพสต์ใหม่ (รูป/วิดีโอ)"):
        with st.form(f"form_{room_id}"):
            msg = st.text_area("เขียนข้อความ...")
            media = st.file_uploader("เลือกไฟล์รูปภาพหรือวิดีโอ", type=['png','jpg','jpeg','mp4'])
            if st.form_submit_button("แชร์โพสต์"):
                if msg or media:
                    m_url, m_type = None, None
                    if media:
                        path = f"{room_id}/{uuid.uuid4()}_{media.name}"
                        blob = bucket.blob(path)
                        blob.upload_from_string(media.getvalue(), content_type=media.type)
                        blob.make_public()
                        m_url = blob.public_url
                        m_type = 'video' if 'video' in media.type else 'image'
                    
                    db.collection(f'posts_{room_id}').add({
                        'user': st.session_state.user, 'text': msg,
                        'media_url': m_url, 'media_type': m_type,
                        'likes': [], 'timestamp': get_thai_time()
                    })
                    st.rerun()

    # ส่วนแสดงโพสต์
    posts = db.collection(f'posts_{room_id}').order_by('timestamp', direction='DESCENDING').stream()
    for doc in posts:
        p, pid = doc.to_dict(), doc.id
        st.markdown('<div class="post-box">', unsafe_allow_html=True)
        st.write(f"👤 **{p['user']}** | 🕒 {p['timestamp'].strftime('%H:%M')}")
        st.write(p['text'])
        if p.get('media_url'):
            if p['media_type'] == 'video': st.video(p['media_url'])
            else: st.image(p['media_url'])
        
        # Like & Comment
        col1, col2 = st.columns([1, 4])
        if col1.button(f"❤️ {len(p.get('likes', []))}", key=f"lk_{pid}"):
            ref = db.collection(f'posts_{room_id}').document(pid)
            if st.session_state.user in p.get('likes', []):
                ref.update({'likes': firestore.ArrayRemove([st.session_state.user])})
            else:
                ref.update({'likes': firestore.ArrayUnion([st.session_state.user])})
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. การจัดการหน้าจอหลัก ---
if 'user' not in st.session_state:
    set_luxury_theme("home")
    st.image("logo.jpg", width=200)
    st.title("🛡️ เข้าสู่ระบบ Synapse")
    u_name = st.text_input("Username")
    u_pass = st.text_input("Password", type="password")
    if st.button("Login"):
        user_ref = db.collection('users').document(u_name).get()
        if user_ref.exists and user_ref.to_dict().get('password') == hash_password(u_pass):
            st.session_state.user = u_name
            st.session_state.page = "home"
            st.rerun()
        else: st.error("ข้อมูลไม่ถูกต้อง")
else:
    if st.session_state.page == "home":
        set_luxury_theme("home")
        st.image("logo.jpg", width=150)
        st.title(f"สวัสดีคุณ {st.session_state.user}")
        
        # Playlist YouTube
        components.html('<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>', height=220)
        
        # Menu
        c1, c2 = st.columns(2)
        if c1.button("🔴 ห้อง YouTube"): st.session_state.page = "red"; st.rerun()
        if c2.button("🔵 ห้อง Facebook (โทรฟรี)"): st.session_state.page = "blue"; st.rerun()
        if c1.button("🟢 ห้องลับส่วนตัว"): st.session_state.page = "green"; st.rerun()
        if c2.button("⚫ ห้อง X เรียลไทม์"): st.session_state.page = "black"; st.rerun()
        if st.button("🚪 Logout"): del st.session_state.user; st.rerun()

    elif st.session_state.page == "red":
        set_luxury_theme("red")
        st.header("🔴 YouTube Room")
        if st.button("⬅️ Back"): st.session_state.page = "home"; st.rerun()
        render_social_logic("red")

    elif st.session_state.page == "blue":
        set_luxury_theme("blue")
        st.header("🔵 Facebook & Call")
        if st.button("⬅️ Back"): st.session_state.page = "home"; st.rerun()
        # ใส่ Logic โทรฟรี (PeerJS) ตรงนี้...
        render_social_logic("blue")

    elif st.session_state.page == "green":
        set_luxury_theme("green")
        st.header("🟢 Secret Chat")
        if st.button("⬅️ Back"): st.session_state.page = "home"; st.rerun()
        st.warning("ห้องนี้เป็นความลับเฉพาะบุคคล")
        render_social_logic("green")

    elif st.session_state.page == "black":
        set_luxury_theme("black")
        st.header("⚫ X Real-time")
        if st.button("⬅️ Back"): st.session_state.page = "home"; st.rerun()
        render_social_logic("black")
