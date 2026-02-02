import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. ดีไซน์สไตล์นาฬิกาในเครื่อง (ดำ-น้ำเงิน-ไม่เหลี่ยม) ---
st.set_page_config(page_title="Money Maverick", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .stNumberInput, .stTextInput, .stDateInput { border-radius: 20px !important; background: #121212 !important; color: white !important; }
    .stButton>button { border-radius: 30px !important; width: 100%; background: #0044cc !important; color: white !important; border: none; height: 50px; }
    .status-card { padding: 30px; border-radius: 30px; text-align: center; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    </style>
""", unsafe_allow_html=True)

# --- 2. ระบบฐานข้อมูล (เก็บในเครื่องชั่วคราว) ---
if 'logs' not in st.session_state:
    st.session_state.logs = pd.DataFrame(columns=['วันที่', 'รายการ', 'จำนวน'])

# --- 3. ส่วนหัวและกำหนดงบ (Default 300) ---
st.markdown("<h1 style='text-align: center; font-weight: 200;'>💰 ออมเงินฉบับคุณพ่อ</h1>", unsafe_allow_html=True)
budget = st.sidebar.number_input("📌 กำหนดงบวันนี้ (บาท):", value=300)

# --- 4. ฟังก์ชันเขียนข้อมูล ---
with st.expander("✍️ เขียนรายจ่าย/ออมใหม่", expanded=True):
    col1, col2 = st.columns(2)
    item = col1.text_input("รายการ:", placeholder="เช่น ค่าข้าว")
    price = col2.number_input("จำนวนเงิน (บาท):", min_value=0.0)
    if st.button("บันทึกข้อมูล"):
        new_row = pd.DataFrame([[datetime.now().date(), item, price]], columns=['วันที่', 'รายการ', 'จำนวน'])
        st.session_state.logs = pd.concat([st.session_state.logs, new_row], ignore_index=True)
        st.toast("บันทึกเรียบร้อย!")

# --- 5. ระบบไฟจราจร (เขียว-แดง) ---
today_total = st.session_state.logs[st.session_state.logs['วันที่'] == datetime.now().date()]['จำนวน'].sum()
if today_total <= budget:
    bg, status, icon = "#003311", "🟢 ปลอดภัย", "✅"
else:
    bg, status, icon = "#440000", "🔴 เกินงบแล้ว!", "⚠️"
    st.audio("https://www.soundjay.com/buttons/beep-01a.mp3") # เสียงเตือน

st.markdown(f"""
    <div class="status-card" style="background: {bg};">
        <h1 style="margin:0;">{today_total:,.2f} / {budget:,.2f}</h1>
        <p style="font-size: 20px;">{status} | "อยู่นิ่งๆ ไม่เจ็บตัว"</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. ปฏิทินและประวัติ ---
st.write("---")
st.subheader("🗓️ ปฏิทินบันทึกรายวัน")
st.dataframe(st.session_state.logs, use_container_width=True)

# --- 7. YouTube Playlist ของคุณพ่อ ---
st.write("---")
st.subheader("🎬 เพลย์ลิสต์โปรดของอยู่นิ้งๆไม่เจ็บตัว")
st.video("https://youtube.com/playlist?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO&si=-xYvhNW1cDlT4yiu")
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#0E1117" />
    
    <stroke
        android:width="2dp"
        android:color="#00FFCC" />
    
    <corners android:radius="25dp" />
    
    <padding
        android:left="10dp"
        android:top="10dp"
        android:right="10dp"
        android:bottom="10dp" />
</shape>


st.markdown("<br><center><p style='color: #444;'>Smart Finance v1.0</p></center>", unsafe_allow_html=True)
