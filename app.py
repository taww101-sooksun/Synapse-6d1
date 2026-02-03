import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. ดีไซน์หน้าจอ (ดำ-เขียว-มน) ---
st.set_page_config(page_title="SYNAPSE Money", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    /* ปรับช่องกรอกให้พิมพ์ง่ายและชัดเจน */
    .stNumberInput input, .stTextInput input {
        border-radius: 15px !important;
        background-color: #121212 !important;
        color: #00FFCC !important;
        border: 1px solid #00FFCC !important;
        height: 45px !important;
    }
    .status-card {
        padding: 25px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #00FFCC;
    }
    .stButton>button {
        border-radius: 25px !important;
        background: #0044cc !important;
        color: white !important;
        height: 50px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. ระบบฐานข้อมูล ---
if 'money_logs' not in st.session_state:
    st.session_state.money_logs = pd.DataFrame(columns=['วันที่', 'รายการ', 'จำนวน'])

# --- 3. ส่วนกำหนดงบ (แก้ให้พิมพ์ได้อิสระ) ---
st.markdown("<h2 style='text-align: center; color: #00FFCC;'>💰 บันทึกงบรายวัน</h2>", unsafe_allow_html=True)

# ใช้ช่องนี้พิมพ์งบได้เลยครับ จะ 300 หรือเท่าไหร่ก็ได้
user_budget = st.number_input("📌 ตั้งงบวันนี้ (บาท):", min_value=0.0, value=300.0, key="daily_budget_input")

# --- 4. ฟังก์ชันบันทึกรายจ่าย ---
with st.expander("✍️ เพิ่มรายการใหม่", expanded=True):
    c1, c2 = st.columns([2, 1])
    item_name = c1.text_input("ซื้ออะไร:", placeholder="เช่น ค่ากาแฟ", key="item_name")
    item_price = c2.number_input("จำนวนเงิน:", min_value=0.0, step=1.0, key="item_price")
    
    if st.button("✅ บันทึกรายจ่าย"):
        if item_name and item_price > 0:
            new_record = pd.DataFrame([[datetime.now().date(), item_name, item_price]], columns=['วันที่', 'รายการ', 'จำนวน'])
            st.session_state.money_logs = pd.concat([st.session_state.money_logs, new_record], ignore_index=True)
            st.toast(f"บันทึก {item_name} แล้ว!")
        else:
            st.warning("ใส่ข้อมูลให้ครบก่อนครับคุณพ่อ")

# --- 5. สรุปยอดและไฟจราจร ---
today_data = st.session_state.money_logs[st.session_state.money_logs['วันที่'] == datetime.now().date()]
total_spent = today_data['จำนวน'].sum()
balance = user_budget - total_spent

# เปลี่ยนสีตามสถานะ
bg_color = "#003311" if balance >= 0 else "#440000"
status_text = "🟢 ยังอยู่ในงบ" if balance >= 0 else "🔴 เกินงบแล้วนะ!"

st.markdown(f"""
    <div class="status-card" style="background-color: {bg_color};">
        <h2 style="margin:0;">ยอดใช้ไป: {total_spent:,.2f} / {user_budget:,.2f}</h2>
        <h3 style="color: #00FFCC;">คงเหลือ: {balance:,.2f} บาท</h3>
        <p>{status_text} | "อยู่นิ่งๆ ไม่เจ็บตัว"</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. แสดงประวัติ ---
if not today_data.empty:
    st.subheader("🗓️ รายการวันนี้")
    st.dataframe(today_data[['รายการ', 'จำนวน']], use_container_width=True)

# --- 7. YouTube Playlist (ติดชัวร์) ---
st.write("---")
st.markdown("<h3 style='color: #FFD700;'>🎵 ฟังเพลงบำบัดใจระหว่างออม</h3>", unsafe_allow_html=True)

# ใส่ YouTube แบบ Embed ให้เล่นในหน้าแอปได้เลย
yt_playlist = "https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
st.markdown(f"""
    <iframe width="100%" height="315" 
    src="{yt_playlist}" 
    title="YouTube video player" frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen style="border-radius:20px; border: 1px solid #FFD700;">
    </iframe>
""", unsafe_allow_html=True)

st.markdown("<br><center><p style='color: #444;'>Smart Finance v1.2 | อยู่นิ่งๆ ไม่เจ็บตัว</p></center>", unsafe_allow_html=True)
