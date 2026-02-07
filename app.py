# [คำอ่าน: อิม-พอท-สตรีม-ลิต]
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import time

# --- 1. การตั้งค่าหน้าจอและดีไซน์ (ดำเงา ทองแสบตา) ---
st.set_page_config(page_title="SYNAPSE X - TRUTH", layout="centered")

st.markdown("""
<style>
    /* พื้นหลังดำเงา */
    .stApp {
        background: linear-gradient(145deg, #1a1a1a, #000000);
        color: #FFD700;
    }
    /* หัวข้อทองแสบตาเรืองแสง */
    h1, h2, h3 {
        color: #FFD700 !important;
        text-shadow: 0 0 20px #FFD700, 0 0 5px #ffffff;
        text-align: center;
    }
    /* กล่องเซนเซอร์สีดำเงา ขอบทอง */
    .sensor-card {
        background: linear-gradient(145deg, #222, #050505);
        border: 2px solid #FFD700;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 0 15px #FFD700;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ SYNAPSE X: MULTI-SENSOR")

# --- 2. ส่วนนาฬิกา (Master Clock) ---
# [คำอ่าน: ไท-นาว] = เวลาตอนนี้
thai_now = datetime.utcnow() + timedelta(hours=7)
current_time = thai_now.strftime("%H:%M:%S")
st.markdown(f"<div class='sensor-card'><h2>🕒 {current_time}</h2><p style='text-align:center;'>THAILAND REAL-TIME</p></div>", unsafe_allow_html=True)

# --- 3. รวมระบบ JavaScript (GPS, Bio, Motion, Sound) ---
# ผมรวม Logic ทั้งหมดไว้ใน Component เดียวเพื่อให้รันได้ลื่นๆ ครับ
combined_js = """
<div style="font-family: monospace;">
    
    <div style="background: linear-gradient(145deg, #00008b, #000033); border: 1px solid #00ffff; border-radius: 15px; padding: 15px; margin-bottom: 10px; text-align: center; color: white;">
        <h3 style="color: #00ffff;">📍 GPS LOCATION</h3>
        <p>Lat: <span id="lat">-</span> | Lon: <span id="lon">-</span></p>
        <button id="gps_btn" style="background: linear-gradient(to bottom, #1e90ff, #00008b); color: white; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer;">กดดึงพิกัดจริง</button>
    </div>

    <div style="background: linear-gradient(145deg, #8b0000, #330000); border: 1px solid #ff0000; border-radius: 15px; padding: 15px; margin-bottom: 10px; text-align: center; color: white;">
        <h3 style="color: #ff4b4b;">❤️ BIO & MOTION</h3>
        <p>BPM: <span id="bpm">0</span> | G-Force: <span id="mag">1.00</span></p>
        <video id="v" style="display:none;" autoplay playsinline></video>
        <canvas id="c" width="10" height="10" style="display:none;"></canvas>
    </div>

</div>

<script>
    // --- Logic GPS ---
    const gpsBtn = document.getElementById('gps_btn');
    gpsBtn.onclick = () => {
        navigator.geolocation.getCurrentPosition((pos) => {
            document.getElementById('lat').innerText = pos.coords.latitude.toFixed(4);
            document.getElementById('lon').innerText = pos.coords.longitude.toFixed(4);
        });
    };

    // --- Logic Motion (G-Force) ---
    window.addEventListener('devicemotion', (e) => {
        let acc = e.accelerationIncludingGravity;
        if(acc) {
            let mag = Math.sqrt(acc.x*acc.x + acc.y*acc
