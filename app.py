# เพิ่มโค้ดส่วนตรวจสอบ Error เข้าไปใน JavaScript เดิม
master_js_v2 = """
<div style="background: linear-gradient(145deg, #1a1a1a, #000); border: 3px solid #FFD700; border-radius: 20px; padding: 25px; font-family: 'Courier New', monospace; box-shadow: 0 0 30px #FFD700; color: #FFD700; text-align: center;">
    
    <h1 id="clock" style="font-size: 70px; margin: 0; text-shadow: 0 0 20px #FFD700;">00:00:00</h1>
    <p id="err_msg" style="color: #ff4b4b; font-size: 12px;"></p> <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top:20px;">
        <div style="border: 1px solid #FFD700; padding: 10px; border-radius: 10px; background: #0a0a0a;">
            <p>📍 LAT: <span id="lat">-</span></p>
            <p>🌍 LON: <span id="lon">-</span></p>
        </div>
        <div style="border: 1px solid #FFD700; padding: 10px; border-radius: 10px; background: #0a0a0a;">
            <p>❤️ BPM: <span id="bpm">0</span></p>
            <p>🎙️ DB: <span id="db">0</span></p>
        </div>
    </div>
    
    <button id="start_btn" style="margin-top:20px; width:100%; padding:15px; background:linear-gradient(to bottom, #1e90ff, #00008b); color:white; border-radius:15px; border:none; cursor:pointer; font-weight:bold;">🚀 START ALL SENSORS</button>
</div>

<script>
    // ส่วนนาฬิกาเดิม
    setInterval(() => {
        const now = new Date();
        const thaiTime = new Date(now.getTime() + (now.getTimezoneOffset() * 60000) + (7 * 3600000));
        document.getElementById('clock').innerText = thaiTime.toTimeString().split(' ')[0];
    }, 1000);

    const btn = document.getElementById('start_btn');
    const err = document.getElementById('err_msg');

    btn.onclick = async () => {
        // --- 1. ขอ GPS ---
        navigator.geolocation.watchPosition(p => {
            document.getElementById('lat').innerText = p.coords.latitude.toFixed(4);
            document.getElementById('lon').innerText = p.coords.longitude.toFixed(4);
        }, e => err.innerText += "GPS Error | ");

        // --- 2. ขอไมค์ (Audio) ---
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const aCtx = new AudioContext();
            const anal = aCtx.createAnalyser();
            aCtx.createMediaStreamSource(stream).connect(anal);
            const data = new Uint8Array(anal.frequencyBinCount);
            function loopA(){
                anal.getByteFrequencyData(data);
                document.getElementById('db').innerText = Math.max(...data);
                requestAnimationFrame(loopA);
            }
            loopA();
        } catch(e) { err.innerText += "ไมค์ไม่ติด (ไม่ได้กดอนุญาต?) | "; }

        // --- 3. ขอกล้อง (Bio) ---
        try {
            const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            // ถ้าถึงตรงนี้ได้ แปลว่ากล้องติดแล้ว
            document.getElementById('bpm').innerText = "SCANNING";
        } catch(e) { err.innerText += "กล้องไม่ติด (ไม่ได้กดอนุญาต?) | "; }
    };
</script>
"""
import streamlit.components.v1 as components
components.html(master_js_v2, height=500)
