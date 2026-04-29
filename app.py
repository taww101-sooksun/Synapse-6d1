import streamlit as st
import os
import base64
import json

# --- CONFIG ---
st.set_page_config(page_title="HAPPY COFFI GOLD", layout="centered")

# --- CSS จัดเต็ม ลบทุกอย่างของ Streamlit ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .stApp {
        background: linear-gradient(180deg, #ff00ff, #0000ff);
        color: white;
    }

    .container {
        text-align: center;
        padding: 20px;
        border: 5px solid #00ff00;
        border-radius: 30px;
        background: rgba(0,0,0,0.5);
    }

    /* ปุ่ม Play ขนาดใหญ่ */
    .play-btn {
        background-color: #00ff00;
        color: black;
        border: none;
        padding: 20px 40px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 50px;
        cursor: pointer;
        box-shadow: 0 0 20px #00ff00;
        margin: 20px 0;
    }
    
    .play-btn:active {
        transform: scale(0.95);
    }

    /* ตัววิ่ง */
    .marquee-box {
        overflow: hidden;
        background: black;
        color: #00ff00;
        padding: 10px;
        margin: 15px 0;
        border-radius: 10px;
    }

    /* กราฟเสียง */
    .bar-container {
        display: flex;
        justify-content: center;
        gap: 5px;
        height: 60px;
        align-items: flex-end;
        margin-bottom: 20px;
    }
    .bar {
        width: 15px;
        background: #ffff00;
        animation: dance 0.5s infinite alternate;
    }
    @keyframes dance {
        from { height: 10px; }
        to { height: 60px; }
    }
    </style>
    """, unsafe_allow_html=True)

# ดึงไฟล์เพลง
music_files = [f for f in os.listdir('.') if f.endswith('.mp3')]

if music_files:
    # แปลงเพลงเป็น Base64
    songs_data = []
    for f in music_files:
        with open(f, "rb") as audio_file:
            b64 = base64.b64encode(audio_file.read()).decode()
            songs_data.append({"name": f, "data": f"data:audio/mp3;base64,{b64}"})

    songs_json = json.dumps(songs_data)

    st.markdown('<div class="container">', unsafe_allow_html=True)
    
    # โลโก้
    if os.path.exists("logo1.png"):
        st.image("logo1.png")

    st.markdown("<h1 style='text-shadow: 3px 3px red;'>HAPPY COFFI GOLD</h1>", unsafe_allow_html=True)

    # กราฟเสียง
    st.markdown('<div class="bar-container">' + '<div class="bar"></div>'*10 + '</div>', unsafe_allow_html=True)

    # พื้นที่แสดงชื่อเพลง (ตัววิ่ง)
    st.markdown('<div class="marquee-box"><marquee id="song-name">กดปุ่มเริ่มเล่นเพลง...</marquee></div>', unsafe_allow_html=True)

    # ปุ่มกดที่สร้างขึ้นมาใหม่
    st.markdown("""
        <button class="play-btn" onclick="playMusic()">▶ PLAY / NEXT</button>
        <audio id="player" style="display:none;"></audio>
        
        <script>
        var songs = """ + songs_json + """;
        var currentIdx = 0;
        var player = document.getElementById('player');
        var nameDisplay = document.getElementById('song-name');

        function playMusic() {
            if (player.paused || player.ended) {
                loadAndPlay(currentIdx);
            } else {
                // ถ้ากดซ้ำให้เปลี่ยนเพลงถัดไปเลย
                nextSong();
            }
        }

        function loadAndPlay(idx) {
            player.src = songs[idx].data;
            nameDisplay.innerText = "กำลังเล่น: " + songs[idx].name;
            player.play();
        }

        function nextSong() {
            currentIdx++;
            if (currentIdx >= songs.length) currentIdx = 0;
            loadAndPlay(currentIdx);
        }

        player.onended = nextSong;
        </script>
    """, unsafe_allow_html=True)

    st.markdown("<p style='margin-top:20px;'>อยู่นิ่งๆ ไม่เจ็บตัว</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("หาไฟล์ .mp3 ไม่เจอครับเพื่อน วางไว้ที่เดียวกับโค้ดหรือยัง?")
