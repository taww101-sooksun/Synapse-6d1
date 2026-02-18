import streamlit as st
import time
from datetime import datetime

# --- 1. ตั้งค่าพื้นฐานเครื่องยนต์ ---
if 'page' not in st.session_state: 
    st.session_state.page = "LANDING"
if 'current_room' not in st.session_state: 
    st.session_state.current_room = "PURPLE"  # ตั้งต้นที่ห้องม่วงตามโค้ดที่คุณให้มา
if 'user_id' not in st.session_state: 
    st.session_state.user_id = "Ta101"
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. ฟังก์ชันสลับมิติ (Gear Shift) ---
def go_to(room_name):
    st.session_state.current_room = room_name
    st.rerun()

# --- 3. ฟังก์ชันเพลงบำบัด ---
def forced_therapy_radio():
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO" 
    st.markdown(f"""
        <div style="display:none;">
            <iframe src="https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1&mute=0" allow="autoplay"></iframe>
        </div>
    """, unsafe_allow_html=True)

# เรียกใช้งานเพลง
forced_therapy_radio()

# --- แยกส่วนตามห้อง (Current Room) ---

# ==========================================
# 1. มิติม่วง (AI Engine)
# ==========================================
if st.session_state.current_room == "PURPLE":
    st.markdown("<h1 style='color:#a020f0;'>🟣 มิติม่วง : AI อัจฉริยะ</h1>", unsafe_allow_html=True)
    
    st.markdown(f"### 🤖 AI: 'สวัสดีครับคุณ {st.session_state.user_id} ผมจำได้ทุกอย่างที่เราคุยกัน...'")

    # แสดงประวัติแชท
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ช่องกรอกข้อความ
    if prompt := st.chat_input("ระบายความลับ หรือปรึกษาเรื่องโปรเจกต์ได้เลยครับ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI กำลังใช้ความจำระดับเทพวิเคราะห์..."):
                time.sleep(1.5) 
                response = f"ในฐานะคู่คิดของคุณ {st.session_state.user_id}, ผมวิเคราะห์ว่าเรื่อง '{prompt}' นี้ พี่ควรใช้หลัก 'อยู่นิ่งๆ ไม่เจ็บตัว' นะครับ"
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    st.markdown("---")
    if st.button("🧹 ล้างความจำ AI (เฉพาะห้องนี้)"):
        st.session_state.messages = []
        st.rerun()

    if st.button("⬅️ ไปมิติแดง"): go_to("RED")

# ==========================================
# 2. มิติแดง (FIREBASE FETCH)
# ==========================================
elif st.session_state.current_room == "RED":
    st.markdown("<h1 style='color:#ff0000;'>🔴 มิติแดง : Feed ความรู้สึก</h1>", unsafe_allow_html=True)
    
    st.markdown("### 📽️ ฟีดล่าสุดจากเพื่อนๆ")
    
    with st.container():
        st.markdown("<div style='border:1px solid #ff0000; padding:10px; border-radius:10px;'>", unsafe_allow_html=True)
        st.write(f"👤 **{st.session_state.user_id}** (คุณ)")
        st.info("วันนี้รู้สึกดีมากที่ระบบเดินเครื่องได้สมบูรณ์!")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.file_uploader("📤 อัปโหลดวิดีโอ/รูปภาพระบายอารมณ์", type=['jpg','png','mp4'])
    
    if st.button("⬅️ กลับมิติม่วง"): go_to("PURPLE")
