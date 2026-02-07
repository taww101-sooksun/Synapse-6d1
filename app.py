import streamlit as st
import streamlit.components.v1 as components

st.title("🛰️ SYNAPSE X: FULL MIXER ACTIVE")
st.write("สถานะ: กำลังประกอบร่างเพลงเข้ากับเสียงคุณ")

full_mixer_html = """
<div style="background: #000; border: 2px solid #00FF00; padding: 25px; border-radius: 15px; color: #00FF00; text-align: center;">
    <h3 id="status">1. เตรียมไฟล์เพลง (เลข 4)</h3>
    <button id="loadBtn" style="background: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin-bottom: 10px;">
        📥 โหลดเพลงธารารัตน์
    </button>
    
    <div id="readyZone" style="display: none;">
        <h3 style="color: #00FF00;">✅ เพลงพร้อมแล้ว!</h3>
        <p>อ่านตาม: " รูปร่างหน้าตาเธอก็ดูจะดี... "</p>
        <button id="startBtn" style="background: #00FF00; color: black; padding: 20px 40px; border: none; border-radius: 50px; font-size: 20px; font-weight: bold; cursor: pointer;">
            🎤 เริ่มแร็ปสวมร่าง
        </button>
    </div>
</div>

<script>
let audioCtx, musicBuffer;

// ขั้นตอนโหลดเพลงลง Memory
document.getElementById('loadBtn').onclick = async () => {
    document.getElementById('status').innerText = "⏳ กำลังดึงเพลงจากดาวเทียม...";
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    try {
        const resp = await fetch('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3');
        const data = await resp.arrayBuffer();
        musicBuffer = await audioCtx.decodeAudioData(data);
        
        document.getElementById('loadBtn').style.display = "none";
        document.getElementById('status').style.display = "none";
        document.getElementById('readyZone').style.display = "block";
    } catch (e) {
        document.getElementById('status').innerText = "❌ โหลดไม่สำเร็จ: " + e.message;
    }
};

// ขั้นตอนการรวมเสียง (1 + 4 = 7)
document.getElementById('startBtn').onclick = async () => {
    if (audioCtx.state === 'suspended') await audioCtx.resume();
    
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const userVoice = audioCtx.createMediaStreamSource(stream);
    
    const musicSource = audioCtx.createBufferSource();
    musicSource.buffer = musicBuffer;
    musicSource.loop = true;

    // ต่อสายไฟ: เสียงคุณ + เพลง -> ลำโพง
    userVoice.connect(audioCtx.destination);
    musicSource.connect(audioCtx.destination);

    musicSource.start();
    document.getElementById('startBtn').innerText = "🔥 ON STAGE! (เสียงเพลงมาแล้ว)";
    document.getElementById('startBtn').style.background = "#FF4B4B";
};
</script>
"""

components.html(full_mixer_html, height=400)
