import streamlit as st
import google.generativeai as genai
import time
import streamlit as st
import google.generativeai as genai

# --- 1. ส่วนฟังก์ชันเครื่องเล่นเพลง (วางไว้ตรงนี้) ---
def forced_therapy_radio():
    # ใช้ ID เพลย์ลิสต์ของลูกพี่อันนี้ครับ
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

# --- 2. ส่วนรันโปรแกรม ---
# เรียกใช้ทันทีเพื่อให้เพลงดังตั้งแต่หน้าแรก
forced_therapy_radio()

# ต่อด้วยโค้ดหน้าด่าน (Landing Page) ที่เราคุยกันไว้
if 'app_locked' not in st.session_state:
    st.session_state.app_locked = True

# ... โค้ดส่วนที่เหลือของลูกพี่ ...

# --- 0. INITIAL SETUP & GLOBAL MUSIC ---
st.set_page_config(page_title="SYNAPSE 6D : CORE", layout="wide", initial_sidebar_state="collapsed")

# ระบบเครื่องเล่นเพลงแบบ Global (ดังทุกห้อง)

# --- 1. CYBERPUNK CSS (รกๆ เท่ๆ มีโลโก้) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Kanit:wght@300;500&display=swap');
    
    .stApp { background: #050505; color: #e0e0e0; font-family: 'Kanit', sans-serif; }
    
    /* Logo Animation */
    .logo-container { text-align: center; padding: 20px; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 0.8; } 50% { opacity: 1; text-shadow: 0 0 30px #ab47bc; } 100% { opacity: 0.8; } }
    
    .main-logo { font-family: 'Orbitron', sans-serif; font-size: 5em; font-weight: 900; background: linear-gradient(45deg, #ab47bc, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    
    .dimension-box {
        background: rgba(255,255,255,0.05); border: 1px solid #333; padding: 20px; border-radius: 15px; margin-bottom: 20px;
        transition: 0.3s; border-left: 5px solid #444;
    }
    .dimension-box:hover { background: rgba(255,255,255,0.1); border-color: #ab47bc; }
    
    .setup-card { background: #111; border: 2px solid #ab47bc; padding: 30px; border-radius: 20px; box-shadow: 0 0 50px rgba(171, 71, 188, 0.2); }
    </style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE (จำรหัสที่ตั้งเอง) ---
if 'app_locked' not in st.session_state: st.session_state.app_locked = True
if 'master_key' not in st.session_state: st.session_state.master_key = ""
if 'user_id' not in st.session_state: st.session_state.user_id = ""

# --- ปรับปรุงหน้า Landing Page ให้ปุ่มอยู่สูงขึ้น ---
if st.session_state.app_locked:
    forced_therapy_radio() # เพลงยังดังต่อเนื่อง
    
    # ใช้ Container บีบให้ทุกอย่างอยู่กลางจอ
    with st.container():
        st.markdown("<h1 style='text-align:center; color:#ab47bc; font-family:Orbitron;'>SYNAPSE 6D</h1>", unsafe_allow_html=True)
        
        # ลดช่องว่างเพื่อให้ปุ่มลอยขึ้นมา
        new_id = st.text_input("👤 ชื่อของคุณ:", value="Ta101", key="input_id") # ตั้งค่าเริ่มต้นตามรูป
        new_key = st.text_input("🔑 รหัสผ่าน:", type="password", key="input_pass")
        
        # ใช้ Column เพื่อให้ปุ่มดูเด่นและกดง่าย
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 ยืนยันเข้าสู่มิติ", use_container_width=True):
                if new_id and new_key:
                    st.session_state.user_id = new_id
                    st.session_state.master_key = new_key
                    st.session_state.app_locked = False
                    st.rerun()
                else:
                    st.warning("กรุณากรอกข้อมูลให้ครบนะคนับ!")

    # คู่มือเอาไว้ข้างล่างสุดแบบย่อ
    with st.expander("📖 วิธีใช้งานและมิติสีต่างๆ"):
        st.write("🔴 RED: ระบาย | 🔵 BLUE: ฟังเพลง | 🟣 PURPLE: AI บำบัด")

        </div>
        <div class='dimension-box' style='border-co
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 INITIATE SYSTEM (เริ่มใช้งาน)"):
            if new_id and new_key:
                st.session_state.user_id = new_id
                st.session_state.master_key = new_key
                st.session_state.app_locked = False
                st.success("ระบบบันทึกรหัสของคุณแล้ว... กำลังเข้าสู่มิติ")
                time.sleep(1.5)
                st.rerun()
            else:
                st.error("กรุณาตั้งชื่อและรหัสผ่านก่อนเข้าใช้งานคนับ!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 4. MAIN INTERFACE (หลังปลดล็อก) ---
else:
    st.markdown(f"<h2 style='text-align:right; color:#ab47bc;'>USER: {st.session_state.user_id} 🔓</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🌌 มิติทั้งหมด", "⚙️ เปลี่ยนรหัส", "🎵 เครื่องเล่นเพลง"])
    
    with tab1:
        st.markdown("### เลือกมิติที่ต้องการบำบัด")
        # โค้ดเลือกห้อง (แดง, ฟ้า, ม่วง ฯลฯ) ที่เราทำไว้เดิม
        st.info("ระบบพร้อมใช้งาน... คุณต้องการไปมิติไหน?")
        if st.button("เข้าสู่มิติม่วง (PURPLE)"):
            st.write("ระบบ AI พร้อมรับฟังความฝันของคุณแล้ว...")

    with tab2:
        st.markdown("### 🔐 จัดการรหัสผ่าน")
        old_pass = st.text_input("ยืนยันรหัสเดิม:", type="password")
        update_key = st.text_input("ตั้งรหัสใหม่:", type="password")
        if st.button("ยืนยันการเปลี่ยนรหัส"):
            if old_pass == st.ses
            else:
                st.error("รหัสเดิมไม่ถูกต้อง!")

    with tab3:
        st.markdown("### 📻 SYNAPSE RADIO")
        st.write("เพลงของลูกพี่กำลังเล่นอยู่ใน Background...")
        st.slider("ปรับความดัง (จำลอง)", 0, 100, 50)
        st.button("เปลี่ยนเพลง")

    if st.button("🚪 LOGOUT"):
        st.session_state.app_locked = True
        st.rerun()
