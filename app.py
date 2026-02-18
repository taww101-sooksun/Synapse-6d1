import streamlit as st
import numpy as np
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time
import io

# --- 0. CONFIGURATION & AI SETUP ---
# ใส่ API Key ของลูกพี่ใน Streamlit Secrets นะคนับ
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"AI Connection Error: {e}")
    model = None

# --- 1. THEME & CYBERPUNK CSS (แบบรกๆ เท่ๆ) ---
st.set_page_config(page_title="SYNAPSE 6D : CORE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Kanit:wght@300;500&display=swap');
    
    .stApp { background: radial-gradient(circle, #0f0f17 0%, #050505 100%); color: #e0e0e0; font-family: 'Kanit', sans-serif; }
    
    /* Header Style */
    .main-title { font-family: 'Orbitron', sans-serif; color: #00ff88; text-shadow: 0 0 20px #00ff88; text-align: center; font-size: 3em; margin-bottom: 0px; }
    .sub-title { text-align: center; color: #ffeb3b; font-size: 1.2em; letter-spacing: 2px; margin-bottom: 30px; }
    
    /* Dimension Buttons */
    .stButton>button { 
        border-radius: 10px; border: 2px solid #444; background: rgba(20,20,20,0.8); 
        color: #fff; height: 80px; transition: 0.4s; font-size: 1.2em; font-weight: bold;
        box-shadow: 5px 5px 0px #222;
    }
    .stButton>button:hover { border-color: #00ff88; transform: translate(-2px, -2px); box-shadow: 8px 8px 0px #00ff88; color: #00ff88; }
    
    /* Cards */
    .dimension-card { 
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255,255,255,0.1); 
        padding: 30px; border-radius: 25px; backdrop-filter: blur(10px); 
        margin-bottom: 25px; border-top: 5px solid #00ff88;
    }
    
    /* Specific Colors */
    .red-txt { color: #ff4b4b; } .blue-txt { color: #00d4ff; } .green-txt { color: #00ff88; } 
    .purple-txt { color: #ab47bc; } .gold-txt { color: #ffd700; }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #050505; }
    ::-webkit-scrollbar-thumb { background: #444; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #00ff88; }
    </style>
""", unsafe_allow_html=True)

# --- 2. FIREBASE ENGINE ---
@st.cache_resource
def init_db():
    if not firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets["firebase_service_account"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except: return None
    return firestore.client()

db = init_db()

# --- 3. SESSION MANAGEMENT ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user_name' not in st.session_state: st.session_state.user_name = ""

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 4. CORE FUNCTIONS (แบบรกๆ ครบเครื่อง) ---

def play_sound():
    audio_url = "https://www.soundjay.com/buttons/sounds/button-20.mp3"
    st.components.v1.html(f'<iframe src="{audio_url}" allow="autoplay" style="display:none"></iframe>', height=0)

def simple_chat(col_name, color):
    st.markdown(f"### 💬 กระดานสนทนามิติ <span style='color:{color}'>{col_name.upper()}</span>", unsafe_allow_html=True)
    if db:
        with st.form(f"f_{col_name}", clear_on_submit=True):
            msg = st.text_area("ระบายทิ้งไว้ในมิตินี้...", height=100)
            if st.form_submit_button("S E N D"):
                if msg:
                    db.collection(col_name).add({'user': st.session_state.user_name, 'msg': msg, 'time': datetime.now()})
                    st.rerun()
        
        msgs = db.collection(col_name).order_by('time', direction='DESCENDING').limit(15).stream()
        for m in msgs:
            d = m.to_dict()
            st.markdown(f"""<div style='border-left:4px solid {color}; padding:10px; background:rgba(255,255,255,0.05); margin-bottom:10px; border-radius:0 10px 10px 0;'>
                <small style='color:#888;'>{d.get('time').strftime('%H:%M:%S')}</small><br>
                <b style='color:{color}'>{d.get('user')}:</b> {d.get('msg')}
            </div>""", unsafe_allow_html=True)

# --- 5. UI PAGES ---

def login_page():
    st.markdown("<h1 class='main-title'>SYNAPSE 6D</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>CORE ACCESS SYSTEM v2.0</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        st.markdown("<div class='dimension-card'>", unsafe_allow_html=True)
        u = st.text_input("IDENTIFIER (ชื่อ):", value="Sooksun_User")
        p = st.text_input("ACCESS CODE (รหัสผ่านหลัก):", type="password")
        if st.button("🚀 INITIATE CONNECTION"):
            if p == "1234": # รหัสผ่านหลัก
                st.session_state.user_name = u
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("ACCESS DENIED: รหัสไม่ถูกต้อง")
        st.markdown("</div>", unsafe_allow_html=True)

def home_page():
    st.markdown("<h1 class='main-title'>CORE DIMENSIONS</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-title'>WELCOME, {st.session_state.user_name.upper()} | สโลแกน: \"อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='dimension-card'>", unsafe_allow_html=True)
    cols = st.columns(5)
    dims = [("🔴 RED", "red"), ("🔵 BLUE", "blue"), ("🟢 GREEN", "green"), ("⚫ BLACK", "black"), ("🟣 PURPLE", "purple")]
    for i, (name, target) in enumerate(dims):
        if cols[i].button(name): navigate_to(target)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ส่วนโชว์เคสความเก๋า
    st.info("💡 คำแนะนำ: มิติสีม่วงคือส่วนของสมอง AI ที่มีความจำยาวนานที่สุด โปรดใช้ด้วยความระมัดระวัง")

def purple_dimension():
    st.markdown("<h1 style='color:#ab47bc; text-align:center;'>🟣 PURPLE : AI THERAPY สมองส่วนลึก</h1>", unsafe_allow_html=True)
    if st.button("⬅️ BACK TO CORE"): navigate_to("home")
    
    st.markdown("<div class='dimension-card' style='border-color:#ab47bc;'>", unsafe_allow_html=True)
    p_code = st.text_input("🔑 PRIVATE KEY (รหัสลับความจำส่วนตัว):", type="password", help="รหัสนี้จะใช้ล็อกลิ้นชักความทรงจำของคุณ")
    
    if p_code:
        history = ""
        if db:
            try:
                memories = db.collection("memories").where("user","==",st.session_state.user_name).where("p_code","==",p_code).order_by("time", direction="DESCENDING").limit(5).stream()
                h_list = [f"อดีต: {m.to_dict().get('chat')}" for m in memories]
                h_list.reverse()
                history = "\n".join(h_list)
            except: pass

        st.success("🔓 ลิ้นชักความทรงจำถูกปลดล็อกแล้ว")
        u_input = st.text_area("ระบายความในใจ หรือเล่าความฝันให้ 'อยู่นิ้งๆ' ฟัง:", height=150)
        
        if st.button("🔮 SYNC WITH AI"):
            if u_input and model:
                with st.spinner("🌀 กำลังปรับจูนคลื่นสมอง..."):
                    prompt = f"คุณคือ AI เพื่อนสนิทชื่อ 'อยู่นิ้งๆไม่เจ็บตัว' สโลแกนคือ 'อยู่นิ่งๆ ไม่เจ็บตัว' อดีตที่เคยคุยกัน: {history} \nเพื่อนระบายว่า: {u_input} \nตอบกลับแบบเพื่อนที่เข้าใจโลก กวนนิดๆ แต่เน้นบำบัดจิตใจ:"
                    response = model.generate_content(prompt)
                    ans = response.text
                    if db:
                        db.collection("memories").add({
                            'user': st.session_state.user_name, 'p_code': p_code,
                            'chat': f"User: {u_input} | AI: {ans}", 'time': datetime.now()
                        })
                    st.markdown(f"<div style='background:#222; padding:20px; border-radius:15px; border-left:5px solid #ab47bc;'><b>🤖 AI:</b><br>{ans}</div>", unsafe_allow_html=True)
                    play_sound()
    else:
        st.warning("🔒 กรุณาระบุรหัสลับเพื่อเรียกคืนความทรงจำ")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. MAIN ROUTING ---
if not st.session_state.logged_in:
    login_page()
else:
    p = st.session_state.page
    if p == "home": home_page()
    elif p == "purple": purple_dimension()
    elif p == "blue": 
        st.title("🔵 BLUE : VOICE HUB")
        if st.button("Back"): navigate_to("home")
        sec = st.text_input("รหัสห้อง (9999):", type="password")
        if sec == "9999": simple_chat("blue_room", "#00d4ff")
    elif p == "green":
        st.title("🟢 GREEN : SECRET CHAT")
        if st.button("Back"): navigate_to("home")
        sec = st.text_input("รหัสห้อง (8888):", type="password")
        if sec == "8888": simple_chat("green_room", "#00ff88")
    elif p in ["red", "black"]:
        color = "#ff4b4b" if p == "red" else "#ffffff"
        st.markdown(f"<h1 style='color:{color};'>{p.upper()} DIMENSION</h1>", unsafe_allow_html=True)
        if st.button("Back"): navigate_to("home")
        simple_chat(f"public_{p}", color)

# --- END OF CODE ---
