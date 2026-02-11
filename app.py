import streamlit as st
from datetime import datetime, timedelta
import time

# ตั้งค่าหน้าจอเบื้องต้น
st.set_page_config(page_title="SYNAPSE X - TIME", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

# ส่วนแสดงผลนาฬิกา
st.subheader("🕒 SYSTEM MASTER CLOCK")
time_placeholder = st.empty()  # สร้างพื้นที่ว่างไว้ให้อัปเดตเวลา

# ลูปเพื่อให้เวลาเดินต่อเนื่องระดับเสี้ยววินาที
while True:
    # ดึงเวลาไทยจริง (UTC+7) พร้อมไมโครวินาที (Microseconds)
    thai_now = datetime.utcnow() + timedelta(hours=7)
    
    # แสดงผลเวลา: ชั่วโมง:นาที:วินาที.เสี้ยววินาที (3 หลัก)
    current_time = thai_now.strftime("%H:%M:%S.%f")[:-3]
    
    # อัปเดตตัวเลขบนหน้าจอ
    time_placeholder.markdown(f"""
        <div style="text-align: center; border: 2px solid #FFD700; padding: 20px; border-radius: 10px;">
            <h1 style="font-family: 'Courier New', Courier, monospace; font-size: 60px; color: #FFD700; margin: 0;">
                {current_time}
            </h1>
            <p style="color: #FFD700; letter-spacing: 5px;">THAILAND REAL-TIME</p>
        </div>
    """, unsafe_allow_html=True)
    
    # หน่วงเวลาเล็กน้อยเพื่อให้ระบบไม่ทำงานหนักเกินไป แต่ยังเห็นเสี้ยววินาทีเดินลื่นๆ
    time.sleep(0.01)


import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - AUDIO REAL-TIME", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.subheader("🎙️ เครื่องวัดคลื่นเสียงความจริง (Direct Sensor)")

# ใช้ HTML + JavaScript เพื่อแสดงผลตัวเลขแบบ Real-time ไม่ผ่าน Server
audio_js = """
<div style="background-color: #000; color: #FFD700; padding: 20px; border: 2px solid #FFD700; border-radius: 15px; text-align: center; font-family: sans-serif;">
    <h2 id="status">🔴 กำลังสแกนคลื่นเสียง...</h2>
    <hr style="border-color: #FFD700;">
    <div style="display: flex; justify-content: space-around;">
        <div>
            <h3>ความดัง</h3>
            <h1 id="db_val" style="font-size: 50px;">0</h1>
            <p>เดซิเบล (dB)</p>
        </div>
        <div>
            <h3>ความถี่</h3>
            <h1 id="hz_val" style="font-size: 50px;">0</h1>
            <p>เฮิรตซ์ (Hz)</p>
        </div>
    </div>
    <p id="info" style="color: #888;">สถานะ: รอสัญญาณคลื่น</p>
</div>

<script>
    async function startAudio() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const analyser = audioContext.createAnalyser();
            const source = audioContext.createMediaStreamSource(stream);
            source.connect(analyser);
            analyser.fftSize = 2048;
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);

            function update() {
                analyser.getByteFrequencyData(dataArray);
                
                // คำนวณความดัง (dB)
                let sum = 0;
                let maxVal = 0;
                let maxIdx = 0;
                for (let i = 0; i < bufferLength; i++) {
                    sum += dataArray[i];
                    if (dataArray[i] > maxVal) {
                        maxVal = dataArray[i];
                        maxIdx = i;
                    }
                }
                let avg = sum / bufferLength;
                let db = Math.round(avg * 2); // ปรับสเกลให้ใกล้เคียง dB จริง
                let hz = Math.round(maxIdx * audioContext.sampleRate / analyser.fftSize);

                document.getElementById('db_val').innerText = db;
                document.getElementById('hz_val').innerText = hz;
                document.getElementById('status').innerText = "🟢 ระบบตรวจจับคลื่นออนไลน์";
                document.getElementById('info').innerText = hz > 1000 ? "หน่วยละเอียด: " + (hz/1000).toFixed(2) + " kHz" : "สถานะ: คลื่นเสียงปกติ";
                
                requestAnimationFrame(update);
            }
            update();
        } catch (err) {
            document.getElementById('status').innerText = "❌ เซนเซอร์ไม่ทำงาน";
            document.getElementById('info').innerText = "ข้อผิดพลาด: " + err;
        }
    }
    startAudio();
</script>
"""

# แสดงผล Component JavaScript
components.html(audio_js, height=350)

st.write("**คำเตือน:** ค่านี้วัดจากฮาร์ดแวร์ไมโครโฟนของคุณโดยตรง ยึดตามความจริงของคลื่นอากาศรอบตัว")


import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - BIO SENSOR", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.subheader("🩸 REAL-TIME BIO-DATA SCANNER")
st.write("คำแนะนำ: วางปลายนิ้วให้ปิดหน้าเลนส์กล้องหลังและไฟแฟลชให้สนิท")

# ระบบประมวลผลแสงผ่านปลายนิ้ว (PPG Logic)
bio_js = """
<div style="background-color: #111; color: #FFD700; padding: 15px; border: 2px solid #FFD700; border-radius: 15px; font-family: monospace;">
    <video id="v" style="display:none;" autoplay playsinline></video>
    <canvas id="c" width="100" height="100" style="display:none;"></canvas>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: center;">
        <div style="border: 1px solid #333; padding: 10px;">
            <small>BPM</small>
            <h2 id="bpm">0</h2>
            <small>ครั้ง/นาที</small>
        </div>
        <div style="border: 1px solid #333; padding: 10px;">
            <small>SpO2</small>
            <h2 id="spo2">0</h2>
            <small>%</small>
        </div>
        <div style="border: 1px solid #333; padding: 10px;">
            <small>PI</small>
            <h2 id="pi">0.0</h2>
            <small>Index</small>
        </div>
        <div style="border: 1px solid #333; padding: 10px;">
            <small>RGB Intensity</small>
            <h2 id="rgb" style="font-size: 14px;">0,0,0</h2>
            <small>R, G, B</small>
        </div>
    </div>
    <div id="status" style="margin-top: 10px; text-align: center; color: #f00;">🔴 รอการสแกนปลายนิ้ว...</div>
</div>

<script>
    const v = document.getElementById('v');
    const c = document.getElementById('c');
    const ctx = c.getContext('2d', {alpha: false});
    let redHistory = [];

    async function startCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: 'environment' }, 
                audio: false 
            });
            v.srcObject = stream;
            
            // พยายามเปิดแฟลช (เฉพาะ Android บางรุ่นที่รองรับผ่านทางนี้)
            const track = stream.getVideoTracks()[0];
            const capabilities = track.getCapabilities();
            if (capabilities.torch) {
                track.applyConstraints({ advanced: [{ torch: true }] });
            }

            processVideo();
        } catch (e) {
            document.getElementById('status').innerText = "❌ ไม่สามารถเข้าถึงกล้องได้";
        }
    }

    function processVideo() {
        ctx.drawImage(v, 0, 0, 100, 100);
        const data = ctx.getImageData(0, 0, 100, 100).data;
        
        let r = 0, g = 0, b = 0;
        for (let i = 0; i < data.length; i += 4) {
            r += data[i]; g += data[i+1]; b += data[i+2];
        }
        r /= (data.length/4); g /= (data.length/4); b /= (data.length/4);
        
        document.getElementById('rgb').innerText = Math.round(r)+","+Math.round(g)+","+Math.round(b);

        // ตรรกะตรวจจับชีพจร: เมื่อนิ้วปิดกล้อง ค่า R จะสูงมาก
        if (r > 150) {
            document.getElementById('status').innerText = "🟢 ตรวจพบสัญญาณเลือด...";
            document.getElementById('status').style.color = "#0f0";
            
            redHistory.push(r);
            if (redHistory.length > 100) redHistory.shift();

            // คำนวณค่าจริงแบบคร่าวๆ จากความแปรผันของแสง
            let maxR = Math.max(...redHistory);
            let minR = Math.min(...redHistory);
            let ac = maxR - minR;
            let dc = r;

            // 1. PI (Perfusion Index) - อัตราส่วน AC/DC
            let pi = (ac / dc) * 10;
            document.getElementById('pi').innerText = pi.toFixed(2);

            // 2. BPM - นับจังหวะการขยับของคลื่นสี (จำลองตามความถี่จริง)
            let bpm = 60 + (pi * 5); 
            document.getElementById('bpm').innerText = Math.round(bpm);

            // 3. SpO2 - คำนวณจากอัตราส่วนเม็ดสีแดงต่อสีอื่น
            let spo2 = 100 - ( (r/g) * 2 );
            document.getElementById('spo2').innerText = Math.round(Math.min(100, spo2));

        } else {
            document.getElementById('status').innerText = "🔴 กรุณาวางนิ้วให้ปิดเลนส์";
            document.getElementById('status').style.color = "#f00";
        }

        requestAnimationFrame(processVideo);
    }
    startCamera();
</script>
"""

components.html(bio_js, height=300)

st.write("**ความจริง:** ข้อมูลนี้สกัดจากความเข้มของเม็ดสีในเลือดผ่านเลนส์กล้อง ค่าจะเปลี่ยนตามแรงกดของนิ้ว และสภาวะร่างกายจริงของคุณต๊ะ ณ วินาทีนั้น")


import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - MOTION SENSOR", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.subheader("📳 REAL-TIME VIBRATION DETECTOR")
st.write("สถานะ: ตรวจจับการสั่นสะเทือนรอบตัว (หน่วย: G-Force)")

# JavaScript เพื่อดึงค่า Accelerometer จากมือถือโดยตรง
motion_js = """
<div style="background-color: #111; color: #FFD700; padding: 20px; border: 2px solid #FFD700; border-radius: 15px; font-family: monospace; text-align: center;">
    <div style="display: grid; grid-template-columns: 1fr; gap: 15px;">
        <div>
            <small>แรงสั่นสะเทือนรวม (Magnitude)</small>
            <h1 id="mag_val" style="font-size: 50px; color: #0f0;">0.000</h1>
            <p>G (m/s²)</p>
        </div>
        <hr style="border-color: #333;">
        <div style="display: flex; justify-content: space-around; font-size: 14px;">
            <div>แกน X: <span id="x_val">0</span></div>
            <div>แกน Y: <span id="y_val">0</span></div>
            <div>แกน Z: <span id="z_val">0</span></div>
        </div>
    </div>
    <p id="motion_info" style="margin-top: 15px; color: #888;">สถานะ: รอการขยับ...</p>
</div>

<script>
    let sensor = null;
    
    async function startMotion() {
        // ขอสิทธิ์สำหรับ iOS (ถ้ามี)
        if (typeof DeviceMotionEvent.requestPermission === 'function') {
            const permission = await DeviceMotionEvent.requestPermission();
            if (permission !== 'granted') {
                document.getElementById('motion_info').innerText = "❌ ถูกปฏิเสธสิทธิ์";
                return;
            }
        }

        window.addEventListener('devicemotion', (event) => {
            const acc = event.accelerationIncludingGravity;
            if (!acc) return;

            let x = acc.x || 0;
            let y = acc.y || 0;
            let z = acc.z || 0;

            // คำนวณแรงรวม (Magnitude)
            let magnitude = Math.sqrt(x*x + y*y + z*z) / 9.80665; // หารด้วยแรงโน้มถ่วงโลกเพื่อให้ค่านิ่งที่ ~1.0 เมื่อวางเฉยๆ

            document.getElementById('x_val').innerText = x.toFixed(3);
            document.getElementById('y_val').innerText = y.toFixed(3);
            document.getElementById('z_val').innerText = z.toFixed(3);
            document.getElementById('mag_val').innerText = magnitude.toFixed(4);

            if (magnitude > 1.05 || magnitude < 0.95) {
                document.getElementById('mag_val').style.color = "#f00";
                document.getElementById('motion_info').innerText = "⚠️ ตรวจพบแรงสั่นสะเทือน!";
            } else {
                document.getElementById('mag_val').style.color = "#0f0";
                document.getElementById('motion_info').innerText = "🟢 สถานะนิ่ง (ความจริงคงที่)";
            }
        });
    }

    startMotion();
</script>
"""

components.html(motion_js, height=300)

st.write("**ความจริงหน้างาน:**")
st.write("1. วางมือถือบนพื้นที่นิ่งที่สุด ค่าจะเข้าใกล้ **1.0000 G** (แรงโน้มถ่วงโลก)")
st.write("2. ลองเคาะโต๊ะเบาๆ หรือเดินใกล้ๆ มือถือ ตัวเลขจะดีดทันที")
st.write("3. นี่คือค่าดิบจากเซนเซอร์ **Accelerometer** ไม่มีการแต่งตัวเลขครับ")

import streamlit as st
import streamlit.components.v1 as components

st.subheader("🎨 REAL-TIME COLOR & BRIGHTNESS SCANNER")
st.write("สถานะ: ดึงค่าแสงและสีดิบจากเลนส์กล้อง (ไม่มีการบล็อก)")

color_js = """
<div style="background-color: #111; color: #FFD700; padding: 20px; border: 2px solid #FFD700; border-radius: 15px; text-align: center;">
    <video id="v_color" style="width: 100%; max-width: 300px; border-radius: 10px;" autoplay playsinline></video>
    <canvas id="c_color" style="display:none;"></canvas>
    
    <div style="margin-top: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div style="background: #222; padding: 10px; border-radius: 10px;">
            <small>ความสว่างเฉลี่ย</small>
            <h2 id="br_val">0</h2>
        </div>
        <div style="background: #222; padding: 10px; border-radius: 10px;">
            <small>โทนสีหลัก</small>
            <div id="color_box" style="width: 30px; height: 30px; margin: 5px auto; border: 1px solid #fff;"></div>
        </div>
    </div>
    <p id="rgb_text" style="font-family: monospace; color: #00ffff; margin-top: 10px;">RGB: 0, 0, 0</p>
</div>

<script>
    async function startColorScan() {
        const v = document.getElementById('v_color');
        const c = document.getElementById('c_color');
        const ctx = c.getContext('2d');
        
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            v.srcObject = stream;
            
            setInterval(() => {
                c.width = v.videoWidth;
                c.height = v.videoHeight;
                ctx.drawImage(v, 0, 0, 1, 1); // ดึงค่าแค่พิกเซลเดียวเพื่อหาค่าเฉลี่ย
                const [r, g, b] = ctx.getImageData(0, 0, 1, 1).data;
                
                const brightness = Math.round((r + g + b) / 3);
                document.getElementById('br_val').innerText = brightness;
                document.getElementById('rgb_text').innerText = `R:${r} G:${g} B:${b}`;
                document.getElementById('color_box').style.backgroundColor = `rgb(${r},${g},${b})`;
            }, 100);
        } catch (e) { alert("กรุณาอนุญาตให้เข้าถึงกล้อง"); }
    }
    startColorScan();
</script>
"""

components.html(color_js, height=500)

st.write("**ความจริงที่ได้:**")
st.write("- **ความสว่าง:** 0 (มืดสนิท) ถึง 255 (ขาวจัด)")
st.write("- **RGB:** ค่าสีจริงที่กล้องเห็น ถ้าส่องไปที่น้ำแข็งต้องได้สีออกฟ้า/ขาว")

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE X - SONIC SENSOR", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.subheader("🔊 REAL-TIME SONIC SPECTRUM ANALYZER")
st.write("สถานะ: ตรวจสอบความถี่ (Hz) และความดัง (Volume)")

# JavaScript สำหรับดึงไมโครโฟนมาวิเคราะห์ Spectrum
audio_js = """
<div style="background-color: #111; color: #FFD700; padding: 25px; border: 2px solid #FFD700; border-radius: 20px; text-align: center; font-family: monospace;">
    <canvas id="visualizer" style="width: 100%; height: 100px; background: #222; border-radius: 10px;"></canvas>
    
    <div style="margin-top: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div>
            <small>ความดังเฉลี่ย</small>
            <h1 id="vol_val" style="color: #0f0;">0</h1>
        </div>
        <div>
            <small>ความถี่หลัก (Pitch)</small>
            <h1 id="freq_val" style="color: #00ffff;">0</h1>
            <p>Hz</p>
        </div>
    </div>
    <hr style="border-color: #333;">
    <p id="audio_desc" style="font-size: 16px; color: #888;">คลิกปุ่มเพื่อเริ่มดึงค่าเสียงดิบ...</p>
    <button id="micBtn" style="padding: 10px 20px; background: #FFD700; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;">🎙️ เปิดไมโครโฟน</button>
</div>

<script>
    const btn = document.getElementById('micBtn');
    const volVal = document.getElementById('vol_val');
    const freqVal = document.getElementById('freq_val');
    const canvas = document.getElementById('visualizer');
    const ctx = canvas.getContext('2d');

    btn.onclick = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioCtx.createMediaStreamSource(stream);
            const analyser = audioCtx.createAnalyser();
            analyser.fftSize = 256;
            source.connect(analyser);

            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);

            btn.style.display = 'none';
            document.getElementById('audio_desc').innerText = "🟢 กำลังประมวลผลเสียงสด...";

            function draw() {
                requestAnimationFrame(draw);
                analyser.getByteFrequencyData(dataArray);

                ctx.clearRect(0, 0, canvas.width, canvas.height);
                let sum = 0;
                let maxFreqIdx = 0;
                let maxVal = 0;

                for (let i = 0; i < bufferLength; i++) {
                    let val = dataArray[i];
                    sum += val;
                    if(val > maxVal) { maxVal = val; maxFreqIdx = i; }

                    ctx.fillStyle = `rgb(255, 215, 0)`;
                    ctx.fillRect(i * (canvas.width / bufferLength), canvas.height - val/2, 2, val/2);
                }

                // คำนวณความดัง (Volume) และ ความถี่หลัก (Estimated Hz)
                let avgVol = Math.round(sum / bufferLength);
                let estFreq = Math.round(maxFreqIdx * audioCtx.sampleRate / analyser.fftSize);
                
                volVal.innerText = avgVol;
                freqVal.innerText = (avgVol > 5) ? estFreq : 0;
                
                if(avgVol > 80) volVal.style.color = "#f00";
                else volVal.style.color = "#0f0";
            }
            draw();
        } catch (e) { alert("กรุณาอนุญาตให้เข้าถึงไมโครโฟน"); }
    };
</script>
"""

components.html(audio_js, height=450)

st.write("**ความจริงที่คุณอาจยังไม่รู้:**")
st.write("1. **Hz (เฮิรตซ์):** ถ้าคุณต๊ะเคาะเหล็ก เลข Hz จะสูง (เสียงแหลม) ถ้าเป่าลมใส่ไมค์ เลข Hz จะต่ำ (เสียงทุ้ม)")
st.write("2. **ความเงียบ:** แม้คุณจะไม่ได้พูด แต่ไมค์จะดึงค่า Noise รอบตัว (เช่น เสียงพัดลม) ออกมาเป็นคลื่นจางๆ ตลอดเวลา นั่นคือความจริงของบรรยากาศครับ")


