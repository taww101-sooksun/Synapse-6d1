import streamlit as st
import streamlit.components.v1 as components

# --- ดีไซน์ ดำเงา ทองแสบตา ---
st.set_page_config(page_title="SYNAPSE X - MASTER", layout="centered")
st.markdown("<style>.stApp {background: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.title("🛡️ SYNAPSE X: ULTIMATE TRUTH")

# --- รวมร่าง นาฬิกาทีเด็ด + เซนเซอร์ ---
master_js = """
<div style="background: linear-gradient(145deg, #1a1a1a, #000); border: 3px solid #FFD700; border-radius: 20px; padding: 25px; font-family: 'Courier New', monospace; box-shadow: 0 0 30px #FFD700; color: #FFD700; text-align: center;">
    
    <div style="margin-bottom: 20px; border-bottom: 2px solid #FFD700; padding-bottom: 10px;">
        <h1 id="clock" style="font-size: 70px; margin: 0; text-shadow: 0 0 20px #FFD700, 0 0 5px #fff;">00:00:00</h1>
        <p style="letter-spacing: 5px; color: #FFD700;">SYSTEM MASTER CLOCK</p>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div style="background: #333; border: 2px solid #00008b; padding: 10px; border-radius: 10px;">
            <h3 style="font-size: 14px; margin:0;">📍 GPS & MOTION</h3>
            <hr>
            <p>Lat: <span id="lat">-</span></p>
            <p>Lon: <span id="lon">-</span></p>
            <p>G-Force: <span id="mag">1.000</span></p>
        </div>
        <div style="background: #111; border: 1px solid #FFD700; padding: 10px; border-radius: 10px;">
            <h3 style="font-size: 14px; margin:0;">❤️ BIO & SOUND</h3>
            <hr>
            <p>BPM: <span id="bpm">0</span></p>
            <p>Sound: <span id="db">0</span> dB</p>
            <p>Freq: <span id="hz">0</span> Hz</p>
        </div>
    </div>

    <button id="start_btn" style="margin-top: 25px; width: 100%; padding: 15px; background: linear-gradient(to bottom, #1e90ff, #00008b); color: white; border: 2px solid #fff; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 20px; box-shadow: 0 5px 15px rgba(0,0,255,0.4);">🛰️ เปิดระบบความจริงทั้งหมด</button>
</div>

<script>
    // --- ฟังก์ชันนาฬิกา (คำอ่าน: อัปเดต-คล็อก) ---
    function updateClock() {
        const now = new Date();
        // ปรับเวลาให้เป็นไทย (UTC+7)
        const thaiTime = new Date(now.getTime() + (now.getTimezoneOffset() * 60000) + (7 * 3600000));
        const h = String(thaiTime.getHours()).padStart(2, '0');
        const m = String(thaiTime.getMinutes()).padStart(2, '0');
        const s = String(thaiTime.getSeconds()).padStart(2, '0');
        document.getElementById('clock').innerText = `${h}:${m}:${s}`;
    }
    setInterval(updateClock, 1000); // ทำงานทุกวินาที
    updateClock();

    // --- ส่วนเซนเซอร์ (เหมือนเดิม) ---
    const btn = document.getElementById('start_btn');
    btn.onclick = async () => {
        btn.innerText = "🌀 ระบบกำลังสแกนความจริง...";
        
        // GPS & MOTION & AUDIO & BIO LOGIC (รันเหมือนที่คุณทำได้แล้ว)
        navigator.geolocation.watchPosition(p => {
            document.getElementById('lat').innerText = p.coords.latitude.toFixed(4);
            document.getElementById('lon').innerText = p.coords.longitude.toFixed(4);
        });

        window.addEventListener('devicemotion', e => {
            let a = e.accelerationIncludingGravity;
            if(a) {
                let m = Math.sqrt(a.x*a.x + a.y*a.y + a.z*a.z) / 9.80665;
                document.getElementById('mag').innerText = m.toFixed(3);
            }
        });
        
        // (ส่วน Audio และ Bio เพิ่มเติมตรงนี้ได้เลยตามโค้ดก่อนหน้า)
    };
</script>
"""

components.html(master_js, height=650)
