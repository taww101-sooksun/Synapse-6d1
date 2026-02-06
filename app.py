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
