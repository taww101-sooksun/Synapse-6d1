import streamlit as st
import os
import base64
import random

# 1. ตั้งค่าหน้าจอ
st.set_page_config(
    page_title="SYNAPSE PRECISION EQ", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ซ่อนติ่ง Streamlit
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp { background-color: #02040a; }
</style>
""", unsafe_allow_html=True)

# ค้นหาไฟล์
current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
mp3_files = [f for f in os.listdir(current_dir) if f.endswith('.mp3')]
logo_path = os.path.join(current_dir, "logo1.png")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""

logo_base64 = get_image_base64(logo_path)

if "current_effect" not in st.session_state:
    st.session_state.current_effect = "NORMAL"

# --- 2. แผงควบคุมดีไซน์ (อยู่นอกกรอบอัดวิดีโอ) ---
st.subheader("📊 PRECISION EQ CONTROL")
col_input1, col_input2, col_input3 = st.columns([2, 1, 1])

with col_input1:
    user_text = st.text_input("✍️ ข้อความวิ่ง:", "🔥 PRECISION EQ ACTIVE • SYNAPSE MASTER PRO • 🔥")
with col_input2:
    text_color = st.color_picker("🎨 สีไฟนีออน", "#00ffff")
with col_input3:
    text_size = st.slider("📏 ขนาดตัวหนังสือ (px)", 16, 50, 26)

if mp3_files:
    selected_song = st.selectbox("🎵 เลือกเพลงสำหรับการอัดหน้าจอ:", mp3_files)
    song_path = os.path.join(current_dir, selected_song)
    with open(song_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
else:
    audio_bytes = None

# --- 3. เช็คเอฟเฟกต์ไฟและจังหวะกราฟ ---
speed = "0.5s"
if st.session_state.current_effect == "FLASH":
    effect_css = "border: 5px solid #fff; animation: flashFx 0.2s infinite;"
    speed = "0.2s" # กราฟเต้นรัว
elif st.session_state.current_effect == "VIBE":
    effect_css = "border: 4px solid #9b51e0; animation: vibeFx 1.5s infinite alternate;"
    speed = "0.8s" # กราฟเต้นช้าๆ เคลิ้มๆ
else:
    effect_css = f"border: 4px solid {text_color}; animation: rainbowFx 6s infinite alternate;"

# --- 4. สร้าง HTML สำหรับกราฟเสียง EQ (Visualizer Bars) ---
bars_html = ""
for i in range(25): # สร้าง 25 แท่ง
    h = random.randint(10, 100)
    d = random.uniform(0, 1)
    bars_html += f'<div class="bar" style="animation-duration: {speed}; animation-delay: -{d}s;"></div>'

# --- 5. CSS สำหรับกราฟเสียงและดีไซน์ทั้งหมด ---
custom_css = """
<style>
    .player-box {
        background: radial-gradient(circle at center, rgba(10,20,40,0.8) 0%, #02040a 100%);
        border-radius: 30px;
        padding: 50px;
        text-align: center;
        max-width: 750px;
        margin: 20px auto;
        position: relative;
        overflow: hidden;
        __DYNAMIC_EFFECT__
    }

    /* พื้นหลังตารางนีออนเบาๆ เหมือนในรูป */
    .player-box::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: linear-gradient(rgba(0, 255, 255, 0.05) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        z-index: 0;
    }

    .content-wrapper { position: relative; z-index: 1; }

    /* โลโก้เต้น */
    .dancing-logo {
        width: 150px; height: 150px;
        object-fit: cover; border-radius: 50%;
        border: 3px solid __TEXT_COLOR__;
        animation: logoDance 2s infinite ease-in-out;
        box-shadow: 0 0 20px __TEXT_COLOR__;
        margin-bottom: 20px;
    }

    /* กราฟเสียง EQ Bars */
    .visualizer {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        height: 100px;
        gap: 4px;
        margin: 20px 0;
    }
    .bar {
        width: 12px;
        background: linear-gradient(to top, __TEXT_COLOR__, #fff);
        border-radius: 2px 2px 0 0;
        animation: barMove infinite ease-in-out alternate;
        box-shadow: 0 0 10px __TEXT_COLOR__;
    }

    @keyframes barMove {
        0% { height: 10%; }
        100% { height: 100%; }
    }

    /* ตัวหนังสือวิ่งเรืองแสงขยับได้ */
    .custom-marquee {
        font-family: 'Courier New', Courier, monospace;
        font-size: __TEXT_SIZE__px;
        font-weight: bold;
        color: #fff;
        background: rgba(0,0,0,0.7);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid __TEXT_COLOR__;
        box-shadow: 0 0 15px __TEXT_COLOR__;
        animation: neonPulse 1.5s infinite alternate;
    }

    @keyframes neonPulse {
        0% { text-shadow: 0 0 5px #fff, 0 0 10px __TEXT_COLOR__; }
        100% { text-shadow: 0 0 15px #fff, 0 0 30px __TEXT_COLOR__; }
    }

    @keyframes logoDance {
        0%, 100% { transform: scale(1); filter: drop-shadow(0 0 10px __TEXT_COLOR__); }
        50% { transform: scale(1.1); filter: drop-shadow(0 0 30px #ff00ff); }
    }

    @keyframes rainbowFx {
        0% { border-color: __TEXT_COLOR__; box-shadow: 0 0 20px __TEXT_COLOR__; }
        50% { border-color: #ff00ff; box-shadow: 0 0 40px #ff00ff; }
        100% { border-color: #00ff00; box-shadow: 0 0 20px #00ff00; }
    }
    /* ปุ่มบอร์ด */
    .stButton>button {
        background: #000; color: __TEXT_COLOR__; border: 2px solid __TEXT_COLOR__;
        border-radius: 10px; font-weight: bold; width: 100%;
    }
</style>
"""

custom_css = custom_css.replace("__DYNAMIC_EFFECT__", effect_css)
custom_css = custom_css.replace("__TEXT_COLOR__", text_color)
custom_css = custom_css.replace("__TEXT_SIZE__", str(text_size))
st.markdown(custom_css, unsafe_allow_html=True)

# --- 6. 🎬 หน้าจอหลักสำหรับการอัดวิดีโอ ---
st.write("---")
st.markdown("<div class='player-box'><div class='content-wrapper'>", unsafe_allow_html=True)

# 1. โลโก้เต้น
if logo_base64:
    st.markdown(f'<img src="data:image/png;base64,{logo_base64}" class="dancing-logo">', unsafe_allow_html=True)
else:
    st.markdown("<div class='dancing-logo' style='display:flex; align-items:center; justify-content:center; margin:0 auto; background:#000;'><h1>🛸</h1></div>", unsafe_allow_html=True)

# 2. กราฟเสียง Precision EQ
st.markdown(f'<div class="visualizer">{bars_html}</div>', unsafe_allow_html=True)

# 3. เครื่องเล่นเพลง
if audio_bytes:
    st.audio(audio_bytes, format="audio/mp3")

# 4. ตัวหนังสือวิ่ง
st.markdown(f"<div class='custom-marquee'><marquee scrollamount='10'>{user_text}</marquee></div>", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# --- 7. EFFECT BOARD ---
st.markdown("<h4 style='text-align:center; color:#fff;'>🎛️ EFFECT BOARD</h4>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    if st.button("⚡ FLASH"):
        st.session_state.current_effect = "FLASH"; st.rerun()
with c2:
    if st.button("🔮 VIBE"):
        st.session_state.current_effect = "VIBE"; st.rerun()
with c3:
    if st.button("🌌 NEON"):
        st.session_state.current_effect = "NEON"; st.rerun()
with c4:
    if st.button("🌀 TUNNEL"):
        st.session_state.current_effect = "TUNNEL"; st.rerun()
with c5:
    if st.button("🔄 RESET"):
        st.session_state.current_effect = "NORMAL"; st.rerun()
