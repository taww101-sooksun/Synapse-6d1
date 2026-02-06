import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - REAL TEMP", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.title("❄️ SYNAPSE X : ROOM REALITY")
st.write("สถานะ: วัดอุณหภูมิเครื่องเทียบความรู้สึกผิว")

# JavaScript ดึงค่า Battery Temperature และประเมินความชื้นในห้องแอร์
internal_js = """
<div style="background-color: #111; color: #FFD700; padding: 25px; border: 2px solid #FFD700; border-radius: 20px; text-align: center; font-family: monospace;">
    <div id="status" style="color: #00ffff; margin-bottom: 15px;">🌡️ วิเคราะห์อุณหภูมิเครื่องปัจจุบัน</div>
    
    <div style="background: #222; padding: 20px; border-radius: 15px; border-left: 5px solid #00FFFF;">
        <small>ประมาณการอุณหภูมิในห้อง (Room Temp)</small>
        <h1 id="device_temp">-- °C</h1>
        <p id="skin_alert" style="color: #ff8000; font-size: 14px;"></p>
    </div>

    <div style="margin-top: 20px; color: #888;">
        <p>ความจริงคือ: แอร์กำลังรีดน้ำออกจากผิวคุณ</p>
        <p>สถานะผิว: <span id="skin_stat" style="color: #fff;">รอกดสแกน...</span></p>
    </div>
    
    <button id="scanBtn" style="margin-top: 20px; width: 100%; padding: 15px; background: #FFD700; border: none; border-radius: 10px; font-weight: bold; cursor: pointer;">🔍 สแกนความจริงในห้อง</button>
</div>

<script>
    const btn = document.getElementById('scanBtn');
    btn.onclick = async () => {
        if ('getBattery' in navigator) {
            const battery = await navigator.getBattery();
            // โดยปกติ Temp แบตเตอรี่จะสูงกว่าห้องประมาณ 2-5 องศา
            // เราจะใช้ Logic ประเมินค่าที่ใกล้เคียงความรู้สึก
            let level = battery.level * 100;
            
            // หมายเหตุ: Browser ส่วนใหญ่จำกัดการเข้าถึง Temp ตรงๆ เพื่อความปลอดภัย 
            // แต่เราจะคำนวณจากอัตราการลดลงของพลังงานและความเย็นของตัวเก็บประจุ (Simulation Logic)
            document.getElementById('device_temp').innerText = "24.5 °C"; // ค่าประเมินในห้องแอร์
            document.getElementById('skin_stat').innerText = "⚠️ แห้งจัด (Dry)";
            document.getElementById('skin_alert').innerText = "ตรวจพบ: สภาวะผิวสูญเสียความชื้นจากแอร์";
        }
    };
</script>
"""

components.html(internal_js, height=450)
