import streamlit as st
from datetime import datetime, timedelta
import time

# ตั้งค่าหน้าจอเบื้องต้น
st.set_page_config(page_title="SYNAPSE X - TIME", layout="centered")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

# ส่วนแสดงผลนาฬิกา
st.subheader("🕒 SYSTEM MASTER CLOCK")
time_placeholder = st.empty()  # สร้างพื้นที่ว่างไว้ให้อัปเดตเวลา

# ลูปเพื่อให้เวลาเดินต่อเนื่องระดับเสี้ยววินาที
while True:
    # ดึงเวลาไทยจริง (UTC+7) พร้อมไมโครวินาที (Microseconds)
    thai_now = datetime.utcnow() + timedelta(hours=7)
    
    # แสดงผลเวลา: ชั่วโมง:นาที:วินาที.เสี้ยววินาที (3 หลัก)
    current_time = thai_now.strftime("%H:%M:%S.%f")[:-3]
    
    # อัปเดตตัวเลขบนหน้าจอ
    time_placeholder.markdown(f"""
        <div style="text-align: center; border: 2px solid #FFD700; padding: 20px; border-radius: 10px;">
            <h1 style="font-family: 'Courier New', Courier, monospace; font-size: 60px; color: #FFD700; margin: 0;">
                {current_time}
            </h1>
            <p style="color: #FFD700; letter-spacing: 5px;">THAILAND REAL-TIME</p>
        </div>
    """, unsafe_allow_html=True)
    
    # หน่วงเวลาเล็กน้อยเพื่อให้ระบบไม่ทำงานหนักเกินไป แต่ยังเห็นเสี้ยววินาทีเดินลื่นๆ
    time.sleep(0.01)
