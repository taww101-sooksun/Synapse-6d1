import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib

# --- 1. ตั้งค่า Firebase (ดึงจากโครงเดิมของคุณ) ---
if not firebase_admin._apps:
    try:
        cred_dict = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error("❌ กรุณาเช็คการตั้งค่า Firebase Secrets")
        st.stop()

db = firestore.client()

# --- 2. Helper Functions ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- 3. หน้า Login สุดเนี๊ยบ (The Vault) ---
def render_login():
    st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle, #001219 0%, #000000 100%); }
        .login-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(212, 175, 55, 0.3);
            padding: 50px; border-radius: 30px;
            backdrop-filter: blur(20px); text-align: center;
            box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        }
        .login-title {
            color: #FFD700; letter-spacing: 10px; font-weight: 900;
            text-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
        }
        /* ปรับแต่งปุ่มให้ดูแพง */
        .stButton>button {
            border-radius: 20px !important;
            border: 1px solid #D4AF37 !important;
            background: transparent !important;
            color: #D4AF37 !important;
            height: 45px; width: 100%;
        }
        .stButton>button:hover {
            background: #D4AF37 !important;
            color: black !important;
            box-shadow: 0 0 20px #D4AF37;
        }
        </style>
    """, unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-title">SYNAPSE</h1>', unsafe_allow_html=True)
        st.markdown("<p style='color:#555;'>SECURE ACCESS PROTOCOL</p>", unsafe_allow_html=True)
        
        u = st.text_input("IDENTIFIER", placeholder="Username", label_visibility="collapsed")
        p = st.text_input("ACCESS KEY", type="password", placeholder="Password", label_visibility="collapsed")
        
        st.write("") # เว้นวรรค
        if st.button("ENTER SYSTEM"):
            user_doc = db.collection('users').document(u).get()
            if user_doc.exists and user_doc.to_dict().get('pw') == hash_password(p):
                st.session_state.user = u
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("ACCESS DENIED: Invalid Credentials")
        
        st.markdown("<small style='color:#333;'>อยู่นิ่งๆ ไม่เจ็บตัว</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. หน้าหลัก (Home/Hub) ---
def render_home():
    st.markdown(f"<h2 style='color:#FFD700;'>Welcome, {st.session_state.user}</h2>", unsafe_allow_html=True)
    st.write("เลือกมิติที่คุณต้องการเข้าถึง:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔵 Blue: Voice Hub"):
            st.session_state.page = "blue"
            st.rerun()
    with col2:
        if st.button("🔴 Red: Media Zone"):
            st.session_state.page = "red"
            st.rerun()

    if st.button("🚪 Logout"):
        del st.session_state.user
        st.rerun()

# --- 5. Main Control Logic ---
if 'user' not in st.session_state:
    render_login()
else:
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    
    if st.session_state.page == "home":
        render_home()
    elif st.session_state.page == "blue":
        st.title("🔵 Blue Room Mode")
        if st.button("Back"): st.session_state.page = "home"; st.rerun()
        # เดี๋ยวเราจะเอาโค้ด Blue Room มาใส่ที่นี่ในขั้นตอนถัดไป
