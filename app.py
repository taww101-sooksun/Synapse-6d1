import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - GPS TEST", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.title("🌍 TEST: GPS & ENVIRONMENT")
st.write("สถานะ: กำลังรอการเชื่อมต่อดาวเทียม...")

# JavaScript สำหรับดึง GPS และเชื่อมต่อ API อากาศ
env_test_js = """
<div style="background-color: #111; color: #FFD700; padding: 25px; border: 2px solid #FFD700; border-radius: 20px; text-align: center; font-family: monospace;">
    <div id="status" style="color: #00ffff; margin-bottom: 15px;">📍 พร้อมสแกนพิกัด</div>
    
    <div style="margin-bottom: 20px;">
        <p style="margin:0;">ละติจูด (Lat)</p>
        <h2 id="lat">-</h2>
        <p style="margin:0;">ลองจิจูด (Lon)</p>
        <h2 id="lon">-</h2>
    </div>

    <div style="background: #222; padding: 20px; border-radius: 15px;">
        <p style="margin:0;">🌡️ อุณหภูมิ: <span id="temp" style="font-size: 25px;">--</span> °C</p>
        <p style="margin:10px 0 0 0;">💧 ความชื้น: <span id="hum" style="font-size: 25px;">--</span> %</p>
    </div>
    
    <button id="btn" style="margin-top: 20px; width: 100%; padding: 15px; background: #FFD700; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 18px;">🌍 กดเพื่อดึงค่าความจริง</button>
</div>

<script>
    const btn = document.getElementById('btn');
    btn.onclick = () => {
        document.getElementById('status').innerText = "🛰️ กำลังติดต่อดาวเทียม...";
        
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async (pos) => {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                
                document.getElementById('lat').innerText = lat.toFixed(4);
                document.getElementById('lon').innerText = lon.toFixed(4);
                document.getElementById('status').innerText = "🟢 เชื่อมต่อพิกัดสำเร็จ";

                // ดึงข้อมูลอากาศจาก Open-Meteo (ไม่ต้องใช้ Key)
                try {
                    const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&hourly=relativehumidity_2m`);
                    const data = await res.json();
                    document.getElementById('temp').innerText = data.current_weather.temperature;
                    document.getElementById('hum').innerText = data.hourly.relativehumidity_2m[0];
                } catch (e) {
                    document.getElementById('status').innerText = "⚠️ ดึงข้อมูลอากาศไม่ได้";
                }
            }, (err) => {
                document.getElementById('status').innerText = "❌ ปฏิเสธการเข้าถึง GPS";
            });
        }
    };
</script>
"""

components.html(env_test_js, height=500)

st.info("💡 เมื่อรันแล้ว อย่าลืมกด 'Allow' หรือ 'อนุญาต' ให้เบราว์เซอร์เข้าถึงตำแหน่ง (Location) นะครับ")
