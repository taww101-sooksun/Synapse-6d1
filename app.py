import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - COMPASS", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.subheader("🧭 เข็มทิศตรวจทิศทางจริง (True North)")

# JavaScript ตัวนี้จะเน้นการขอสิทธิ์และดึงค่าองศาที่แม่นยำที่สุด
compass_js = """
<div style="background-color: #111; color: #FFD700; padding: 20px; border: 2px solid #FFD700; border-radius: 15px; text-align: center; font-family: sans-serif;">
    <div id="compass_ring" style="width: 200px; height: 200px; border-radius: 50%; border: 5px solid #FFD700; margin: 0 auto; position: relative; transition: transform 0.1s;">
        <div style="width: 5px; height: 100px; background: red; position: absolute; top: 0; left: 97.5px; border-radius: 5px;"></div>
        <div style="position: absolute; top: 5px; left: 92px; font-weight: bold;">N</div>
        <div style="position: absolute; bottom: 5px; left: 92px; font-weight: bold;">S</div>
        <div style="position: absolute; top: 90px; left: 5px; font-weight: bold;">W</div>
        <div style="position: absolute; top: 90px; right: 5px; font-weight: bold;">E</div>
    </div>
    <h1 id="degrees" style="font-size: 40px; margin-top: 20px;">0°</h1>
    <h2 id="direction_th" style="color: #00ffff;">รอการขยับ...</h2>
    <button id="askBtn" style="padding: 10px 20px; background: #FFD700; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">เปิดใช้งานเซนเซอร์เข็มทิศ</button>
</div>

<script>
    const ring = document.getElementById('compass_ring');
    const degText = document.getElementById('degrees');
    const dirTh = document.getElementById('direction_th');
    const btn = document.getElementById('askBtn');

    async function initCompass() {
        if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission === 'function') {
            try {
                const permission = await DeviceOrientationEvent.requestPermission();
                if (permission === 'granted') {
                    startCompass();
                }
            } catch (e) { console.error(e); }
        } else {
            startCompass();
        }
    }

    function startCompass() {
        btn.style.display = 'none';
        window.addEventListener('deviceorientationabsolute', (event) => {
            let heading = event.alpha || event.webkitCompassHeading;
            if (heading === null) return;

            // ปรับองศา (ต้องติดลบเพื่อให้เข็มหมุนทวนเข็มตามการหันของเรา)
            let rotateDeg = 360 - heading;
            ring.style.transform = `rotate(${rotateDeg}deg)`;
            degText.innerText = Math.round(heading) + "°";

            let th = "";
            if(heading > 337.5 || heading <= 22.5) th = "ทิศเหนือ";
            else if(heading > 22.5 && heading <= 67.5) th = "ตะวันออกเฉียงเหนือ";
            else if(heading > 67.5 && heading <= 112.5) th = "ทิศตะวันออก";
            else if(heading > 112.5 && heading <= 157.5) th = "ตะวันออกเฉียงใต้";
            else if(heading > 157.5 && heading <= 202.5) th = "ทิศใต้";
            else if(heading > 202.5 && heading <= 247.5) th = "ตะวันตกเฉียงใต้";
            else if(heading > 247.5 && heading <= 292.5) th = "ทิศตะวันตก";
            else if(heading > 292.5 && heading <= 337.5) th = "ตะวันตกเฉียงเหนือ";
            dirTh.innerText = th;
        }, true);
    }

    btn.onclick = initCompass;
</script>
"""

components.html(compass_js, height=450)

st.warning("⚠️ ถ้าเข็มไม่หมุน: กรุณากดปุ่มสีเหลือง 'เปิดใช้งานเซนเซอร์เข็มทิศ' และหมุนโทรศัพท์เป็นรูปเลข 8 เพื่อปรับแต่งเซนเซอร์ (Calibration) ครับ")
