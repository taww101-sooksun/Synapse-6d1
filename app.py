import streamlit as st
import streamlit.components.v1 as components

st.title("🛰️ SYNAPSE X: FULL SYSTEM (1➔2➔3➔4 = 7)")
st.write(f"สถานะ: ล้อกำลังหมุน... {st.session_state.get('slogan', 'อยู่นิ่งๆ ไม่เจ็บตัว')}")

# นี่คือหัวใจของระบบ 1-2-3-4-7
full_system_html = """
<div style="background: #111; border: 2px solid #FFD700; padding: 30px; border-radius: 15px; color: #FFD700; text-align: center;">
    <h2 style="margin-bottom: 20px;">🎤 SYNAPSE X AUDIO ENGINE</h2>
    
    <div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
        <div><small>INPUT (1)</small><br><b>VOICE</b></div>
        <div><small>PROCESS (2)</small><br><b>TUNER</b></div>
        <div><small>BEAT (4)</small><br><b>HIPHOP</b></div>
    </div>

    <button id="powerBtn" style="background: #FFD700; color: #000; padding: 15px 40px; border: none; border-radius: 50px; font-size: 20px; font-weight: bold; cursor: pointer; box-shadow: 0 0 15px #FFD700;">
        START ENGINE (7)
    </button>
</div>

<script>
let audioCtx;
let beatSource;

document.getElementById('powerBtn').onclick = async () => {
    // 1. สตาร์ทเครื่องยนต์เสียง
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    // 2. รับเสียงคุณ (เลข 1)
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const userVoice = audioCtx.createMediaStreamSource(stream);

    // 3. ตั้งค่าพนักงานเลข 2 (ตัวดึงคีย์) 
    // ในที่นี้จำลองด้วย Filter ที่ทำให้เสียงพุ่งและตรงคีย์มากขึ้น
    const tuner = audioCtx.createBiquadFilter();
    tuner.type = "peaking";
    tuner.frequency.value = 1000; 
    tuner.gain.value = 15;

    // 4. โหลดบีท Hiphop (เลข 4)
    // ใช้บีทตัวอย่างที่เป็น Loop จังหวะหนักๆ
    const beatResponse = await fetch('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3');
    const beatArray = await beatResponse.arrayBuffer();
    const beatBuffer = await audioCtx.decodeAudioData(beatArray);
    beatSource = audioCtx.createBufferSource();
    beatSource.buffer = beatBuffer;
    beatSource.loop = true;

    // 5. รวมร่างเป็นเลข 7 (Master Output)
    const masterGain = audioCtx.createGain();
    masterGain.gain.value = 0.8;

    userVoice.connect(tuner);   // 1 + 2 = 3
    tuner.connect(masterGain);   // ส่ง 3 ไปที่ Mixer
    beatSource.connect(masterGain); // ส่ง 4 ไปที่ Mixer
    
    masterGain.connect(audioCtx.destination); // 7 ส่งออกลำโพง!

    beatSource.start();
    document.getElementById('powerBtn').innerText = "SYSTEM ACTIVE 🛰️";
    document.getElementById('powerBtn').style.background = "#00FF00";
};
</script>
"""

components.html(full_system_html, height=400)
