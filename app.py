import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - LIGHT SENSOR", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.subheader("💡 REAL-TIME LIGHT INTENSITY SCANNER")
st.write("สถานะ: ตรวจวัดปริมาณแสงที่ตกกระทบหน้าจอ")

# JavaScript สำหรับดึงค่า Ambient Light Sensor
light_js = """
<div style="background-color: #111; color: #FFD700; padding: 25px; border: 2px solid #FFD700; border-radius: 20px; text-align: center; font-family: monospace;">
    <div id="light_box" style="width: 100px; height: 100px; background: #FFD700; border-radius: 50%; margin: 0 auto; box-shadow: 0 0 20px #FFD700; transition: 0.3s;"></div>
    
    <h1 id="lux_val" style="font-size: 60px; margin: 20px 0;">0</h1>
    <h2 style="color: #FFD700;">Lux (ลักซ์)</h2>
    
    <hr style="border-color: #333;">
    <p id="light_desc" style="font-size: 18px; color: #00ffff;">รอรับสัญญาณแสง...</p>
</div>

<script>
    const luxVal = document.getElementById('lux_val');
    const lightBox = document.getElementById('light_box');
    const lightDesc = document.getElementById('light_desc');

    // ตรวจสอบว่าเบราว์เซอร์รองรับ Generic Sensor API หรือไม่
    if ('AmbientLightSensor' in window) {
        try {
            const sensor = new AmbientLightSensor();
            sensor.onreading = () => {
                let lux = sensor.illuminance;
                luxVal.innerText = Math.round(lux);
                
                // ปรับความสว่างของวงกลมตามค่าแสงจริง
                let brightness = Math.min(lux / 10, 100);
                lightBox.style.filter = `brightness(${50 + brightness}%)`;
                lightBox.style.boxShadow = `0 0 ${lux/5}px #FFD700`;

                if(lux < 10) lightDesc.innerText = "🌑 มืดมาก (เหมาะกับการพักผ่อน)";
                else if(lux < 100) lightDesc.innerText = "☁️ แสงสลัว (ในอาคาร)";
                else if(lux < 500) lightDesc.innerText = "🏠 แสงสว่างปกติ (สำนักงาน)";
                else if(lux < 2000) lightDesc.innerText = "☀️ แสงจ้า (กลางแจ้ง/สปอร์ตไลท์)";
                else lightDesc.innerText = "🔥 แสงรุนแรง (แดดจัด)";
            };
            sensor.start();
        } catch (err) {
            lightDesc.innerText = "❌ เซนเซอร์ถูกบล็อก (เข้าไม่ถึงค่าดิบ)";
        }
    } else {
        // วิธีสำรอง: ใช้การคำนวณจากความสว่างหน้าจอหรือ API อื่น (ถ้ามี)
        lightDesc.innerText = "⚠️ เบราว์เซอร์ไม่รองรับ AmbientLight API";
        
        // ทดสอบด้วยการจำลองเลขวิ่งตาม Noise (เพื่อให้รู้ว่าระบบยังทำงาน)
        setInterval(() => {
            if(luxVal.innerText == "0") {
                lightDesc.innerText = "ระบบกำลังรอสิทธิ์เข้าถึงเซนเซอร์แสง...";
            }
        }, 2000);
    }
</script>
"""

components.html(light_js, height=450)

st.write("---")
st.write("**วิธีพิสูจน์ความจริง:**")
st.write("1. ลองเอามือ **'ปิด'** บริเวณด้านบนของหน้าจอ (แถวๆ กล้องหน้า) ตัวเลข Lux ต้องดิ่งลงใกล้ 0")
st.write("2. ลองหันหน้าจอไปทาง **'หลอดไฟ'** ตัวเลขต้องพุ่งขึ้นทันที")
st.write("3. ถ้าเลขเปลี่ยนตามจังหวะที่คุณเอามือปิด-เปิด นั่นคือ **'ความจริง'** ครับ")
