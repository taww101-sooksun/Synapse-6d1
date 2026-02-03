import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. ดีไซน์สไตล์ SYNAPSE (ดำ-เขียวมินต์-มน) ---
st.set_page_config(page_title="Money Maverick", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    /* ปรับแต่งกล่องข้อความให้มนเหมือนกรอบนาฬิกาที่คุณพ่อชอบ */
    .stNumberInput, .stTextInput, .stDateInput { 
        border-radius: 20px !important; 
        background: #0E1117 !important; 
        color: #00FFCC !important; 
        border: 1px solid #00FFCC !important;
    }
    .stButton>button { 
        border-radius: 30px !important; 
        width: 100%; 
        background: #0044cc !important; 
        color: white !important; 
        border: none; 
        height: 50px; 
    }
    .status-card { 
        padding: 30px; 
        border-radius: 30px; 
        text-align: center; 
        margin-bottom: 20px; 
        box-shadow: 0 10px 30px rgba(0,255,204,0.2); 
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. ระบบฐานข้อมูล ---
if 'logs' not in st.session_state:
    st.session_state.logs = pd.DataFrame(columns=['วันที่', 'รายการ', 'จำนวน'])

# --- 3. ส่วนหัว ---
st.markdown("<h1 style='text-align: center; color: #00FFCC;'>💰 SYNAPSE ออมเงิน</h1>", unsafe_allow_html=True)
budget = st.sidebar.number_input("📌 กำหนดงบวันนี้ (บาท):", value=300)

# --- 4. บันทึกข้อมูล ---
with st.expander("✍️ บันทึกรายจ่ายใหม่", expanded=True):
    col1, col2 = st.columns(2)
    item = col1.text_input("รายการ:", placeholder="เช่น ค่ากาแฟ")
    price = col2.number_input("จำนวนเงิน (บาท):", min_value=0.0)
    if st.button("บันทึกข้อมูล"):
        if item:
            new_row = pd.DataFrame([[datetime.now().date(), item, price]], columns=['วันที่', 'รายการ', 'จำนวน'])
            st.session_state.logs = pd.concat([st.session_state.logs, new_row], ignore_index=True)
            st.toast("บันทึกเรียบร้อย!")
        else:
            st.warning("กรุณาใส่ชื่อรายการด้วยครับ")

# --- 5. ระบบไฟจราจร (เขียว-แดง) ---
today_total = st.session_state.logs[st.session_state.logs['วันที่'] == datetime.now().date()]['จำนวน'].sum()
if today_total <= budget:
    bg, status = "#003311", "🟢 ปลอดภัย"
else:
    bg, status = "#440000", "🔴 เกินงบแล้ว!"
    st.audio("https://www.soundjay.com/buttons/beep-01a.mp3")

st.markdown(f"""
    <div class="status-card" style="background: {bg}; border: 2px solid #00FFCC;">
        <h1 style="margin:0; color: white;">{today_total:,.2f} / {budget:,.2f}</h1>
        <p style="font-size: 20px; color: #00FFCC;">{status} | "อยู่นิ่งๆ ไม่เจ็บตัว"</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. ประวัติ ---
st.subheader("🗓️ บันทึกวันนี้")
st.dataframe(st.session_state.logs, use_container_width=True)

# --- 7. YouTube (แก้ปัญหาไม่ติด) ---
st.write("---")
st.subheader("🎬 เพลย์ลิสต์บำบัดใจ")
# ใช้ปุ่มกดแทนเพื่อให้เปิดติด 100% ในทุกเครื่อง
yt_link = "https://youtube.com/playlist?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
if st.button("🎵 กดตรงนี้เพื่อฟังเพลง (ติดแน่นอน)"):
    st.markdown(f'<meta http-equiv="refresh" content="0;url={yt_link}">', unsafe_allow_html=True)
    st.write(f"หากไม่เด้ง [คลิกที่นี่]({yt_link})")

st.markdown("<br><center><p style='color: #444;'>SYNAPSE Smart Finance v1.1</p></center>", unsafe_allow_html=True)
