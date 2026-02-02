import streamlit as st
import time

# --- 1. ปรับแต่งดีไซน์ให้ "จี๊ดจ๊าด" และ "ไม่เหลี่ยม" ---
st.set_page_config(page_title="Father's Wealth AI", layout="centered")

st.markdown("""
    <style>
    /* พื้นหลังแบบไล่เฉดมืดหรู */
    .stApp {
        background: radial-gradient(circle at top, #1a2a22 0%, #0a0a0a 100%);
    }
    
    /* การ์ดสรุปยอดแบบโปร่งแสง (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 35px;
        padding: 30px;
        border: 1px solid rgba(0, 255, 135, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        text-align: center;
        margin-bottom: 25px;
    }

    /* ตัวเลขยอดเงินเน้นสีทองนีออน */
    .money-text {
        font-size: 50px !important;
        font-weight: 900;
        color: #00FF87;
        text-shadow: 0 0 20px rgba(0, 255, 135, 0.5);
    }

    /* ปุ่มกดทรงมนสุดล้ำ */
    .stButton>button {
        border-radius: 50px !important;
        background: linear-gradient(90deg, #00FF87, #60EFFF) !important;
        color: #000 !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
        padding: 15px 30px !important;
        transition: 0.3s all ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(0, 255, 135, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. หน้าจอ Dashboard ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("<p style='color: #888; margin-bottom: 0;'>ยอดสะสมรายปีของคุณ</p>", unsafe_allow_html=True)
st.markdown('<p class="money-text">฿ 850,240.00</p>', unsafe_allow_html=True)
st.markdown("<p style='color: #00FF87;'>▲ เพิ่มขึ้น 12% จากเดือนที่แล้ว</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. ระบบสแกนอัตโนมัติ ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📸 อัปโหลดสลิป")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

with col2:
    st.markdown("### ⏳ สถานะ AI")
    if uploaded_file:
        # จำลองระบบอ่านอัตโนมัติ
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        
        st.success("สแกนสำเร็จ!")
        st.metric("ตรวจพบยอดโอน", "฿ 1,500.00", "+500")
        st.balloons() # ฉลองความสำเร็จแบบจัดเต็ม!

# --- 4. ตารางประวัติรายวัน (สไตล์คนรุ่นใหม่) ---
st.markdown("---")
st.subheader("🗓️ รายละเอียด 24 ชั่วโมงล่าสุด")
data = {
    "เวลา": ["10:30", "12:15", "14:45"],
    "รายการ": ["โอนเงินเข้า", "ซื้อกาแฟ", "ออมเพิ่ม"],
    "จำนวน": ["+ 5,000", "- 120", "+ 1,500"]
}
st.table(data)

# --- 5. สโลแกนประจำตัวคุณพ่อ ---
st.markdown("<br><center><p style='color: #555;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\" - Smart Finance 2026</p></center>", unsafe_allow_html=True)
