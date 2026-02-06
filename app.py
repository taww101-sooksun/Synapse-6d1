import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.title("🛡️ MATRIX_V2: ระบบความจริงร้อยเอ็ด (Update)")
st.write("สโลแกน: **อยู่นิ่งๆ ไม่เจ็บตัว**")

# 1. พิกัดร้อยเอ็ดที่ถูกต้อง
target_lat = 16.0540 
target_lon = 103.6520

# 2. ตั้งค่าเวลาเป็น 16:45 ตามที่คุณระบุ
current_time_set = datetime.datetime.now().replace(hour=16, minute=45, second=0, microsecond=0)
ts = current_time_set.timestamp()

st.success(f"📍 พิกัด: ร้อยเอ็ด ({target_lat}, {target_lon})")
st.info(f"🕒 เวลาประมวลผล: {current_time_set.strftime('%H:%M:%S')} น.")

# 3. คำนวณรหัส 44 กุญแจ ด้วยเวลา 16:45
gates = ['A: Stability', 'B: Filtering', 'C: Reflection', 'D: Equilibrium', 'E: Silence', 'F: Unity']
results = []

for i, gate in enumerate(gates):
    # สูตรที่ใช้ "พิกัดร้อยเอ็ด" และ "เวลา 16:45" เป็นตัวแปรจริง
    g_plus = np.sin(ts + target_lat + i) * 44 
    s_minus = np.cos(ts + target_lon + i) * 44
    sc_unit = abs(g_plus + s_minus) / 7.33
    
    results.append({
        "ด่าน (Gate)": gate,
        "G+ (16:45)": round(g_plus, 4),
        "S- (16:45)": round(s_minus, 4),
        "SC (สมดุล)": round(sc_unit, 4)
    })

st.table(pd.DataFrame(results))

# แสดงค่าสมดุลของด่าน D เพื่อดูความนิ่ง
st.metric("สมดุล ณ เวลา 16:45", value=f"{results[3]['SC (สมดุล)']}")
