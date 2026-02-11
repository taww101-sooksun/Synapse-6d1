import streamlit as st
import numpy as np

st.title("🎧 MATRIX_V2: Full Hip-Hop Production")
st.write("Status: Music + Vocal + 147Hz Sync")

def create_full_track():
    sr = 44100
    duration = 8.0
    t = np.linspace(0, duration, int(sr * duration), False)
    
    # 1. กลอง Hip-Hop (Kick & Snare)
    # Kick ใช้ฐาน 147Hz เพื่อความนิ่ง
    kick = np.sin(2 * np.pi * 147 * t) * (np.sin(2 * np.pi * 1.5 * t) > 0.9)
    # Snare (Noise เบาๆ)
    snare = np.random.uniform(-1, 1, len(t)) * (np.sin(2 * np.pi * 1.5 * t) < -0.9) * 0.2
    
    # 2. เสียงดนตรีเปียโน (Melody จากรหัส 680 / 528)
    # เล่นโน้ตสลับไปมาให้ดูเหมือนดนตรีจริง
    melody = np.sin(2 * np.pi * 528 * t) * 0.1 * (np.sin(2 * np.pi * 0.75 * t) > 0) # ความรัก
    chords = np.sin(2 * np.pi * 135.42 * t) * 0.1 # ทองคำ (เล่นพื้นหลัง)
    
    # รวมร่างดนตรี
    music_mix = (kick * 0.5) + (snare * 0.3) + melody + chords
    
    return music_mix * 0.3, sr

if st.button("🚀 รันเพลงเต็มรูปแบบ (Music + Vocal Mode)"):
    # สร้างดนตรี
    audio_data, rate = create_full_track()
    
    # แสดงตัวเล่นเสียงดนตรี
    st.subheader("1. ภาคดนตรี (Hip-Hop Beats 147)")
    st.audio(audio_data, sample_rate=rate)
    
    # ส่วนของเสียงร้อง (ใช้ gTTS ตามที่คุยกัน)
    st.subheader("2. ภาคเสียงร้อง (Real Vocal)")
    from gtts import gTTS
    from io import BytesIO
    
    voice_buffer = BytesIO()
    tts = gTTS(text="หก แปด ศูนย์ สอง เจ็ด สอง หนึ่ง ศูนย์ แปด แปด. อยู่นิ่งๆ ไม่เจ็บตัว", lang='th')
    tts.write_to_fp(voice_buffer)
    st.audio(voice_buffer)
    
    st.success("แจ๋ว! ตอนนี้มิติของคุณมีทั้ง บีท ดนตรี และเสียงคนร้องแล้วครับ")
