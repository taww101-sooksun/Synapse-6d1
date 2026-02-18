import streamlit as st
import google.generativeai as genai
import time

# --- 0. INITIAL SETUP ---
st.set_page_config(page_title="SYNAPSE 6D : CORE", layout="wide", initial_sidebar_state="collapsed")

# --- 1. FUNCTION: เครื่องเล่นเพลงมัดมือฟัง (หมัดเด็ด 2 หมื่นวิว) ---
def forced_therapy_radio():
    # ใช้ ID เพลย์ลิสต์ 60 เพลงของลูกพี่
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO" 
    
    st.markdown(f"""
        <div style="display:none;">
            <iframe 
                src="https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1&mute=0" 
                allow="autoplay">
            </iframe>
        </div>
        <div style="position: fixed; top: 10px; right: 10px; z-index: 1000; opacity: 0.6;">
            <p style="color: #00ff88; font-size: 0.6em; font-family: 'Orbitron';">
                📡 THERAPY STREAMING... (CONNECTED)
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- 2. CYBERPUNK CSS (ตกแต่งหน้าตา) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Kanit:wght@300;500&display=swap');
    .stApp { background: #050505; color: #e0e0e0; font-family: 'Kanit', sans-serif; }
    .logo-container { text-align: center; padding: 10px; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 0.8; } 50% { opacity: 1; text-shadow: 0 0 30px #ab47bc; } 100% { opacity: 0.8; } }
    .main-logo { font-family: 'Orbitron', sans-serif; font-size: 4em; font-weight: 900; background: linear-gradient(45deg, #ab47bc, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
    .setup-card { background: #111; border: 2px solid #ab47bc; padding: 20px; border-radius: 20px; box-shadow: 0 0 30px rgba(171, 71, 188, 0.2); }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE (ระบบความจำแอป) ---
if 'app_locked' not in st.session_state: st.session_state.app_locked = True
if 'current_room' not in st.session_state: st.session_state.current_room = "MAIN"
if 'user_id' not in st.session_state: st.session_state.user_id = "Ta101" # ตามรูป
if 'master_key' not in st.session_state: st.session_state.master_key = ""

# รันเพลงมัดมือฟังทันที
forced_therapy_radio()

# --- 4. หน้า LANDING PAGE (หน้าแรก/ตั้งรหัส) ---
if st.session_state.app_locked:
    st.markdown("<div class='logo-container'><h1 class='main-logo'>SYNAPSE 6D</h1></div>", unsafe_allow_html=True)
    with st.container():
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("<div class='setup-card'>", unsafe_allow_html=True)
            st.subheader("🔑 ตั้งรหัสผ่านมิติของคุณ")
            new_id = st.text_input("👤 ชื่อของคุณ:", value=st.session_state.user_id, key="input_id")
            new_key = st.text_input("🔒 รหัสผ่านเข้าใช้งาน:", type="password", key="input_pass")
            if st.button("🚀 ยืนยันเริ่มระบบบำบัด", use_container_width=True):
                if new_id and new_key:
                    st.session_state.user_id = new_id
                    st.session_state.master_key = new_key
                    st.session_state.app_locked = False
                    st.rerun() # ปลดล็อกเข้าหน้าหลัก
                else:
                    st.error("ใส่ข้อมูลให้ครบก่อนคนับ!")
            st.markdown("</div>", unsafe_allow_html=True)

# --- 5. MAIN INTERFACE (หลังปลดล็อกเข้าสู่มิติ) ---
else:
    # ส่วนหัวโชว์ชื่อ User
    st.markdown(f"<h2 style='text-align:right; color:#ab47bc; font-family:Orbitron;'>USER: {st.session_state.user_id} 🔓</h2>", unsafe_allow_html=True)

    # เช็กว่าต้องแสดงหน้าจอของห้องไหน
    if st.session_state.current_room == "MAIN":
        tab1, tab2, tab3 = st.tabs(["🌌 มิติทั้งหมด", "⚙️ เปลี่ยนรหัส", "🎵 เครื่องเล่นเพลง"])
        
        with tab1:
            st.markdown("### 🌈 เลือกมิติที่ต้องการบำบัด")
            st.info(f"ยินดีต้อนรับคุณ {st.session_state.user_id} เข้าสู่ระบบหลัก")
            
            # ปุ่มเข้าห้องสีต่างๆ
            if st.button("🔴 เข้าสู่มิติแดง (Vent)", use_container_width=True):
                st.session_state.current_room = "RED"
                st.rerun()
                
            if st.button("🟣 เข้าสู่มิติม่วง (Deep Memory)", use_container_width=True):
                st.session_state.current_room = "PURPLE"
                st.rerun()

    # หน้ามิติสีแดง
    elif st.session_state.current_room == "RED":
        st.markdown("<h2 style='color:#ff4b4b;'>🔴 มิติสีแดง : พื้นที่ระบายความในใจ</h2>", unsafe_allow_html=True)
        st.text_area("ระบายทุกอย่างที่อัดอั้นออกมาที่นี่...", height=250)
        if st.button("⬅️ กลับสู่หน้ามิติหลัก"):
            st.session_state.current_room = "MAIN"
            st.rerun()

    # หน้ามิติสีม่วง
    elif st.session_state.current_room == "PURPLE":
        st.markdown("<h2 style='color:#ab47bc;'>🟣 มิติสีม่วง : สมองส่วนลึก</h2>", unsafe_allow_html=True)
        st.write("คุยกับ AI บำบัดส่วนตัวของคุณที่นี่...")
        # (ลูกพี่เอาโค้ดคุยกับ AI มาวางต่อตรงนี้ได้เลย)
        if st.button("⬅️ กลับสู่หน้ามิติหลัก"):
            st.session_state.current_room = "MAIN"
            st.rerun()

    st.markdown("---")
    if st.button("🚪 LOGOUT (ออกจากมิติ)", use_container_width=True):
        st.session_state.app_locked = True
        st.session_state.current_room = "MAIN"
        st.rerun()
