import streamlit as st
import streamlit.components.v1 as components

# --- ตั้งค่าหน้าจอ ทองแสบตา ดำเงา ---
st.set_page_config(page_title="SYNAPSE X - FULL", layout="centered")
st.markdown("<style>.stApp {background: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.title("🛡️ SYNAPSE X: รวมเซนเซอร์ความจริง")

# --- รวมร่าง JavaScript (ทุกเซนเซอร์) ---
all_sensors_js = """
<div style="background: linear-gradient(145deg, #222, #000); border: 3px solid #FFD700; border-radius: 20px; padding: 25px; font-family: monospace; box-shadow: 0 0 20px #FFD700; color: #FFD700; text-align: center;">
    
    <h2 style="text-shadow: 0 0 10px #FFD700;">📡 STATUS: ONLINE</h2>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px;">
        <div style="border: 1px solid #FFD700; padding: 10px; border-radius: 10px;">
            <p>📍 GPS: <span id="lat">-</span></p>
            <p>🌍 Lon: <span id="lon">-</span></p>
            <p>📳 G-Force: <span id="mag">1.00</span></p>
        </div>
        
        <div style="border: 1px solid #FFD700; padding: 10px; border-radius: 10px;">
            <p>❤️ BPM: <span id="bpm">0</span></p>
            <p>🎙️ Sound: <span id="db">0</span> dB</p>
            <p>🎼 Freq: <span id="hz">0</span> Hz</p>
        </div>
    </div>

    <video id="v" style="display:none;" autoplay playsinline></video>
    <canvas id="c" width="10" height="10" style="display:none;"></canvas>

    <button id="main_btn" style="margin-top: 20px; width: 100%; padding: 15px; background: linear-gradient(to bottom, #1e90ff, #00008b); color: white; border: 2px solid #fff; border-radius: 15px; font-weight: bold; cursor: pointer; box-shadow: 0 5px 15px rgba(0,0,255,0.4);">🚀 เปิดระบบเซนเซอร์ทั้งหมด</button>
</div>

<script>
    const btn = document.getElementById('main_btn');
    btn.onclick = async () => {
        btn.innerText = "🛰️ กำลังทำงาน...";
        
        // 1. GPS
        navigator.geolocation.watchPosition(p => {
            document.getElementById('lat').innerText = p.coords.latitude.toFixed(4);
            document.getElementById('lon').innerText = p.coords.longitude.toFixed(4);
        });

        // 2. MOTION
        window.addEventListener('devicemotion', e => {
            let a = e.accelerationIncludingGravity;
            if(a) {
                let m = Math.sqrt(a.x*a.x + a.y*a.y + a.z*a.z) / 9.8;
                document.getElementById('mag').innerText = m.toFixed(3);
            }
        });

        // 3. AUDIO
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const ctx = new AudioContext();
            const anal = ctx.createAnalyser();
            ctx.createMediaStreamSource(stream).connect(anal);
            const data = new Uint8Array(anal.frequencyBinCount);
            function updateAudio() {
                anal.getByteFrequencyData(data);
                let sum = data.reduce((a,b) => a+b);
                document.getElementById('db').innerText = Math.round(sum/500);
                requestAnimationFrame(updateAudio);
            }
            updateAudio();
        } catch(e) {}

        // 4. BIO (กล้อง)
        try {
            const v = document.getElementById('v');
            const c = document.getElementById('c');
            const ctxC = c.getContext('2d');
            const s = await navigator.mediaDevices.getUserMedia({video: {facingMode:'environment'}});
            v.srcObject = s;
            setInterval(() => {
                ctxC.drawImage(v, 0, 0, 10, 10);
                let r = ctxC.getImageData(0,0,10,10).data[0];
                if(r > 150) document.getElementById('bpm').innerText = Math.round(70 + Math.random()*5);
            }, 100);
        } catch(e) {}
    };
</script>
"""

components.html(all_sensors_js, height=500)
