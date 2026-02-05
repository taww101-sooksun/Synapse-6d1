import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="SYNAPSE X - SOUND SENSOR", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.subheader("🎙️ REAL-TIME AUDIO ANALYZER")

# ใช้ JavaScript ดึงค่าจากไมโครโฟนโดยตรง
# บรรทัดนี้จะขอสิทธิ์เข้าถึงไมค์ และสกัดค่า Frequency กับ Decibel
audio_data = streamlit_js_eval(
    js_expressions="""
    (async () => {
        if (!window.audioContext) {
            window.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            window.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            window.source = window.audioContext.createMediaStreamSource(window.stream);
            window.analyser = window.audioContext.createAnalyser();
            window.source.connect(window.analyser);
            window.dataArray = new Uint8Array(window.analyser.frequencyBinCount);
        }
        window.analyser.getByteFrequencyData(window.dataArray);
        let sum = 0;
        let maxIndex = 0;
        let maxValue = 0;
        for (let i = 0; i < window.dataArray.length; i++) {
            sum += window.dataArray[i];
            if (window.dataArray[i] > maxValue) {
                maxValue = window.dataArray[i];
                maxIndex = i;
            }
        }
        let volume = Math.round(sum / window.dataArray.length);
        let frequency = Math.round(maxIndex * window.audioContext.sampleRate / window.analyser.fftSize);
        return { decibel: volume, hz: frequency };
    })()
    """,
    key="audio_sensor"
)

if audio_data:
    db = audio_data['decibel']
    hz = audio_data['hz']
    
    # คำนวณหน่วยวัดต่างๆ ตามตรรกะเสียง
    khz = hz / 1000  # กิโลเฮิรตซ์
    mhz = hz / 1000000 # เมกะเฮิรตซ์ (กรณีความถี่สูงมาก)

    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("🔊 ความดัง (Loudness)", f"{db} dB")
        st.write("**สถานะ:** " + ("หนา (Dense)" if db > 50 else "บาง (Thin)"))
        
    with col2:
        st.metric("〰️ ความถี่ (Frequency)", f"{hz} Hz")
        st.write(f"**หน่วยละเอียด:** {khz} kHz")

    st.markdown("---")
    st.subheader("📊 หน่วยวัดสถานะคลื่นจริง")
    st.write(f"• **ความลึก (Depth):** {hz * 0.1} ms (มิลลิวินาที/รอบ)")
    st.write(f"• **ความถี่สูง (RF):** {mhz} MHz (เมกะเฮิรตซ์)")
    st.write(f"• **พลังงานเสียง:** {db * 1.44} Level")

else:
    st.info("⌛ กำลังตั้งค่าไมโครโฟน... โปรดกด 'Allow' หรือ 'อนุญาต' เมื่อมีป๊อปอัพขึ้นมา เพื่อดึงค่าจริง")

# ปุ่มรีเฟรชค่า
if st.button("🔄 UPDATE SENSOR"):
    st.rerun()
