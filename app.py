import streamlit as st
import streamlit.components.v1 as components

st.title("🛰️ SYNAPSE X: JUMPSTART ENGINE")
st.write("เป้าหมาย: ทำให้ล้อหมุน (มีเสียงออก) ให้ได้ก่อน!")

repair_code = """
<div style="background: #000; border: 2px dashed #FFD700; padding: 25px; border-radius: 15px; color: #FFD700; text-align: center;">
    <h3 id="engineStatus">🔴 ENGINE OFF</h3>
    <p>ใส่หูฟัง แล้วกดปุ่มข้างล่างค้างไว้ 2 วินาทีครับ</p>
    
    <button id="igniteBtn" style="background: #FFD700; color: black; padding: 15px 30px; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 18px;">
        IGNITE (สตาร์ทเครื่อง)
    </button>

    <div id="log" style="margin-top: 20px; font-family: monospace; font-size: 12px; color: #888;"></div>
</div>

<script>
const log = (msg) => { document.getElementById('log').innerText += "\\n> " + msg; };

document.getElementById('igniteBtn').onclick = async () => {
    try {
        log("กำลังขอเข้าถึงไมโครโฟน...");
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        log("AudioContext สถานะ: " + audioCtx.state);

        if (audioCtx.state === 'suspended') {
            await audioCtx.resume();
            log("ปลุกระบบที่หลับอยู่... Resume สำเร็จ!");
        }

        const source = audioCtx.createMediaStreamSource(stream);
        
        // เลข 2: ตัวดึงเสียงแบบง่าย (High-pass) เพื่อเช็คว่าผ่านการปรุงแต่งไหม
        const processor = audioCtx.createBiquadFilter();
        processor.type = "highpass";
        processor.frequency.value = 800;

        source.connect(processor);
        processor.connect(audioCtx.destination);

        document.getElementById('engineStatus').innerText = "🟢 ENGINE RUNNING";
        document.getElementById('engineStatus').style.color = "#00FF00";
        log("เครื่องติดแล้ว! ลองพูดดูครับ");

    } catch (err) {
        log("ERROR: " + err.message);
        document.getElementById('engineStatus').innerText = "❌ ENGINE FAILURE";
    }
};
</script>
"""

components.html(repair_code, height=350)
