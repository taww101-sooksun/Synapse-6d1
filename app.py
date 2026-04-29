import streamlit as st
import os
import base64

# --- CONFIG ---
st.set_page_config(page_title="HAPPY COFFI GOLD", layout="centered")

# --- CSS ลบติ่ง Streamlit & ปรับสีจัดจ้าน ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .stApp {
        background: linear-gradient(180deg, #6200ea, #d500f9);
        color: white;
    }
    
    .main-box {
        text-align: center;
        background: rgba(0, 0, 0, 0.7);
        padding: 30px;
        border-radius: 25px;
        border: 4px solid #00ff00;
        box-shadow: 0 0 25px #00ff00;
    }

    h1 {
        color: #fff;
        text-shadow: 3px 3px #ff0000;
        font-size: 45px !important;
    }

    /* กราฟเสียงวิ่ง */
    .visualizer {
        display: flex;
        justify-content: center;
        gap: 4px;
        height: 40px;
        margin: 20px 0;
    }
    .bar {
        width: 12px;
        background: #ffff00;
        animation: wave 0.6s infinite alternate;
    }
    @keyframes wave {
        from { height: 5px; }
        to { height: 40px; }
    }
    </style>
    """, unsafe_allow_html=True)

# ฟังก์ชันอ่านไฟล์เพลง (อ่านทีละไฟล์เมื่อเรียกใช้ เพื่อประหยัด RAM)
def load_audio_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.markdown('<div class="main-box">', unsafe_allow_html=True)

# แสดง Logo
if os.path.exists("logo1.png"):
    st.image("logo1.png")

st.markdown("<h1>HAPPY COFFI GOLD</h1>", unsafe_allow_html=True)

# กราฟเสียง
st.markdown('<div class="visualizer">' + '<div class="bar" style="animation-delay:0.1s"></div>'*10 + '</div>', unsafe_allow_html=True)

# ค้นหาเพลง
music_files = sorted([f for f in os.listdir('.') if f.endswith('.mp3')])

if music_files:
    # ใช้ Session State เก็บลำดับเพลง
    if 'track_index' not in st.session_state:
        st.session_state.track_index = 0

    current_song = music_files[st.session_state.track_index]
    audio_base64 = load_audio_as_base64(current_song)
    
    st.markdown(f"### 🎵 กำลังเล่น: {current_song}")

    # ตัวเล่นเพลง HTML5 แบบมาตรฐาน (มีปุ่ม Play ให้เห็นชัดเจน)
    # เพิ่ม JavaScript ให้พอจบเพลง (onended) ให้สั่งกดปุ่ม "Next" ของ Streamlit อัตโนมัติ
    audio_html = f"""
        <audio id="audio-player" controls autoplay style="width: 100%; height: 50px;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        <script>
            var audio = document.getElementById('audio-player');
            audio.onended = function() {{
                // ค้นหาปุ่มที่มีคำว่า Next เพลง แล้วสั่งคลิก
                var buttons = window.parent.document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {{
                    if (buttons[i].innerText.includes('Next เพลง')) {{
                        buttons[i].click();
                        break;
                    }}
                }}
            }};
        </script>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

    # ปุ่มควบคุมของ Streamlit
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏮ ก่อนหน้า"):
            st.session_state.track_index = (st.session_state.track_index - 1) % len(music_files)
            st.rerun()
    with col2:
        if st.button("Next เพลง ⏭"):
            st.session_state.track_index = (st.session_state.track_index + 1) % len(music_files)
            st.rerun()

    st.info(f"ทั้งหมด {len(music_files)} เพลง | ลำดับที่ {st.session_state.track_index + 1}")

else:
    st.error("ไม่เจอไฟล์ .mp3 เลยครับเพื่อน! ตรวจสอบที่เก็บไฟล์อีกทีนะ")

st.markdown("<p style='margin-top:30px;'>อยู่นิ่งๆ ไม่เจ็บตัว</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
