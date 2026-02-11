import streamlit as st
import numpy as np
from gtts import gTTS
from io import BytesIO

st.title("💎 MATRIX_V2: Ultimate Harmony")
st.write("สถานะ: Full Sync (Music + Vocal) | พิกัด: 147")

# 1. ฟังก์ชันสร้างดนตรี Lo-fi แบบจูนคีย์ D Major (147Hz)
def generate_master_music(duration=10):
    sr = 44100
    t = np.linspace(0, duration, int(sr * duration), False)
    
    # Bass Line 147Hz (เต้นเป็นจังหวะ 4/4)
    bass = np.sin(2 * np.pi * 147 * t) * (np.sin(2 * np.pi * 1.5 * t) > 0) * 0.4
    
    # Melody Piano (D Major: D, F#, A) - จูนให้เข้ากับรหัส 680...
    melody = (np.sin(2 * np.pi * 587 * t) * 0.1 * (np.sin(2 * np.pi * 0.5 * t) > 0.5) +  # High D
              np.sin(2 * np.pi * 370 * t) * 0.05 * (np.sin(2 * np.pi * 0.25 * t) > 0.5)) # F#
    
    # Atmosphere (Pink Noise เหมือนเสียงฝน)
    rain = np.random.normal(0, 0.02, len(t))
    
    full_audio = bass + melody + rain
    return full_audio * 0.3, sr

# 2. ระบบรันพร้อมกัน (Vocal + Music)
if st.button("🔥 รันมิติแบบ 'สุดแจ๋ว' (Full Merge)"):
    # --- ส่วนของดนตรี ---
    music, sr = generate_master_music()
    
    # --- ส่วนของเสียงร้อง (จูนรหัส 6802721088 x 61244252) ---
    vocal_text = "หก แปด ศูนย์ สอง เจ็ด สอง หนึ่ง ศูนย์ แปด แปด. หก หนึ่ง สอง สี่ สี่ สอง ห้า สอง. อยู่นิ่งๆ ไม่เจ็บตัว"
    tts = gTTS(text=vocal_text, lang='th')
    voice_bytes = BytesIO()
    tts.write_to_fp(voice_bytes)
    
    # --- แสดง
