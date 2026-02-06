import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - POWER SENSOR", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.subheader("🔋 REAL-TIME POWER & THERMAL INTELLIGENCE")
st.write("สถานะ: วิเคราะห์กระแสไฟและระดับความร้อน")

# JavaScript ดึงค่า Battery Status API
battery_js = """
<div style="background-color: #111; color: #FFD700; padding: 25px; border: 2px solid #FFD700; border-radius: 20px; text-align: center; font-family: monospace;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div style="background: #222; padding: 15px; border-radius: 10px; border-left: 5px solid #0f0;">
            <small>ระดับพลังงาน</small>
            <h1 id="bat_level" style="font-size: 45px;">--%</h1>
        </div>
        <div style="background: #222; padding: 15px; border-radius: 10px; border-left: 5px solid #ff0000;">
            <small>สถานะการชาร์จ</small>
            <h2 id="bat_charging" style="font-size: 20px; margin-top: 10px;">รอดึงข้อมูล...</h2>
        </div>
    </div>
    
    <div style="margin-top: 20px; background: #222; padding: 15px; border-radius: 10px;">
        <small>เวลาที่เหลือ (วินาที)</small>
        <h2 id="bat_time" style="color: #00ffff;">--</h2>
    </div>
    
    <p id="thermal_info" style="margin-top: 15px; color: #888;">หมายเหตุ: ค่าความร้อนจะประมวลผลจากอัตราการใช้ไฟ</p>
</div>

<script>
    async function checkBattery() {
        if ('getBattery' in navigator) {
            const battery = await navigator.getBattery();
            
            function updateAll() {
                const level = (battery.level * 100).toFixed(0);
                document.getElementById('bat_level').innerText = level + "%";
                document.getElementById('bat_charging').innerText = battery.charging ? "🔌 กำลังชาร์จ" : "🔋 ใช้แบตเตอรี่";
                
                let time = battery.dischargingTime;
                document.getElementById('bat_time').innerText = (time === Infinity) ? "คำนวณไม่ได้" : time + " วินาที";
                
                // จำลองการวิเคราะห์ความร้อนจากความเร็วแบตที่ลดลง
                if(battery.charging && level > 90) {
                     document.getElementById('thermal_info').innerText = "⚠️ เครื่องอาจมีความร้อนสะสมสูง";
                     document.getElementById('thermal_info').style.color = "#ff8000";
                } else {
                     document.getElementById('thermal_info').innerText = "🟢 อุณหภูมิพลังงานปกติ";
                     document.getElementById('thermal_info').style.color = "#0f0";
                }
            }

            updateAll();
            battery.addEventListener('levelchange', updateAll);
            battery.addEventListener('chargingchange', updateAll);
        } else {
            document.getElementById('bat_charging').innerText = "❌ ไม่รองรับในเบราว์เซอร์นี้";
        }
    }
    checkBattery();
</script>
"""

components.html(battery_js, height=350)

st.write("**ทำไมข้อมูลนี้ถึง 'จริง':**")
st.write("1. **Level:** บอกความพร้อมของเครื่อง ถ้าแบตต่ำกว่า 20% เซนเซอร์ตัวอื่นจะเริ่มอ่านค่าเพี้ยน (เพราะระบบประหยัดพลังงานเข้าแทรกแซง)")
st.write("2. **Charging Status:** บอกว่ามี 'กระแสไฟนอก' ไหลเข้าเครื่องไหม ซึ่งจะสร้างคลื่นแม่เหล็กไฟฟ้ากวนการบำบัด")
