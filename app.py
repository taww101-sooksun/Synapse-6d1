import streamlit as st
import time
from datetime import datetime

# --- 1. ตั้งค่าพื้นฐานเครื่องยนต์ ---
if 'page' not in st.session_state: 
    st.session_state.page = "LANDING"
if 'current_room' not in st.session_state: 
    st.session_state.current_room = "MAIN"
if 'user_id' not in st.session_state: 
    st.session_state.user_id = "Ta101"

# --- 2. ฟังก์ชันสลับมิติ (Gear Shift) ---
def go_to(room_name):
    st.session_state.current_room = room_name
    st.rerun()

# --- 3. ฟังก์ชันเพลงบำบัด (ห้ามดับ) ---
def forced_therapy_radio():
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO" 
    st.markdown(f"""
        <div style="display:none;">
            <iframe src="https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1&mute=0" allow="autoplay"></iframe>
        </div>
    """, unsafe_allow_html=True)

# เรียกใช้งานเพลงทันที
forced_therapy_radio()
# --- เครื่องในห้องม่วง (AI Engine) ---
st.markdown("<h1 class='neon-text'>🟣 มิติม่วง : AI อัจฉริยะ</h1>", unsafe_allow_html=True)
    
    # ดึงค่า API Key (ต้องตั้งค่าใน st.secrets["gemini_key"])
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # AI ทักทายด้วยชื่อคุณพี่จากระบบ
    st.markdown(f"### 🤖 AI: 'สวัสดีครับคุณ {st.session_state.user_id} ผมจำได้ทุกอย่างที่เราคุยกัน...'")

    # กล่องแชทแบบเห็นประวัติ (เครื่องในเดินแล้ว!)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ช่องกรอกข้อความขนาดใหญ่ตามสั่ง
    if prompt := st.chat_input("ระบายความลับ หรือปรึกษาเรื่องโปรเจกต์ได้เลยครับ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI กำลังใช้ความจำระดับเทพวิเคราะห์..."):
                # ตรงนี้คือการส่งไปหา AI จริงๆ (จำลองการเดินเครื่อง)
                time.sleep(1.5) 
                response = f"ในฐานะคู่คิดของคุณ {st.session_state.user_id}, ผมวิเคราะห์ว่าเรื่อง '{prompt}' นี้ พี่ควรใช้หลัก 'อยู่นิ่งๆ ไม่เจ็บตัว' นะครับ"
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    st.markdown("---")
    if st.button("🧹 ล้างความจำ AI (เฉพาะห้องนี้)"):
        st.session_state.messages = []
        st.rerun()

    if st.button("⬅️ กลับหน้าหลัก"): go_to("MAIN")

# ==========================================
# 3. ส่วนเครื่องในห้องแดง (FIREBASE FETCH) - ตัวอย่างการเดินระบบ
# ==========================================
elif st.session_state.current_room == "RED":
    st.markdown("<h1 style='color:#ff0000;'>🔴 มิติแดง : Feed ความรู้สึก</h1>")
    
    # จำลองการดึง Feed จาก Firebase
    st.markdown("### 📽️ ฟีดล่าสุดจากเพื่อนๆ")
    
    # สร้างการแสดงผลแบบ Card
    with st.container():
        st.markdown("<div class='setup-card'>", unsafe_allow_html=True)
        st.write(f"👤 **{st.session_state.user_id}** (คุณ)")
        st.info("วันนี้รู้สึกดีมากที่ระบบเดินเครื่องได้สมบูรณ์!")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.file_uploader("📤 อัปโหลดวิดีโอ/รูปภาพระบายอารมณ์", type=['jpg','png','mp4'])
    
    if st.button("⬅️ กลับ"): go_to("MAIN")
