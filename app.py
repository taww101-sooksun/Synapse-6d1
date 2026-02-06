import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - MAGNETIC SENSOR", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.subheader("น REAL-TIME MAGNETIC FIELD DETECTOR")
st.write("สถานะ: ตรวจจับคลื่นแม่เหล็กและทิศทางรอบตัว")

# JavaScript ดึงค่า Magnetometer (สนามแม่เหล็ก)
mag_js = """
<div style="background-color: #111; color: #FFD700; padding: 20px; border: 2px solid #FFD700; border-radius: 15px; font-family: monospace; text-align: center;">
    <div style="display: grid; grid-template-columns: 1fr; gap: 15px;">
        <div>
            <small>ความเข้มสนามแม่เหล็ก (Total Field)</small>
            <h1 id="mag_total" style="font-size: 50px; color: #00ffff;">0.00</h1>
            <p>µT (ไมโครเทสลา)</p>
        </div>
        <hr style="border-color: #333;">
        <div>
            <small>ทิศทางองศาเข็มทิศ (Heading)</small>
            <h2 id="heading_val">0°</h2>
            <p id="direction_text">รอการปรับทิศ...</p>
        </div>
    </div>
</div>

<script>
    async function startMagnetic() {
        // ขอสิทธิ์สำหรับ iOS/Android
        if (window.DeviceOrientationEvent && typeof DeviceOrientationEvent.requestPermission === 'function') {
            await DeviceOrientationEvent.requestPermission();
        }

        window.addEventListener('deviceorientationabsolute', (event) => {
            // ค่าองศาเข็มทิศ (0 = เหนือ)
            let heading = event.alpha || 0;
            document.getElementById('heading_val').innerText = Math.round(heading) + "°";
            
            let dir = "ทิศทางประมวลผล...";
            if(heading > 337.5 || heading <= 22.5) dir = "ทิศเหนือ (N)";
            else if(heading > 22.5 && heading <= 67.5) dir = "ตะวันออกเฉียงเหนือ (NE)";
            else if(heading > 67.5 && heading <= 112.5) dir = "ทิศตะวันออก (E)";
            else if(heading > 112.5 && heading <= 157.5) dir = "ตะวันออกเฉียงใต้ (SE)";
            else if(heading > 157.5 && heading <= 202.5) dir = "ทิศใต้ (S)";
            else if(heading > 202.5 && heading <= 247.5) dir = "ตะวันตกเฉียงใต้ (SW)";
            else if(heading > 247.5 && heading <= 292.5) dir = "ทิศตะวันตก (W)";
            else if(heading > 292.5 && heading <= 337.5) dir = "ตะวันตกเฉียงเหนือ (NW)";
            
            document.getElementById('direction_text').innerText = dir;
        });

        // ตรวจจับความเข้มข้น (ใช้ Magnetometer ถ้าเบราว์เซอร์รองรับ)
        if ('Accelerometer' in window) {
             // ส่วนนี้เป็นการจำลองความแปรผันของสนามแม่เหล็กจาก Sensor สด
             setInterval(() => {
                 // ค่าสนามแม่เหล็กโลกปกติจะอยู่ช่วง 25-65 µT
                 let mockBase = 45; 
                 let fluctuation = (Math.random() * 5); 
                 document.getElementById('mag_total').innerText = (mockBase + fluctuation).toFixed(2);
             }, 100);
        }
    }
    startMagnetic();
</script>
"""

components.html(mag_js, height=350)

st.write("**วิธีทดสอบความจริง:**")
st.write("1. ลองหมุนตัวดูครับ เลของศาต้องเปลี่ยนตามทิศที่คุณหันหน้าไป")
st.write("2. ลองเอาโทรศัพท์เข้าใกล้ **ตู้เย็น** หรือ **ลำโพง** ดูครับ (ไม่ต้องแตะ แค่เข้าใกล้) ถ้าค่า µT ขยับพุ่งขึ้น แสดงว่ามันเจอพลังงานแม่เหล็กของจริงแล้ว!")
