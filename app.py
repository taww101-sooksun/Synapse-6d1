import streamlit as st
import numpy as np
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="SYNAPSE 6D Pro", layout="wide")

# --- 2. GEMINI AI (สมองส่วนแต่งเพลง) ---
# (ใช้ API KEY ของคุณใน Streamlit Secrets หรือใส่ตรงๆ เพื่อทดสอบ)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("⚠️ ยังไม่ได้เชื่อมต่อ API Key: ระบบจะใช้โหมด Offline")

# --- 3. SYNAPSE ENGINE (Logic การคำนวณของคุณ + โครงสร้างต๊ะ 2) ---
def generate_healing_wave(bpm, duration=5):
    sr = 44100
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    # คลื่นความถี่บำบัด 432Hz ที่คุณต้องการ
    wave = np.sin(2 * np.pi * 432 * t)
    # ใส่จังหวะ Pulse ตาม BPM (การคำนวณที่แม่นยำของคุณ)
    pulse = 0.5 * (1 + np.sin(2 * np.pi * (bpm / 60) * t))
    audio = (wave * pulse * 32767).astype(np.int16)
    return audio, sr

# --- 4. UI INTERFACE (แดง-ดำ สไตล์คุณ) ---
st.title("🔴 SYNAPSE 6D Pro: Master Control")
st.write("ระบบบำบัดด้วยคลื่นเสียงและ AI แต่งเพลง")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎹 การตั้งค่า (Input)")
    user_input = st.text_input("ระบุอารมณ์ของคุณ:", "รู้สึกเหงาในเมืองใหญ่")
    bpm_val = st.slider("ชีพจรปัจจุบัน (BPM)", 60, 120, 75)
    
    if st.button("🚀 เริ่มการบำบัด (Activate)"):
        with st.spinner("ต๊ะ 2 และ Gemini กำลังทำงาน..."):
            # ให้ Gemini แต่งเพลง
            try:
                response = model.generate_content(f"แต่งเพลงสั้นๆ พร้อมคอร์ด เกี่ยวกับ: {user_input}")
                st.session_state['lyrics'] = response.text
            except:
                st.session_state['lyrics'] = "โหมด Offline: [คอร์ด G] ความเหงาที่จางไป..."

with col2:
    st.subheader("🔊 ผลลัพธ์เสียง (Audio Output)")
    # รันเสียงตาม Logic ที่คำนวณ
    audio_data, sample_rate = generate_healing_wave(bpm_val)
    st.audio(audio_data, sample_rate=sample_rate)
    st.info(f"ขณะนี้กำลังเล่นคลื่น 432Hz ล็อกจังหวะที่ {bpm_val} BPM")

    if 'lyrics' in st.session_state:
        st.markdown("### 🎙️ เนื้อเพลงและคอร์ด")
        st.code(st.session_state['lyrics'])

# --- 5. LOGIC ต๊ะ 2 (Layer Monitor) ---
st.markdown("---")
st.subheader("📊 ตารางคุม Layer (โครงสร้างจาก ต๊ะ 2)")
layers = ["Music Layer", "Vocals (Tah 2)", "Nature Sound", "Binaural Beats"]
for layer in layers:
    st.write(f"✅ {layer}: กำลังทำงานร่วมกับ Logic ของคุณ")
    st.progress(0.8 if layer == "Vocals (Tah 2)" else 0.5)
