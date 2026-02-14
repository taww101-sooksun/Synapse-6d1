import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime
import uuid

# --- 1. ตั้งค่าและเชื่อมต่อ Firebase ---
if "firebase_service_account" not in st.secrets:
    st.error("ไม่พบการตั้งค่า Secrets! กรุณาสร้างไฟล์ .streamlit/secrets.toml")
    st.stop()

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
try:
    bucket = storage.bucket()
except:
    st.error("ไม่พบ Storage Bucket")

# --- 2. จัดการ State (หน้าและ User) ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'user' not in st.session_state: st.session_state.user = ''

# --- 3. ฟังก์ชันตกแต่ง CSS (เปลี่ยนสีตามห้อง) ---
def set_theme(room_color):
    themes = {
        "home": ("#ffffff", "#000000"), # พื้นขาว ตัวดำ
        "red": ("#800000", "#ffffff"),  # พื้นแดงเลือดหมู ตัวขาว
        "blue": ("#000080", "#ffffff"), # พื้นน้ำเงินเข้ม ตัวขาว
        "green": ("#006400", "#ffffff"),# พื้นเขียวแก่ ตัวขาว
        "black": ("#000000", "#ffffff") # พื้นดำ ตัวขาว
    }
    bg, text = themes.get(room_color, ("#ffffff", "#000000"))
    
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {bg}; }}
        h1, h2, h3, p, span, div, label {{ color: {text} !important; }}
        .stButton>button {{
            border-radius: 20px;
            background-color: white;
            color: black;
            border: 1px solid #ccc;
        }}
        .post-box {{
            border: 1px solid {text};
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            background-color: rgba(255,255,255,0.1);
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. ฟังก์ชันสำหรับห้องแชท (Reusable) ---
def render_room(room_id, room_name_th):
    st.title(f"ห้อง{room_name_th}")
    
    if st.button("⬅️ กลับหน้าหลัก"):
        st.session_state.page = 'home'
        st.rerun()

    # --- ส่วนโพสต์ ---
    with st.expander("vb เขียนโพสต์ใหม่ / อัปโหลดรูป", expanded=True):
        with st.form(f"post_form_{room_id}"):
            msg = st.text_area("คุยอะไรกันดี...")
            media = st.file_uploader("รูป/วิดีโอ", type=['png','jpg','mp4','mov'])
            submitted = st.form_submit_button("โพสต์เลย")
            
            if submitted and (msg or media):
                media_url, media_type = None, None
                if media:
                    with st.spinner("กำลังอัปโหลด..."):
                        ext = media.name.split('.')[-1]
                        fname = f"{room_id}/{uuid.uuid4()}.{ext}"
                        blob = bucket.blob(fname)
                        blob.upload_from_string(media.getvalue(), content_type=media.type)
                        blob.make_public()
                        media_url = blob.public_url
                        media_type = 'video' if 'video' in media.type else 'image'
                
                db.collection(f'posts_{room_id}').add({
                    'user': st.session_state.user,
                    'text': msg,
                    'media_url': media_url,
                    'media_type': media_type,
                    'likes': [], # เก็บรายชื่อคนกดไลค์
                    'timestamp': firestore.SERVER_TIMESTAMP
                })
                st.success("โพสต์แล้ว!")
                st.rerun()

    # --- ส่วนแสดงฟีด ---
    docs = db.collection(f'posts_{room_id}').order_by('timestamp', direction='DESCENDING').stream()
    
    for doc in docs:
        d = doc.to_dict()
        did = doc.id
        likes = d.get('likes', [])
        is_liked = st.session_state.user in likes
        
        st.markdown(f'<div class="post-box">', unsafe_allow_html=True)
        st.caption(f"👤 {d.get('user')} • {d.get('timestamp', '')}")
        st.write(d.get('text'))
        
        if d.get('media_url'):
            if d.get('media_type') == 'video':
                st.video(d.get('media_url'))
            else:
                st.image(d.get('media_url'))
        
        # ปุ่ม Like & Share
        c1, c2, c3 = st.columns([1, 1, 4])
        with c1:
            like_label = f"❤️ {len(likes)}" if is_liked else f"🤍 {len(likes)}"
            if st.button(like_label, key=f"like_{did}"):
                ref = db.collection(f'posts_{room_id}').document(did)
                if is_liked:
                    ref.update({'likes': firestore.ArrayRemove([st.session_state.user])})
                else:
                    ref.update({'likes': firestore.ArrayUnion([st.session_state.user])})
                st.rerun()
        with c2:
            if st.button("🔗 แชร์", key=f"share_{did}"):
                st.toast("จำลอง: คัดลอกลิงก์เรียบร้อย!")
                
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. ส่วนควบคุมหลัก (Main Controller) ---

# หน้า Login
if st.session_state.user == '':
    set_theme("home")
    st.title("🔐 เข้าสู่ระบบ")
    name = st.text_input("ตั้งชื่อเล่นของคุณ:")
    if st.button("เริ่มเล่น") and name:
        st.session_state.user = name
        st.rerun()

# หน้าหลัก (เลือกห้อง)
elif st.session_state.page == 'home':
    set_theme("home")
    st.title(f"สวัสดี {st.session_state.user} 👋")
    st.subheader("เลือกห้องที่ต้องการเข้า:")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔴 ห้องสีแดง", use_container_width=True): 
            st.session_state.page = 'red'
            st.rerun()
        if st.button("🔵 ห้องสีน้ำเงิน", use_container_width=True): 
            st.session_state.page = 'blue'
            st.rerun()
    with c2:
        if st.button("🟢 ห้องสีเขียว", use_container_width=True): 
            st.session_state.page = 'green'
            st.rerun()
        if st.button("⚫ ห้องสีดำ", use_container_width=True): 
            st.session_state.page = 'black'
            st.rerun()
            
    if st.button("ออกจากระบบ"):
        st.session_state.user = ''
        st.rerun()

# หน้าห้องต่างๆ
elif st.session_state.page == 'red':
    set_theme("red")
    render_room('red', 'สีแดง')
elif st.session_state.page == 'blue':
    set_theme("blue")
    render_room('blue', 'สีน้ำเงิน')
elif st.session_state.page == 'green':
    set_theme("green")
    render_room('green', 'สีเขียว')
elif st.session_state.page == 'black':
    set_theme("black")
    render_room('black', 'สีดำ')
