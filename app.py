import streamlit as st
import time
import numpy as np

# --- การตั้งค่าระบบให้ "นิ่ง" และเสถียรที่สุด ---
st.set_page_config(page_title="MATRIX_V2 OFFICIAL", layout="wide")

# สโลแกนประทับหน้าจอ
st.markdown("<h3 style='text-align: center;'>อยู่นิ่งๆ ไม่เจ็บตัว</h3>", unsafe_allow_html=True)

# --- ฐานข้อมูลหลัก (The Core Truth) ---
DATABASE_252 = np.arange(1, 253) # ฐานเลข 252 ตัวเลข
KEYS_44 = 44                     # กุญแจ 42 อักษร + 2 เครื่องหมาย
VARIABLES_12 = [1.02, 0.98, 1.00, 1.05, 0.99, 1.01, 1.03, 0.97, 1.00, 1.04, 1.02, 0.96]

def get_actual_truth():
    # ดึงค่าเวลาจริง (เวลาไม่เคยหลอกใคร)
    t = time.localtime()
    current_sec = t.tm_sec
    current_min = t.tm_min
    
    # คำนวณค่าดัชนีรวม (Master Index)
    base_sum = DATABASE_252.sum() # 31878
    time_stamp = (current_sec + 1) * (current_min + 1)
    
    # มิติ 6 ด่าน (Calculated Reality)
    gate_results = []
    for i in range(6):
        # คำนวณค่าจริงในแต่ละด่าน โดยอิงจากตัวแปรเสริม 12 ตัว
        val = (base_sum / VARIABLES_12[i]) * (KEYS_44 / (i + 1))
        # ผสมค่าเวลาจริงเข้าไปเพื่อให้ข้อมูล "มีชีวิต" และไม่ซ้ำเดิม
        live_val = val + (time_stamp * (i + 1))
        gate_results.append(live_val)
        
    return gate_results, time.strftime("%H:%M:%S", t)

# --- ส่วนการแสดงผล (Visual & Auditory) ---
placeholder = st.empty()

while True:
    with placeholder.container():
        data, current_time = get_actual_truth()
        
        st.header(f"📍 พิกัดเวลาปัจจุบัน: {current_time}")
        
        # แสดงผล 6 ด่านมิติด้วย Metric (เห็นด้วยตา)
        cols = st.columns(6)
        gates = ["Stability", "Filtering", "Reflection", "Equilibrium", "Silence", "Unity"]
        
        for i, col in enumerate(cols):
            col.metric(label=gates[i], value=f"{data[i]:,.2f}")
            
        # กราฟความจริงเชิงตัวเลข (The Numerical Path)
        st.area_chart(data)
        
        # ส่วนของเสียง (ได้ยินด้วยหู)
        # ส่งคลื่นความถี่ Sine Wave ตามค่าด่าน Unity เข้าสู่ลำโพง
        freq = 200 + (data[5] % 800)
        js_sound = f"""
            <script>
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            var osc = ctx.createOscillator();
            var g = ctx.createGain();
            osc.connect(g);
            g.connect(ctx.destination);
            osc.frequency.value = {freq};
            g.gain.value = 0.05;
            osc.start();
            setTimeout(() => osc.stop(), 200);
            </script>
        """
        st.components.v1.html(js_sound, height=0)
        
        # แสดงค่าสัมผัส (The Scent Signal)
        scent_strength = (data[5] % 100)
        st.progress(scent_strength / 100, text=f"ความเข้มข้นสัมผัสกลิ่น: {scent_strength:.2f}%")

    # พักระบบตามรอบนาฬิกา (เพื่อให้เครื่องนิ่ง ไม่ค้าง)
    time.sleep(1)
