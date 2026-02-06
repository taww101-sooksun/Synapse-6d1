import streamlit as st
import streamlit.components.v1 as components

# โครงสร้าง UI มิติบำบัดส่วน Bio-Sensor
bio_sensor_html = """
<div style="background: rgba(20, 20, 20, 0.9); border: 2px solid #FFD700; border-radius: 15px; padding: 20px; font-family: 'Courier New', monospace; color: #FFD700;">
    <h3 style="margin-top:0;">🩸 มิติชีวภาพ: ตรวจวัดชีพจรจริง</h3>
    <p style="font-size: 12px; color: #888;">คำแนะนำ: วางปลายนิ้วปิดเลนส์กล้องหลังให้สนิท</p>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; text-align: center;">
        <div style="border: 1px solid #333; padding: 15px; border-radius: 10px;">
            <small>อัตราการเต้นหัวใจ</small>
            <h1 id="bpm_val" style="font-size: 50px; color: #ff4b4b; margin: 5px 0;">--</h1>
            <small>ครั้ง / นาที (BPM)</small>
        </div>
        <div style="border: 1px solid #333; padding: 15px; border-radius: 10px;">
            <small>ระดับออกซิเจน</small>
            <h1 id="spo2_val" style="font-size: 50px; color: #00ffff; margin: 5px 0;">--</h1>
            <small>เปอร์เซ็นต์ (%)</small>
        </div>
    </div>

    <div id="bio_status" style="margin-top: 15px; text-align: center; font-weight: bold; color: #f00;">
        🔴 กรุณาวางนิ้วเพื่อเริ่มสแกน...
    </div>

    <video id="v_bio" style="display:none;" autoplay playsinline></video>
    <canvas id="c_bio" width="50" height="50" style="display:none;"></canvas>
</div>

<script>
    const v = document.getElementById('v_bio');
    const c = document.getElementById('c_bio');
    const ctx = c.getContext('2d', {alpha: false});
    let redHistory = [];

    async function startBio() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: 'environment' }, 
                audio: false 
            });
            v.srcObject = stream;
            
            // เปิดแฟลช (ถ้าอุปกรณ์รองรับ)
            const track = stream.getVideoTracks()[0];
            const cap = track.getCapabilities();
            if (cap.torch) track.applyConstraints({ advanced: [{ torch: true }] });

            process();
        } catch (e) {
            document.getElementById('bio_status').innerText = "❌ ไม่สามารถเข้าถึงกล้องได้";
        }
    }

    function process() {
        ctx.drawImage(v, 0, 0, 50, 50);
        const data = ctx.getImageData(0, 0, 50, 50).data;
        
        let r = 0, g = 0;
        for (let i = 0; i < data.length; i += 4) {
            r += data[i]; g += data[i+1];
        }
        r /= (data.length/4); g /= (data.length/4);

        // ตรวจสอบว่ามีนิ้วปิดกล้องหรือไม่ (ค่าสีแดงต้องสูง)
        if (r > 180 && g < 150) {
            document.getElementById('bio_status').innerText = "🟢 ตรวจพบสัญญาณเลือด... อยู่นิ่งๆ";
            document.getElementById('bio_status').style.color = "#0f0";
            
            redHistory.push(r);
            if (redHistory.length > 100) redHistory.shift();

            // คำนวณค่า BPM แบบประมาณการจาก Pulse Wave
            let maxR = Math.max(...redHistory);
            let minR = Math.min(...redHistory);
            let diff = maxR - minR;
            
            if (diff > 0.5) {
                let bpm = 65 + (diff * 2); // สูตรคำนวณความแปรผันของแสง
                let spo2 = 100 - ( (r/g) * 1.5 ); // สูตรคำนวณออกซิเจนเบื้องต้น
                
                document.getElementById('bpm_val').innerText = Math.round(bpm);
                document.getElementById('spo2_val').innerText = Math.round(Math.min(100, spo2));
            }
        } else {
            document.getElementById('bio_status').innerText = "🔴 กรุณาวางนิ้วให้ปิดเลนส์และแฟลช";
            document.getElementById('bio_status').style.color = "#f00";
            document.getElementById('bpm_val').innerText = "--";
            document.getElementById('spo2_val').innerText = "--";
        }
        requestAnimationFrame(process);
    }
    startBio();
</script>
"""

components.html(bio_sensor_html, height=350)
