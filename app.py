import streamlit as st
import os
import base64

# ตั้งค่าหน้าตาแอปให้ดูดี
st.set_page_config(page_title="Music Player", layout="centered")

# --- ปรับแต่งหน้าตาด้วย CSS (เน้นขอบหนา 4px และสีน้ำเงิน-แดงตามที่คุณชอบ) ---
st.markdown("""
    <style>
    .main-player-card {
        border: 4px solid #0055ff;
        border-radius: 15px;
        padding: 20px;
        background-color: #111111;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .song-title {
        color: #ff3333;
        font-size: 24px !important;
        font-weight: bold !important;
        text-align: center;
        margin-bottom: 15px;
    }
    .custom-text {
        font-size: 18px !important;
        font-weight: 500;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# --- ฟังก์ชันสำหรับแปลงไฟล์ MP3 เป็น Base64 ---
def get_audio_html(file_path):
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    # ส่งกลับเป็นแท็ก HTML Audio ที่มีคำสั่งเล่นอัตโนมัติเมื่อกดเลือก
    return f'<audio controls autoplay style="width: 100%;"><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'

# --- ส่วนหัวข้อหลักแอป ---
st.markdown("<h2 style='text-align: center; color: #0055ff;'>🎵 เครื่องเล่นเพลงพกพา</h2>", unsafe_allow_html=True)
st.write("---")

# 1. ค้นหาไฟล์ .mp3 ในโฟลเดอร์เดียวกันกับโค้ดนี้
current_folder = os.path.dirname(__file__) if __file__ else "."
all_files = os.listdir(current_folder)
mp3_files = [f for f in all_files if f.endswith('.mp3')]

# 2. แสดงผลและเลือกเพลง
if not mp3_files:
    st.warning("⚠️ ไม่พบไฟล์ .mp3 ในโฟลเดอร์นี้เลยเพื่อน! ลองเอาไฟล์เพลงมาวางไว้คู่กับไฟล์โค้ดนี้นะ")
else:
    st.markdown("<p class='custom-text'>เลือกเพลงที่คุณต้องการฟังจากรายการด้านล่าง:</p>", unsafe_allow_html=True)
    
    # ตัวเลือกเพลง (ทำขนาดใหญ่ให้จิ้มง่ายๆ บนมือถือ)
    selected_song = st.selectbox(
        "", 
        options=mp3_files,
        index=0,
        label_visibility="collapsed"
    )
    
    st.write("") # เว้นช่องไฟ
    
    # 3. แสดงหน้าจอเครื่องเล่นเพลงเมื่อเลือกเพลง
    if selected_song:
        full_path = os.path.join(current_folder, selected_song)
        
        # กล่องเครื่องเล่นเพลง
        st.markdown(f"""
            <div class='main-player-card'>
                <div class='song-title'>กำลังเล่น: {selected_song}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # รันเครื่องเล่น HTML Audio ออกมาทำงาน
        try:
            audio_html = get_audio_html(full_path)
            st.markdown(audio_html, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"ไม่สามารถเล่นไฟล์นี้ได้เกิดข้อผิดพลาด: {e}")

# ส่วนท้ายแอปพลิเคชัน
st.write("---")
st.markdown("<p style='text-align: center; color: #888888; font-style: italic;'>อยู่นิ่งๆ ไม่เจ็บตัว</p>", unsafe_allow_html=True)
