import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
import hashlib
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components
import re

# --- 1. การตั้งค่าหน้าจอเบื้องต้น ---
st.set_page_config(page_title="Synapse Luxury App", layout="wide")

# --- 2. เชื่อมต่อ Firebase (ใช้ st.secrets) ---
if not firebase_admin._apps:
    try:
        cred_dict = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'storageBucket': st.secrets["firebase_config"]["storageBucket"]
        })
    except Exception as e:
        st.error(f"❌ เชื่อมต่อ Firebase ไม่สำเร็จ: {e}")
        st.stop()

db = firestore.client()
bucket = storage.bucket()

# --- 3. ฟังก์ชันเสริม (Helper Functions) ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_thai_time():
    return datetime.utcnow() + timedelta(hours=7)

def get_youtube_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- 4. ระบบธีม (Luxury Theme) ---
def set_luxury_theme(room_type):
    themes = {
        "home":  {"bg": "#001219", "text": "#FFD700", "accent": "#D4AF37"},
        "red":   {"bg": "#3d0000", "text": "#FFFFFF", "accent": "#FF4D4D"},
        "blue":  {"bg": "#002147", "text": "#FFFFFF", "accent": "#00A8E8"},
        "green": {"bg": "#0a2910", "text": "#FFFFFF", "accent": "#38B000"},
        "black": {"bg": "#121212", "text": "#FFFFFF", "accent": "#E5E5E5"}
    }
    cfg = themes.get(room_type, themes["home"])
    st.markdown(f"""
        <style>
        .stApp {{ background: {cfg['bg']}; color: {cfg['text']}; }}
        .post-box {{
            border: 1px solid {cfg['accent']};
            background: rgba(255, 255, 255, 0.05);
            padding: 15px; border-radius: 12px; margin-bottom: 10px;
        }}
        .stButton>button {{
            background: {cfg['accent']}; color: black !important;
            font-weight: bold; border-radius: 8px; width: 100%;
            transition: 0.3s;
        }}
        .stButton>button:hover {{ transform: scale(1.02); }}
        </style>
    """, unsafe_allow_html=True)

# --- 5. ระบบแสดงโพสต์ ---
def render_posts(room_id):
    try:
        posts_ref = db.collection(f'posts_{room_id}').order_by('time', direction='DESCENDING').limit(15)
        docs = posts_ref.stream()
        for doc in docs:
            p = doc.to_dict()
            pid = doc.id
            st.markdown(f'''<div class="post-box">
                <b>👤 {p.get("user")}</b> | <small>{p.get("time").strftime("%H:%M") if p.get("time") else ""}</small><br>
                {p.get("text", "")}
            </div>''', unsafe_allow_html=True)
            
            if p.get('type') == 'youtube': st.video(p['media'])
            elif p.get('media'):
                if p.get('type') == 'video': st.video(p['media'])
                else: st.image(p['media'])
    except:
        st.info("เริ่มโพสต์คนแรกของห้องนี้เลย!")

# --- 6. ระบบ Logic หลัก ---

# ตรวจสอบ Session State
if 'user' not in st.session_state:
    # --- หน้า Login ---
    set_luxury_theme("home")
    st.title("🛡️ Synapse Security Login")
    with st.container():
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        c1, c2 = st.columns(2)
        if c1.button("เข้าสู่ระบบ"):
            user_doc = db.collection('users').document(u).get()
            if user_doc.exists and user_doc.to_dict().get('pw') == hash_password(p):
                st.session_state.user = u
                st.session_state.page = "home"
                st.rerun()
            else: st.error("❌ ข้อมูลไม่ถูกต้อง")
        if c2.button("ลงทะเบียน"):
            if u and p:
                db.collection('users').document(u).set({'pw': hash_password(p)})
                st.success("✅ สมัครแล้ว กดเข้าสู่ระบบได้เลย")
