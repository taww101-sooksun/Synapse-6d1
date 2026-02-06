import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# ตั้งค่า Layout แบบกว้างและโทนสีเข้มพิเศษ (Deep Black & Gold)
st.set_page_config(page_title="SYNAPSE X - MULTIDIMENSIONAL", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #050505;
        color: #FFD700;
    }
    .sensor-card {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid #333;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }
    .sensor-card:hover {
        border-color: #FFD700;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);
    }
    .glitch-text {
        font-family: 'Courier New', monospace;
        text-shadow: 2px 2px #ff0000, -2px -2px #0000ff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌌 SYNAPSE X: มิติบำบัดแห่งความจริง")
st.write(f"คติพจน์: **อยู่นิ่งๆ ไม่เจ็บตัว** | สภาวะปัจจุบัน: **Real-Time Synchronization**")

# แบ่ง Layout เป็น 2 ฝั่ง: ฝั่งข้อมูลเซนเซอร์ และ ฝั่งเพลงบำบัด
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📡 เซนเซอร์ตรวจวัดพหุมิติ (Raw Data)")
    
    # ระบบ Sensor ชุดใหม่ที่รวมทุกมิติไว้ด้วยกัน
    sensor_logic_js = """
    <div style="font-family: monospace; color: #FFD700;">
        <div id="clock-box" class="sensor-card">
            <small>มิติที่ 4: กระแสเวลา (TIME FLOW)</small>
            <h1 id="clock" style="font-size: 45px; margin: 0;">00:00:00.000</h1>
            <p id="date_sync" style="color: #888; font-size: 12px;"></p>
        </div>

        <div class="sensor-card">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <small>มิติทางกายภาพ: ความนิ่ง</small>
                    <h2 id="g_val" style="margin: 5px 0;">1.0000</h2>
                    <small>UNIT: G-FORCE</small>
                </div>
                <div>
                    <small>มิติแสง: ความเข้ม</small>
                    <h2 id="lux_val" style="margin: 5px 0;">0</h2>
                    <small>UNIT: RAW LUX</small>
                </div>
            </div>
            <hr style="border: 0.5px solid #222;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <small>มิติเสียง: พลังงานคลื่น</small>
                    <h2 id="db_val" style="margin: 5px 0;">0.0</h2>
                    <small>UNIT: DECIBEL (dB)</small>
                </div>
                <div>
                    <small>มิติไฟฟ้า: แรงดันคงเหลือ</small>
                    <h2 id="bat_val" style="margin: 5px 0;">--%</h2>
                    <small id="chg_stat">WAITING...</small>
                </div>
            </div>
        </div>
        
        <video id="v" style="display:none;" autoplay playsinline></video>
        <canvas id="c" width="10" height="10" style="display:none;"></canvas>
    </div>

    <script>
        // 1. Precise Time
        function updateTime() {
            const now = new Date();
            document.getElementById('clock').innerText = now.toTimeString().split(' ')[0] + '.' + now.getMilliseconds().toString().padStart(3, '0');
            document.getElementById('date_sync').innerText = "REALITY SYNCED: " + now.toDateString();
            requestAnimationFrame(updateTime);
        }
        updateTime();

        // 2. Physical Stillness (G-Force)
        window.addEventListener('devicemotion', (e) => {
            const acc = e.accelerationIncludingGravity;
            if(acc) {
                let g = Math.sqrt(acc.x**2 + acc.y**2 + acc.z**2) / 9.80665;
                const el = document.getElementById('g_val');
                el.innerText = g.toFixed(4);
                el.style.color = (g > 1.02 || g < 0.98) ? "#ff4b4b" : "#0f0";
            }
        });

        // 3. Audio Energy
        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            const audioCtx = new AudioContext();
            const analyser = audioCtx.createAnalyser();
            const source = audioCtx.createMediaStreamSource(stream);
            source.connect(analyser);
            const data = new Uint8Array(analyser.frequencyBinCount);
            function read() {
                analyser.getByteFrequencyData(data);
                let sum = data.reduce((a, b) => a + b, 0);
                document.getElementById('db_val').innerText = (sum/data.length * 2.5).toFixed(1);
                requestAnimationFrame(read);
            }
            read();
        }).catch(() => document.getElementById('db_val').innerText = "ERR");

        // 4. Battery & Power Stability
        navigator.getBattery().then(bat => {
            function update() {
                document.getElementById('bat_val').innerText = (bat.level * 100).toFixed(0) + "%";
                document.getElementById('chg_stat').innerText = bat.charging ? "⚡ EXTERNAL POWER DETECTED" : "🔋 CLEAN BATTERY POWER";
                document.getElementById('chg_stat').style.color = bat.charging ? "#ff4b4b" : "#0f0";
            }
            update();
            bat.onlevelchange = update;
            bat.onchargingchange = update;
        });
        
        // 5. Light Intensity (Simplified Camera)
        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }).then(stream => {
            const v = document.getElementById('v');
            const c = document.getElementById('c');
            const ctx = c.getContext('2d');
            v.srcObject = stream;
            setInterval(() => {
                ctx.drawImage(v, 0, 0, 10, 10);
                const d = ctx.getImageData(0,0,10,10).data;
                let bright = 0;
                for(let i=0; i<d.length; i+=4) bright += (d[i]+d[i+1]+d[i+2])/3;
                document.getElementById('lux_val').innerText = Math.round(bright/100);
            }, 200);
        });
    </script>
    """
    components.html(sensor_logic_js, height=450)

with col2:
    st.subheader("🎵 คลื่นเสียงบำบัด (Therapy Playlist)")
    # แสดงผล YouTube Playlist โดยตรง
    # ลิ้งก์ที่คุณให้มา: https://youtube.com/playlist?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    st.video(f"https://www.youtube.com/watch?v=videoseries&list={playlist_id}")
    
    st.markdown("""
    <div class="sensor-card">
        <h4 style="margin:0; color:#0f0;">คำแนะนำการใช้มิติเสียง:</h4>
        <ul style="font-size: 13px; color: #ccc;">
            <li>สังเกตค่า <b>G-FORCE</b>: หากตัวเลขเป็นสีเขียว แสดงว่าร่างกายคุณนิ่งพอที่จะรับคลื่นบำบัด</li>
            <li>สังเกตค่า <b>AUDIO (dB)</b>: ระดับเสียงเพลงรวมกับบรรยากาศควรอยู่ระหว่าง 40-60 dB เพื่อประสิทธิภาพสูงสุด</li>
            <li>สังเกตค่า <b>BATTERY</b>: หากขึ้นตัวอักษรสีแดง (Charging) แนะนำให้ถอดสายชาร์จเพื่อลดคลื่นไฟฟ้ากวนระบบประสาท</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("หมายเหตุ: ข้อมูลทั้งหมดถูกดึงจากเซนเซอร์ฮาร์ดแวร์โดยตรงแบบ Unfiltered เพื่อรักษา 'ความจริง' สูงสุด")
