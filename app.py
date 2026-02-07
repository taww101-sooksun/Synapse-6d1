import streamlit as st
import streamlit.components.v1 as components

st.title("🛰️ SYNAPSE X: HIPHOP ENGINE ACTIVE")

full_power_code = """
<div style="background: #000; border: 2px solid #FFD700; padding: 25px; border-radius: 15px; color: #FFD700; text-align: center;">
    <h2 style="color: #00FF00;">🟢 SYSTEM ONLINE</h2>
    <p>1. ใส่หูฟัง | 2. กดปุ่มทอง | 3. เริ่มแร็ปได้เลย!</p>
    
    <button id="startBtn" style="background: #FFD700; color: black; padding: 20px; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; width: 100%; font-size: 20px; box-shadow: 0 0 20px #FFD700;">
        🔥 START HIPHOP SESSION
    </button>

    <div style="margin-top: 20px;">
        <label>ปรับระดับเสียงบีท (เลข 4)</label><br>
        <input type="range" id="beatVol" min="0" max="1" step="0.1" value="0.5" style="width: 80%;">
    </div>
</div>

<script>
let audioCtx, beatSource, beatGain;

document.getElementById('startBtn').onclick = async () => {
    if (audioCtx) return; // กันกดซ้ำ
    
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    // --- เลข 1 & 2 (เสียงคุณ) ---
    const userVoice = audioCtx.createMediaStreamSource(stream);
    const tuner = audioCtx.createBiquadFilter();
    tuner.type = "peaking";
    tuner.frequency.value = 1500; // จูนเสียงให้พุ่ง
    tuner.gain.value = 10;

    // --- เลข 4 (บีท Hiphop) ---
    beatGain = audioCtx.createGain();
    beatGain.gain.value = 0.5;
    
    // ผมใช้บีท Hiphop แบบเบสแน่นๆ ให้ครับ
    const resp = await fetch('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3');
    const arrayBuffer = await resp.arrayBuffer();
    const buffer = await audioCtx.decodeAudioData(arrayBuffer);
    
    beatSource = audioCtx.createBufferSource();
    beatSource.buffer = buffer;
    beatSource.loop = true;

    // --- รวมร่างเป็นเลข 7 ---
    userVoice.connect(tuner);
    tuner.connect(audioCtx.destination);
    
    beatSource.connect(beatGain);
    beatGain.connect(audioCtx.destination);

    beatSource.start();
    document.getElementById('startBtn').innerText = "🎤 ON STAGE!";
    document.getElementById('startBtn').style.background = "#00FF00";
};

// ตัวปรับเสียงบีท
document.getElementById('beatVol').oninput = (e) => {
    if (beatGain) beatGain.gain.value = e.target.value;
};
</script>
"""

components.html(full_power_code, height=450)
