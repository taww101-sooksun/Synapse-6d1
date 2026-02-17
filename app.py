import streamlit as st
import streamlit.components.v1 as components

# --- 1. ตั้งค่าพื้นฐาน (ป้องกันหน้าจอขาว) ---
st.set_page_config(page_title="Synapse Home", layout="centered")

# จำลองสถานะ Login เพื่อให้รันหน้าหลักได้ทันที
if 'user' not in st.session_state:
    st.session_state.user = "Synapse User"
if 'page' not in st.session_state:
    st.session_state.page = "home"

# --- 2. CSS ปรับแต่งรูปลักษณ์ ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle, #001219 0%, #000000 100%);
        color: white;
    }
    .logo-container {
        display: flex; justify-content: center; padding: 20px;
    }
    .logo-img {
        width: 300px; border-radius: 20px;
        border: 2px solid #D4AF37;
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.5);
    }
    .stButton>button {
        width: 100%; height: 60px; border-radius: 12px; font-weight: bold;
    }
    /* สีปุ่มแยกตามมิติ */
    button[key="red"] { background: #4a0000 !important; }
    button[key="blue"] { background: #002147 !important; }
    button[key="green"] { background: #0a2910 !important; }
    button[key="black"] { background: #1a1a1a !important; }
    button[key="purple"] { background: #2d004d !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. ฟังก์ชันหน้าหลัก ---
def render_home():
    # แสดงโลโก้ที่เป็นความจริงจาก GitHub ของคุณ
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    # ใช้ลิงก์ดิบ (Raw) เพื่อให้ Streamlit ดึงภาพมาแสดงได้ชัวร์ๆ
    logo_url = "https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg"
    st.image(logo_url, width=300)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center; color:#FFD700;'>SYNAPSE COMMAND CENTER</h2>", unsafe_allow_html=True)

    # YouTube Playlist ของคุณ
    st.write("### 🎬 Synapse Playlist")
    components.html(f"""
        <iframe width="100%" height="315" 
        src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" 
        frameborder="0" allowfullscreen style="border-radius:15px; border:1px solid #444;"></iframe>
    """, height=330)

    st.divider()

    # ปุ่ม 5 ห้อง 5 สี
    st.subheader("🌐 เลือกเข้าสู่มิติ")
    c1, c2, c3 = st.columns(3)
    c4, c5 = st.columns(2)

    with c1:
        if st.button("🔴 RED", key="red"): st.info("กำลังพัฒนาห้อง RED")
    with c2:
        if st.button("🔵 BLUE", key="blue"): st.session_state.page = "blue"; st.rerun()
    with c3:
        if st.button("🟢 GREEN", key="green"): st.info("กำลังพัฒนาห้อง GREEN")
    with c4:
        if st.button("⚫ BLACK", key="black"): st.info("กำลังพัฒนาห้อง BLACK")
    with c5:
        if st.button("🟣 PURPLE", key="purple"): st.info("กำลังพัฒนาห้อง PURPLE")

# --- 4. การควบคุมหน้าจอ ---
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "blue":
    st.title("🔵 Blue Room (Voice Hub)")
    if st.button("⬅️ กลับหน้าหลัก"): st.session_state.page = "home"; st.rerun()
