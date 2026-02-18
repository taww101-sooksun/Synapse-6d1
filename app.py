import streamlit as st
import google.generativeai as genai
import time

# --- 0. INITIAL SETUP ---
st.set_page_config(page_title="SYNAPSE 6D : CORE", layout="wide", initial_sidebar_state="collapsed")

# --- 1. FUNCTION: เครื่องเล่นเพลงมัดมือฟัง (หมัดเด็ด) ---
def forced_therapy_radio():
    # ใช้ ID เพลย์ลิสต์ของลูกพี่
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
    
    /* Logo Animation */
    .logo-container { text-align: center; padding: 10px; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 0.8; } 50% { opacity: 1; text-shadow: 0 0 30px #ab47bc; } 100% { opacity: 0.8; } }
    
    .main-logo { font-family: 'Orbitron', sans-serif; font-size: 4em; font-weight: 900; background: linear-gradient(45deg, #ab47bc, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
    
    .setup-card { background: #111; border: 2px solid #ab47bc; padding: 20px; border-radius: 20px; box-shadow: 0 0 30px rgba(171, 71, 188, 0.2); }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE (ระบบจำตัวตน) ---
if 'app_locked' not in st.session_state: st.session_state.app_locked = True
if 'master_key' not in st.session_state: st.session_state.master_key = ""
if 'user_id' not in st.session_state: st.session_state.user_id = ""

# รันเพลงทันที
forced_therapy_radio()

# --- 4. หน้า LANDING PAGE (หน้าแรก) ---
if st.session_state.app_locked:
    st.markdown("<div class='logo-container'><h1 class='main-logo'>SYNAPSE 6D</h1></div>", unsafe_allow_html=True)
    
    with st.container():
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("<div class='setup-card'>", unsafe_allow_html=True)
            st.subheader("🔑 ตั้งรหัสผ่านมิติของคุณ")
            
            new_id = st.text_input("👤 ชื่อของคุณ:", value="Ta101", key="input_id")
            new_key = st.text_input("🔒 รหัสผ่านเข้าใช้งาน:", type="password", key="input_pass")
            
            if st.button("🚀 ยืนยันเริ่มระบบบำบัด", use_container_width=True):
                if new_id and new_key:
                    st.session_state.user_id = new_id
                    st.session_state.master_key = new_key
                    st.session_state.app_locked = False
                    st.success("กำลังเชื่อมต่อสัญญาณ...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("ใส่ข้อมูลให้ครบก่อนคนับหัวหน้า!")
            st.markdown("</div>", unsafe_allow_html=True)

    # คู่มือแบบย่อ
    with st.expander("📖 คู่มือการเข้าแต่ละห้องสี"):
        st.write("🔴 RED: ห้องระบายอารมณ์ | 🔵 BLUE: เครื่องเล่นเพลง | 🟣 PURPLE: AI สมองส่วนลึก")

# --- 5. MAIN INTERFACE (หลังปลดล็อกเข้าสู่มิติ) ---
else:
    # แสดงหัวแอป
    st.markdown(f"<h2 style='text-align:right; color:#ab47bc;'>USER: {st.session_state.user_id} 🔓</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🌌 มิติทั้งหมด", "⚙️ เปลี่ยนรหัส", "🎵 เครื่องเล่นเพลง"])
    
    with tab1:
        st.markdown("### 🌈 เลือกมิติที่ต้องการบำบัด")
        st.info(f"ยินดีต้อนรับคุณ {st.session_state.user_id} เข้าสู่ระบบหลัก")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔴 เข้าสู่มิติแดง (Vent)", use_container_width=True):
                st.write("พื้นที่สำหรับระบายความในใจ...")
        with col_b:
            if st.button("🟣 เข้าสู่มิติม่วง (Deep Memory)", use_container_width=True):
                st.write("AI กำลังดึงความจำเรื่องฝันขึ้นมา...")

    with tab2:
        st.markdown("### 🔐 จัดการรหัสผ่าน")
        old_pass = st.text_input("ยืนยันรหัสเดิม:", type="password")
        update_key = st.text_input("ตั้งรหัสใหม่:", type="password")
        if st.button("ยืนยันการเปลี่ยนรหัส"):
            if old_pass == st.session_state.master_key:
                st.session_state.master_key = update_key
                st.success("เปลี่ยนรหัสสำเร็จ!")
            else:
                st.error("รหัสเดิมไม่ถูกต้อง!")

    with tab3:
        st.markdown("### 📻 SYNAPSE RADIO")
        st.write("เพลงบำบัด 60 เพลงของลูกพี่กำลังเล่นอยู่เบื้องหลัง...")
        st.info("ระบบมัดมือฟังทำงานอยู่... หลับตาฟังแล้วปล่อยใจไปครับ")

    st.markdown("---")
    if st.button("🚪 LOGOUT (ออกจากมิติ)"):
        st.session_state.app_locked = True
        st.rerun()
