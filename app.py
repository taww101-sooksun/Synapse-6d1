import streamlit as st
import streamlit.components.v1 as components

st.title("🛰️ SYNAPSE X: EMERGENCY START")

fix_code = """
<div style="background: #000; border: 2px solid #00FF00; padding: 20px; border-radius: 15px; color: #00FF00; text-align: center;">
    <h3 id="st">สถานะ: รอการกดปุ่ม</h3>
    <button id="go" style="background: #00FF00; padding: 15px 30px; border: none; border-radius: 10px; cursor: pointer; font-weight: bold;">
        ▶️ ลองอีกครั้ง (FORCE START)
    </button>
</div>

<script>
document.getElementById('go').onclick = async () => {
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') await audioCtx.resume();

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const source = audioCtx.createMediaStreamSource(stream);
        
        // ต่อตรงเพื่อเช็คเสียงก่อน
        source.connect(audioCtx.destination);
        
        document.getElementById('st').innerText = "🔊 เครื่องติดแล้ว! พูดเลยครับ";
        document.getElementById('go').style.display = "none";
    } catch (e) {
        document.getElementById('st').innerText = "ติดปัญหา: " + e.message;
    }
};
</script>
"""
components.html(fix_code, height=200)
