import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
import hashlib
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components

# --- 1. เชื่อมต่อ Firebase (ส่วนหัวใจ) ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(dict(st.secrets["firebase_service_account"]))
        firebase_admin.initialize_app(cred, {'storageBucket': st.secrets["firebase_config"]["storageBucket"]})
    except Exception as e:
        st.error("การเชื่อมต่อฐานข้อมูลล้มเหลว ตรวจสอบ Secrets ของคุณ")
        st.stop()

db = firestore.client()
bucket = storage.bucket()

# --- 2. ฟังก์ชันรักษาความปลอดภัย ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_thai_time():
    return datetime.utcnow() + timedelta(hours=7)

# --- 3. ธีมสี (เข้มหรู กรอบทอง - ตามใจคุณท่าน) ---
def set_luxury_theme(room_id):
    themes = {
        "home":  {"bg": "#001219", "text": "#FFD700", "accent": "#D4AF37"},
        "red":   {"bg": "#3d0000", "text": "#FFFFFF", "accent": "#FF4D4D"},
        "blue":  {"bg": "#002147", "text": "#FFFFFF", "accent": "#00A8E8"},
        "green": {"bg": "#0a2910", "text": "#FFFFFF", "accent": "#38B000"},
        "black": {"bg": "#121212", "text": "#FFFFFF", "accent": "#E5E5E5"}
    }
    cfg = themes.get(room_id, themes["home"])
    st.markdown(f"""
        <style>
        .stApp {{ background: {cfg['bg']}; color: {cfg['text']}; }}
        h1, h2, h3, p, label {{ color: {cfg['text']} !important; }}
        .post-box {{
            border: 2px solid #D4AF37;
            background: rgba(255, 255, 255, 0.05);
            padding: 15px; border-radius: 15px; margin-bottom: 15px;
            color: white !important;
        }}
        .stButton>button {{
            background: {cfg['accent']}; color: black !important;
            font-weight: bold; border-radius: 12px; width: 100%; height: 50px;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. ฟังก์ชันจัดการโพสต์ (เกรดใช้งานจริง) ---
def render_posts(room_id):
    # ส่วนเขียนโพสต์
    with st.expander("📝 เขียนโพสต์ใหม่ (แบ่งปันความรู้สึก)"):
        with st.form(f"f_{room_id}", clear_on_submit=True):
            msg = st.text_area("ข้อความของคุณ...")
            file = st.file_uploader("แนบรูป/วิดีโอ", type=['jpg','png','mp4'])
            if st.form_submit_button("แชร์สู่สาธารณะ"):
                if msg or file:
                    url, f_type = None, None
                    if file:
                        path = f"{room_id}/{uuid.uuid4()}_{file.name}"
                        blob = bucket.blob(path)
                        blob.upload_from_string(file.getvalue(), content_type=file.type)
                        blob.make_public()
                        url, f_type = blob.public_url, ('video' if 'video' in file.type else 'image')
                    
                    db.collection(f'posts_{room_id}').add({
                        'user': st.session_state.user, 'text': msg,
                        'media': url, 'type': f_type,
                        'likes': [], 'time': get_thai_time()
                    })
                    st.rerun()

    # ส่วนแสดงโพสต์ (จำกัด 20 โพสต์ล่าสุดเพื่อความลื่นไหล)
    docs = db.collection(f'posts_{room_id}').order_by('time', direction='DESCENDING').limit(20).stream()
    for d in docs:
        p, pid = d.to_dict(), d.id
        st.markdown(f'<div class="post-box"><b>👤 {p["user"]}</b> | <small>{p["time"].strftime("%H:%M")}</small><br>{p["text"]}</div>', unsafe_allow_html=True)
        if p.get('media'):
            if p['type'] == 'video': st.video(p['media'])
            else: st.image(p['media'])
        
        if st.button(f"❤️ {len(p.get('likes',[]))}", key=f"l_{pid}"):
            ref = db.collection(f'posts_{room_id}').document(pid)
            if st.session_state.user in p.get('likes', []):
                ref.update({'likes': firestore.ArrayRemove([st.session_state.user])})
            else:
                ref.update({'likes': firestore.ArrayUnion([st.session_state.user])})
            st.rerun()

# --- 5. ระบบหน้าจอและการโทร ---
if 'user' not in st.session_state:
    set_luxury_theme("home")
    st.image("logo.jpg", width=200)
    st.title("🛡️ เข้าสู่ระบบ Synapse")
    u = st.text_input("ชื่อผู้ใช้")
    p = st.text_input("รหัสผ่าน", type="password")
    c1, c2 = st.columns(2)
    if c1.button("ล็อกอิน"):
        res = db.collection('users').document(u).get()
        if res.exists and res.to_dict().get('pw') == hash_password(p):
            st.session_state.user, st.session_state.page = u, "home"
            st.rerun()
        else: st.error("ข้อมูลไม่ถูกต้อง")
    if c2.button("ลงทะเบียน"):
        if u and p:
            db.collection('users').document(u).set({'pw': hash_password(p)})
            st.success("สำเร็จ! กรุณาล็อกอิน")
else:
    if st.session_state.page == "home":
        set_luxury_theme("home")
        st.image("logo.jpg", width=150)
        st.title(f"สวัสดีคุณ {st.session_state.user}")
        
        # YouTube Playlist ของคุณท่าน
        components.html('<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>', height=220)
        
        st.subheader("📂 เลือกห้องเพื่อเริ่มต้น")
        c1, c2 = st.columns(2)
        if c1.button("🔴 YouTube"): st.session_state.page = "red"; st.rerun()
        if c2.button("🔵 Facebook (โทรฟรี)"): st.session_state.page = "blue"; st.rerun()
        if c1.button("🟢 ห้องแชทลับ"): st.session_state.page = "green"; st.rerun()
        if c2.button("⚫ ห้อง X เรียลไทม์"): st.session_state.page = "black"; st.rerun()
        if st.button("🚪 ออกจากระบบ"): del st.session_state.user; st.rerun()

    elif st.session_state.page == "blue":
        set_luxury_theme("blue")
        st.header("🔵 Facebook & Call Free")
        if st.button("⬅️ กลับ"): st.session_state.page = "home"; st.rerun()
        
        # --- ระบบโทรฟรี PeerJS ---
        st.markdown('<div class="post-box">📞 โทรฟรีหาเพื่อน</div>', unsafe_allow_html=True)
        friends = [u.id for u in db.collection('users').stream() if u.id != st.session_state.user]
        target = st.selectbox("เลือกเพื่อน", [""] + friends)
        if target:
            components.html(f"""
                <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
                <button id="call" style="width:100%; padding:15px; background:#28a745; color:white; border:none; border-radius:10px; font-weight:bold;">🟢 เริ่มโทรออก</button>
                <audio id="v" autoplay></audio>
                <script>
                    const p = new Peer('{st.session_state.user}');
                    p.on('call', c => {{ navigator.mediaDevices.getUserMedia({{audio:true}}).then(s => {{ c.answer(s); c.on('stream', r => {{ document.getElementById('v').srcObject = r; }}); }}); }});
                    document.getElementById('call').onclick = () => {{
                        navigator.mediaDevices.getUserMedia({{audio:true}}).then(s => {{ const c = p.call('{target}', s); c.on('stream', r => {{ document.getElementById('v').srcObject = r; }}); }});
                    }};
                </script>
            """, height=100)
        render_posts("blue")

    elif st.session_state.page == "green":
        set_luxury_theme("green")
        st.header("🟢 Secret Chat")
        if st.button("⬅️ กลับ"): st.session_state.page = "home"; st.rerun()
        
        friends = [u.id for u in db.collection('users').stream() if u.id != st.session_state.user]
        target = st.selectbox("คุยกับใครดี?", [""] + friends)
        if target:
            cid = "".join(sorted([st.session_state.user, target]))
            with st.form("sc", clear_on_submit=True):
                m = st.text_input("ความลับที่อยากบอก...")
                if st.form_submit_button("ส่งลับๆ"):
                    db.collection('s_chat').add({'cid': cid, 's': st.session_state.user, 't': m, 'time': get_thai_time()})
                    st.rerun()
            for msg in db.collection('s_chat').where('cid', '==', cid).order_by('time', direction='DESCENDING').limit(10).stream():
                d = msg.to_dict()
                st.markdown(f'<div class="post-box"><b>{d["s"]}:</b> {d["t"]}</div>', unsafe_allow_html=True)
    
    # ห้องอื่นๆ (Red, Black) ให้เรียก render_posts(room_id) ได้เลยครับ
