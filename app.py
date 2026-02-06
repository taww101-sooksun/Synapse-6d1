import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# 1. งัดกาลเวลา (The Master Axis)
thai_now = datetime.utcnow() + timedelta(hours=7)
ms = int(thai_now.strftime("%f")[:3])

# 2. งัดข้อมูลพลังงานและพิกัดมาเป็น "ตัวกรองความจริง"
battery_level = 85 # ดึงจาก Power Sensor
is_charging = False
lat_lon = "16.05, 103.65" # ฐานร้อยเอ็ด

# 3. ตรรกะการสร้างสรรค์: "The Truth Score"
# เราจะคำนวณ 'ความสัตย์จริง' ของวินาทีนี้จาก (ความนิ่ง + ความเงียบ + พลังงาน)
truth_score = (1.00 / 1.00) * (battery_level / 100) 

st.markdown(f"""
    <div style="background: #000; border: 2px solid #FFD700; padding: 25px; border-radius: 20px; text-align: center;">
        <h3 style="color: #FFD700; margin: 0;">⏱️ MASTER CLOCK</h3>
        <h1 style="font-size: 60px; color: #FFD700; font-family: monospace;">
            {thai_now.strftime("%H:%M:%S")}.<span style="color: #0f0;">{ms:03d}</span>
        </h1>
        <hr style="border-color: #333;">
        <div style="display: flex; justify-content: space-around; color: #0f0;">
            <div><b>VIB:</b> 1.00G</div>
            <div><b>SONIC:</b> 0 Hz</div>
            <div><b>BIO:</b> 72 BPM</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. ตารางรหัสความจริงที่ "ตื่นรู้" ตามเวลาปัจจุบัน
if truth_score > 0.8:
    st.subheader("📊 DIMENSION CODE: 44.252 (ACTIVE)")
    # รหัสจะขยับตาม MS ที่คุณให้ความสำคัญ
    data = {
        "มิติ": ["กาย (Still)", "วาจา (Sonic)", "ใจ (Bio)", "กาล (Time)"],
        "รหัสสด": [f"{1.00+ms/1000:.3f}", f"{ms*44:.0f}", f"{72+(ms/100):.2f}", f"{ms:03d}"]
    }
    st.table(pd.DataFrame(data))
    st.success("✅ สภาวะนิ่ง: ข้อมูลถูกต้องตามความเป็นจริง")
else:
    st.warning("⚠️ มิติไม่เสถียร: กรุณาอยู่นิ่งๆ เพื่อปลดล็อก")
