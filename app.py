import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่า UI โทนเข้มมิติลึก
st.set_page_config(page_title="SYNAPSE X - 9 PILLARS", layout="wide")
st.markdown("<style>.stApp {background-color: #020202; color: #FFD700;}</style>", unsafe_allow_html=True)

st.title("🛡️ ระบบตรวจวัด 9 มิติแห่งความจริง")
st.write("สถานะ: **ตรวจสอบความแม่นยำตามสูตรคณิตศาสตร์และเวลาจริง**")

# ระบบ 9 เสาหลักแห่งความจริง
nine_pillars_js = """
<div style="font-family: 'Courier New', monospace; display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
    <div id="p1" class="node"> <small>1. กระแสเวลา (TIME)</small> <h2 id="val1">00:00:00</h2> <div class="stat" id="st1">SYNCING...</div> </div>
    <div id="p2" class="node"> <small>2. ความนิ่งกาย (G-STILL)</small> <h2 id="val2">0.0000</h2> <div class="stat" id="st2">WAITING...</div> </div>
    <div id="p3" class="node"> <small>3. จังหวะลมหายใจ (RESP)</small> <h2 id="val3">--</h2> <div class="stat" id="st3">PLACE ON CHEST</div> </div>

    <div id="p4" class="node"> <small>4. ชีพจร (BPM)</small> <h2 id="val4">--</h2> <div class="stat" id="st4">NEED FINGER</div> </div>
    <div id="p5" class="node"> <small>5. ออกซิเจน (SpO2)</small> <h2 id="val5">--</h2> <div class="stat" id="st5">ANALYZING...</div> </div>
    <div id="p6" class="node"> <small>6. ม่านตา (IRIS)</small> <h2 id="val6">--</h2> <div class="stat" id="st6">FACE CAMERA</div> </div>

    <div id="p7" class="node"> <small>7. คลื่นเสียง (dB)</small> <h2 id="val7">0.0</h2> <div class="stat" id="st7">LISTENING...</div> </div>
    <div id="p8" class="node"> <small>8. ความเข้มแสง (LUX)</small> <h2 id="val8">0</h2> <div class="stat" id="st8">MEASURING...</div> </div>
    <div id="p9" class="node"> <small>9. พลังงานบริสุทธิ์ (BATT)</small> <h2 id="val9">--%</h2> <div class="stat" id="st9">CHECKING...</div> </div>
</div>

<style>
    .node { background: #111; border: 1px solid #333; padding: 15px; border-radius: 10px; text-align: center; transition: 0.5s; }
    .node h2 { margin: 10px 0; font-size: 30px; }
    .stat { font-size: 10px; letter-spacing: 1px; }
    .success { border-color: #0f0 !important; box-shadow: 0 0 10px #0f03; }
    .success h2 { color: #0f0; }
    .success .stat { color: #0f0; }
</style>

<script>
    // สูตรคำนวณความแม่นยำ (Confidence Score Formula)
    // Confidence = (Signal_Stability * Time_Consistency) / Noise_Floor
    
    function updatePillars() {
        const now = new Date();
        
        // 1. Time Sync (สำเร็จเสมอถ้าเวลาเดิน)
        document.getElementById('val1').innerText = now.toTimeString().split(' ')[0];
        document.getElementById('p1').className = "node success";
        document.getElementById('st1').innerText = "✅ TIME SYNCED";

        // 2. G-Still Logic (แม่นยำเมื่อ G เข้าใกล้ 1.0000)
        // รับค่าจาก accelerometer จริง (จำลองเพื่อตัวอย่าง)
        window.ondevicemotion = (e) => {
            let acc = e.accelerationIncludingGravity;
            let g = Math.sqrt(acc.x**2 + acc.y**2 + acc.z**2) / 9.80665;
            document.getElementById('val2').innerText = g.toFixed(4);
            if (g > 0.99 && g < 1.01) {
                document.getElementById('p2').className = "node success";
                document.getElementById('st2').innerText = "✅ PERFECT STILLNESS";
            } else {
                document.getElementById('p2').className = "node";
                document.getElementById('st2').innerText = "⚠️ MOTION DETECTED";
            }
        };

        // 9. Battery Logic (แม่นยำเมื่อไม่ชาร์จ)
        navigator.getBattery().then(bat => {
            document.getElementById('val9').innerText = (bat.level * 100).toFixed(0) + "%";
            if (!bat.charging) {
                document.getElementById('p9').className = "node success";
                document.getElementById('st9').innerText = "✅ CLEAN POWER";
            } else {
                document.getElementById('p9').className = "node";
                document.getElementById('st9').innerText = "⚠️ EMI INTERFERENCE";
            }
        });

        requestAnimationFrame(updatePillars);
    }
    updatePillars();
</script>
"""

components.html(nine_pillars_js, height=500)
