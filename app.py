import streamlit as st
import time
from datetime import datetime
import numpy as np

# --- การตั้งค่าระบบความปลอดภัยสูงสุด ---
st.set_page_config(page_title="MATRIX_V2 | ABSOLUTE TRUTH", layout="wide")

st.markdown("<h2 style='text-align: center;'>อยู่นิ่งๆ ไม่เจ็บตัว</h2>", unsafe_allow_html=True)

# --- ส่วนประกอบ: การดึงพิกัด GPS จริงจาก Browser ---
def get_gps_script():
    # ใช้ JavaScript ดึงพิกัดจากอุปกรณ์ของผู้ใช้โดยตรงเพื่อให้ "จริง" ที่สุด
    js_gps = """
    <script>
    navigator.geolocation.getCurrentPosition(function(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const gps_display = document.getElementById("gps_data");
        if(gps_display) {
            gps_display.innerHTML = "📍 พิกัดความจริง (GPS): " + lat.toFixed(6) + ", " + lon.toFixed(6);
        }
    });
    </script>
    <div id="gps_data" style="font-family: monospace; font-size: 1.2rem; color: #00FF00; text-align: center; padding: 10px;">
        🔍 กำลังค้นหาพิกัดจากดาวเทียม...
    </div>
    """
    st.components.v1.html(js_gps, height=60)

# --- ฐานข้อมูลหลัก (Core Logic) ---
DATABASE_252 = np.arange(1, 253)
KEYS_44 = 44
VARS_12 = [1.02, 0.98, 1.00, 1.05, 0.99, 1.01, 1.03, 0.97, 1.00, 1.04, 1.02, 0.96]

def calculate_v2_logic():
    # เวลาที่เดินอย่างซื่อตรง (Absolute Time)
    now = datetime.now()
    t_stamp = now.timestamp()
    
    base_truth = DATABASE_252.sum() # 31878
    gates_data = []
    
    for i in range(6):
        # สมการถอดรหัสที่เชื่อมโยง 'เลข-เวลา-กุญแจ'
        val = (base_truth / VARS_12[i]) * (KEYS_44 / (i + 1))
        # ทำให้ข้อมูลขยับตามเวลาจริงเสี้ยววินาที
        sync_val = val + (now.second * (i + 1)) + (now.microsecond / 1000000)
        gates_data.append(sync_val)
        
    return gates_data, now.strftime("%H:%M:%S")

# --- การแสดงผลแบบ Real-time ---
get_gps_script() # แสดง GPS ด้านบนสุดของระบบ
placeholder = st.empty()

while True:
    with placeholder.container():
        data, time_label = calculate_v2_logic()
        
        st.subheader(f"⏱️ เวลาที่เดินถูกที่: {time_label}")
        
        # แสดงผล 6 ด่านมิติ
        cols = st.columns(6)
        gates = ["ความเสถียร", "การกรอง", "การสะท้อน", "สมดุล", "ความเงียบ", "ความสามัคคี"]
        
        for i, col in enumerate(cols):
            col.metric(label=gates[i], value=f"{data[i]:,.2f}")
            
        # กราฟเส้นแสดงทิศทางของข้อมูล
        st.line_chart(data)
        
        # เสียงความถี่ (Auditory Truth) - ดังตามความจริงของด่านสุดท้าย
        freq = 300 + (data[5] % 500)
        js_sound = f"""
            <script>
            var ctx = new AudioContext();
            var osc = ctx.createOscillator();
            var g = ctx.createGain();
            osc.connect(g); g.connect(ctx.destination);
            osc.frequency.value = {freq};
            g.gain.value = 0.03;
            osc.start(); setTimeout(() => osc.stop(), 150);
            </script>
        """
        st.components.v1.html(js_sound, height=0)
        
        st.progress((data[5] % 100) / 100, text=f"ความแม่นยำของสัมผัสปัจจุบัน: {(data[5] % 100):.2f}%")

    time.sleep(1) # รักษาจังหวะให้เดินตามนาฬิกาจริง
