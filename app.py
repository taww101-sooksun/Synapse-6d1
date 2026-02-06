import streamlit as st
import pandas as pd
import numpy as np
import time

# --- CONFIG & LOGIC ---
st.set_page_config(page_title="MATRIX_V2: อ่อนนุช 65", layout="wide")

# สโลแกนของคุณ
SLOGAN = "อยู่นิ่งๆ ไม่เจ็บตัว"

def get_matrix_logic(lat, lon, keys_44):
    # ฐานข้อมูล 252 มาจากกุญแจ 44 คูณกับมิติแปรผันและเวลา
    current_sec = time.localtime().tm_sec
    base_val = (lat + lon) * keys_44
    
    # สร้าง 6 ด่าน (A-F)
    gates = ['A: Stability', 'B: Filtering', 'C: Reflection', 
             'D: Equilibrium', 'E: Silence', 'F: Unity']
    
    results = []
    for i, gate in enumerate(gates):
        # กลไก G+ (เพิ่ม) และ S- (ลด) เพื่อหักล้างกัน
        g_plus = np.sin(current_sec + i) * 100 
        s_minus = np.cos(current_sec + i) * 100
        
        # การหักล้าง (Cancellation)
        balance = g_plus + s_minus 
        
        # หน่วยวัดสภาวะ (SC/GU)
        sc_unit = abs(balance) / 12  # หารด้วย 12 ตำแหน่ง
        
        results.append({
            "ด่าน (Gate)": gate,
            "G+ (ดึง)": round(g_plus, 2),
            "S- (ลด)": round(s_minus, 2),
            "ความนิ่ง (Balance)": "คงที่" if abs(balance) < 10 else "กำลังปรับจูน",
            "หน่วยวัด (SC)": round(sc_unit, 2)
        })
    return pd.DataFrame(results)

# --- UI ---
st.title(f"🌀 MATRIX_V2: {SLOGAN}")
st.write(f"พิกัดปัจจุบัน: **อ่อนนุช 65 (ประเวศ)**")

# ส่วนดึง GPS (รองรับทั้ง Manual และ Browser)
st.sidebar.header("📍 ระบบระบุพิกัด")
lat_input = st.sidebar.number_input("Latitude", value=13.72, format="%.5f")
lon_input = st.sidebar.number_input("Longitude", value=100.65, format="%.5f")
keys_input = st.sidebar.slider("กุญแจ 44 จุด (Key Multiplier)", 1, 44, 44)

# แสดงผล 6 มิติ
st.subheader("📊 การคำนวณ 6 มิติ (หักล้าง G+ / S-)")
data = get_matrix_logic(lat_input, lon_input, keys_input)

# จัดหน้าจอเป็น 2 ฝั่ง
col1, col2 = st.columns([2, 1])

with col1:
    st.table(data)
    st.write("*(หมายเหตุ: ตัวเลขจะหักล้างกันเพื่อเข้าสู่จุดศูนย์กลางที่คุณอยู่)*")

with col2:
    # กราฟแสดงความนิ่ง
    st.line_chart(data["หน่วยวัด (SC)"])
    st.metric(label="ฐานข้อมูลรวม", value="252 Points", delta=f"{keys_input} Keys")

# ระบบเสียง/สัมผัส (Simulated)
if st.button("🔊 สัมผัสความถี่ด่าน F (Unity)"):
    st.success("ระบบกำลังส่งคลื่นความถี่ 'นิ่ง' เพื่อหักล้างสัญญาณรบกวนรอบตัวคุณ...")
    st.toast("สัมผัสแรงดึงดูดที่จุดศูนย์กลาง...")

# --- FOOTER ---
st.divider()
st.caption(f"MATRIX_V2 System | {time.strftime('%Y-%m-%d %H:%M:%S')} | ประเวศ, กรุงเทพฯ")
