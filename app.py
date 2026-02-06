import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - TRUE COMPASS", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.subheader("🧭 เครื่องนำทางความจริง (Anti-Ghost Compass)")

compass_v2_js = """
<div style="background-color: #111; color: #FFD700; padding: 25px; border: 3px solid #FFD700; border-radius: 20px; text-align: center; font-family: sans-serif;">
    <div id="compass_ui" style="width: 220px; height: 220px; border-radius: 50%; border: 8px double #FFD700; margin: 0 auto; position: relative; transition: transform 0.2s cubic-bezier(0.1, 0.5, 0.1, 1);">
        <div style="width: 4px; height: 110px; background: linear-gradient(to bottom, #ff0000 50%, #ffffff 50%); position: absolute; top: 0; left: 108px; border-radius: 2px;"></div>
        <div style="position: absolute; top: 10px; left: 102px; font-weight: bold; font-size: 20px;">N</div>
    </div>
    
    <h1 id="deg_display" style="font-size: 50px; margin: 20px 0; text-shadow: 0 0 10px #FFD700;">---°</h1>
    <p id="status_text" style="color: #00ffff; font-weight: bold;">⚠️ เซนเซอร์ยังปิดอยู่</p>
    
    <button id="start_btn" style="width: 100%; padding: 15px; background: #FFD700; color: #000; border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 15px rgba(255,215,0,0.3);">
        📍 คลิกเพื่อเชื่อมต่อเข็มทิศ
    </button>
</div>

<script>
    const ui = document.getElementById('compass_ui');
    const degDisp = document.getElementById('deg_display');
    const status = document.getElementById('status_text');
    const btn = document.getElementById('start_btn');

    function handleOrientation(event) {
        // ลองดึงค่าจากหลายๆ แหล่ง (absolute, webkit, alpha)
        let heading = event.webkitCompassHeading || event.alpha;
        
        if (event.absolute === true || event.webkitCompassHeading !== undefined) {
            if (heading !== null) {
                let angle = Math.round(heading);
                ui.style.transform = `rotate(${-angle}deg)`;
                degDisp.innerText = angle + "°";
                status.innerText = "🟢 ตรวจพบทิศเหนือจริง";
                status.style.color = "#0f0";
            }
        } else {
            status.innerText = "🟡 กำลังคำนวณจากแรงเหวี่ยง...";
            // ถ้าไม่มีเข็มทิศแม่เหล็ก ให้ใช้ค่า Alpha แทน (อาจจะไม่แม่นเท่าแต่เข็มจะขยับ)
            let angle = Math.round(event.alpha);
            ui.style.transform = `rotate(${-angle}deg)`;
            degDisp.innerText = angle + "°";
        }
    }

    btn.onclick = async () => {
        if (typeof DeviceOrientationEvent.requestPermission === 'function') {
            const permission = await DeviceOrientationEvent.requestPermission();
            if (permission === 'granted') {
                window.addEventListener('deviceorientation', handleOrientation, true);
                btn.style.display = 'none';
            }
        } else {
            window.addEventListener('deviceorientationabsolute', handleOrientation, true);
            // ถ้าไม่รองรับ absolute ให้ลองธรรมดา
            window.addEventListener('deviceorientation', handleOrientation, true);
            btn.style.display = 'none';
        }
    };
</script>
"""

components.html(compass_v2_js, height=500)

st.info("💡 **สโลแกน: อยู่นิ่งๆ ไม่เจ็บตัว** - ถ้าเข็มขยับแล้ว ให้ลองหันไปทางทิศตะวันออก (90°) เพื่อเช็กความแม่นยำครับ")
