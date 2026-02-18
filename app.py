import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, firestore, storage

# --- 1. ระบบ 6 ภาษา (ของจริงที่คุณพี่คัดมา) ---
translations = {
    "app_title": {"en": "SYNAPSE 6D", "th": "SYNAPSE 6D", "lo": "SYNAPSE 6D", "my": "SYNAPSE 6D", "zh": "SYNAPSE 6D", "ja": "SYNAPSE 6D"},
    "welcome": {"en": "Welcome", "th": "ยินดีต้อนรับ", "lo": "ຍິນດີຕ້ອນຮັບ", "my": "ကြိုဆိုပါတယ်", "zh": "欢迎", "ja": "ようこそ"},
    "login_btn": {"en": "Login", "th": "ยืนยันรหัสเข้าสู่มิติ", "lo": "ເຂົ້າສູ່ມິຕິ", "my": "ရှုထောင့်ထဲသို့ဝင်ရန်", "zh": "登录", "ja": "ログイン"}
    # (... ดึงค่า translations เดิมที่คุณพี่โพสต์ไว้มาใส่ให้ครบตรงนี้ ...)
}

def get_text(key):
    lang = st.session_state.get('lang', 'th')
    return translations.get(key, {}).get(lang, translations.get(key, {}).get("th", key))

# --- 2. ตั้งค่า FIREBASE (ของจริงสำหรับห้องแดง/น้ำเงิน) ---
if not firebase_admin._apps:
    try:
        # ใช้ secrets จาก streamlit สำหรับของจริง
        cred = credentials.Certificate(st.secrets["firebase"])
        firebase_admin.initialize_app(cred, {'storageBucket': f"{st.secrets['firebase']['project_id']}.appspot.com"})
        db = firestore.client()
        bucket = storage.bucket()
    except:
        st.error("ระบบฐานข้อมูลยังไม่ได้เชื่อมต่อ (โปรดเช็คไฟล์ secrets)")

# --- 3. CSS ปุ่มนูนสะท้อนแสง (แบบที่คุณพี่ชอบ) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #ff0000, #00ff88, #0000ff, #ffff00, #ab47bc); background-size: 400% 400%; animation: gradient 10s infinite; }
    .stButton>button { 
        height: 80px !important; width: 100% !important; font-size: 22px !important; 
        border-radius: 15px !important; border: 4px solid #fff !important;
        box-shadow: 0 0 20px rgba(255,255,255,0.5) !important;
        background: rgba(0,0,0,0.8) !important; color: #fff !important;
    }
    /* ปุ่มเรืองแสงแยกตามสีห้อง */
    .btn-red button { border-color: #ff0000 !important; box-shadow: 0 0 30px #ff0000 !important; }
    .btn-blue button { border-color: #0000ff !important; box-shadow: 0 0 30px #0000ff !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. ฟังก์ชันเพลง (ห้ามดับ) ---
def forced_therapy_radio():
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    st.markdown(f'<iframe src="https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1&mute=0" style="display:none;"></iframe>', unsafe_allow_html=True)

# --- เริ่มการทำงาน ---
forced_therapy_radio()

if 'page' not in st.session_state: st.session_state.page = "LANDING"

# หน้าแรก
if st.session_state.page == "LANDING":
    st.markdown("<h1 style='text-align:center;'>SYNAPSE 6D</h1>", unsafe_allow_html=True)
    st.image("logo.jpg", width=200) # โลโก้จริง
    lang = st.selectbox("🌐 เลือกภาษา", ["th", "en", "lo", "my", "zh", "ja"])
    st.session_state.lang = lang
    if st.button(get_text("login_btn")):
        st.session_state.page = "MAIN"
        st.rerun()

# หน้าหลัก (ห้องต่างๆ)
elif st.session_state.page == "MAIN":
    st.markdown(f"### {get_text('welcome')}คุณ Ta101")
    # ปุ่มมิติแดง (ระบาย)
    st.markdown('<div class="btn-red">', unsafe_allow_html=True)
    if st.button("🔴 RED ROOM (FIREBASE FEED)"):
        st.session_state.page = "RED"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ปุ่มมิติเขียว (ลับ)
    if st.button("🟢 GREEN ROOM (SECRET CHAT)"):
        st.snow() # หิมะร่วงของจริง
        st.balloons() # ดอกไม้ไฟ
