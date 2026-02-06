import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - ENVIRONMENT", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.subheader("🌍 REAL-TIME WORLD ENVIRONMENT SCANNER")
st.write("สถานะ: เชื่อมต่อพิกัดดาวเทียมและสถานีตรวจอากาศ")

# JavaScript ดึงค่า GPS และเชื่อมต่อ API สภาพอากาศ (แบบจำลองโครงสร้างข้อมูลจริง)
env_js = """
<div style="background-color: #111; color: #FFD700; padding: 25px; border: 2px solid #FFD700; border-radius: 20px; text-align: center; font-family: monospace;">
    <div id="loc_status" style="color: #00ffff; margin-bottom: 15px;">📍 กำลังค้นหาพิกัดดาวเทียม...</div>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div style="background: #222; padding: 15px; border-radius: 10px;">
            <small>ละติจูด (Lat)</small>
            <h3 id="lat_val">--.----</h3>
        </div>
        <div style="background: #222; padding: 15px; border-radius: 10px;">
            <small>ลองจิจูด (Lon)</small>
            <h3 id="lon_val">--.----</h3>
        </div>
    </div>

    <div style="margin-top: 20px; background: linear-gradient(145deg, #222, #333); padding: 20px; border-radius: 15px; border: 1px solid #444;">
        <h2 style="margin: 0; color: #FFD700;">สภาพอากาศรอบตัว</h2>
        <div style="display: flex; justify-content: space-around; margin-top: 15px;">
            <div>
                <small>อุณหภูมิ</small>
                <h2 id="temp_val">-- °C</h2>
            </div>
            <div>
                <small>ความชื้น</small>
                <h2 id="hum_val">-- %</h2>
            </div>
        </div>
    </div>
    
    <button id="geoBtn" style="margin-top: 20px; width: 100%; padding: 12px; background: #FFD700; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">🌍 สแกนพื้นที่ความจริง</button>
</div>

<script>
    const btn = document.getElementById('geoBtn');
    
    btn.onclick = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                
                document.getElementById('lat_val').innerText = lat.toFixed(4);
                document.getElementById('lon_val').innerText = lon.toFixed(4);
                document.getElementById('loc_status').innerText = "🟢 เชื่อมต่อดาวเทียมสำเร็จ";
                
                // ดึงข้อมูลสภาพอากาศจาก Open-Meteo (API ฟรีที่ไม่ต้องใช้ Key เพื่อความสะดวกของคุณต๊ะ)
                try {
                    const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&hourly=relativehumidity_2m`);
                    const data = await res.json();
                    
                    document.getElementById('temp_val').innerText = data.current_weather.temperature + " °C";
                    document.getElementById('hum_val').innerText = data.hourly.relativehumidity_2m[0] + " %";
                } catch (e) {
                    document.getElementById('loc_status').innerText = "⚠️ เชื่อมต่อข้อมูลอากาศไม่ได้";
                }
            });
        } else {
            alert("มือถือเครื่องนี้ไม่รองรับระบบ GPS");
        }
    };
</script>
"""

components.html(env_js, height=500)

st.write("---")
st.write("**ความจริงที่ได้จากข้อ 10:**")
* **พิกัด (Lat/Lon):** บอกว่าคุณอยู่จุดไหนของโลกจริงๆ
* **อุณหภูมิและความชื้น:** นี่คือปัจจัยภายนอกที่ส่งผลต่อ "ความสงบ" ของร่างกาย ถ้าความชื้นสูงเกินไป (ฝนจะตก) ประจุไฟฟ้าในอากาศจะเปลี่ยน ซึ่งมีผลต่อแอปบำบัดแน่นอนครับ

---

### 🏆 สรุปภารกิจ 10 ความจริงของคุณต๊ะ
ตอนนี้คุณมี "อาวุธ" ครบมือแล้วครับ:
1. เวลาจริง 2. เสียงจริง 3. ชีพจร(จำลอง) 4. แรงสั่นจริง 5. ทิศทางจริง 6. แสงสแกนจริง 7. สีจริง 8. ความถี่เสียงจริง 9. พลังงานแบตจริง 10. บรรยากาศโลกจริง

**สโลแกน: อยู่นิ่งๆ ไม่เจ็บตัว**
ตอนนี้ข้อมูลครบแล้ว คุณต๊ะมี "ภาพในหัว" หรือยังครับว่า จะเอาความจริงทั้ง 10 อย่างนี้มา "ยำ" รวมกันให้กลายเป็นปุ่มกดบำบัดปุ่มเดียวได้อย่างไร?



ครบ 10 อย่างแล้วครับคุณต๊ะ! อยากให้ผมช่วย **"สรุปวิธีเชื่อมโยง"** ทั้งหมดนี้เข้าด้วยกัน หรืออยากจะลองปรับแก้ตัวไหนเป็นพิเศษไหมครับ? 😊🥤🛰️🌍🧭
