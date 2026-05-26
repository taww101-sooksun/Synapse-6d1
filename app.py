import streamlit as st
import os
import base64

# 1. ตั้งค่าหน้าจอ ซ่อนแถบข้างตอนเริ่มต้น
st.set_page_config(
    page_title="SYNAPSE COMMAND CENTER", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ซ่อนส่วนเกินของ Streamlit เกลี้ยงตั๊บ
hide_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp { background-color: #030712; }
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# ค้นหาไฟล์ในโฟลเดอร์
current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
mp3_files = [f for f in os.listdir(current_dir) if f.endswith('.mp3')]
logo_path = os.path.join(current_dir, "logo1.png")

# ฟังก์ชันดึงรูปภาพทำเป็น Base64
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""

logo_base64 = get_image_base64(logo_path)

# --- ระบบจำสถานะเอฟเฟกต์ปุ่มกด ---
if "current_effect" not in st.session_state:
    st.session_state.current_effect = "NORMAL"

# --- 2. แถบควบคุมด้านหน้าแอป สำหรับพิมพ์ข้อความและเลือกเพลง (แยกจากกรอบอัดวิดีโอ) ---
st.subheader("🎨 แผงควบคุมดีไซน์ และ เลือกเพลง")
col_input1, col_input2, col_input3 = st.columns([2, 1, 1])

with col_input1:
    user_text = st.text_input("✍️ พิมพ์ข้อความวิ่งของคุณที่นี่:", "🔥 SYNAPSE MASTER PRO • อยู่นิ่งๆ ไม่เจ็บตัว • SYSTEM ACTIVE 🔥")
with col_input2:
    text_color = st.color_picker("🎨 เลือกสีหลักของนีออนตัวหนังสือ", "#ff00ff")
with col_input3:
    text_size = st.slider("📏 ขนาดตัวหนังสือ (px)", 16, 50, 28)

# ส่วนเลือกเพลง (ย้ายขึ้นมาไว้ข้างบน จะได้ไม่ไปรกในกรอบนีออน)
if mp3_files:
    selected_song = st.selectbox("🎵 เลือกเพลงที่ต้องการเล่น:", mp3_files)
    song_path = os.path.join(current_dir, selected_song)
    with open(song_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
else:
    audio_bytes = None

# --- 3. เช็คสถานะเอฟเฟกต์ไฟนีออนรอบกรอบเครื่องเล่นหลัก ---
if st.session_state.current_effect == "FLASH":
    effect_css = "border: 5px solid #fff; animation: flashFx 0.2s infinite;"
elif st.session_state.current_effect == "VIBE":
    effect_css = "border: 4px solid #9b51e0; animation: vibeFx 1.5s infinite alternate;"
elif st.session_state.current_effect == "NEON":
    effect_css = "border: 4px solid #ff00ff; animation: neonFx 0.8s infinite alternate;"
elif st.session_state.current_effect == "TUNNEL":
    effect_css = "border: 4px solid #0066ff; animation: tunnelFx 3s infinite;"
else:
    effect_css = "border: 4px solid #00ffff; animation: rainbowFx 6s infinite alternate;"


# --- 4. CSS แก้ไข Bug ปีกกา และเพิ่มแอนิเมชันตัวหนังสือนีออนไม่นิ่ง ---
custom_css = """
<style>
    /* กล่องเครื่องเล่นหลัก (คลีนๆ เอาตัวหนังสือขยะออกหมดแล้ว) */
    .player-box {
        background: rgba(7, 11, 22, 0.9);
        border-radius: 25px;
        padding: 40px;
        text-align: center;
        max-width: 680px;
        margin: 20px auto;
        __DYNAMIC_EFFECT__
    }

    /* โลโก้เต้นขยับโชว์ไฟนีออนฟุ้งๆ */
    .dancing-logo {
        width: 180px;
        height: 180px;
        object-fit: cover;
        border-radius: 50%;
        border: 3px solid #00ffff;
        animation: logoDance 2.5s infinite ease-in-out;
        margin-bottom: 20px;
    }

    /* ตัวหนังสือวิ่งแบบไฟนีออนขยับวาบตลอดเวลา ไมู่อยู่นิ่ง */
    .custom-marquee {
        font-family: 'Orbitron', sans-serif;
        font-size: __TEXT_SIZE__px;
        font-weight: bold;
        color: #ffffff;
        background: #000000;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid __TEXT_COLOR__;
        margin-top: 25px;
        box-shadow: 0 0 15px __TEXT_COLOR__;
        animation: textNeonPulse 1.5s infinite alternate;
    }

    /* ================= KEYFRAMES ANIMATIONS ================= */
    /* โลโก้เต้นสาดไฟ */
    @keyframes logoDance {
        0%, 100% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 15px #00ffff); }
        50% { transform: scale(1.1) rotate(5deg); filter: drop-shadow(0 0 35px #ff00ff); }
    }

    /* แอนิเมชันไฟนีออนตัวหนังสือวูบวาบตามสีที่เลือก */
    @keyframes textNeonPulse {
        0% { text-shadow: 0 0 5px #fff, 0 0 10px __TEXT_COLOR__, 0 0 20px __TEXT_COLOR__; }
        100% { text-shadow: 0 0 10px #fff, 0 0 25px __TEXT_COLOR__, 0 0 40px __TEXT_COLOR__; }
    }

    /* เอฟเฟกต์ไฟรอบกรอบ */
    @keyframes rainbowFx {
        0% { border-color: #00ffff; box-shadow: 0 0 20px #00ffff; }
        50% { border-color: #ff00ff; box-shadow: 0 0 35px #ff00ff; }
        100% { border-color: #facc15; box-shadow: 0 0 20px #facc15; }
    }
    @keyframes flashFx {
        0%, 100% { border-color: #fff; box-shadow: 0 0 45px #fff, inset 0 0 25px #ffcc00; }
        50% { border-color: #ffcc00; box-shadow: 0 0 5px #ffcc00; }
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

    /* สไตล์ปุ่มเอฟเฟกต์ */
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

# ใช้ .replace แทนสลับค่าตัวแปร (ผ่านฉลุย 100%)
custom_css = custom_css.replace("__DYNAMIC_EFFECT__", effect_css)
custom_css = custom_css.replace("__TEXT_COLOR__", text_color)
custom_css = custom_css.replace("__TEXT_SIZE__", str(text_size))

st.markdown(custom_css, unsafe_allow_html=True)


# --- 5. 🎬 โซนเครื่องเล่นหลักสำหรับอัดวิดีโอ (คลีน ไร้สิ่งรกตา) ---
st.write("---")

st.markdown("<div class='player-box'>", unsafe_allow_html=True)

# 1. แสดงโลโก้เต้นสาดไฟ
if logo_base64:
    st.markdown(f'<img src="data:image/png;base64,{logo_base64}" class="dancing-logo">', unsafe_allow_html=True)
else:
    st.markdown("<div class='dancing-logo' style='display:flex; align-items:center; justify-content:center; margin:0 auto; background:#000;'><h1 style='margin:0; font-size:70px;'>📀</h1></div>", unsafe_allow_html=True)

# 2. เครื่องเล่นเพลงของระบบ (โชว์เฉพาะตัวกด Play)
if audio_bytes:
    st.audio(audio_bytes, format="audio/mp3")
else:
    st.markdown("<p style='color:#ff3333;'>⚠️ ไม่พบไฟล์เพลง .mp3 ในโฟลเดอร์</p>", unsafe_allow_html=True)

# 3. ตัวหนังสือวิ่งแบบนีออน วูบวาบตามสีที่เลือกเอง
st.markdown(f"""
<div class='custom-marquee'>
    <marquee scrollamount='8'>{user_text}</marquee>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# --- 6. EFFECT BOARD บอร์ดกดเปลี่ยนโหมดไฟนีออนรอบกรอบ ---
st.write("<br>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#fff;'>🎛️ CONTROL EFFECT BOARD</h4>", unsafe_allow_html=True)

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
