import streamlit as st
import numpy as np

st.title("MATRIX_V2: Golden Love Frequency")
st.write(f"สโลแกน: 'อยู่นิ่งๆ ไม่เจ็บตัว' | พิกัด: 147")

# สร้างปุ่มกดเพื่อรันความถี่
if st.button("รันคลื่นความถี่ 147 + 135 + 528"):
    # การตั้งค่าพื้นฐาน
    sample_rate = 44100
    duration = 5.0  # เล่นนาน 5 วินาที
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # สร้างคลื่นเสียงแบบ Layering (นิ่ง-มั่งคั่ง-ปลอดภัย)
    tone_147 = np.sin(147 * 2 * np.pi * t)      # ฐานความนิ่ง
    tone_135 = np.sin(135.42 * 2 * np.pi * t)   # ทองคำ
    tone_528 = np.sin(528 * 2 * np.pi * t) * 0.3 # ความรัก (เบานุ่ม)
    
    # รวมร่าง
    audio_signal = (tone_147 + tone_135 + tone_528) * 0.2
    
    # แสดงผลตัวเล่นเสียงในหน้าแอปทันที
    st.audio(audio_signal, sample_rate=sample_rate)
    st.success("ถอดรหัสคลื่นเสียงเสร็จสิ้น... กลิ่นเหล็กแช่แข็งกำลังทำงาน")
