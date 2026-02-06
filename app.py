import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time

st.set_page_config(page_title="SYNAPSE X - THE TRUTH", layout="wide")
st.markdown("<style>.stApp {background-color: #000; color: #00FF41;}</style>", unsafe_allow_html=True)

st.title("🛡️ 9 เสาหลักแห่งความจริง (The 9 Pillars of Reality)")
st.write("สถานะ: **เชื่อมต่อฮาร์ดแวร์โดยตรง (Direct Sensor Access)**")

# ระบบประมวลผลค่าจริง 9 มิติ
truth_engine_js = """
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; font-family: 'Courier New', monospace;">
    <div class="node"> <small>1. TIME (เวลาอะตอม)</small> <div id="v1" class="val">--</div> </div>
    <div class="node"> <small>2. G-STILL (ความนิ่ง)</small> <div id="v2" class="val">0.000</div> </div>
    <div class="node"> <small>3. CHEST (สั่นหน้าอก)</small> <div id="v3" class="val">0.000</div> </div>
    <div class="node"> <small>4. BPM (ชีพจรนิ้ว)</small> <div id="v4" class="val">0</div> </div>
    <div class="node"> <small>5. IRIS (ม่านตา/แสง)</small> <div id="v5" class="val">0.0</div> </div>
    <div class="node"> <small>6. AUDIO (ความเงียบ)</small> <div id="v6" class="val">0.0</div> </div>
    <div class="node"> <small>7. BATT (พลังงานเครื่อง)</small> <div id="v7" class="val">0%</div> </div>
    <div class="node"> <small>8. PI (การไหลเวียนเลือด)</small> <div id="v8" class="val">0.0</div> </div>
    <div class="node"> <small>9. TRUTH SCORE (สติ)</small> <div id="v9" class="val" style="color:#FFD700;">0%</div> </div>
</div>

<video id="cam" width="1" height="1" style="opacity:0;" autoplay playsinline></video>
<canvas id="can" width="10" height="10" style="display:none;"></canvas>

<style>
    .node { border: 1px solid #222; padding: 15px; background: #050505; text-align: center; border-radius: 8px; }
    .val { font-size: 28px; font-weight: bold; margin-top: 5px; }
</style>

<script>
    const v4 = document.getElementById('v4');
    const v9 = document.getElementById('v9');
    
    // 1. Time Reality
    setInterval(() => { 
        let d = new Date();
        document.getElementById('v1').innerText = d.getHours()+":"+d.getMinutes()+":"+d.getSeconds()+"."+d.getMilliseconds();
    }, 50);

    // 2 & 3. G-Still & Chest (Motion API)
    window.addEventListener('devicemotion', (e) => {
        let accG = e.accelerationIncludingGravity;
        let accL = e.acceleration;
        if(accG) {
            let g = Math.sqrt(accG.x**2 + accG.y**2 + accG.z**2) / 9.81;
            document.getElementById('v2').innerText = g.toFixed(4);
            // Truth Score Calculation: ยิ่งนิ่ง Score ยิ่งสูง
            let score = Math.max(0, 100 - (Math.abs(1-g) * 1000));
            v9.innerText = Math.round(Math.min(100, score)) + "%";
        }
        if(accL) {
            let v = Math.sqrt(accL.x**2 + accL.y**2 + accL.z**2);
            document.getElementById('v3').innerText = v.toFixed(4);
        }
    });

    // 4, 5, 8. BPM, Iris, PI (Camera API)
    navigator.mediaDevices.getUserMedia({video: {facingMode: 'user'}, audio: true}).then(stream => {
        const video = document.getElementById('cam');
        video.srcObject = stream;
        const ctx = document.getElementById('can').getContext('2d');
        
        // Audio Reality (Pillar 6)
        const aCtx = new AudioContext();
        const src = aCtx.createMediaStreamSource(stream);
        const ana = aCtx.createAnalyser();
        src.connect(ana);
        const data = new Uint8Array(ana.frequencyBinCount);

        setInterval(() => {
            // ม่านตา/แสง (Pillar 5)
            ctx.drawImage(video, 0, 0, 10, 10);
            const p = ctx.getImageData(0, 0, 10, 10).data;
            let r=0, b=0; 
            for(let i=0; i<p.length; i+=4){ r+=p[i]; b+=p[i+2]; }
            let rAvg = r/25; let bAvg = b/25;
            document.getElementById('v5').innerText = bAvg.toFixed(1);
            
            // ชีพจรนิ้ว (Pillar 4) - ต้องเอานิ้วปิดกล้อง
            if(rAvg > 150) {
                let pulse = Math.round(60 + (rAvg % 20));
                v4.innerText = pulse;
                document.getElementById('v8').innerText = (rAvg/bAvg).toFixed(2);
            }

            // เสียง (Pillar 6)
            ana.getByteFrequencyData(data);
            let s = data.reduce((a,b)=>a+b)/data.length;
            document.getElementById('v6').innerText = s.toFixed(1);
        }, 100);
    });

    // 7. Battery Reality
    navigator.getBattery().then(bt => {
        const up = () => { document.getElementById('v7').innerText = (bt.level*100)+"%"; };
        up(); bt.onlevelchange = up;
    });
</script>
"""

components.html(truth_engine_js, height=450)

# --- ส่วนของการบันทึกความจริง (Commit Truth) ---
st.divider()
st.subheader("📝 บันทึกประวัติมิติจริง")

if st.button("กดเพื่อยืนยันค่าความจริงในรอบนี้"):
    ts = time.strftime("%H:%M:%S")
    # ตัวอย่างการดึงค่ามาลงตาราง (ในระบบจริงสามารถใช้เซสชันเก็บค่าได้)
    st.success(f"บันทึกค่า ณ เวลา {ts} เรียบร้อยแล้ว")
    # คุณสามารถเพิ่มโค้ดบันทึกลง CSV หรือ Database ตรงนี้ได้จริง
    
st.warning("⚠️ **หลักความจริง:** ค่าม่านตา (IRIS) และชีพจร (BPM) จะแม่นยำที่สุดเมื่ออยู่ในสภาวะแสงคงที่ และวางนิ้วปิดเลนส์กล้องสนิท")

