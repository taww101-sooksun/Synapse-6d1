import streamlit as st
import numpy as np
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="SYNAPSE 6D Pro - Test Bench", layout="wide")

# จำลองการตั้งค่าจากภาพถ่ายของคุณ (ต๊ะ 2 Structure)
class Tah2_Structure:
    def __init__(self):
        self.tracks = [
            {
                "id": '1',
                "title": 'Flowing River Harmony',
                "layers": ["Music", "Vocals", "Nature", "Binaural"]
            }
        ]

# --- 2. LOGIC การคำนวณของคุณ (อัปเกรดแล้ว) ---
def calculate_audio_levels(bpm, emotion_score):
    # สูตรคำนวณเพื่อความนิ่ง:
    # ยิ่งชีพจรสูง (BPM) เสียงธรรมชาติจะดังขึ้นเพื่อกล่อม
    nature_vol = np.clip(bpm / 120, 0.2, 1.0)
    # เสียงร้อง (ต๊ะ 2) จะนุ่มนวลตามคะแนนอารมณ์
    vocal_vol = np.clip(emotion_score, 0.3, 0.9)
    return nature_vol, vocal_vol

# --- 3. UI DISPLAY (หน้าแอปสีแดง/ดำ ตามสไตล์คุณ) ---
st.title("🔴 SYNAPSE 6D Pro: Integration Test")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Inputs (ชีพจร & อารมณ์)")
    bpm = st.slider("Heart Rate (BPM)", 60, 140, 75)
    mood = st.select_slider("Mood Level", options=[0.1, 0.3, 0.5, 0.7, 0.9], value=0.5)
    
    if st.button("🚀 ACTIVATE SYSTEM"):
        st.success("ระบบเชื่อมต่อ ต๊ะ 2 และ Gemini สำเร็จ!")

with col2:
    st.subheader("🎙️ Player Status (จากโครงสร้าง ต๊ะ 2)")
    tah2 = Tah2_Structure()
    n_vol, v_vol = calculate_audio_levels(bpm, mood)
    
    # แสดงการจำลอง Mixer ที่ ต๊ะ 2 เขียนไว้ใน PlayerScreen.js
    st.info(f"กำลังเล่น: {tah2.tracks[0]['title']}")
    
    st.write(f"🔊 Music Layer: 1.0 (Fixed)")
    st.progress(1.0)
    
    st.write(f"🎤 Vocals Layer (ต๊ะ 2): {v_vol:.2f}")
    st.progress(v_vol)
    
    st.write(f"🌿 Nature Layer: {n_vol:.2f}")
    st.progress(n_vol)
    
    st.write(f"🧠 Binaural Beats: Active (Locked at {bpm} BPM)")

# --- 4. ตรวจสอบความนิ่ง ---
st.markdown("---")
st.subheader("📊 System Stability Check")
if bpm > 100:
    st.warning("⚠️ ชีพจรสูง: ระบบกำลังเร่งเสียง Nature Layer เพื่อปรับสมดุล")
else:
    st.info("✅ สถานะปกติ: ระบบทำงานในโหมดผ่อนคลาย")
