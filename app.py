import streamlit as st
import os
import base64

# --- CONFIG ---
st.set_page_config(page_title="HAPPY COFFI GOLD", layout="centered")

# --- ลบทุกอย่างที่เป็น Streamlit ออกให้เกลี้ยง ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stAppViewBlockContainer"] {padding: 1rem;}
    
    /* พื้นหลังสีจัดจ้าน */
    .stApp {
        background: linear-gradient(180deg, #7f00ff, #e100ff);
        color: white;
        font-family: 'Tahoma', sans-serif;
    }

    .main-card {
        background: rgba(0, 0, 0, 0.4);
        border-radius: 30px;
        border: 4px solid #00ff00;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 0px 20px #00ff00;
    }

    /* ตัวหนังสือวิ่ง */
    .marquee {
        font-size: 24px;
        font-weight: bold;
        color: #ffff00;
        white-space: nowrap;
        overflow: hidden;
        box-sizing: border-box;
        margin: 15px 0;
    }
    .marquee span {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 10s linear infinite;
    }
    @keyframes marquee {
        0%   { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }

    /* กราฟเสียงจำลอง */
    .visualizer {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        height: 50px;
        gap: 3px;
        margin: 20px 0;
    }
    .bar {
        width: 10px;
        background: #00ff00;
        animation: bounce 0.5s ease-in-out infinite alternate;
    }
    @keyframes bounce {
        from { height: 5px; }
        to { height: 50px; }
    }
    /* สุ่มความสูงให้บาร์แต่ละอัน */
    .bar:nth-child(2) { animation-duration: 0.7s; background: #ff00ff; }
    .bar:nth-child(3) { animation-duration: 0.4s; background: #ffff00; }
    .bar:nth-child(4) { animation-duration: 0.9s; background: #00ffff; }
    .bar:nth-child(5) { animation-duration: 0.6s; background: #ff4500; }
    </style>
    """, unsafe_allow_html=True)

# ฟังก์ชันแปลงไฟล์เป็น Base64
def get_audio_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# เตรียมลิสต์เพลง
music_files = [f for f in os.listdir('.') if f.endswith('.mp3')]
audio_data_list = []

for song in music_files:
    b64 = get_audio_base64(song)
    audio_data_list.append({"name": song, "data": f"data:audio/mp3;base64,{b64}"})

# --- เริ่มวาดหน้าจอ ---
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Logo
if os.path.exists("logo1.png"):
    st.image("logo1.png", width=250)

# หัวข้อจัดจ้าน
st.markdown("""
    <h1 style='color: white; text-shadow: 4px 4px #ff0000; font-size: 50px;'>
        HAPPY COFFI GOLD
    </h1>
    """, unsafe_allow_html=True)

# กราฟเสียงวิ่งๆ
st.markdown("""
    <div class="visualizer">
        <div class="bar"></div><div class="bar"></div><div class="bar"></div>
        <div class="bar"></div><div class="bar"></div><div class="bar"></div>
        <div class="bar"></div><div class="bar"></div>
    </div>
    """, unsafe_allow_html=True)

if audio_data_list:
    # ตัวหนังสือวิ่งบอกชื่อเพลง
    st.markdown(f"""
        <div class="marquee">
            <span id="song-title">กำลังโหลดเพลง...</span>
        </div>
        """, unsafe_allow_html=True)

    # ปุ่มควบคุมและ Logic การเล่นต่อเนื่องด้วย JS
    import json
    songs_json = json.dumps(audio_data_list)
    
    player_html = f"""
        <audio id="main-player" controls style="width: 100%; filter: invert(100%);"></audio>
        <div style="margin-top:20px; font-weight:bold;">
            <p>อยู่นิ่งๆ ไม่เจ็บตัว</p>
        </div>

        <script>
            const songs = {songs_json};
            let currentIdx = 0;
            const player = document.getElementById('main-player');
            const title = document.getElementById('song-title');

            function loadSong(idx) {{
                player.src = songs[idx].data;
                title.innerText = "Playing: " + songs[idx].name;
                player.play();
            }}

            // เล่นเพลงแรกทันทีที่โหลด (ถ้า Browser ยอม)
            window.onload = () => {{
                loadSong(currentIdx);
            }};

            // เมื่อจบเพลง ให้ไปเพลงถัดไป
            player.onended = () => {{
                currentIdx++;
                if (currentIdx >= songs.length) {{
                    currentIdx = 0; // วนกลับเริ่มใหม่
                }}
                loadSong(currentIdx);
            }};
        </script>
    """
    st.markdown(player_html, unsafe_allow_html=True)
else:
    st.error("ไม่เจอไฟล์ MP3 ในโฟลเดอร์เลยเพื่อน!")

st.markdown('</div>', unsafe_allow_html=True)
