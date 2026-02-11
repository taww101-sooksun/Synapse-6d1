import numpy as np
import scipy.io.wavfile as wav
import streamlit as st

# สร้างไฟล์เสียงความถี่รวม
rate = 44100
t = np.linspace(0, 5, rate * 5)
# ผสม 147Hz + 135Hz + 528Hz
audio_data = np.sin(2*np.pi*147*t) + np.sin(2*np.pi*135*t) + (np.sin(2*np.pi*528*t) * 0.3)
audio_data = (audio_data * 32767 / np.max(np.abs(audio_data))).astype(np.int16)

# บันทึกและแสดงผลตัวเล่นเสียงบนหน้าจอ
wav.write("matrix_sound.wav", rate, audio_data)
st.audio("matrix_sound.wav")
