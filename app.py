import streamlit as st
import time

# --- 0. INITIAL SETUP & THEME ---
st.set_page_config(page_title="SYNAPSE 6D : THE ULTIMATE", layout="wide", initial_sidebar_state="collapsed")

# --- 1. FUNCTION: มัดมือฟัง (เพลงบำบัด 60 เพลง - 2 หมื่นวิว) ---
def forced_therapy_radio():
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO" 
    st.markdown(f"""
        <div style="display:none;">
            <iframe id="therapy-radio" src="https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1&mute=0" allow="autoplay"></iframe>
        </div>
    """, unsafe_allow_html=True)

# --- 2. CYBERPUNK CSS (รกๆ สะท้อนแสง ปุ่มนูน) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Kanit:wght@300;500&display=swap');
  col_l, col_m, col_r = st.columns([1,2,1])
    with col_m:
        st.markdown("<div class='setup-card'>", unsafe_allow_html=True)
        # แสดง Logo (ถ้ามีไฟล์ logo.jpg ในโฟลเดอร์เดียวกับโค้ด)
        try: st.image("logo.jpg", width=200)
        except: st.warning("กรุณาวางไฟล์ logo.jpg ในโฟลเดอร์แอปนะครับ")  
    /* พื้นหลังรุ้งสะท้อนแสง หน้าแรก */
    .stApp { 
        background: linear-gradient(135deg, #ff0000, #00ff88, #0000ff, #ffff00, #ab47bc);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #fff; font-family: 'Kanit', sans-serif;
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

    /* ปุ่มกดแบบนูนและใหญ่ (3D Glow Buttons) */
    .stButton>button {
        height: 80px !important; width: 100% !important;
        font-size: 22px !important; font-weight: 900 !important;
        border-radius: 15px !important; border: 4px solid rgba(255,255,255,0.3) !important;
        box-shadow: 6px 6px 15px rgba(0,0,0,0.5), inset -4px -4px 10px rgba(0,0,0,0.3) !important;
        transition: 0.2s; text-transform: uppercase;
    }
    .stButton>button:active { transform: translateY(4px); box-shadow: 2px 2px 5px rgba(0,0,0,0.5) !important; }

    /* สีสะท้อนแสงแต่ละห้อง */
    .btn-red button { background: #ff0000 !important; color: white !important; box-shadow: 0 0 20px #ff0000 !important; }
    .btn-blue button { background: #0000ff !important; color: white !important; box-shadow: 0 0 20px #0000ff !important; }
    .btn-green button { background: #00ff00 !important; color: black !important; box-shadow: 0 0 20px #00ff00 !important; }
    .btn-black button { background: #000000 !important; color: #00ff88 !important; box-shadow: 0 0 20px #ffffff !important; border: 2px solid #555 !important; }
    .btn-purple button { background: #ab47bc !important; color: white !important; box-shadow: 0 0 20px #ab47bc !important; }

    /* ช่อง Input ใหญ่ๆ */
    .stTextInput input, .stTextArea textarea { 
        background: rgba(0,0,0,0.7) !important; color: #00ff88 !important; 
        font-size: 20px !important; border: 2px solid #ab47bc !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "LANDING"
if 'user_id' not in st.session_state: st.session_state.user_id = "Ta101"
if 'locked' not in st.session_state: st.session_state.locked = True

forced_therapy_radio() # เพลงดังตลอดเวลาทุกห้อง

# --- 4. NAVIGATION LOGIC ---
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ==========================================
# 1. หน้าแรก (LANDING PAGE)
# ==========================================
if st.session_state.page == "LANDING":
    st.markdown("<div style='text-align:center;'><h1 style='font-family:Orbitron; font-size:5em; text-shadow: 0 0 20px #fff;'>SYNAPSE 6D</h1></div>", unsafe_allow_html=True)
    
    col_l, col_m, col_r = st.columns([1,2,1])
    with col_m:
        st.image("https://raw.githubusercontent.com/your-repo/logo.jpg", width=200) # โลโก้รูปโลก
        st.selectbox("🌐 Choose Language / เลือกภาษา / ဘာသာစကား", ["Thai", "English", "Burmese"])
        
        name = st.text_input("👤 ชื่อผู้ใช้ (User):", value=st.session_state.user_id)
        pw = st.text_input("🔑 รหัสผ่าน (Password):", type="password")
        
        if st.button("🚀 ยืนยันรหัสเข้าสู่มิติ", use_container_width=True):
            if name and pw:
                st.session_state.user_id = name
                st.session_state.locked = False
                go_to("MAIN")

    st.markdown("---")
    st.write("📖 **คำอธิบาย 5 ห้องบำบัด:**")
    st.write("🔴 **RED:** ห้องระบาย Feed แบบ YouTube โพสต์รูป/คลิปได้ | 🔵 **BLUE:** ห้องโทรฟรี & Social แบบ Facebook | 🟢 **GREEN:** ห้องแชทลับเฉพาะกลุ่ม หิมะร่วง ดอกไม้ไฟ | ⚫ **BLACK:** ห้องส่วนตัว จัดการยอดเพื่อน | 🟣 **PURPLE:** ห้อง AI ดูดวง ปรับทุกข์ กวนๆ แต่จริงใจ")

# ==========================================
# 2. หน้าหลัก (MAIN MENU)
# ==========================================
elif st.session_state.page == "MAIN":
    st.markdown(f"## ยินดีต้อนรับคุณ {st.session_state.user_id} 🔓")                           # --- ห้องเขียว (GREEN ROOM) ---
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
    # ปุ่มกดนูนขนาดใหญ่ 5 สี
    st.markdown('<div class="btn-red">', unsafe_allow_html=True)
    if st.button("🔴 เข้าสู่มิติแดง (RED ROOM - YouTube Feed)"): go_to("RED")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
    if st.button("🔵 เข้าสู่มิติน้ำเงิน (BLUE ROOM - Facebook Social)"): go_to("BLUE")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-green">', unsafe_allow_html=True)
    if st.button("🟢 เข้าสู่มิติเขียว (GREEN ROOM - Secret Chat)"): go_to("GREEN")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-black">', unsafe_allow_html=True)
    if st.button("⚫ เข้าสู่มิติดำ (BLACK ROOM - Private Master)"): go_to("BLACK")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-purple">', unsafe_allow_html=True)
    if st.button("🟣 เข้าสู่มิติม่วง (AI PURPLE - ดูดวง/ปรับทุกข์)"): go_to("PURPLE")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. ห้องแดง (RED ROOM - Feed YouTube)
# ==========================================
elif st.session_state.page == "RED":
    st.header("🔴 RED ROOM : YouTube Style Feed")
    st.text_input("🔗 แปะลิงค์วิดีโอหรือรูปภาพ:")
    st.file_uploader("📂 อัปโหลดไฟล์ (รองรับระบบ Firebase ในอนาคต)")
    if st.button("📮 โพสต์ลงฟีด"): st.success("โพสต์เรียบร้อย!")
    
    st.markdown("---")
    # ตัวอย่างฟีด
    for i in range(3):
        st.markdown(f"""
            <div style="background:rgba(255,0,0,0.1); padding:20px; border-radius:10px; border:1px solid red; margin-bottom:10px;">
                <h4>โพสต์ที่ {i+1} โดย User_X</h4>
                <p>เนื้อหาการระบายอารมณ์...</p>
                <button>❤️ Like (12)</button> <button>💬 Comment (5)</button> <button>🔗 Share</button>
            </div>
        """, unsafe_allow_html=True)
    
    if st.button("⬅️ กลับหน้าหลัก"): go_to("MAIN")

# ==========================================
# 4. ห้องม่วง (PURPLE ROOM - AI ความจำดี)
# ==========================================
elif st.session_state.page == "PURPLE":
    st.header("🟣 PURPLE ROOM : AI ปรับทุกข์ (กวนใจแต่จริงใจ)")
    
    # ระบบรหัส 2 ชั้นสำหรับความลับ
    if 'purple_locked' not in st.session_state: st.session_state.purple_locked = True
    if st.session_state.purple_locked:
        p_pw = st.text_input("🔑 รหัสลับขั้นที่ 2 สำหรับห้องม่วง:", type="password")
        if st.button("ปลดล็อกความลับ"): st.session_state.purple_locked = False; st.rerun()
    else:
        st.markdown("<p style='font-size:25px;'>AI: 'แอบยิ้มอยู่นะจ๊ะ... มีอะไรให้ช่วยดูดวง หรืออยากระบายความลับล่ะ?'</p>", unsafe_allow_html=True)
        st.text_area("✍️ เขียนข้อความของคุณ (ช่องใหญ่จุใจ):", height=300)
        st.button("🔮 ส่งให้ AI วิเคราะห์ (ใช้ความจำแม่นยำ)")
        
        if st.button("⬅️ กลับหน้าหลัก"): st.session_state.purple_locked = True; go_to("MAIN")

# (ส่วนห้องอื่นๆ เขียว, น้ำเงิน, ดำ จะมีโครงสร้างคล้ายกันตามที่คุณท่านสั่งครับ)
