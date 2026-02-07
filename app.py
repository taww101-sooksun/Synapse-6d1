import streamlit as st
import streamlit.components.v1 as components

st.title("🛰️ SYNAPSE X: ARTIST COVER MODE")
st.subheader("Song: ธารารัตน์ (YOUNGOHM)")

artist_mode_html = """
<div style="background: #000; border: 3px solid #00FF00; padding: 25px; border-radius: 15px; color: #00FF00; text-align: center;">
    <h3 id="status">เตรียมตัวพยากรณ์เสียง...</h3>
    
    <div style="background: #222; padding: 15px; margin: 15px 0; border-radius: 10px; font-size: 20px;">
        <p id="lyric">" รูปร่างหน้าตาเธอก็ดูจะดี... "</p>
    </div>

    <button id="startBtn" style="background: #00FF00; color: black; padding: 15px 40px; border: none; border-radius: 50px; font-size: 18px; font-weight: bold; cursor: pointer;">
        ▶️ เริ่มการสวมร่าง (START SESSION)
    </button>
</div>

<script>
document.getElementById('startBtn').onclick = async () => {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    // โหลดเพลงต้นฉบับ (เลข 3 + 4)
    // หมายเหตุ: ในระบบจริงเราจะใช้ไฟล์ที่คุณเตรียมไว้ แต่ตรงนี้ผมใช้ตัวอย่างเสียงนำทางครับ
    const resp = await fetch('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'); 
    const buffer = await audioCtx.decodeAudioData(await resp.arrayBuffer());
    const source = audioCtx.createBufferSource();
    source.buffer = buffer;

    // ระบบเลข 2: เชื่อมเสียงไมค์คุณ (1) เข้ากับระบบ
    const userVoice = audioCtx.createMediaStreamSource(stream);
    
    // รวมร่างออกลำโพง (7)
    source.connect(audioCtx.destination);
    userVoice.connect(audioCtx.destination);

    source.start();
    document.getElementById('status').innerText = "🔴 กำลังอัดเสียง... พูดตามเลย!";
    document.getElementById('startBtn').style.display = "none";
};
</script>
"""

components.html(artist_mode_html, height=400)
