import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time
import google.generativeai as genai

# --- 0. ตั้งค่าสมอง AI GEMINI (บ่ลืมกัน) ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    model = None

# --- ฟังก์ชันเล่นเสียงแจ้งเตือน (ความม่วนซื่น) ---
def play_notification_sound():
    audio_url = "https://www.soundjay.com/buttons/sounds/button-20.mp3"
    audio_html = f"""
        <iframe src="{audio_url}" allow="autoplay" style="display:none"></iframe>
        <audio autoplay><source src="{audio_url}" type="audio/mp3"></audio>
    """
    st.components.v1.html(audio_html, height=0)

# --- 1. SETTING & STYLE (งามคือเก่า) ---
st.set_page_config(page_title="Synapse Core", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { border-radius: 20px; border: 1px solid #444; background: #111; color: #00ff88; height: 3em; transition: 0.3s; width: 100%; font-weight: bold; }
    .stButton>button:hover { border-color: #00ff88; box-shadow: 0 0 20px #00ff88; color: white; }
    .dimension-card { background: rgba(255, 255, 255, 0.05); border: 1px solid #444; padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px; }
    .call-btn { background-color: #00d4ff !important; color: black !important; font-weight: bold !important; text-decoration: none; display: block; padding: 15px; border-radius: 12px; margin-top: 15px; transition: 0.3s; text-align: center; }
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

# --- 4. LOGIN (ดักความจำรายคน) ---
def show_login():
    st.markdown("<h1 style='text-align:center; color:#00ff88;'>🔒 SYNAPSE AUTH</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.info("กรุณาระบุชื่อเพื่อเชื่อมต่อลิ้นชักความทรงจำ...")
        user_input = st.text_input("ชื่อในมิติของคุณ:", value="Sooksun_Guest")
        if st.button("🚀 ENTER SYNAPSE"):
            st.session_state.user_name = user_input
            st.session_state.logged_in = True
            st.rerun()

# --- 5. HOME ---
def show_home():
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg", use_container_width=True)
        st.markdown("<h2 style='text-align:center; letter-spacing: 5px;'>SYNAPSE CORE</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#00ff88; font-size:22px;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)
    
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
        messages = db.collection(collection_name).order_by('time', direction='DESCENDING').limit(15).stream()
        for m in messages:
            d = m.to_dict()
            st.markdown(f"<div style='border-left: 3px solid {color_code}; padding-left:10px; margin-bottom:5px;'><b>{d.get('name')}</b>: {d.get('text')}</div>", unsafe_allow_html=True)

# --- 7. มิติพื้นฐาน ---
def show_dimension(name, color_code, glow_class):
    st.markdown(f"<h1 style='color:{color_code};'>{name} DIMENSION</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก"): navigate_to("home")
    st.markdown(f"<div class='dimension-card {glow_class}'>", unsafe_allow_html=True)
    simple_chat(f"chat_{name.lower()}", color_code)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 8. BLUE, 9. GREEN ---
def show_blue():
    st.markdown("<h1 style='color:#00d4ff;'>🔵 BLUE VOICE</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก"): navigate_to("home")
    room = st.text_input("รหัสช่องสัญญาณ:")
    if room:
        url = f"https://meet.jit.si/Synapse-{room}"
        st.markdown(f"<a href='{url}' target='_blank' class='call-btn'>📞 START CALL</a>", unsafe_allow_html=True)

def show_green():
    st.markdown("<h1 style='color:#00ff88;'>🟢 GREEN SECRET</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก"): navigate_to("home")
    simple_chat("messages", "#00ff88")

# --- 10. PURPLE (หัวใจสำคัญ: ความจำถาวรของใครของมัน) ---
def show_purple():
    st.markdown("<h1 style='color:#ab47bc;'>🟣 มิติพยากรณ์ & เพื่อนซี้</h1>", unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก"): navigate_to("home")
    
    # ดึงความจำเก่าของคนนี้
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
        except: history_context = "เพิ่งคุยกันครั้งแรก"

    st.markdown(f"""
        <div class='dimension-card purple-glow'>
            <h3 style='color:#ab47bc;'>🤖 AI: อยู่นิ้งๆไม่เจ็บตัว</h3>
            <p style='color:#888;'>สถานะ: จำคุณ <b>{st.session_state.user_name}</b> ได้แม่นยำ</p>
        </div>
    """, unsafe_allow_html=True)

    user_input = st.text_area("ปรึกษา / ดูดวง / เว้าพื้น :", placeholder="ระบายมาเพื่อน...")

    if st.button("🔮 ส่งสัญญาณปรึกษา"):
        if user_input:
            with st.status("🌀 กำลังค้นหาลิ้นชักความทรงจำ...", expanded=True) as s:
                try:
                    if model:
                        prompt = f"""คุณคือ AI เพื่อนสนิทชื่อ 'อยู่นิ้งๆไม่เจ็บตัว'
                        นี่คือสิ่งที่เคยคุยกับ {st.session_state.user_name}: {history_context}
                        เขาบอกว่า: {user_input}
                        จงตอบกลับด้วยภาษาเดียวกับเขา (ถ้าเขาส่งภาษาอีสานมาให้ตอบอีสานกวนๆ) 
                        สไตล์เพื่อนซี้ กวนตีนนิดๆ แต่จริงใจ และแสดงว่าจำเรื่องเก่าได้:"""
                        
                        response = model.generate_content(prompt)
                        ans = response.text if response else "มึนตึ้บ..."
                        
                        if db:
                            db.collection("ai_memories").add({
                                'user': st.session_state.user_name,
                                'chat_history': f"User: {user_input} | AI: {ans}",
                                'timestamp': datetime.now()
                            })
                    else: ans = "สมองกลยังไม่เชื่อมต่อคนับ"
                except Exception as e: ans = f"Error: {e}"
                
                st.markdown(f"**🤖 AI:** {ans}")
                s.update(label="บันทึกความจำเรียบร้อย!", state="complete")
            play_notification_sound()
            st.toast(f"จำเรื่องของ {st.session_state.user_name} ไว้แล้ว!")

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
