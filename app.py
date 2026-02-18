import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time
import google.generativeai as genai

# --- 0. ตั้งค่าสมอง AI GEMINI ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # เลือกโมเดลที่เสถียรที่สุด
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    model = None

# --- ฟังก์ชันเล่นเสียงแจ้งเตือน ---
def play_notification_sound():
    audio_url = "https://www.soundjay.com/buttons/sounds/button-20.mp3"
    audio_html = f"""
        <iframe src="{audio_url}" allow="autoplay" style="display:none"></iframe>
        <audio autoplay><source src="{audio_url}" type="audio/mp3"></audio>
    """
    st.components.v1.html(audio_html, height=0)

# --- 1. SETTING & STYLE ---
st.set_page_config(page_title="Synapse Core", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { border-radius: 20px; border: 1px solid #444; background: #111; color: #00ff88; height: 3em; transition: 0.3s; width: 100%; font-weight: bold; }
    .stButton>button:hover { border-color: #00ff88; box-shadow: 0 0 20px #00ff88; color: white; }
    .dimension-card { background: rgba(255, 255, 255, 0.05); border: 1px solid #444; padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px; }
    .purple-glow { border-color: #ab47bc !important; box-shadow: 0 0 15px #ab47bc; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATABASE ---
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

# --- 3. SESSION & NAV ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user_name' not in st.session_state: st.session_state.user_name = "Synapse_User"

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 4. LOGIN ---
def show_login():
    st.markdown("<h1 style='text-align:center; color:#00ff88;'>🔒 SYNAPSE AUTH</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.info("กรุณาระบุตัวตนเพื่อเชื่อมต่อระบบความทรงจำ...")
        user_input = st.text_input("ระบุชื่อในมิติของคุณ (ใช้ชื่อเดิมเพื่อดึงความจำ):", value="Sooksun_Guest")
        if st.button("🚀 ENTER SYNAPSE"):
            st.session_state.user_name = user_input
            st.session_state.logged_in = True
            st.rerun()

# --- 5. HOME ---
def show_home():
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg", use_container_width=True)
        st.markdown("<h2 style='text-align:center;'>SYNAPSE CORE</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#00ff88;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)
    
    st.divider()
    st.write("### 🌐 เลือกมิติที่ต้องการเชื่อมต่อ")
    m1, m2, m3, m4, m5 = st.columns(5)
    if m1.button("🔴 RED"): navigate_to("red")
    if m2.button("🔵 BLUE"): navigate_to("blue")
    if m3.button("🟢 GREEN"): navigate_to("green")
    if m4.button("⚫ BLACK"): navigate_to("black")
    if m5.button("🟣 PURPLE"): navigate_to("purple")

# --- 6. แชทมิติทั่วไป ---
def simple_chat(collection_name, color_code):
    st.markdown(f"### 💬 แชทมิติ {collection_name.upper()}")
    if db:
        with st.form(f"form_{collection_name}", clear_on_submit=True):
            msg = st.text_input("พิมพ์ข้อความ...")
            if st.form_submit_button("SEND"):
                if msg:
                    db.collection(collection_name).add({
                        'name': st.session_state.user_name, 
                        'text': msg, 
                        'time': datetime.now()
                    })
                    st.rerun()
        messages = db.collection(collection_name).order_by('time', direction='DESCENDING').limit(10).stream()
        for m in messages:
            d = m.to_dict()
            st.markdown(f"<div style='border-left: 3px solid {color_code}; padding-left:10px;'><b>{d.get('name')}</b>: {d.get('text')}</div>", unsafe_allow_html=True)

# --- 7. มิติม่วง (AI ความจำถาวรของใครของมัน) ---
def show_purple():
    st.markdown("<h1 style='color:#ab47bc;'>🟣 มิติพยากรณ์ & เพื่อนซี้</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก"): navigate_to("home")
    
    # --- ดึงความจำเก่าจาก Firestore ---
    history_context = ""
    if db:
        try:
            memories = db.collection("ai_memories") \
                         .where("user", "==", st.session_state.user_name) \
                         .order_by("timestamp", direction="DESCENDING") \
                         .limit(5).stream()
            history_list = [m.to_dict().get('chat_history') for m in memories]
            history_list.reverse()
            history_context = "\n".join(history_list)
        except:
            history_context = "เพิ่งคุยกันครั้งแรก"

    st.markdown(f"<div class='dimension-card purple-glow'><h3>🤖 AI: อยู่นิ้งๆไม่เจ็บตัว</h3><p>สถานะ: จำคุณ <b>{st.session_state.user_name}</b> ได้แม่นยำ</p></div>", unsafe_allow_html=True)

    user_input = st.text_area("อยากระบายอะไร หรือถามดวง จัดมาเลยเพื่อน:")

    if st.button("🔮 ส่งสัญญาณปรึกษา"):
        if user_input:
            with st.status("🌀 กำลังรื้อฟื้นความทรงจำ...", expanded=True) as s:
                try:
                    if model:
                        prompt = f"""คุณคือ AI เพื่อนสนิทชื่อ 'อยู่นิ้งๆไม่เจ็บตัว' 
                        อดีตที่เคยคุยกับคนนี้: {history_context}
                        เขากำลังพูดว่า: {user_input}
                        ตอบกลับแบบเพื่อนซี้ กวนตีนนิดๆ แต่จริงใจ และแสดงว่าจำเรื่องเก่าได้ถ้าเกี่ยวกัน:"""
                        
                        response = model.generate_content(prompt)
                        ans = response.text if response else "มึนตึ้บ..."
                        
                        if db:
                            db.collection("ai_memories").add({
                                'user': st.session_state.user_name,
                                'chat_history': f"User: {user_input} | AI: {ans}",
                                'timestamp': datetime.now()
                            })
                    else: ans = "สมองกลไม่เชื่อมต่อ"
                except Exception as e: ans = f"Error: {e}"
                
                st.markdown(f"**🤖 AI:** {ans}")
                s.update(label="จดจำเรียบร้อย!", state="complete")
            play_notification_sound()
            st.toast("บันทึกความจำแล้ว!")

# --- 8. มิติอื่นๆ ---
def show_blue():
    st.markdown("<h1 style='color:#00d4ff;'>🔵 BLUE VOICE</h1>")
    if st.button("⬅️ กลับหน้าหลัก"): navigate_to("home")
    room = st.text_input("รหัสช่องสัญญาณ:")
    if room: st.markdown(f"<a href='https://meet.jit.si/Synapse-{room}' target='_blank' class='call-btn'>📞 START CALL</a>", unsafe_allow_html=True)

def show_green():
    st.markdown("<h1 style='color:#00ff88;'>🟢 GREEN SECRET</h1>")
    if st.button("⬅️ กลับหน้าหลัก"): navigate_to("home")
    simple_chat("messages", "#00ff88")

# --- MAIN CONTROL ---
if not st.session_state.logged_in:
    show_login()
else:
    p = st.session_state.page
    if p == "home": show_home()
    elif p == "blue": show_blue()
    elif p == "green": show_green()
    elif p == "purple": show_purple()
    elif p == "red": show_dimension("RED", "#ff4b4b", "red-glow")
    elif p == "black": show_dimension("BLACK", "#ffffff", "black-glow")
