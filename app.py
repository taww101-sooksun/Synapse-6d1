import streamlit as st
import streamlit.components.v1 as components

# --- 1. SETUP ---
st.set_page_config(page_title="SYNAPSE X - MASTER", layout="wide")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.title("🛰️ SYNAPSE X : REALITY DASHBOARD")
st.subheader("ระบบรวมเซนเซอร์ความจริง (Version 1.0)")

# --- 2. MASTER LOGIC (HTML/JS) ---
# ส่วนนี้คือส่วนที่ดึงค่าจริงจากมือถือคุณต๊ะ
master_html = """
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-family: sans-serif;">
    
    <div style="border: 2px solid #FFD700; padding: 15px; border-radius: 12px; background: #111;">
        <small style="color: #888;">COLOR SCAN (RGB)</small>
        <video id="webcam" style="width: 100%; border-radius: 8px; margin-top: 5px;" autoplay playsinline></video>
        <canvas id="canvas" style="display:none;"></canvas>
        <h2 id="rgb_txt" style="color: #FFD700; margin-top: 10px;">R:0 G:0 B:0</h2>
    </div>

    <div style="border: 2px solid #00FFFF; padding: 15px; border-radius: 12px; background: #111;">
        <small style="color: #888;">SOUND FREQUENCY (Hz)</small>
        <div style="height: 60px; background: #222; margin-top: 5px; border-radius: 5px; overflow: hidden;">
            <canvas id="audio_viz" style="width: 100%; height: 100%;"></canvas>
        </div>
        <h2 id="hz_txt" style="color: #00FFFF; margin-top: 10px;">0 Hz</h2>
    </div>

    <div style="border: 2px solid #0f0; padding: 15px; border-radius: 12px; background: #111;">
        <small style="color: #888;">POWER STATUS</small>
        <h1 id="bat_txt" style="color: #0f0; font-size: 40px;">--%</h1>
        <p id="charge_txt" style="margin: 0;">รอกดเริ่ม...</p>
    </div>

    <div style="border: 2px solid #ff00ff; padding: 15px; border-radius: 12px; background: #111;">
        <small style="color: #888;">GEOLOCATION</small>
        <p id="gps_txt" style="font-size: 14px; margin-top: 10px;">LAT: -- <br> LON: --</p>
        <button id="mainBtn" style="width: 100%; padding: 12px; background: #FFD700; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;">🟢 เริ่มดึงค่าความจริง</button>
    </div>

</div>

<script>
    const btn = document.getElementById('mainBtn');
    
    async function startSensors() {
        // --- 1. Camera & Audio Stream ---
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: true });
        document.getElementById('webcam').srcObject = stream;

        // --- 2. Audio Context (Hz) ---
        const audioCtx = new AudioContext();
        const source = audioCtx.createMediaStreamSource(stream);
        const analyser = audioCtx.createAnalyser();
        analyser.fftSize = 256;
        source.connect(analyser);
        const dataArray = new Uint8Array(analyser.frequencyBinCount);

        // --- 3. Battery & GPS ---
        const battery = await navigator.getBattery();
        navigator.geolocation.getCurrentPosition(p => {
            document.getElementById('gps_txt').innerHTML = `LAT: ${p.coords.latitude.toFixed(4)} <br> LON: ${p.coords.longitude.toFixed(4)}`;
        });

        // --- 4. Update Loop ---
        btn.style.display = 'none';
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');

        function update() {
            // Update Color
            canvas.width = 1; canvas.height = 1;
            ctx.drawImage(document.getElementById('webcam'), 0, 0, 1, 1);
            const [r, g, b] = ctx.getImageData(0, 0, 1, 1).data;
            document.getElementById('rgb_txt').innerText = `R:${r} G:${g} B:${b}`;

            // Update Sound
            analyser.getByteFrequencyData(dataArray);
            let maxVal = 0; let maxIdx = 0;
            for(let i=0; i<dataArray.length; i++) {
                if(dataArray[i] > maxVal) { maxVal = dataArray[i]; maxIdx = i; }
            }
            document.getElementById('hz_txt').innerText = `${Math.round(maxIdx * audioCtx.sampleRate / 256)} Hz`;

            // Update Battery
            document.getElementById('bat_txt').innerText = Math.round(battery.level * 100) + "%";
            document.getElementById('charge_txt').innerText = battery.charging ? "🔌 Charging" : "🔋 Discharging";

            requestAnimationFrame(update);
        }
        update();
    }
    btn.onclick = startSensors;
</script>
"""

components.html(master_html, height=550)

st.warning("⚠️ โปรดก๊อปปี้เฉพาะโค้ดในกล่องดำนี้ไปวางเท่านั้น ห้ามเอาคำอธิบายภาษาไทยไปวางในไฟล์ .py นะครับ")
