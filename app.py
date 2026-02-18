import streamlit as st
import google.generativeai as genai
import time

# --- 0. INITIAL SETUP & GLOBAL MUSIC ---
st.set_page_config(page_title="SYNAPSE 6D : CORE", layout="wide", initial_sidebar_state="collapsed")

# ระบบเครื่องเล่นเพลงแบบ Global (ดังทุกห้อง)
def play_bg_music():
    # เปลี่ยน URL ตรงนี้เป็นไฟล์เพลงของลูกพี่นะคนับ (Direct Link .mp3)
    music_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" 
    st.markdown(f"""
        <iframe src="{music_url}" allow="autoplay" style="display:none" id="bgAudio"></iframe>
        <audio autoplay loop style="width: 100%; filter: invert(100%); opacity: 0.5;">
            <source src="{music_url}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

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

# --- 3. LANDING PAGE : โลโก้ + ตั้งรหัสเอง ---
if st.session_state.app_locked:
    play_bg_music() # เปิดเพลงตั้งแต่หน้าแรก
    st.markdown("<div class='logo-container'><h1 class='main-logo'>SYNAPSE 6D</h1><p style='letter-spacing:5px;'>ULTIMATE THERAPY SYSTEM</p></div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div class='setup-card'>", unsafe_allow_html=True)
        st.subheader("🔑 สร้างอัตลักษณ์และรหัสผ่านเข้าถึง")
        
        new_id = st.text_input("ตั้งชื่อเรียกของคุณ (Identity Name):", placeholder="เช่น นักเดินทาง...")
        new_key = st.text_input("ตั้งรหัสผ่านเข้ามิติ (Access Code):", type="password", help="รหัสนี้จะใช้เปลี่ยนมิติในอนาคต")
        
        st.markdown("---")
        st.markdown("### 📜 คู่มือมิติ (Dimension Capabilities)")
        
        st.markdown("""
        <div class='dimension-box' style='border-color: #ff4b4b;'>
            <b style='color:#ff4b4b;'>🔴 RED (Emotional Vent)</b><br>
            <b>ความสามารถ:</b> ปลดปล่อยความโกรธ ความอึดอัดที่พูดให้ใครฟังไม่ได้<br>
            <b>วิธีใช้:</b> พิมพ์ทุกอย่างที่ขวางหน้าแล้วกด Send เพื่อทิ้งมันไปในหลุมดำ
        </div>
        <div class='dimension-box' style='border-color: #00d4ff;'>
            <b style='color:#00d4ff;'>🔵 BLUE (Voice & Flow)</b><br>
            <b>ความสามารถ:</b> พื้นที่แห่งความสงบ ฟังเสียงบำบัดและเสียงเพลง<br>
            <b>วิธีใช้:</b> ต้องมีรหัสผ่านเฉพาะห้องเพื่อเข้าถึงคลังเสียงส่วนตัว
        </div>
        <div class='dimension-box' style='border-color: #ab47bc;'>
            <b style='color:#ab47bc;'>🟣 PURPLE (Deep Brain Memory)</b><br>
            <b>ความสามารถ:</b> AI บำบัดที่จำความฝันและความรู้สึกคุณได้ตลอดกาล<br>
            <b>วิธีใช้:</b> ใช้รหัสลับส่วนตัวล็อกลิ้นชักความจำ ยิ่งคุย AI ยิ่งรู้จักคุณ
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
    play_bg_music() # เพลงยังคงดังต่อเนื่อง
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
            if old_pass == st.session_state.master_key:
                st.session_state.master_key = update_key
                st.success("เปลี่ยนรหัสสำเร็จ! ครั้งหน้าต้องใช้รหัสใหม่นะคนับ")
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
