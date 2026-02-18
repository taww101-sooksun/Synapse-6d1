import streamlit as st
import google.generativeai as genai
import time

# --- 0. INITIAL SETUP ---
st.set_page_config(page_title="SYNAPSE 6D : FINAL", layout="wide", initial_sidebar_state="collapsed")

# --- 1. FUNCTION: เพลงมัดมือฟัง (ลิขสิทธิ์คุณพี่ 60 เพลง) ---
def forced_therapy_radio():
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    st.markdown(f"""
        <div style="display:none;">
            <iframe src="https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1&mute=0" allow="autoplay"></iframe>
        </div>
        <div style="position: fixed; bottom: 10px; left: 10px; z-index: 9999; color: #00ff88; font-family: 'Orbitron'; font-size: 0.7em;">
            📡 ON AIR: อยู่นิ่งๆ ไม่เจ็บตัว Radio
        </div>
    """, unsafe_allow_html=True)

# --- 2. CSS: ปุ่มนูน 3D + สีสะท้อนแสง + ตัวหนังสือเรืองแสง ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Kanit:wght@300;500&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #ff0000, #00ff88, #0000ff, #ffff00, #ab47bc);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
        color: #fff; font-family: 'Kanit', sans-serif;
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

    /* ปุ่มนูนสะท้อนแสง 3D */
    .stButton>button {
        height: 80px !important; width: 100% !important;
        font-size: 24px !important; font-weight: 900 !important;
        border-radius: 20px !important; border: 4px solid rgba(255,255,255,0.4) !important;
        box-shadow: 8px 8px 20px rgba(0,0,0,0.6), inset -5px -5px 10px rgba(0,0,0,0.3) !important;
        transition: 0.2s; text-transform: uppercase;
    }
    .stButton>button:hover { transform: scale(1.02); filter: brightness(1.2); }
    
    /* สีห้องแต่ละห้อง */
    .btn-red button { background: #ff0000 !important; box-shadow: 0 0 30px #ff0000 !important; }
    .btn-blue button { background: #0000ff !important; box-shadow: 0 0 30px #0000ff !important; }
    .btn-green button { background: #00ff00 !important; color: black !important; box-shadow: 0 0 30px #00ff00 !important; }
    .btn-black button { background: #000000 !important; color: white !important; box-shadow: 0 0 30px #ffffff !important; }
    .btn-purple button { background: #ab47bc !important; box-shadow: 0 0 30px #ab47bc !important; }

    .neon-text { text-shadow: 0 0 10px #ab47bc, 0 0 20px #ab47bc, 0 0 30px #fff; font-family: 'Orbitron'; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "LANDING"
if 'user_id' not in st.session_state: st.session_state.user_id = "Ta101"
if 'current_dimension' not in st.session_state: st.session_state.current_dimension = "MAIN"
if 'purple_locked' not in st.session_state: st.session_state.purple_locked = True

forced_therapy_radio()

def go_to(dim_name):
    st.session_state.current_dimension = dim_name
    st.rerun()

# ==========================================
# หน้าแรก : LANDING (LOGO & LOGIN)
# ==========================================
if st.session_state.page == "LANDING":
    st.markdown("<h1 class='neon-text' style='text-align:center; font-size:5em;'>SYNAPSE 6D</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</h2>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        try: st.image("logo.jpg", width=250)
        except: st.info("🌐 [LOGO.JPG SPACE]")
        
        st.text_input("👤 Username:", value=st.session_state.user_id)
        st.text_input("🔑 Password:", type="password")
        if st.button("🚀 เข้าสู่มิติ"):
            st.session_state.page = "APP"
            st.rerun()

# ==========================================
# หน้าแอปหลัก : DIMENSION SELECTOR
# ==========================================
elif st.session_state.page == "APP":
    
    if st.session_state.current_dimension == "MAIN":
        st.markdown(f"<h2 class='neon-text'>USER: {st.session_state.user_id} 🔓</h2>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="btn-red">', unsafe_allow_html=True)
            if st.button("🔴 RED DIMENSION (FEED/ระบาย)"): go_to("RED")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="btn-green">', unsafe_allow_html=True)
            if st.button("🟢 GREEN DIMENSION (แชทลับ/หิมะ)"): go_to("GREEN")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_b:
            st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
            if st.button("🔵 BLUE DIMENSION (โทรฟรี/SOCIAL)"): go_to("BLUE")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="btn-purple">', unsafe_allow_html=True)
            if st.button("🟣 PURPLE DIMENSION (AI ปรับทุกข์)"): go_to("PURPLE")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="btn-black">', unsafe_allow_html=True)
        if st.button("⚫ BLACK DIMENSION (ศูนย์ควบคุม/โปรเจกต์)"): go_to("BLACK")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ห้องสีต่างๆ ---
    elif st.session_state.current_dimension == "RED":
        st.header("🔴 มิติแดง : Feed ความรู้สึก")
        st.text_area("✍️ ระบายออกมาให้สุด...")
        st.file_uploader("🖼️ โพสต์รูป/วิดีโอ")
        if st.button("⬅️ กลับหน้าหลัก"): go_to("MAIN")

    elif st.session_state.current_dimension == "BLUE":
        st.header("🔵 มิติน้ำเงิน : โทรฟรี & Social")
        st.button("☎️ กดเพื่อเริ่มสายโทรฟรีออนไลน์")
        st.markdown("---")
        st.write("ฟีดแชร์เรื่องราวสไตล์ Facebook...")
        if st.button("⬅️ กลับหน้าหลัก"): go_to("MAIN")

    elif st.session_state.current_dimension == "GREEN":
        st.header("🟢 มิติเขียว : แชทลับ & หิมะร่วง")
        st.snow() # หิมะร่วงตามสั่ง
        st.markdown("> **คู่มือ:** ห้องนี้เป็นความลับเฉพาะคุณและเพื่อนที่รู้ ID เท่านั้น")
        st.text_input("➕ ใส่ ID เพื่อน:")
        if st.button("🎇 ส่งดอกไม้ไฟ (Fireworks)"): st.balloons()
        if st.button("⬅️ กลับหน้าหลัก"): go_to("MAIN")

    elif st.session_state.current_dimension == "PURPLE":
        st.markdown("<h1 class='neon-text'>🟣 มิติม่วง : AI ดูดวง & ปรับทุกข์</h1>", unsafe_allow_html=True)
        if st.session_state.purple_locked:
            pw2 = st.text_input("🔐 รหัสลับชั้นที่ 2:", type="password")
            if st.button("ปลดล็อก"): st.session_state.purple_locked = False; st.rerun()
        else:
            st.write("AI: 'กวนนิดๆ แต่จริงใจ 100% จำได้ทุกคำที่คุยกันครับ'")
            st.text_area("เขียนถึง AI (ช่องใหญ่พิเศษ):", height=400)
            if st.button("⬅️ กลับหน้าหลัก"): st.session_state.purple_locked = True; go_to("MAIN")

    elif st.session_state.current_dimension == "BLACK":
        st.header("⚫ มิติดำ : Master Control")
        st.subheader("⚙️ ตั้งค่าโปรเจกต์ & เปลี่ยนชื่อ")
        st.text_input("ชื่อใหม่:", value=st.session_state.user_id)
        st.button("💾 บันทึกโปรเจกต์")
        if st.button("⬅️ กลับหน้าหลัก"): go_to("MAIN")

    if st.button("🚪 Logout"):
        st.session_state.page = "LANDING"
        st.session_state.current_dimension = "MAIN"
        st.rerun()
