import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="Music Crossfader Pro", layout="centered")

# CSS พื้นหลังรุ้ง (ตามที่คุณต้องการเป๊ะๆ)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff);
        background-size: 1200% 1200%;
        animation: RainbowFlow 10s ease infinite;
    }
    @keyframes RainbowFlow {
        0%{background-position:0% 50%}
        50%{background-position:100% 50%}
        100%{background-position:0% 50%}
    }
    #MainMenu, footer, header {visibility: hidden;}
    .stFileUploader {background: rgba(255,255,255,0.1); border-radius: 15px; padding: 10px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 Music Crossfader Pro")

uploaded_files = st.file_uploader("เลือกไฟล์เพลง (เลือกหลายไฟล์ได้)", type=["mp3", "wav"], accept_multiple_files=True)

if uploaded_files:
    # เตรียมข้อมูลไฟล์ส่งให้ JavaScript
    audio_data = []
    for f in uploaded_files:
        # แปลงไฟล์เป็น Base64 เพื่อให้ส่งเข้าไปเล่นใน HTML ได้โดยตรง
        b64 = base64.b64encode(f.read()).decode()
        audio_data.append({"name": f.name, "data": f"data:audio/mp3;base64,{b64}"})
    
    # HTML/JS Player แบบ Crossfade 15 วินาที
    player_html = f"""
    <div id="wrapper" style="text-align: center; font-family: sans-serif;">
        <div style="background: rgba(0,0,0,0.7); color: #AFEEEE; padding: 15px; margin-bottom: 20px; border-radius: 10px; overflow: hidden;">
            <marquee id="marquee" style="font-size: 20px; font-weight: bold;">พร้อมเล่นเพลง... กรุณากดปุ่มด้านล่าง</marquee>
        </div>
        
        <div id="art" style="width: 280px; height: 280px; background: #AFEEEE; border: 8px solid #FF7F50; border-radius: 30px; margin: 0 auto 30px; display: flex; align-items: center; justify-content: center; font-size: 14px; box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
            <span id="art-text">Music Cover</span>
        </div>

        <button id="main-btn" style="
            padding: 20px 50px; 
            font-size: 1.5rem; 
            background: #FF7F50; 
            color: white; 
            border: none; 
            border-radius: 35% 65% 65% 35% / 30% 35% 65% 70%;
            cursor: pointer;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            transition: 0.3s;
        ">เล่นเพลง (START)</button>
    </div>

    <script>
        const playlist = {audio_data};
        let currentIndex = 0;
        const fadeTime = 15; // วินาที

        const btn = document.getElementById('main-btn');
        const marquee = document.getElementById('marquee');
        const art = document.getElementById('art');

        function playTrack(index) {{
            if (index >= playlist.length) index = 0;
            const track = playlist[index];
            
            const audio = new Audio(track.data);
            audio.volume = 0;
            
            marquee.innerText = "กำลังเล่น: " + track.name + "  >>>  เพลงถัดไป: " + (playlist[index+1] ? playlist[index+1].name : playlist[0].name);
            
            audio.play();
            fadeIn(audio);

            audio.ontimeupdate = function() {{
                const timeLeft = audio.duration - audio.currentTime;
                if (timeLeft <= fadeTime && !audio.isFadingOut) {{
                    audio.isFadingOut = true;
                    fadeOut(audio);
                    playTrack(index + 1);
                }}
            }};
        }}

        function fadeIn(audio) {{
            let v = 0;
            const interval = setInterval(() => {{
                if (v < 1) {{ v += 0.05; audio.volume = Math.min(v, 1); }}
                else clearInterval(interval);
            }}, (fadeTime * 1000) / 20);
        }}

        function fadeOut(audio) {{
            let v = 1;
            const interval = setInterval(() => {{
                if (v > 0) {{ v -= 0.05; audio.volume = Math.max(v, 0); }}
                else {{ clearInterval(interval); audio.pause(); }}
            }}, (fadeTime * 1000) / 20);
        }}

        btn.onclick = () => {{
            btn.style.display = 'none';
            playTrack(0);
        }};
    </script>
    """
    components.html(player_html, height=600)

else:
    st.info("💡 กรุณาเลือกไฟล์เพลงก่อนครับ (กดปุ่ม Browse files ด้านบน)")
