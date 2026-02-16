import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components

# --- 1. ตั้งค่าและเชื่อมต่อ Firebase ---
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
        st.error(f"เชื่อมต่อ Firebase ไม่ได้: {e}")
        st.stop()

db = firestore.client()
bucket = storage.bucket()

# --- 2. ฟังก์ชันพิเศษ: เวลาไทย & ธีมหน้าจอ ---
def get_thai_time():
    """ดึงเวลาปัจจุบันบวก 7 ชั่วโมงให้ตรงกับไทย"""
    return datetime.utcnow() + timedelta(hours=7)

def set_room_theme(room_id):
    """ปรับแต่งสีพื้นหลังและตัวหนังสือให้ชัดเจนทุกห้อง"""
    themes = {
        "home":  {
            "bg": "linear-gradient(45deg, #FFC0CB, #ADD8E6, #90EE90, #FFD700, #FFA07A)", 
            "text": "#1A1A1A", # หน้าหลักใช้ตัวหนังสือสีเข้มเพื่อให้เห็นชัดบนสีพาสเทล
            "accent": "#FFFFFF"
        },
        "red":   {"bg": "linear-gradient(180deg, #8b0000, #ff4b4b)", "text": "#FFFFFF", "accent": "#FF4B4B"},
        "blue":  {"bg": "linear-gradient(180deg, #000046, #1cb5e0)", "text": "#FFFFFF", "accent": "#1DA1F2"},
        "green": {"bg": "linear-gradient(180deg, #004d00, #2ecc71)", "text": "#FFFFFF", "accent": "#25D366"},
        "black": {"bg": "linear-gradient(180deg, #000000, #434343)", "text": "#FFFFFF", "accent": "#555555"}
    }
    cfg = themes.get(room_id, themes["home"])
    
    st.markdown(f"""
        <style>
        .stApp {{ background: {cfg['bg']}; color: {cfg['text']}; }}
        /* บังคับสีตัวหนังสือให้ชัดเจน ไม่ให้หมอง */
        h1, h2, h3, p, span, label, .stMarkdown, .stCaption, .stExpander {{ 
            color: {cfg['text']} !important; 
        }}
        .post-box {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 20px; border-radius: 20px; margin-bottom: 20px;
        }}
        .stButton>button {{
            background-color: {cfg['accent']};
            color: {"#1A1A1A" if cfg['accent'] == "#FFFFFF" else "#FFFFFF"} !important;
            border-radius: 50px; font-weight: bold; width: 100%; transition: 0.3s;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 3. ระบบวิดีโอคอล/โทรฟรี (Peer-to-Peer) ---
def render_call_feature(target_user):
    """ระบบโทรฟรีเฉพาะห้อง Facebook"""
    if target_user:
        components.html(f"""
            <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
            <div style="text-align:center; padding:15px; border-radius:15px; background:rgba(255,255,255,0.2); border:1px solid white;">
                <button id="callBtn" style="padding:10px 20px; border-radius:20px; border:none; background:#28a745; color:white; font-weight:bold; cursor:pointer; width:100%;">📞 กดโทรออก (Free)</button>
                <p id="callStatus" style="color:white; font-size:14px; margin-top:10px;">สถานะ: พร้อมโทรหา {target_user}</p>
                <audio id="remoteAudio" autoplay></audio>
            </div>
            <script>
                const peer = new Peer('{st.session_state.user}');
                peer.on('call', (call) => {{
                    navigator.mediaDevices.getUserMedia({{audio: true}}).then((stream) => {{
                        call.answer(stream);
                        document.getElementById('callStatus').innerText = "กำลังรับสาย...";
                        call.on('stream', (rms) => {{ document.getElementById('remoteAudio').srcObject = rms; }});
                    }});
                }});
                document.getElementById('callBtn').onclick = () => {{
                    navigator.mediaDevices.getUserMedia({{audio: true}}).then((stream) => {{
                        const call = peer.call('{target_user}', stream);
                        document.getElementById('callStatus').innerText = "กำลังโทรออก...";
                        call.on('stream', (rms) => {{ document.getElementById('remoteAudio').srcObject = rms; }});
                    }});
                }};
            </script>
        """, height=150)

# --- 4. ฟังก์ชันหลักสำหรับห้องโซเชียล ---
def render_social_room(room_id, room_name):
    set_room_theme(room_id)
    st.title(f"{room_name} Room")
    
    if room_id == "blue":
        st.subheader("📞 วิดีโอคอล/โทรฟรี")
        friend_list = [u.id for u in db.collection('users').stream() if u.id != st.session_state.user]
        target = st.selectbox("เลือกเพื่อนที่จะโทรหา", [""] + friend_list)
        if target: render_call_feature(target)
        st.markdown("---")

    with st.expander("📝 สร้างโพสต์ใหม่"):
        with st.form(f"form_{room_id}"):
            msg = st.text_area("คุณกำลังคิดอะไรอยู่?")
            media = st.file_uploader("แนบรูปหรือวิดีโอ", type=['png','jpg','mp4'])
            if st.form_submit_button("โพสต์"):
                m_url, m_type = None, None
                if media:
                    blob = bucket.blob(f"{room_id}/{uuid.uuid4()}_{media.name}")
                    blob.upload_from_string(media.getvalue(), content_type=media.type)
                    blob.make_public()
                    m_url, m_type = blob.public_url, ('video' if 'video' in media.type else 'image')
                db.collection(f'posts_{room_id}').add({
                    'user': st.session_state.user, 'text': msg, 'media_url': m_url, 
                    'media_type': m_type, 'likes': [], 'timestamp': get_thai_time()
                })
                st.rerun()

    for doc in db.collection(f'posts_{room_id}').order_by('timestamp', direction='DESCENDING').stream():
        p, pid = doc.to_dict(), doc.id
        st.markdown('<div class="post-box">', unsafe_allow_html=True)
        st.write(f"**👤 {p['user']}**")
        st.caption(f"🕒 {p['timestamp'].strftime('%H:%M | %d/%m/%Y')}")
        st.write(p['text'])
        if p.get('media_url'):
            if p['media_type'] == 'video': st.video(p['media_url'])
            else: st.image(p['media_url'])
        
        if st.button(f"❤️ {len(p.get('likes', []))}", key=f"lk_{pid}"):
            ref = db.collection(f'posts_{room_id}').document(pid)
            if st.session_state.user in p.get('likes', []):
                ref.update({'likes': firestore.ArrayRemove([st.session_state.user])})
            else: ref.update({'likes': firestore.ArrayUnion([st.session_state.user])})
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. การประมวลผลหน้าจอหลัก ---
if 'user' not in st.session_state:
    set_room_theme("home")
    st.title("🚀 Firebase Social 2026")
    u_input = st.text_input("กรุณาระบุชื่อผู้ใช้")
    if st.button("เข้าสู่ระบบ"):
        if u_input:
            st.session_state.user = u_input
            db.collection('users').document(u_input).set({'last_active': get_thai_time()}, merge=True)
            st.rerun()
else:
    with st.sidebar:
        st.header(f"สวัสดี, {st.session_state.user}")
        menu = st.radio("เลือกหน้า", ["หน้าหลัก", "YouTube (Red)", "Facebook (Blue)", "Line (Green)", "X (Black)"])
        if st.button("ออกจากระบบ"):
            del st.session_state.user
            st.rerun()
        st.markdown("---")
        st.subheader("👥 สมาชิกในระบบ")
        for u in db.collection('users').limit(10).stream(): st.write(f"• {u.id}")

    if menu == "หน้าหลัก":
        set_room_theme("home")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try: st.image("logo.jpg", use_container_width=True)
            except: st.warning("ไม่พบไฟล์ logo.jpg")
        st.markdown("<h1 style='text-align: center;'>Firebase Social 2026</h1>", unsafe_allow_html=True)
        st.info("💡 วิธีใช้: เลือกห้องทางซ้ายมือ ห้อง Facebook สามารถโทรฟรีหาเพื่อนได้!")
    else:
        mapping = {"YouTube (Red)": ("red", "YouTube"), "Facebook (Blue)": ("blue", "Facebook"), 
                   "Line (Green)": ("green", "Line"), "X (Black)": ("black", "X")}
        render_social_room(*mapping[menu])
