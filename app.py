import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
import hashlib
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components
import re # สำหรับ YouTube URL parsing

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

def get_youtube_id(url):
    """Extracts YouTube video ID from a URL."""
    if not url:
        return None
    
    # Regular expression for YouTube video IDs
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    match = re.match(youtube_regex, url)
    if match:
        return match.group(6)
    return None

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
            border: 2px solid {cfg['accent']}; /* กรอบสี accent */
            background: rgba(255, 255, 255, 0.05);
            padding: 15px; border-radius: 15px; margin-bottom: 15px;
            color: white !important;
        }}
        .stButton>button {{
            background: {cfg['accent']}; color: black !important;
            font-weight: bold; border-radius: 12px; width: 100%; height: 50px;
        }}
        .stSelectbox>div>div, .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stFileUploader>div>div {{
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .stSelectbox>div>div>span, .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
            color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. ฟังก์ชันแสดงโพสต์และจัดการไลค์ (แยกออกมาเพื่อความยืดหยุ่น) ---
def render_post_display_and_likes(room_id):
    # ส่วนแสดงโพสต์ (จำกัด 20 โพสต์ล่าสุดเพื่อความลื่นไหล)
    docs = db.collection(f'posts_{room_id}').order_by('time', direction='DESCENDING').limit(20).stream()
    post_placeholder = st.empty() # ใช้ empty เพื่อ clear และ re-render เฉพาะส่วนโพสต์

    with post_placeholder.container():
        for d in docs:
            p, pid = d.to_dict(), d.id
            
            # แปลง Timestamp เป็น datetime object สำหรับการแสดงผล
            post_time = p['time']
            if isinstance(post_time, datetime):
                time_str = post_time.strftime("%H:%M:%S %d/%m/%Y")
            else: # กรณีเป็น Firestore Timestamp object
                time_str = post_time.astimezone(timedelta(hours=7)).strftime("%H:%M:%S %d/%m/%Y")

            st.markdown(f'<div class="post-box"><b>👤 {p["user"]}</b> | <small>{time_str}</small><br>{p["text"]}</div>', unsafe_allow_html=True)
            
            if p.get('media'):
                if p['type'] == 'youtube':
                    # แสดง YouTube video โดยใช้ embed URL
                    # ตรวจสอบว่าได้ ID มาถูกต้องก่อน
                    video_id = get_youtube_id(p['media'])
                    if video_id:
                        st.video(f"https://www.youtube.com/watch?v={video_id}")
                    else:
                        st.error(f"ไม่สามารถโหลดวิดีโอ YouTube จาก URL: {p['media']} ได้")
                elif p['type'] == 'video':
                    st.video(p['media'])
                else: # image
                    st.image(p['media'])
            
            # ปุ่มไลค์
            col_like, col_comment = st.columns([0.1, 0.9])
            with col_like:
                current_likes = p.get('likes', [])
                liked_by_user = st.session_state.user in current_likes
                like_button_text = f"❤️ {len(current_likes)}" if not liked_by_user else f"💖 {len(current_likes)}"

                if st.button(like_button_text, key=f"like_{pid}"):
                    ref = db.collection(f'posts_{room_id}').document(pid)
                    if liked_by_user:
                        ref.update({'likes': firestore.ArrayRemove([st.session_state.user])})
                    else:
                        ref.update({'likes': firestore.ArrayUnion([st.session_state.user])})
                    st.rerun() # รีเฟรชหน้าเพื่อแสดงผลการไลค์ล่าสุด


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
        st.markdown("<p style='color:#FFD700;'>🎬 เพลย์ลิสต์แนะนำจาก Synapse</p>", unsafe_allow_html=True)
        components.html('<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>', height=220)
        
        st.subheader("📂 เลือกห้องเพื่อเริ่มต้น")
        c1, c2 = st.columns(2)
        if c1.button("🔴 YouTube Zone"): st.session_state.page = "red"; st.rerun()
        if c2.button("🔵 Facebook (โทรฟรี)"): st.session_state.page = "blue"; st.rerun()
        if c1.button("🟢 ห้องแชทลับ"): st.session_state.page = "green"; st.rerun()
        if c2.button("⚫ ห้อง X เรียลไทม์"): st.session_state.page = "black"; st.rerun()
        if st.button("🚪 ออกจากระบบ"): del st.session_state.user; st.rerun()

    # --- ห้องสีแดง: YouTube Zone (เน้นการแชร์และดูวิดีโอ) ---
    elif st.session_state.page == "red":
        set_luxury_theme("red")
        st.header("🔴 YouTube Zone: แชร์ & ดูวิดีโอ")
        if st.button("⬅️ กลับหน้าหลัก"): st.session_state.page = "home"; st.rerun()
        
        with st.expander("📝 สร้างโพสต์ YouTube ใหม่"):
            with st.form("f_red_post", clear_on_submit=True):
                msg = st.text_area("ข้อความของคุณ (บรรยายวิดีโอ)...")
                youtube_url_input = st.text_input("ลิงก์ YouTube Video (เช่น https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
                
                # ตรวจสอบ YouTube URL และดึง ID
                youtube_video_id = get_youtube_id(youtube_url_input)
                
                file = st.file_uploader("แนบรูป/วิดีโออื่นๆ (ไม่บังคับ)", type=['jpg','png','mp4'])
                
                if st.form_submit_button("แชร์วิดีโอ/โพสต์"):
                    if msg or youtube_url_input or file:
                        post_media_url, post_media_type = None, None

                        if youtube_video_id: # YouTube URL มีความสำคัญกว่าไฟล์แนบ
                            post_media_url = f"https://www.youtube.com/watch?v={youtube_video_id}"
                            post_media_type = 'youtube'
                        elif file:
                            path = f"red/{uuid.uuid4()}_{file.name}"
                            blob = bucket.blob(path)
                            blob.upload_from_string(file.getvalue(), content_type=file.type)
                            blob.make_public()
                            post_media_url, post_media_type = blob.public_url, ('video' if 'video' in file.type else 'image')
                        
                        db.collection('posts_red').add({
                            'user': st.session_state.user, 'text': msg,
                            'media': post_media_url, 'type': post_media_type,
                            'likes': [], 'time': get_thai_time()
                        })
                        st.success("โพสต์ของคุณถูกแชร์แล้ว!")
                        st.rerun()
                    else:
                        st.warning("กรุณาใส่ข้อความ, ลิงก์ YouTube หรือแนบไฟล์")
        
        render_post_display_and_likes("red")

    # --- ห้องสีฟ้า: Facebook (โทรฟรี) ---
    elif st.session_state.page == "blue":
        set_luxury_theme("blue")
        st.header("🔵 Facebook & Call Free")
        if st.button("⬅️ กลับ"): st.session_state.page = "home"; st.rerun()
        
        # --- ระบบโทรฟรี PeerJS ---
        st.markdown('<div class="post-box">📞 โทรฟรีหาเพื่อน (ทดลอง)</div>', unsafe_allow_html=True)
        friends_ref = db.collection('users').stream()
        friends = [u.id for u in friends_ref if u.id != st.session_state.user]
        
        target = st.selectbox("เลือกเพื่อนที่จะโทรหา:", [""] + friends)
        if target:
            components.html(f"""
                <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
                <div style="background: rgba(255,255,255,0.05); padding:10px; border-radius:10px; margin-bottom:10px;">
                    <p style="color:white;">สถานะ: <span id="status">กำลังรอ...</span></p>
                    <button id="call" style="width:100%; padding:15px; background:#28a745; color:white; border:none; border-radius:10px; font-weight:bold;">🟢 เริ่มโทรออกไป {target}</button>
                    <button id="hangup" style="width:100%; padding:15px; background:#dc3545; color:white; border:none; border-radius:10px; font-weight:bold; margin-top:10px;">🔴 วางสาย</button>
                    <audio id="localAudio" autoplay muted style="display:none;"></audio>
                    <audio id="remoteAudio" autoplay></audio>
                </div>
                <script>
                    const peer = new Peer('{st.session_state.user}');
                    let currentCall = null;
                    const status = document.getElementById('status');
                    const remoteAudio = document.getElementById('remoteAudio');
                    const localAudio = document.getElementById('localAudio');

                    peer.on('open', id => {{
                        status.textContent = `เชื่อมต่อแล้ว, ID: ${id}`;
                    }});

                    peer.on('call', call => {{
                        status.textContent = `มีสายเรียกเข้าจาก ${call.peer}! กำลังรับ...`;
                        navigator.mediaDevices.getUserMedia({{ audio: true, video: false }})
                            .then(stream => {{
                                localAudio.srcObject = stream;
                                call.answer(stream);
                                call.on('stream', remoteStream => {{
                                    remoteAudio.srcObject = remoteStream;
                                    status.textContent = `กำลังสนทนากับ ${call.peer}`;
                                }});
                                call.on('close', () => {{
                                    status.textContent = `สายหลุดจาก ${call.peer}`;
                                    remoteAudio.srcObject = null;
                                    stream.getTracks().forEach(track => track.stop());
                                    currentCall = null;
                                }});
                                currentCall = call;
                            }})
                            .catch(err => {{
                                console.error("ไม่สามารถเข้าถึงไมโครโฟน: ", err);
                                status.textContent = "ปฏิเสธ: ไม่สามารถเข้าถึงไมโครโฟน";
                            }});
                    }});

                    peer.on('error', err => {{
                        console.error("PeerJS Error:", err);
                        status.textContent = `เกิดข้อผิดพลาด: ${err.type}`;
                    });

                    document.getElementById('call').onclick = () => {{
                        const targetPeerId = '{target}';
                        if (!targetPeerId) {{
                            status.textContent = "กรุณาเลือกเพื่อนที่จะโทรหา";
                            return;
                        }}
                        status.textContent = `กำลังโทรหา ${targetPeerId}...`;
                        navigator.mediaDevices.getUserMedia({{ audio: true, video: false }})
                            .then(stream => {{
                                localAudio.srcObject = stream;
                                const call = peer.call(targetPeerId, stream);
                                call.on('stream', remoteStream => {{
                                    remoteAudio.srcObject = remoteStream;
                                    status.textContent = `กำลังสนทนากับ ${targetPeerId}`;
                                });
                                call.on('close', () => {{
                                    status.textContent = `สายหลุดจาก ${targetPeerId}`;
                                    remoteAudio.srcObject = null;
                                    stream.getTracks().forEach(track => track.stop());
                                    currentCall = null;
                                }});
                                call.on('error', (err) => {{
                                    console.error("Call Error:", err);
                                    status.textContent = `เกิดข้อผิดพลาดในการโทร: ${err}`;
                                    stream.getTracks().forEach(track => track.stop());
                                    currentCall = null;
                                }});
                                currentCall = call;
                            }})
                            .catch(err => {{
                                console.error("ไม่สามารถเข้าถึงไมโครโฟน: ", err);
                                status.textContent = "โทรออกไม่สำเร็จ: ไม่สามารถเข้าถึงไมโครโฟน";
                            }});
                    }};

                    document.getElementById('hangup').onclick = () => {{
                        if (currentCall) {{
                            currentCall.close();
                            status.textContent = "วางสายแล้ว";
                            remoteAudio.srcObject = null;
                            if (localAudio.srcObject) {{
                                localAudio.srcObject.getTracks().forEach(track => track.stop());
                            }}
                            currentCall = null;
                        }}
                    }};
                </script>
            """, height=350) # เพิ่มความสูงเพื่อให้มีที่สำหรับสถานะและปุ่มวางสาย
        
        # ฟอร์มสร้างโพสต์สำหรับ Facebook
        with st.expander("📝 สร้างโพสต์ใหม่"):
            with st.form("f_blue_post", clear_on_submit=True):
                msg = st.text_area("ข้อความของคุณ...")
                file = st.file_uploader("แนบรูป/วิดีโอ (ไม่บังคับ)", type=['jpg','png','mp4'])
                if st.form_submit_button("แชร์สู่ Facebook"):
                    if msg or file:
                        url, f_type = None, None
                        if file:
                            path = f"blue/{uuid.uuid4()}_{file.name}"
                            blob = bucket.blob(path)
                            blob.upload_from_string(file.getvalue(), content_type=file.type)
                            blob.make_public()
                            url, f_type = blob.public_url, ('video' if 'video' in file.type else 'image')
                        
                        db.collection('posts_blue').add({
                            'user': st.session_state.user, 'text': msg,
                            'media': url, 'type': f_type,
                            'likes': [], 'time': get_thai_time()
                        })
                        st.success("โพสต์ของคุณถูกแชร์แล้ว!")
                        st.rerun()
                    else:
                        st.warning("กรุณาใส่ข้อความหรือแนบไฟล์")
        
        render_post_display_and_likes("blue")

    # --- ห้องสีเขียว: Secret Chat (แชทส่วนตัว) ---
    elif st.session_state.page == "green":
        set_luxury_theme("green")
        st.header("🟢 Secret Chat: คุยส่วนตัว")
        if st.button("⬅️ กลับ"): st.session_state.page = "home"; st.rerun()
        
        friends_ref = db.collection('users').stream()
        friends = [u.id for u in friends_ref if u.id != st.session_state.user]
        target = st.selectbox("เลือกเพื่อนที่จะคุยด้วย:", [""] + friends)

        if target:
            # สร้าง Chat ID แบบมีมาตรฐาน (เรียงตามตัวอักษรเพื่อไม่ให้ซ้ำ)
            cid = "".join(sorted([st.session_state.user, target]))
            
            # ฟอร์มสำหรับส่งข้อความลับ
            with st.form("sc", clear_on_submit=True):
                m = st.text_input("ความลับที่อยากบอก...")
                if st.form_submit_button("ส่งลับๆ"):
                    if m:
                        db.collection('s_chat').add({
                            'cid': cid,
                            'sender': st.session_state.user, # เปลี่ยน 's' เป็น 'sender' เพื่อความชัดเจน
                            'message': m,                     # เปลี่ยน 't' เป็น 'message'
                            'time': get_thai_time()
                        })
                        st.rerun()
                    else:
                        st.warning("กรุณาพิมพ์ข้อความ")
            
            st.markdown("---")
            st.subheader(f"การสนทนากับ {target}")
            
            # แสดงข้อความแชท
            # ใช้ empty placeholder เพื่อให้ข้อความรีเฟรชได้โดยไม่ต้องรีเฟรชทั้งหน้า
            chat_placeholder = st.empty()
            with chat_placeholder.container():
                # ดึงข้อความล่าสุด 10 ข้อความ
                messages_ref = db.collection('s_chat').where('cid', '==', cid).order_by('time', direction='DESCENDING').limit(10).stream()
                messages = sorted([msg.to_dict() for msg in messages_ref], key=lambda x: x['time']) # เรียงลำดับจากเก่าไปใหม่
                
                for msg_data in messages:
                    msg_time = msg_data['time']
                    if isinstance(msg_time, datetime):
                        time_str = msg_time.strftime("%H:%M:%S")
                    else:
                        time_str = msg_time.astimezone(timedelta(hours=7)).
