import streamlit as st
import numpy as np

st.title("🎸 MATRIX_V2: Chord Progression Mode")
st.write("การเรียงตัวของมิติในรูปแบบคอร์ดเพลง | สโลแกน: 'อยู่นิ่งๆ ไม่เจ็บตัว'")

def play_chord(root_freq, type="major", dur=2.0):
    sr = 44100
    t = np.linspace(0, dur, int(sr * dur), False)
    
    # คำนวณความถี่คู่เสียง (Intervals)
    if type == "major":
        chord = [1.0, 1.25, 1.5] # Root, Major 3rd, Perfect 5th
    else: # minor
        chord = [1.0, 1.18, 1.5] # Root, Minor 3rd, Perfect 5th
        
    combined_signal = sum(np.sin(root_freq * i * 2 * np.pi * t) for i in chord)
    return combined_signal * 0.2, sr

if st.button("เริ่มรันลำดับคอร์ด (Start Progression)"):
    # คอร์ด D -> Bm -> G -> A
    chords = [(147.0, "major", "D"), (123.4, "minor", "Bm"), (196.0, "major", "G"), (220.0, "major", "A")]
    
    for freq, c_type, name in chords:
        sig, rate = play_chord(freq, c_type)
        st.write(f"กำลังรันคอร์ด: **{name}**")
        st.audio(sig, sample_rate=rate)
        
    st.success("จบลำดับมิติ... ระบบนิ่งสนิทและปลอดภัย")
