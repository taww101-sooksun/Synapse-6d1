import streamlit as st
import os
import base64

# 1. ตั้งค่าหน้าจอแบบเต็มตา ซ่อนแถบข้างตอนเริ่มต้น
st.set_page_config(
    page_title="SYNAPSE COMMAND CENTER", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ค้นหาไฟล์ในโฟลเดอร์
current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
mp3_files = [f for f in os.listdir(current_dir) if f.endswith('.mp3')]
logo_path = os.path.join(current_dir, "logo1.png")

# ฟังก์ชันดึงรูปภาพทำเป็น Base64 ให้ CSS ไปใช้งาน
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""

logo_base64 = get_image_base64(logo_path)

# --- ระบบจำสถานะเอฟเฟกต์ปุ่มกด ---
if "current_effect" not in st.session_state:
    st.session_state.current_effect = "NORMAL"

# --- 2. ออกแบบแถบควบคุมด้านหน้าแอป (ให้ผู้ใช้ปรับแต่งเอง) ---
st.subheader("🎨 ออกแบบหน้าจอแอปของคุณ")
col_input1, col_input2, col_input3 = st.columns([2, 1, 1])

with col_input1:
    user_text = st.text_input("✍️ พิมพ์ข้อความวิ่งของคุณที่นี่:", "🔥 SYNAPSE MASTER PRO • อยู่นิ่งๆ ไม่เจ็บตัว • SYSTEM ACTIVE 🔥")
with col_input2:
    text_color = st.color_picker("🎨 สีข้อความวิ่ง", "#00ffff")
with col_input3:
    text_size = st.slider("📏 ขนาดตัวหนังสือ (px)", 16, 40, 24)

# --- 3. เช็คสถานะเอฟเฟกต์ไฟนีออนรอบกรอบเครื่องเล่น ---
if st.session_state.current_effect == "FLASH":
    effect_css = "border: 5px solid #ffcc00; animation: flashFx 0.2s infinite;"
elif st.session_state.current_effect == "VIBE":
    effect_css = "border: 4px solid #9b51e0; animation: vibeFx 1.5s infinite alternate;"
elif st.session_state.current_effect == "NEON":
    effect_css = "border: 4px solid #ff00ff; animation: neonFx 0.8s infinite alternate;"
elif st.session_state.current_effect == "TUNNEL":
    effect_css = "border: 4px solid #0066ff; animation: tunnelFx 3s infinite;"
else:
    effect_css = "border: 4px solid #00ffff; animation: rainbowFx 6s infinite alternate;"


# --- 4. CSS ขั้นเทพ: ลบติ่ง Streamlit + แอนิเมชันโลโก้เต้นและสาดแสงไฟ (แก้ไขไม่ให้เอ๋อ) ---
custom_css = """
<style>
    /* ลบส่วนเกินของ Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp { background-color: #030712; }
    
    /* กล่องเครื่องเล่นหลัก */
    .player-box {
        background: rgba(10, 15, 30, 0.85);
        border-radius: 25px;
        padding: 40px;
        text-align: center;
        max-width: 650px;
        margin: 20px auto;
        __DYNAMIC_EFFECT__ /* ตัวแปรเปลี่ยนเอฟเฟกต์กรอบไฟ */
    }

    /* โลโก้เต้นขยับโชว์ไฟนีออนรอบรูป */
    .dancing-logo {
        width: 160px;
        height: 160px;
        object-fit: cover;
        border-radius: 50%;
        border: 3px solid #00ffff;
        animation: logoDance 2.5s infinite ease-in-out;
    }}

    /* ออกแบบตัวหนังสือวิ่งตามสไตล์ผู้ใช้ */
    .custom-marquee {
        font-family: 'Orbitron', sans-serif;
        font-size: __TEXT_SIZE__px;
        font-weight: bold;
        color: __TEXT_COLOR__;
        text-shadow: 0 0 10px __TEXT_COLOR__, 0 0 20px __TEXT_COLOR__;
        background: #000000;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #222;
        margin: 20px 0;
    }

    /* ================= KEYFRAMES ANIMATIONS ================= */
    @keyframes logoDance {
        0%, 100% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 15px #00ffff); }
        50% { transform: scale(1.12) rotate(4deg); filter: drop-shadow(0 0 35px #ff00ff); }
    }

    @keyframes rainbowFx {
        0% { border-color: #00ffff; box-shadow: 0 0 20px #00ffff; }
        50% { border-color: #ff00ff; box-shadow: 0 0 35px #ff00ff; }
        100% { border-color: #facc15; box-shadow: 0 0 20px #facc15; }
    }
    @keyframes flashFx {
        0%, 100% { border-color: #fff; box-shadow: 0 0 40px #fff, inset 0 0 20px #facc15; }
        50% { border-color: #facc15; box-shadow: 0 0 5px #facc15; }
    }
    @keyframes vibeFx {
        0% { border-color: #9b51e0; box-shadow: 0 0 15px #9b51e0; }
        100% { border-color: #00ffff; box-shadow: 0 0 40px #00ffff; }
    }
    @keyframes neonFx {
        0% { border-color: #ff00ff; box-shadow: 0 0 35px #ff00ff, inset 0 0 15px #ff00ff; }
        100% { border-color: #05070f; box-shadow: 0 0 5px #05070f; }
    }
    @keyframes tunnelFx {
        0%, 100% { border-color: #0066ff; box-shadow: 0 0 15px #0066ff; }
        50% { border-color: #ff0055; box-shadow: 0 0 45px #ff0055; }
    }

    /* สไตล์ปุ่มเอฟเฟกต์บอร์ด */
    .stButton>button {
        background-color: #0b0f19;
        color: #00ffff;
        border: 2px solid #00ffff;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,255,255,0.3);
        font-weight: bold;
        transition: 0.2s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00ffff;
        color: #000;
        box-shadow: 0 0 25px #00ffff;
    }
</style>
"""

# ใช้คำสั่ง .replace แทนการใช้ f-string เพื่อป้องกันปีกกาตีกันแบบ 100%
custom_css = custom_css.replace("__DYNAMIC_EFFECT__", effect_css)
custom_css = custom_css.replace("__TEXT_COLOR__", text_color)
custom_css = custom_css.replace("__TEXT_SIZE__", str(text_size))

st.markdown(custom_css, unsafe_allow_html=True)


# --- 5. พื้นที่เครื่องเล่นเพลงหลัก (UI) ---

st.markdown("<div class='player-box'>", unsafe_allow_html=True)

# ดึงรูป logo1.png มาแสดงและใส่เอฟเฟกต์เต้นสาดไฟ
if logo_base64:
    st.markdown(f'<img src="data:image/png;base64,{logo_base64}" class="dancing-logo">', unsafe_allow_html=True)
else:
    st.markdown("<div class='dancing-logo' style='display:flex; align-items:center; justify-content:center; margin:0 auto; background:#000;'><h1 style='margin:0; font-size:60px;'>📀</h1></div>", unsafe_allow_html=True)

st.markdown("<h2 style='color:#fff; font-family:Sans-serif; letter-spacing:2px; margin-top:15px;'>SYNAPSE COMMAND CENTER</h2>", unsafe_allow_html=True)

# ตัวหนังสือวิ่งที่ผู้ใช้ปรับแต่งและพิมพ์ข้อความได้เองสดๆ หน้าแอป
st.markdown(f"""
<div class='custom-marquee'>
    <marquee scrollamount='8'>{user_text}</marquee>
</div>
""", unsafe_allow_html=True)

# เครื่องเล่นเพลงเลือกจากไฟล์ในโฟลเดอร์
if mp3_files:
    selected_song = st.selectbox("🎵 เลือกเพลงสำหรับการอัดหน้าจอ:", mp3_files)
    song_path = os.path.join(current_dir, selected_song)
    with open(song_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
else:
    st.warning("⚠️ ไม่พบไฟล์ .mp3 เอาไฟล์มาวางคู่กับไฟล์โค้ดนี้ก่อนนะครับเพื่อน")

st.markdown("</div>", unsafe_allow_html=True)


# --- 6. EFFECT BOARD บอร์ดกดเปลี่ยนโหมดไฟนีออนสดๆ ---
st.write("---")
st.markdown("<h3 style='text-align:center; color:#fff;'>🎛️ CONTROL EFFECT BOARD</h3>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("⚡ FLASH"):
        st.session_state.current_effect = "FLASH"
        st.rerun()
with col2:
    if st.button("🔮 VIBE"):
        st.session_state.current_effect = "VIBE"
        st.rerun()
with col3:
    if st.button("🌌 NEON"):
        st.session_state.current_effect = "NEON"
        st.rerun()
with col4:
    if st.button("🌀 TUNNEL"):
        st.session_state.current_effect = "TUNNEL"
        st.rerun()
with col5:
    if st.button("🔄 RESET"):
        st.session_state.current_effect = "NORMAL"
        st.rerun()
