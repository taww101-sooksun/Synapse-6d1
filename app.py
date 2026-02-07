import streamlit as st
import streamlit.components.v1 as components

st.title("🛰️ SYNAPSE X: AUDIO TEST (1 ➔ 2 ➔ 3)")
st.write(f"สโลแกน: {st.session_state.get('slogan', 'อยู่นิ่งๆ ไม่เจ็บตัว')}")

# สร้างหน้าต่างสำหรับรันพนักงานเลข 2 (Javascript)
audio_logic = """
<div style="background: #222; border: 2px solid #FFD700; padding: 20px; border-radius: 10px; color: white; text-align: center;">
    <h3>🎤 ระบบประมวลผลเลข 2</h3>
    <p>กดเริ่มแล้วลองพูดดูครับ ระบบจะดึงเสียงคุณให้สูงขึ้น (Pitch Shift)</p>
    <button id="startBtn" style="background: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">เริ่มระบบ</button>
</div>

<script>
let audioCtx;
let processor;

document.getElementById('startBtn').onclick = async () => {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const source = audioCtx.createMediaStreamSource(stream);

    // นี่คือไส้ในเลข 2 แบบง่าย (BiquadFilter ดึงความถี่)
    const filter = audioCtx.createBiquadFilter();
    filter.type = "highshelf";
    filter.frequency.value = 1000;
    filter.gain.value = 25; // ดึงให้เสียงแหลมขึ้น (จำลองการดึงไปหาเลข 3)

    source.connect(filter);
    filter.connect(audioCtx.destination);
    
    document.getElementById('startBtn').innerText = "ระบบกำลังทำงาน...";
    document.getElementById('startBtn').style.background = "#00FF00";
};
</script>
"""

components.html(audio_logic, height=250)
