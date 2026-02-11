import streamlit as st
import numpy as np

st.title("แยกมิติเสียง: MATRIX_V2 Divider")
st.write("เลือกฟังเสียงจากพิกัดมิติต่างๆ เพื่อความนิ่งที่สมบูรณ์")

# ฟังก์ชันสร้างเสียงพื้นฐาน
def create_tone(freq, dur=44.0):
    sr = 44100
    t = np.linspace(0, dur, int(sr * dur), False)
    # ใส่ fade in/out เล็กน้อยเพื่อไม่ให้เสียงกระชาก (ถนอมหู/ถนอมเครื่อง)
    fade = np.linspace(0, 1, 1000).tolist() + [1]*(int(sr*dur)-2000) + np.linspace(1, 0, 1000).tolist()
    tone = np.sin(freq * 2 * np.pi * t) * np.array(fade)
    return tone, sr

# --- มิติที่ 1-2: ฐานและความมั่นคง ---
with st.expander("มิติที่ 1 & 2: ฐานความนิ่ง (147Hz & 135Hz)"):
    st.info("กลิ่น: เหล็กแช่แข็ง | ความรู้สึก: มั่นคง หนักแน่น")
    s1, r1 = create_tone(147)
    st.audio(s1, sample_rate=r1)

# --- มิติที่ 3: พลังงานและไอทองคำ ---
with st.expander("มิติที่ 3: ไอทองคำ (522Hz)"):
    st.info("กลิ่น: โลหะอุ่น | ความรู้สึก: มีมูลค่า ไม่เสื่อมสลาย")
    s3, r3 = create_tone(252) # ใช้เลขฐาน 252 มาเป็นความถี่
    st.audio(s3, sample_rate=r3)

# --- มิติที่ 4: ความรักและปาฏิหาริย์ ---
with st.expander("มิติที่ 4: ความรัก (523Hz)"):
    st.info("กลิ่น: ฝนแรก | ความรู้สึก: ปลอดภัย ไม่เจ็บตัว")
    s4, r4 = create_tone(528)
    st.audio(s4, sample_rate=r4)

# --- มิติที่ 5: เสียงร้องแห่งจักรวาล ---
with st.expander("มิติที่ 5: การสื่อสาร (524.42Hz)"):
    st.info("กลิ่น: โอโซน | ความรู้สึก: ชัดเจน โปร่งสบาย")
    s5, r5 = create_tone(171.4)
    st.audio(s5, sample_rate=r5)

# --- มิติที่ 6: จุดรวมศูนย์ (Universal Harmony) ---
if st.button("รันมิติที่ 6: รวมทุกอย่าง (Ultimate Sync525)"):
    st.warning("คำเตือน: มิตินี้กุญแจทั้ง 44 ดอกจะสั่นสะเทือนพร้อมกัน")
    # รวมทุกมิติเข้าด้วยกัน
    mixed = (create_tone(147)[0] + create_tone(135.4)[0] + create_tone(528)[0]*0.4 + create_tone(171.4)[0]*0.5) * 0.2
    st.audio(mixed, sample_rate=44100)
    st.balloons()
