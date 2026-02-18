import streamlit as st
import time

# --- 0. SETUP ---
st.set_page_config(page_title="SYNAPSE 6D : มัดน็อก", layout="wide", initial_sidebar_state="collapsed")

# --- 1. หมัดเด็ดเพลงบำบัด (ห้ามเอาออก) ---
def forced_therapy_radio():
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO" 
    st.markdown(f"""
        <div style="display:none;">
            <iframe src="https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1&mute=0" allow="autoplay"></iframe>
        </div>
    """, unsafe_allow_html=True)

# --- 2. CYBERPUNK CSS (สีสะท้อนแสง + ตัวหนังสือเรืองแสง + ปุ่มนูน) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Kanit:wght@300;500&display=swap');
    
    /* พื้นหลังรุ้งสะท้อนแสง */
    .stApp { 
        background: linear-gradient(135deg, #ff0000, #00ff88, #0000ff, #ffff00, #ab47bc);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
        color: #fff; font-family: 'Kanit', sans-serif;
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

    /* ตัวหนังสือเรืองแสง */
    .neon-text {
        color: #fff;
        text-shadow: 0 0 10px #ab47bc, 0 0 20px #ab47bc, 0 0 40px #ab47bc;
        font-family: 'Orbitron', sans-serif;
        text-align: center;
    }

    /* ปุ่มนูนสะท้อนแสงแรงๆ */
    .stButton>button {
        height: 70px !important; width: 100% !important;
        font-size: 20px !important; font-weight: 900 !important;
        border-radius: 20px !important; border: 3px solid rgba(255,255,255,0.5) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important;
        transition: 0.3s;
    }
    .btn-red button { background: #ff0000 !important; box-shadow: 0 0 30px #ff0000 !important; }
    .btn-blue button { background: #0000ff !important; box-shadow: 0 0 30px #0000ff !important; }
    .btn-green button { background: #00ff00 !important; color: #000 !important; box-shadow: 0 0 30px #00ff00 !important; }
    .btn-black button { background: #000000 !important; color: #fff !important; box-shadow: 0 0 30px #ffffff !important; }
    .btn-purple button { background: #ab47bc !important; box-shadow: 0 0 30px #ab47bc !important; }

    .setup-card { background: rgba(0,0,0,0.8); padding: 30px; border-radius: 30px; border: 2px solid #fff; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "LANDING"
if 'current_room' not in st.session_state: st.session_state.current_room = "MAIN"
if 'user_id' not in st.session_state: st.session_state.user_id = "Ta101"

forced_therapy_radio()

def go_to(page_name):
    st.session_state.current_room = page_name
    st.rerun()

# ==========================================
# 1. หน้าแรก (LANDING PAGE)
# ==========================================
if st.session_state.page == "LANDING":
    st.markdown("<h1 class='neon-text' style='font-size:4em;'>SYNAPSE 6D</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:white;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</h3>", unsafe_allow_html=True)
    
    col_l, col_m, col_r = st.columns([1,2,1])
    with col_m:
        st.markdown("<div class='setup-card'>", unsafe_allow_html=True)
        # แสดง Logo (ถ้ามีไฟล์ logo.jpg ในโฟลเดอร์เดียวกับโค้ด)
        try: st.image("logo.jpg", width=200)
        except: st.warning("กรุณาวางไฟล์ logo.jpg ในโฟลเดอร์แอปนะครับ")
        
        st.text_input("👤 ชื่อผู้ใช้:", value=st.session_state.user_id, key="name_input")
        st.text_input("🔑 รหัสผ่าน:", type="password", key="pass_input")
        
        if st.button("🚀 ยืนยันเข้าสู่มิติ"):
            st.session_state.page = "APP"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 2. ส่วนแอปหลัก
# ==========================================
elif st.session_state.page == "APP":
    
    if st.session_state.current_room == "MAIN":
        st.markdown("<h1 class='neon-text'>เลือกมิติการบำบัด</h1>", unsafe_allow_html=True)
        
        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
        if st.button("🔴 มิติแดง (โพสต์รูป/วิดีโอ/ฟีด)"): go_to("RED")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
        if st.button("🔵 มิติน้ำเงิน (Social/โทรฟรี/แชทสด)"): go_to("BLUE")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="btn-green">', unsafe_allow_html=True)
        if st.button("🟢 มิติเขียว (แชทลับ/เพิ่มเพื่อน)"): go_to("GREEN")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="btn-black">', unsafe_allow_html=True)
        if st.button("⚫ มิติดำ (ตั้งค่า/โปรเจกต์/เปลี่ยนรหัส)"): go_to("BLACK")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="btn-purple">', unsafe_allow_html=True)
        if st.button("🟣 มิติม่วง (AI คู่คิด/ความจำดี)"): go_to("PURPLE")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ห้องน้ำเงิน (BLUE ROOM) ---
    elif st.session_state.current_room == "BLUE":
        st.markdown("<h1 style='color:blue;'>🔵 มิติน้ำเงิน : Social Connect</h1>", unsafe_allow_html=True)
        st.markdown("### 📞 ระบบโทรฟรี (Voice Call Online)")
        st.button("☎️ กดเพื่อโทรออกหาเพื่อน")
        st.markdown("---")
        st.text_area("💬 แชทสดๆ ตรงนี้:")
        st.button("ส่งข้อความ")
        if st.button("⬅️ กลับ"): go_to("MAIN")

    # --- ห้องเขียว (GREEN ROOM) ---
    elif st.session_state.current_room == "GREEN":
        st.markdown("<h1 style='color:green;'>🟢 มิติเขียว : ความลับสีเขียว</h1>", unsafe_allow_html=True)
        st.info("📖 **วิธีใช้งาน:** ห้องนี้เป็นแชทลับออนไลน์ คุณต้องกด 'เพิ่มเพื่อน' โดยใช้ ID เพื่อนก่อนถึงจะเริ่มคุยกันได้ ข้อมูลในนี้จะไม่ถูกเปิดเผยต่อสาธารณะ")
        st.text_input("➕ ใส่ ID เพื่อนเพื่อเพิ่มเพื่อน:")
        st.button("ยืนยันการเพิ่มเพื่อน")
        st.text_input("🔗 ส่งลิงก์วิดีโอให้เพื่อน:")
        if st.button("⬅️ กลับ"): go_to("MAIN")

    # --- ห้องดำ (BLACK ROOM) ---
    elif st.session_state.current_room == "BLACK":
        st.markdown("<h1 style='color:white; text-shadow:0 0 10px #00ff88;'>⚫ มิติดำ : ศูนย์ควบคุม</h1>", unsafe_allow_html=True)
        st.subheader("⚙️ การตั้งค่าส่วนตัว")
        st.text_input("🔄 เปลี่ยนชื่อผู้ใช้:", value=st.session_state.user_id)
        st.text_input("🔑 เปลี่ยนรหัสผ่านใหม่:", type="password")
        st.subheader("📂 โปรเจกต์ของฉัน")
        st.button("➕ สร้างโปรเจกต์ใหม่")
        if st.button("⬅️ กลับ"): go_to("MAIN")

    # --- ห้องม่วง (PURPLE ROOM) ---
    elif st.session_state.current_room == "PURPLE":
        st.markdown("<h1 class='neon-text'>🟣 มิติม่วง : AI อัจฉริยะ</h1>", unsafe_allow_html=True)
        st.write("AI: 'ยินดีที่ได้พบกันอีกครั้ง... จำได้ไหมเราเคยคุยเรื่องอะไรกันไว้?'")
        st.text_area("ช่องเขียนข้อความ (ขนาดใหญ่พิเศษ):", height=400)
        if st.button("⬅️ กลับ"): go_to("MAIN")

    if st.button("🚪 LOGOUT"):
        st.session_state.page = "LANDING"
        st.rerun()
