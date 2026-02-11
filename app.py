import streamlit as st
from gtts import gTTS
from io import BytesIO

st.title("🎤 MATRIX_V2: Real Human Voice Sync")

text_input = "หกแปดศูนย์สองเจ็ดสองหนึ่งศูนย์แปดแปด อยู่นิ่งๆ ไม่เจ็บตัว"

if st.button("ปล่อยเสียงร้องจริง"):
    sound_file = BytesIO()
    tts = gTTS(text=text_input, lang='th')
    tts.write_to_fp(sound_file)
    
    st.audio(sound_file)
    st.success("ส่งเสียงมนุษย์เข้าสู่มิติพิกัด 147 เรียบร้อย!")