else:
    # --- หน้าหลักและห้องต่างๆ ---
    page = st.session_state.get('page', 'home')
    set_luxury_theme(page)

    if page == "home":
        st.title(f"ยินดีต้อนรับคุณ {st.session_state.user}")
        st.markdown("### 📂 เลือกพื้นที่การใช้งาน")
        col1, col2 = st.columns(2)
        if col1.button("🔴 YouTube Zone"): st.session_state.page = "red"; st.rerun()
        if col2.button("🔵 Blue (โทรฟรี)"): st.session_state.page = "blue"; st.rerun()
        if col1.button("🟢 ห้องแชทลับ"): st.session_state.page = "green"; st.rerun()
        if col2.button("⚫ ห้อง X Realtime"): st.session_state.page = "black"; st.rerun()
        if st.sidebar.button("🚪 Log out"): del st.session_state.user; st.rerun()

    else:
        # ส่วนของหน้าห้องย่อย
        st.header(f"ห้อง {page.upper()}")
        if st.button("⬅️ กลับหน้าหลัก"): st.session_state.page = "home"; st.rerun()

        # ฟีเจอร์พิเศษ: โทรฟรี (เฉพาะห้อง Blue)
        if page == "blue":
            st.info("📞 ระบบโทรฟรีผ่าน WebRTC (PeerJS)")
            u_ref = db.collection('users').limit(10).stream()
            friends = [u.id for u in u_ref if u.id != st.session_state.user]
            target = st.selectbox("เลือกเพื่อน:", [""] + friends)
            
            html_call = f"""
            <div style="background:#002147; padding:15px; border-radius:10px; border:1px solid #00A8E8; color:white;">
                <p id="status">🔵 พร้อมใช้งานในชื่อ: {st.session_state.user}</p>
                <button id="callBtn" style="width:100%; padding:10px; background:#28a745; color:white; border:none; border-radius:5px; cursor:pointer;">🟢 กดเพื่อโทรออก</button>
                <audio id="remoteAudio" autoplay controls style="margin-top:10px; width:100%;"></audio>
            </div>
            <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
            <script>
                const peer = new Peer('{st.session_state.user}');
                peer.on('call', c => {{
                    navigator.mediaDevices.getUserMedia({{audio:true}}).then(s => {{
                        c.answer(s);
                        c.on('stream', rs => {{ document.getElementById('remoteAudio').srcObject = rs; }});
                        document.getElementById('status').innerText = "📞 กำลังรับสาย...";
                    }});
                }});
                document.getElementById('callBtn').onclick = () => {{
                    const t = "{target}";
                    if(!t) return alert("เลือกคนที่จะโทรหาก่อน!");
                    navigator.mediaDevices.getUserMedia({{audio:true}}).then(s => {{
                        const call = peer.call(t, s);
                        call.on('stream', rs => {{ document.getElementById('remoteAudio').srcObject = rs; }});
                        document.getElementById('status').innerText = "⏳ กำลังโทรหา " + t + "...";
                    }});
                }};
            </script>
            """
            components.html(html_call, height=220)

        # ฟอร์มโพสต์ข้อความ
        with st.expander("📝 โพสต์ข้อความใหม่"):
            with st.form(f"post_{page}", clear_on_submit=True):
                msg = st.text_area("ข้อความ")
                file = st.file_uploader("แนบไฟล์ (ถ้ามี)", type=['jpg','png','mp4'])
                if st.form_submit_button("🚀 ส่งโพสต์"):
                    m_url, m_type = None, None
                    if file:
                        path = f"{page}/{uuid.uuid4()}_{file.name}"
                        blob = bucket.blob(path)
                        blob.upload_from_string(file.getvalue(), content_type=file.type)
                        blob.make_public()
                        m_url, m_type = blob.public_url, ("video" if "video" in file.type else "image")
                    db.collection(f'posts_{page}').add({
                        'user': st.session_state.user, 'text': msg,
                        'media': m_url, 'type': m_type, 'time': get_thai_time()
                    })
                    st.rerun()

        render_posts(page)
