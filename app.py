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
