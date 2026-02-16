import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components

# --- 1. การเชื่อมต่อ Firebase & ตั้งค่าพื้นฐาน ---
if not firebase_admin._apps:
    try:
        cred_info = dict(st.secrets["firebase_service_account"])
        if "\\n" in cred_info["private_key"]:
            cred_info["private_key"] = cred_info["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(cred_info)
        firebase_admin.initialize_app(cred, {
            'storageBucket': st.secrets["firebase_config"]["storageBucket"]
        })
    except Exception as e:
        st.error(f"Error connecting to Firebase: {e}")
        st.stop()

db = firestore.client()
bucket = storage.bucket()

# --- 2. ฟังก์ชันพิเศษ (Utility) ---
def get_thai_time():
    return datetime.utcnow() + timedelta(hours=7)

def set_room_theme(room_id):
    themes = {
        "home":  {"bg": "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)", "text": "#1e3a5f", "accent": "#4a90e2"},
        "red":   {"bg": "linear-gradient(180deg, #8b0000 0%, #ff4b4b 100%)", "text": "#ffffff", "accent": "#ffffff"},
        "blue":  {"bg": "linear-gradient(180deg, #000046 0%, #1cb5e0 100%)", "text": "#ffffff", "accent": "#ffffff"},
        "green": {"bg": "linear-gradient(180deg, #004d00 0%, #2ecc71 100%)", "text": "#ffffff", "accent": "#ffffff"},
        "black": {"bg": "linear-gradient(180deg, #000000 0%, #434343 100%)", "text": "#ffffff", "accent": "#aaaaaa"}
    }
    cfg = themes.get(room_id, themes["home"])
    st.markdown(f"""
        <style>
        .stApp {{ background: {cfg['bg']}; color: {cfg['text']}; }}
        h1, h2, h3, p, span, label {{ color: {cfg['text']} !important; font-family: 'Kanit', sans-serif; }}
        .post-box {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 20px; border-radius: 20px; margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0,0,0,0.3);
        }}
        .stButton>button {{
            border-radius: 30px; border: none; font-weight: bold;
            transition: 0.3s; background: {cfg['accent']}; color: white !important;
        }}
        .stButton>button:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}
        </style>
    """, unsafe_allow_html=True)

# --- 3. ส่วนระบบโทร (WebRTC) ---
def render_call_feature(target_user):
    if target_user:
        st.info(f"🟢 พร้อมโทรหา: {target_user}")
        components.html(f"""
            <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
            <div style="text-align:center; padding:10px; border-radius:15px; background:rgba(255,255,255,0.2);">
                <button id="callBtn" style="padding:10px 20px; border-radius:20px; border:none; background:#28a745; color:white; cursor:pointer;">📞 กดโทรออก (Free)</button>
                <p id="callStatus" style="color:white; font-size:12px; margin-top:5px;">สถานะ: พร้อม</p>
                <audio id="remoteAudio" autoplay></audio>
            </div>
            <script>
                const peer = new Peer('{st.session_state.user}');
                const status = document.getElementById('callStatus');
                peer.on('call', (call) => {{
                    navigator.mediaDevices.getUserMedia({{audio: true}}).then((stream) => {{
                        call.answer(stream);
                        status.innerText = "กำลังรับสาย...";
                        call.on('stream', (rms) => {{ document.getElementById('remoteAudio').srcObject = rms; }});
                    }});
                }});
                document.getElementById('callBtn').onclick = () => {{
                    navigator.mediaDevices.getUserMedia({{audio: true}}).then((stream) => {{
                        const call = peer.call('{target_user}', stream);
                        status.innerText = "กำลังโทรออก...";
                        call.on('stream', (rms) => {{ document.getElementById('remoteAudio').srcObject = rms; }});
                    }});
                }};
            </script>
        """, height=120)

# --- 4. ฟังก์ชันจัดการห้อง (Unified Room Logic) ---
def render_social_room(room_id, room_name):
    set_room_theme(room_id)
    st.title(f"{room_name} Room")
    
    if room_id == "blue":
        st.subheader("📞 วิดีโอคอล/โทรฟรี")
        friend_to_call = st.selectbox("เลือกเพื่อนในระบบ", [d.id for d in db.collection('users').stream() if d.id != st.session_state.user])
        render_call_feature(friend_to_call)
        st.markdown("---")

    # ส่วนโพสต์ใหม่
    with st.expander("📝 สร้างโพสต์ใหม่"):
        with st.form(f"post_{room_id}"):
            msg = st.text_area("คุณกำลังคิดอะไรอยู่?")
            media = st.file_uploader("แนบรูปหรือวิดีโอ", type=['png','jpg','mp4'])
            if st.form_submit_button("โพสต์"):
                m_url, m_type = None, None
                if media:
                    path = f"{room_id}/{uuid.uuid4()}_{media.name}"
                    blob = bucket.blob(path)
                    blob.upload_from_string(media.getvalue(), content_type=media.type)
                    blob.make_public()
                    m_url = blob.public_url
                    m_type = 'video' if 'video' in media.type else 'image'
                
                db.collection(f'posts_{room_id}').add({
                    'user': st.session_state.user,
                    'text': msg, 'media_url': m_url, 'media_type': m_type,
                    'likes': [], 'timestamp': get_thai_time()
                })
                st.rerun()

    # ส่วนแสดงโพสต์
    posts = db.collection(f'posts_{room_id}').order_by('timestamp', direction='DESCENDING').stream()
    for post in posts:
        p = post.to_dict()
        pid = post.id
        st.markdown(f'<div class="post-box">', unsafe_allow_html=True)
        st.write(f"**👤 {p['user']}**")
        st.caption(f"🕒 {p['timestamp'].strftime('%H:%M | %d/%m/%Y')}")
        st.write(p['text'])
        if p.get('media_url'):
            if p['media_type'] == 'video': st.video(p['media_url'])
            else: st.image(p['media_url'])
        
        # Like & Comment Section
        likes = p.get('likes', [])
        c1, c2 = st.columns([1, 5])
        if c1.button(f"❤️ {len(likes)}", key=f"lk_{pid}"):
            if st.session_state.user in likes:
                db.collection(f'posts_{room_id}').document(pid).update({'likes': firestore.ArrayRemove([st.session_state.user])})
            else:
                db.collection(f'posts_{room_id}').document(pid).update({'likes': firestore.ArrayUnion([st.session_state.user])})
            st.rerun()
        
        # ส่วนคอมเมนต์ (มีทุกห้องเพื่อความเท่าเทียม)
        with st.expander("💬 ดูความคิดเห็น"):
            for cm in db.collection(f'posts_{room_id}').document(pid).collection('comments').order_by('timestamp').stream():
                c = cm.to_dict()
                st.write(f"**{c['user']}**: {c['text']}")
            with st.form(f"cm_form_{pid}"):
                c_text = st.text_input("พิมพ์คอมเมนต์...")
                if st.form_submit_button("ส่ง"):
                    db.collection(f'posts_{room_id}').document(pid).collection('comments').add({
                        'user': st.session_state.user, 'text': c_text, 'timestamp': get_thai_time()
                    })
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. โครงสร้างหลัก (Main Execution) ---
if 'user' not in st.session_state:
    set_room_theme("home")
    st.title("🚀 Firebase Social 2026")
    u_name = st.text_input("กรุณาระบุชื่อผู้ใช้")
    if st.button("เข้าสู่ระบบ"):
        if u_name:
            st.session_state.user = u_name
            db.collection('users').document(u_name).set({'last_active': get_thai_time()}, merge=True)
            st.rerun()
else:
    with st.sidebar:
        st.title(f"สวัสดี, {st.session_state.user}")
        menu = st.selectbox("เลือกหน้า", ["หน้าหลัก", "YouTube (Red)", "Facebook (Blue)", "Line (Green)", "X (Black)"])
        if st.button("ออกจากระบบ"):
            del st.session_state.user
            st.rerun()
        st.markdown("---")
        st.subheader("👥 ใครอยู่บ้าง?")
        for u in db.collection('users').limit(10).stream():
            st.write(f"• {u.id}")

    if menu == "หน้าหลัก":
        set_room_theme("home")
        st.header("🏠 ยินดีต้อนรับสู่สังคมออนไลน์")
        st.write("เลือกห้องทางด้านซ้ายเพื่อเริ่มพูดคุยและโทรหาเพื่อนฟรี!")
    else:
        room_data = {"YouTube (Red)": ("red", "YouTube"), "Facebook (Blue)": ("blue", "Facebook"), 
                     "Line (Green)": ("green", "Line"), "X (Black)": ("black", "X")}
        r_id, r_name = room_data[menu]
        render_social_room(r_id, r_name)
