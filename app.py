import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# --- ส่วนดีไซน์ ดำเงา ทองแสบตา ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(145deg, #1a1a1a, #000000); color: #FFD700; }
    h1 { color: #FFD700 !important; text-shadow: 0 0 20px #FFD700; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ SYNAPSE X: MULTI-SENSOR")

# --- ส่วนเนื้อหา (JavaScript) ---
# [คำอ่าน: คอม-ไบน์-เจ-เอส]
combined_js = """
<div style="background: linear-gradient(145deg, #222, #000); border: 2px solid #FFD700; border-radius: 20px; padding: 20px; text-align: center; color: #FFD700;">
    <h2>📍 SENSOR STATUS</h2>
    <p>GPS: <span id="lat">-</span>, <span id="lon">-</span></p>
    <p>MOTION: <span id="mag">0</span> G</p>
    <button id="btn" style="background: linear-gradient(to bottom, #1e90ff, #00008b); color: white; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer;">START SENSOR</button>
</div>

<script>
    const btn = document.getElementById('btn');
    btn.onclick = () => {
        // ขอ GPS
        navigator.geolocation.getCurrentPosition((pos) => {
            document.getElementById('lat').innerText = pos.coords.latitude.toFixed(4);
            document.getElementById('lon').innerText = pos.coords.longitude.toFixed(4);
        });
        // ขอ Motion
        window.addEventListener('devicemotion', (e) => {
            let acc = e.accelerationIncludingGravity;
            if(acc) {
                let m = Math.sqrt(acc.x*acc.x + acc.y*acc.y + acc.z*acc.z) / 9.8;
                document.getElementById('mag').innerText = m.toFixed(3);
            }
        });
    };
</script>
""" # <--- ตัวปัญหาอยู่ตรงนี้! ต้องแน่ใจว่ามี """ ปิดท้ายบรรทัดนะครับ

# สั่งให้แสดงผลบนเว็บ
components.html(combined_js, height=400)
