import streamlit as st
import os
import base64

# ตั้งค่าหน้าแอป
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="wide", initial_sidebar_state="collapsed")

# ซ่อนติ่ง Streamlit เหมือนเดิม
hide_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp { background-color: #050505; }
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# ค้นหาไฟล์
current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
mp3_files = [f for f in os.listdir(current_dir) if f.endswith('.mp3')]

# --- ระบบจำสถานะเอฟเฟกต์ (ถ้ายังไม่มีให้ตั้งค่าเริ่มต้นเป็น NORMAL) ---
if "current_effect" not in st.session_state:
    st.session_state.current_effect = "NORMAL"

# --- เช็คสถานะปัจจุบันแล้วเลือกสไตล์ CSS ให้ตรงกับปุ่มที่กด ---
effect_css = ""

if st.session_state.current_effect == "FLASH":
    # เอฟเฟกต์ FLASH: ไฟสีเหลือง-ขาว กระพริบถี่ๆ สายตื๊ด
    effect_css = """
    @keyframes flashEffect {
        0% { border-color: #fff; box-shadow: 0 0 40px #fff, inset 0 0 20px #ffcc00; }
        50% { border-color: #ffcc00; box-shadow: 0 0 10px #ffcc00; }
        100% { border-color: #fff; box-shadow: 0 0 40px #fff, inset 0 0 20px #ffcc00; }
    }
    .player-container { animation: flashEffect 0.3s infinite; border: 5px solid #ffcc00; }
    """
elif st.session_state.current_effect == "VIBE":
    # เอฟเฟกต์ VIBE: ไฟสีม่วงดนตรี R&B สมูทๆ ค่อยๆ เรืองแสง
    effect_css = """
    @keyframes vibeEffect {
        0% { border-color: #9b51e0; box-shadow: 0 0 15px #9b51e0; }
        100% { border-color: #e051b8; box-shadow: 0 0 35px #e051b8; }
    }
    .player-container { animation: vibeEffect 2s infinite alternate; border: 4px solid #9b51e0; }
    """
elif st.session_state.current_effect == "NEON":
    # เอฟเฟกต์ NEON: สีเขียวมินต์สว่างๆ วิบวับกระชากสายตา
    effect_css = """
    @keyframes neonEffect {
        0% { border-color: #00ffcc; box-shadow: 0 0 30px #00ffcc, inset 0 0 15px #00ffcc; }
        100% { border-color: #0033aa; box-shadow: 0 0 10px #0033aa; }
    }
    .player-container { animation: neonEffect 1s infinite alternate; border: 4px solid #00ffcc; }
    """
elif st.session_state.current_effect == "TUNNEL":
    # เอฟเฟกต์ TUNNEL: ไฟสีน้ำเงินไซไฟ วนลูปหลอนๆ
    effect_css = """
    @keyframes tunnelEffect {
        0% { border-color: #0066ff; box-shadow: 0 0 20px #0066ff; }
        50% { border-color: #ff0055; box-shadow: 0 0 40px #ff0055; }
        100% { border-color: #0066ff; box-shadow: 0 0 20px #0066ff; }
    }
    .player-container { animation: tunnelEffect 4s infinite; border: 4px solid #0066ff; }
    """
else:
    # สถานะธรรมดา (Normal) ไฟวิ่ง RGB ชิลๆ ตอนยังไม่กดอะไร
    effect_css = """
    @keyframes neonRainbow {
        0% { border-color: #ff0055; box-shadow: 0 0 15px #ff0055; }
        50% { border-color: #00ffcc; box-shadow: 0 0 25px #00ffcc; }
        100% { border-color: #9b51e0; box-shadow: 0 0 15px #9b51e0; }
    }
    .player-container { animation: neonRainbow 5s infinite alternate; border: 4px solid #ff0055; }
    """

# พ่น CSS ของเอฟเฟกต์ลงหน้าเว็บ
style_setup = f"""
<style>
    .player-container {{
        border-radius: 20px;
        padding: 30px;
        background: rgba(15, 15, 15, 0.9);
        text-align: center;
        max-width: 600px;
        margin: 0 auto;
    }}
    .neon-marquee {{
        font-size: 22px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 0 0 10px #00ffcc;
        background: #000000;
        padding: 8px;
        border-radius: 10px;
    }}
    {effect_css}
</style>
"""
st.markdown(style_setup, unsafe_allow_html=True)


# --- หน้าตาแอป (UI) ---
st.write("<br>", unsafe_allow_html=True)

# กล่องเครื่องเล่นหลัก (จะเปลี่ยนสีตามปุ่มที่กด)
st.markdown("<div class='player-container'>", unsafe_allow_html=True)
st.markdown(f"<h2 style='color:#fff;'>🪐 SYNAPSE COMMAND CENTER</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#aaa;'>โหมดปัจจุบัน: <b style='color:#00ffcc;'>{st.session_state.current_effect}</b></p>", unsafe_allow_html=True)

# ข้อความวิ่ง
st.markdown("""
<div class='neon-marquee'>
    <marquee scrollamount='8'>🔥 SYSTEM ACTIVE • อยู่นิ่งๆ ไม่เจ็บตัว • NOW PLAYING 🔥</marquee>
</div>
<br>
""", unsafe_allow_html=True)

# ส่วนเลือกเพลง
if mp3_files:
    selected_song = st.selectbox("🎵 เลือกเพลงที่จะอัดวิดีโอ:", mp3_files)
    song_path = os.path.join(current_dir, selected_song)
    with open(song_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
else:
    st.error("❌ ไม่เจอไฟล์ .mp3 ในโฟลเดอร์เดียวกับโค้ด")

st.markdown("</div>", unsafe_allow_html=True)


# --- 🎛️ EFFECT BOARD (โซนปุ่มกดเปลี่ยนเอฟเฟกต์จริง) ---
st.write("<br><br>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#fff;'>🎛️ EFFECT BOARD (กดเพื่อเปลี่ยนแสงไฟ)</h3>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("⚡ FLASH"):
        st.session_state.current_effect = "FLASH"
        st.rerun() # สั่งให้หน้าจอรีเฟรชเพื่อเปลี่ยนสีไฟทันที
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
