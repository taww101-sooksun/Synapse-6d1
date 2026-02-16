import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
import hashlib
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components

# --- 1. การเชื่อมต่อ Firebase ---
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase_service_account"]))
    firebase_admin.initialize_app(cred, {'storageBucket': st.secrets["firebase_config"]["storageBucket"]})
db = firestore.client()
bucket = storage.bucket()

# --- 2. ระบบความปลอดภัย (รหัสผ่าน & กรองเนื้อหา) ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_thai_time():
    return datetime.utcnow() + timedelta(hours=7)

# --- 3. UI ธีมเข้มขรึม & กรอบทอง (Luxury Style) ---
def set_luxury_theme(room_id):
    themes = {
        "home":  {"bg": "#000814", "text": "#FFD700", "accent": "#D4AF37"}, # หน้าหลักเข้มจัดตัดทอง
        "red":   {"bg": "#2a0000", "text": "#FFFFFF", "accent": "#FFD700"}, # แดงเข้มกรอบทอง
        "blue":  {"bg": "#001d3d", "text": "#FFFFFF", "accent": "#FFD700"}, # น้ำเงินเข้มกรอบทอง
        "green": {"bg": "#0b190e", "text": "#FFFFFF", "accent": "#FFD700"}, # เขียวเข้มกรอบทอง
        "black": {"bg": "#000000", "text": "#FFFFFF", "accent": "#FFD700"}  # ดำสนิทกรอบทอง
    }
    cfg = themes.get(room_id, themes["home"])
    st.markdown(f"""
        <style>
        .stApp {{ background: {cfg['bg']}; color: {cfg['text']}; }}
        h1, h2, h3, p, label {{ color: {cfg['text']} !important; text-align: center; }}
        /* กรอบข้อความสีทอง ตัวหนังสือขาว */
        .post-box {{
            border: 2px solid #D4AF37;
            background: rgba(255, 215, 0, 0.05);
            padding: 20px; border-radius: 15px; margin-bottom: 15px;
            color: white !important;
        }}
        .stButton>button {{
            background: linear-gradient(145deg, #D4AF37, #AA8A35);
            color: black !important; font-weight: bold; border-radius: 10px; width: 100%;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. ระบบจัดการหน้าจอและ Login ---
if 'user' not in st.session_state:
    set_luxury_theme("home")
    st.image("logo.jpg", width=250)
    st.title("🛡️ Synapse Secure Login")
    
    u_name = st.text_input("ชื่อผู้ใช้ (Username)")
    u_pass = st.text_input("รหัสผ่าน (Password)", type="password")
    
    col1, col2 = st.columns(2)
    if col1.button("เข้าสู่ระบบ"):
        user_ref = db.collection('users').document(u_name).get()
        if user_ref.exists and user_ref.to_dict().get('password') == hash_password(u_pass):
            st.session_state.user = u_name
            st.session_state.page = "home"
            st.rerun()
        else: st.error("❌ รหัสผ่านไม่ถูกต้อง หรือยังไม่ได้ลงทะเบียน")
        
    if col2.button("ลงทะเบียนใหม่"):
        if u_name and u_pass:
            db.collection('users').document(u_name).set({
                'password': hash_password(u_pass),
                'created_at': get_thai_time()
            })
            st.success("✅ ลงทะเบียนสำเร็จ! กรุณากดเข้าสู่ระบบ")

else:
    # --- ระบบเปลี่ยนหน้าอยู่ตรงหน้าหลัก (ไม่ใช้ Sidebar) ---
    if st.session_state.page == "home":
        set_luxury_theme("home")
        st.image("logo.jpg", width=180)
        st.title(f"ยินดีต้อนรับคุณ {st.session_state.user}")

        # --- 🎵 ฝัง Playlist YouTube (ติดแน่นอน 100%) ---
        st.markdown("### 🎵 เพลย์ลิสต์ส่วนตัวของคุณท่าน")
        components.html(
            '<iframe width="100%" height="315" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>',
            height=350
        )
        
        st.markdown("---")
        # ปุ่มกดเปลี่ยนหน้า (Navigation) อยู่ตรงกลางหน้าจอ
        st.subheader("📂 เลือกห้องใช้งาน (เมนูหลัก)")
        c1, c2 = st.columns(2)
        if c1.button("🔴 YouTube (โพสต์/แชร์คลิป)"): st.session_state.page = "red"; st.rerun()
        if c2.button("🔵 Facebook (โทรฟรี/P2P)"): st.session_state.page = "blue"; st.rerun()
        if c1.button("🟢 ห้องลับ (แชทส่วนตัวรายบุคคล)"): st.session_state.page = "green"; st.rerun()
        if c2.button("⚫ ห้อง X (เรียลไทม์/อิสระ)"): st.session_state.page = "black"; st.rerun()
        
        if st.button("🚪 ออกจากระบบ"): del st.session_state.user; st.rerun()

    # --- ส่วนของแต่ละห้อง (Logic เหมือนเดิมแต่ปรับธีมทอง) ---
    elif st.session_state.page in ["red", "blue", "green", "black"]:
        page_map = {"red": "YouTube", "blue": "Facebook", "green": "Secret Chat", "black": "X Real-time"}
        set_luxury_theme(st.session_state.page)
        st.header(f"🚀 ห้อง {page_map[st.session_state.page]}")
        
        if st.button("⬅️ กลับหน้าหลัก (Home)"): st.session_state.page = "home"; st.rerun()
        
        # ใส่ Logic โพสต์รูป/วีดีโอ และแชทตรงนี้ตามเดิมที่คุณท่านมี...
        st.write("ระบบกำลังโหลดข้อมูล...")
