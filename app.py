import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
import hashlib
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components
import re

# --- 1. ตั้งค่าการเชื่อมต่อ Firebase ---
if not firebase_admin._apps:
    try:
        cred_dict = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'storageBucket': st.secrets["firebase_config"]["storageBucket"]
        })
    except Exception as e:
        st.error(f"❌ เชื่อมต่อฐานข้อมูลไม่สำเร็จ: {e}")
        st.stop()

db = firestore.client()
bucket = storage.bucket()

# --- 2. ฟังก์ชันเสริม (Helper Functions) ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_thai_time():
    return datetime.utcnow() + timedelta(hours=7)

def get_youtube_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- 3. ธีมสุดหรู (Luxury Theme) ---
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
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. ฟังก์ชันแสดงโพสต์และระบบ Like ---
def render_posts(room_id):
    try:
        posts_ref = db.collection(f'posts_{room_id}').order_by('time', direction='DESCENDING').limit(20)
        docs = posts_ref.stream()
        
        has_post = False
        for doc in docs:
            has_post = True
            p = doc.to_dict()
            pid = doc.id
            st.markdown(f'''<div class="post-box">
                <b>👤 {p.get("user", "ไม่ระบุชื่อ")}</b> | <small>{p.get("time").strftime("%H:%M") if p.get("time") else ""}</small><br>
                {p.get("text", "")}
            </div>''', unsafe_allow_html=True)
            
            if p.get('type') == 'youtube':
                st.video(p['media'])
            elif p.get('media'):
                if p.get('type') == 'video': st.video(p['media'])
                else: st.image(p['media'])
            
            likes = p.get('likes', [])
            if st.button(f"❤️ {len(likes)}", key=f"like_{room_id}_{pid}"):
                ref = db.collection(f'posts_{room_id}').document(pid)
                if st.session_state.user in likes:
                    ref.update({'likes': firestore.ArrayRemove([st.session_state.user])})
                else:
                    ref.update({'likes': firestore.ArrayUnion([st.session_state.user])})
                st.rerun()
        
        if not has_post:
            st.info("ยังไม่มีโพสต์ในห้องนี้ เริ่มโพสต์คนแรกเลย!")
    except Exception as e:
        st.warning("กำลังเตรียมฐานข้อมูลหรือยังไม่มีข้อมูลโพสต์")

# --- 5. ระบบจัดการหน้าจอ (Logic) ---
if 'user' not in st.session_state:
    set_luxury_theme("home")
    st.title("🛡️ Synapse Login")
    u = st.text_input("ชื่อผู้ใช้ (Username)")
    p = st.text_input("รหัสผ่าน (Password)", type="password")
    
    col1, col2 = st.columns(2)
    if col1.button("เข้าสู่ระบบ"):
        user_doc = db.collection('users').document(u).get()
        if user_doc.exists and user_doc.to_dict().get('pw') == hash_password(p):
            st.session_state.user = u
            st.session_state.page = "home"
            st.rerun()
        else: st.error("❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
        
    if col2.button("ลงทะเบียนใหม่"):
        if u and p:
            db.collection('users').document(u).set({'pw': hash_password(p)})
            st.success("✅ ลงทะเบียนสำเร็จ! กรุณากดเข้าสู่ระบบ")

else:
    # หน้าหลัก
    if st.session_state.page == "home":
        set_luxury_theme("home")
        st.title(f"ยินดีต้อนรับ, {st.session_state.user}")
        st.markdown("<p style='color:#FFD700;'>🎬 เพลย์ลิสต์แนะนำจาก Synapse</p>", unsafe_allow_html=True)
        components.html('<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>', height=220)
        
        st.subheader("📂 เลือกห้องสนทนา")
        c1, c2 = st.columns(2)
        if c1.button("🔴 YouTube Zone"): st.session_state.page = "red"; st.rerun()
        if c2.button("🔵 Facebook (โทรฟรี)"): st.session_state.page = "blue"; st.rerun()
        if c1.button("🟢 ห้องแชทลับ"): st.session_state.page = "green"; st.rerun()
        if c2.button("⚫ ห้อง X เรียลไทม์"): st.session_state.page = "black"; st.rerun()
        if st.button("🚪 ออกจากระบบ"): del st.session_state.user; st.rerun()

    # หน้าห้องต่างๆ
    elif st.session_state.page in ["red", "blue", "green", "black"]:
        set_luxury_theme(st.session_state.page)
        room = st.session_state.page
        st.header(f"ห้อง {room.upper()}")
        if st.button("⬅️ กลับหน้าหลัก"): st.session_state.page = "home"; st.rerun()

        # ระบบโทรฟรีเฉพาะห้อง BLUE
        if room == "blue":
            st.markdown('<div class="post-box">📞 โทรฟรีหาเพื่อน</div>', unsafe_allow_html=True)
            u_ref = db.collection('users').stream()
            friends = [u.id for u in u_ref if u.id != st.session_state.user]
            target = st.selectbox("เลือกเพื่อน:", [""] + friends)
            if target:
                html_code = """
                <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
                <div style="background:rgba(255,255,255,0.05);padding:10px;border-radius:10px;color:white;text-align:center;">
                    <p id="status">สถานะ: พร้อมใช้งาน</p>
                    <button id="callBtn" style="width:100%%;padding:10px;background:#28a745;color:white;border:none;border-radius:5px;">🟢 โทรออก</button>
                    <audio id="remoteAudio" autoplay></audio>
                </div>
                <script>
                    const peer = new Peer('%s');
                    document.getElementById('callBtn').onclick = () => {
                        navigator.mediaDevices.getUserMedia({audio:true}).then(s => {
                            const call = peer.call('%s', s);
                            call.on('stream', rs => { document.getElementById('remoteAudio').srcObject = rs; });
                        });
                    };
                    peer.on('call', c => {
                        navigator.mediaDevices.getUserMedia({audio:true}).then(s => {
                            c.answer(s);
                            c.on('stream', rs => { document.getElementById('remoteAudio').srcObject = rs; });
                        });
                    });
                </script>
                """ % (st.session_state.user, target)
                components.html(html_code, height=180)

        # ฟอร์มโพสต์
        with st.expander("📝 เขียนโพสต์ใหม่"):
            with st.form(f"f_{room}", clear_on_submit=True):
                msg = st.text_area("ข้อความ...")
                yt_link = st.text_input("ลิงก์ YouTube") if room == "red" else ""
                file = st.file_uploader("รูป/วิดีโอ", type=['jpg','png','mp4'])
                if st.form_submit_button("🚀 ส่ง"):
                    if msg or yt_link or file:
                        m_url, m_type = None, None
                        y_id = get_youtube_id(yt_link)
                        if y_id: m_url, m_type = f"https://www.youtube.com/watch?v={y_id}", "youtube"
                        elif file:
                            path = f"{room}/{uuid.uuid4()}_{file.name}"
                            blob = bucket.blob(path)
                            blob.upload_from_string(file.getvalue(), content_type=file.type)
                            blob.make_public()
                            m_url, m_type = blob.public_url, ("video" if "video" in file.type else "image")
                        db.collection(f'posts_{room}').add({
                            'user': st.session_state.user, 'text': msg,
                            'media': m_url, 'type': m_type,
                            'likes': [], 'time': get_thai_time()
                        })
                        st.rerun()

        render_posts(room)
