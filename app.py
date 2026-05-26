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
        padding:
