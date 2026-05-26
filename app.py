import streamlit as st
import os
import base64

# 1. ตั้งค่าหน้าแอปแบบกว้างและซ่อนเมนู Streamlit แท้ๆ
st.set_page_config(
    page_title="SYNAPSE COMMAND CENTER", 
    layout="wide",
    initial_sidebar_state="collapsed" # ซ่อนแถบข้างตอนเริ่มเพื่อให้พื้นที่เต็มจอ
)

# ค้นหาไฟล์ในโฟลเดอร์
current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
mp3_files = [f for f in os.listdir(current_dir) if f.endswith('.mp3')]
logo_path = os.path.join(current_dir, "logo1.png")

# ฟังก์ชันแปลงรูปภาพเป็น Base64 เพื่อให้เรียกใช้ใน HTML/CSS ได้ชัวร์ๆ
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""

logo_base64 = get_image_base64(logo_path)

# --- 2. CSS ขั้นเทพ: ลบทุกอย่างที่เป็น Streamlit + ใส่แสงนีออนเคลื่อนไหว (Animation) ---
custom_css = f"""
<style>
    /* ลบแถบด้านบน เมนู และปุ่มด้านล่างของ Streamlit ออกให้หมด */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    
    /* ปรับพื้นหลังแอปให้มืดสนิท เพื่อให้ไฟนีออนเด่น */
    .stApp {{
        background-color: #050505;
    }}

    /* แอนิเมชันเปลี่ยนสีนีออนแบบวนลูป (RGB Rainbow Effect) */
    @keyframes neonRainbow {{
        0% {{ border-color: #ff0055; box-shadow: 0 0 15px #ff0055, inset 0 0 15px #ff0055; }}
        25% {{ border-color: #00ffcc; box-shadow: 0 0 25px #00ffcc, inset 0 0 10px #00ffcc; }}
        50% {{ border-color: #9b51e0; box-shadow: 0 0 15px #9b51e0, inset 0 0 15px #9b51e0; }}
        75% {{ border-color: #ffcc00; box-shadow: 0 0 25px #ffcc00, inset 0 0 10px #ffcc00; }}
        100% {{ border-color: #ff0055; box-shadow: 0 0 15px #ff0055, inset 0 0 15px #ff0055; }}
    }}

    /* แอนิเมชันโลโก้หมุนขยับไม่ให้อยู่นิ่ง */
    @keyframes logoPulse {{
        0% {{ transform: scale(1); filter: drop-shadow(0 0 10px #00ffcc); }}
        50% {{ transform: scale(1.05); filter: drop-shadow(0 0 25px #ff0055); }}
        100% {{ transform: scale(1); filter: drop-shadow(0 0 10px #00ffcc); }}
    }}

    /* กล่องเครื่องเล่นหลัก */
    .player-container {{
        border: 4px solid #ff0055;
        border-radius: 20px;
        padding: 30px;
        background: rgba(15, 15, 15, 0.9);
        text-align: center;
        animation: neonRainbow 8s infinite alternate;
        max-width: 700px;
        margin: 0 auto;
    }}

    /* สไตล์โลโก้ */
    .neon-logo {{
        width: 150px;
        height: 150px;
        object-fit: cover;
        border-radius: 50%;
        animation: logoPulse 3s infinite ease-in-out;
    }}

    /* ตัวหนังสือวิ่งแบบนีออนไล่สี */
    .neon-marquee {{
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 30px #00ffcc;
        background: #000000;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #333;
    }}
    
    /* สไตล์ปุ่มกดให้ดูเป็นคลับนีออน */
    .stButton>button {{
        background-color: #111;
        color: #00ffcc;
        border: 2px solid #00ffcc;
        border-radius: 10px;
        box-shadow: 0 0 8px #00ffcc;
        transition: 0.3s;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: #00ffcc;
        color: #111;
        box-shadow: 0 0 20px #00ffcc;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# --- 3. ส่วนการแสดงผลบนหน้าจอ (UI) ---

st.write("<br>", unsafe_allow_html=True)

# กล่องเครื่องเล่นเพลงหลัก
st.markdown("<div class='player-container'>", unsafe_allow_html=True)

# แสดงโลโก้ logo1.png (ถ้ามีไฟล์)
if logo_base64:
    st.markdown(f'<img src="data:image/png;base64,{logo_base64}" class="neon-logo">', unsafe_allow_html=True)
else:
    # ถ้าไม่มีรูปจะขึ้นเป็นไอคอนนีออนแก้ขัดให้ก่อน
    st.markdown("<h1 style='font-size:80px; animation: logoPulse 3s infinite;'>🛸</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='color:#fff; text-shadow: 0 0 10px #ff0055;'>SYNAPSE PLAYER</h2>", unsafe_allow_html=True)

# ข้อความวิ่งแบบนีออนหลายสี (ไมู่อยู่นิ่ง)
st.markdown("""
<div class='neon-marquee'>
    <marquee scrollamount='8'>🔥 NOW PLAYING • อยู่นิ่งๆ ไม่เจ็บตัว • SYSTEM ACTIVE • SYSTEM ACTIVE • 🔥</marquee>
</div>
<br>
""", unsafe_allow_html=True)

# ตัวเลือกเพลงและเครื่องเล่น
if mp3_files:
    selected_song = st.selectbox("🎵 เลือกเพลงที่จะอัดวิดีโอ:", mp3_files)
    song_path = os.path.join(current_dir, selected_song)
    
    with open(song_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    
    # ตัวเล่นเพลง
    st.audio(audio_bytes, format="audio/mp3")
else:
    st.error("❌ ไม่เจอไฟล์ .mp3 ในโฟลเดอร์เลยครับเพื่อน เอาไฟล์มาวางคู่กับโค้ดก่อนนะ")

st.markdown("</div>", unsafe_allow_html=True) # ปิดกล่องเครื่องเล่น


# --- 4. ปุ่มเอฟเฟกต์วิบวับด้านล่าง ---
st.write("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#fff;'>🎛️ EFFECT BOARD</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⚡ FLASH"):
        st.toast("EFFECT: FLASH!")
with col2:
    if st.button("🔮 VIBE"):
        st.toast("EFFECT: PURE VIBE")
with col3:
    if st.button("🌌 NEON"):
        st.toast("EFFECT: NEON GLOW")
with col4:
    if st.button("🌀 TUNNEL"):
        st.toast("EFFECT: WARP")
