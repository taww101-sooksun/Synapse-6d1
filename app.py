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
    effect_css = "border: 5px solid #ffcc00; animation: flashFx 0.2s infinite; "
elif st.session_state.current_effect == "VIBE":
    effect_css = "border: 4px solid #9b51e0; animation: vibeFx 1.5s infinite alternate; "
elif st.session_state.current_effect == "NEON":
    effect_css = "border: 4px solid #ff00ff; animation: neonFx 0.8s infinite alternate; "
elif st.session_state.current_effect == "TUNNEL":
    effect_css = "border: 4px solid #0066ff; animation: tunnelFx 3s infinite; "
else:
    effect_css = "border: 4px solid #00ffff; animation: rainbowFx 6s infinite alternate; "


# --- 4. CSS ขั้นเทพ: ลบติ่ง Streamlit + แอนิเมชันโลโก้เต้นและสาดแสงไฟ ---
custom_css = f"""
<style>
    /* ลบส่วนเกินของ Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    .stApp {{ background-color: #030712; }}
    
    /* กล่องเครื่องเล่นหลัก */
    .player-box {{
        background: rgba(10, 15, 30, 0.85);
        border-radius: 25px;
        padding: 40px;
        text-align: center;
        max-width: 650px;
        margin: 20px auto;
        {effect_css} /* ใส่เอฟเฟกต์ไฟตามปุ่มที่เลือก */
    }}

    /* โลโก้เต้นขยับโชว์ไฟนีออนรอบรูป */
    .dancing-logo {{
        width: 160px;
        height: 160px;
        object-fit: cover;
        border-radius: 50%;
        border: 3px solid #00ffff;
        animation: logoDance 2.5s infinite ease-in-out;
    }}

    /* ออกแบบตัวหนังสือวิ่งตามสไตล์ผู้ใช้ */
    .custom-marquee {{
        font-family: 'Orbitron', sans-serif;
        font-size: {text_size}px;
        font-weight: bold;
        color: {text_color};
        text-shadow: 0 0 10px {text_color}, 0 0 20px {text_color};
        background: #000000;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #222;
        margin: 20px 0;
    }}
