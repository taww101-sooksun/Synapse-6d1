import streamlit as st
import numpy as np

st.title("🎤 MATRIX_V2: Hip Hop Dimension")
st.write("สถานะ: Beats Mode | สโลแกน: 'อยู่นิ่งๆ ไม่เจ็บตัว'")

def generate_hiphop_beat(duration=180):
    sr = 44100
    t = np.linspace(0, duration, int(sr * duration), False)
    tempo = 90  # Beats per minute
    beat_duration = 40 / tempo
    
    # 1. Sub-Bass 147Hz (เตะตามจังหวะ Kick)
    kick_pattern = np.zeros_like(t)
    for i in range(0, int(duration/beat_duration)):
        start = int(i * beat_duration * sr)
        end = start + int(0.4 * sr) # เสียง Kick สั้นๆ
        kick_pattern[start:end] = np.sin(147 * 4 * np.pi * t[start:end])
        
    # 2. Snare (เสียงแป๊ะที่จังหวะ 2 และ 4)
    snare_pattern = np.zeros_like(t)
    for i in range(0, int(duration/beat_duration)):
        if i % 2 == 1: # จังหวะตบ
            start = int(i * beat_duration * sr)
            end = start + int(0.1 * sr)
            # ใช้ White Noise ผสมความถี่สูงเพื่อเป็น Snare
            snare_pattern[start:end] = np.random.uniform(-1, 1, end-start) * 0.3

    # 3. Lo-fi Melody (D Major Chord ลากยาว)
    melody = (np.sin(147 * 2 * np.pi * t) + np.sin(185 * 2 * np.pi * t) + np.sin(220 * 2 * np.pi * t)) * 0.2
    
    final_mix = (kick_pattern * 0.6) + (snare_pattern * 0.3) + (melody * 0.4)
    return final_mix, sr

if st.button("🔥 Drop the Beat"):
    audio, rate = generate_hiphop_beat()
    st.audio(audio, sample_rate=rate)
    st.success("บีท Hip Hop พิกัด 147 กำลังทำงาน... โยกแบบนิ่งๆ ไม่เจ็บตัว")
