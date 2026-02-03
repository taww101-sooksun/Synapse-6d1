import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. ดีไซน์หน้าจอ (ดำ-เขียว-มน) ---
st.set_page_config(page_title="SYNAPSE Money", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0A0A0A; color: white; }
    /* ปรับช่องกรอกให้จิ้มง่าย แป้นพิมพ์ขึ้นทันที */
    .stNumberInput input {
        border-radius: 15px !important;
        background-color: #121212 !important;
        color: #00FFCC !important;
        border: 1px solid #00FFCC !important;
        height: 50px !important;
        font-size: 20px !important;
    }
    .status-card {
        padding: 25px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #00FFCC;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. ระบบฐานข้อมูล ---
if 'money_logs' not in st.session_state:
    st.session_state.money_logs = pd.DataFrame(columns=['วันที่', 'รายการ', 'จำนวน'])

st.markdown("<h2 style='text-align: center; color: #00FFCC;'>💰 บันทึกงบรายวัน</h2>", unsafe_allow_html=True)

# --- [ จุดที่แก้ให้คุณพ่อ ] ---
# 1. value=300: ตั้งเริ่มที่ 300
# 2. step=1.0: เวลากดบวก/ลบ ให้ขยับทีละ 1 บาท ไม่ใช่สตางค์
# 3. format="%.0f": แสดงผลเป็นเลขกลมๆ จะได้ดูง่ายครับ
user_budget = st.number_input("📌 ตั้งงบวันนี้ (บาท):", min_value=0.0, value=300.0, step=1.0, format="%.0f", key="daily_budget_input")
# --- ส่วนบันทึกที่มีปฏิทิน ---
with st.expander("✍️ บันทึกเตือนความจำ/รายจ่าย", expanded=True):
    # ช่องปฏิทิน จิ้มแล้วเลือกวันได้เลย
    selected_date = st.date_input("📅 วันที่:", value=datetime.now().date(), key="calendar_input")
    
    item_desc = st.text_input("📝 เรื่องที่บันทึก:", placeholder="เช่น จ่ายค่าน้ำ หรือ ซื้อของ")
    item_amt = st.number_input("💰 จำนวนเงิน (ถ้ามี):", min_value=0.0, step=1.0)
    
    if st.button("✅ บันทึกข้อมูล"):
        # เก็บข้อมูลพร้อมวันที่ที่เลือกจากปฏิทิน
        new_row = pd.DataFrame([[selected_date, item_desc, item_amt]], columns=['วันที่', 'รายการ', 'จำนวน'])
        st.session_state.money_logs = pd.concat([st.session_state.money_logs, new_row], ignore_index=True)
        st.success(f"บันทึกเรื่อง '{item_desc}' ของวันที่ {selected_date} เรียบร้อย!")


st.info("💡 คำแนะนำ: คุณพ่อจิ้มไปที่ตัวเลข {0} แล้วพิมพ์เลขใหม่จากแป้นพิมพ์ได้เลยครับ!".format(int(user_budget)))

# --- 3. ฟังก์ชันบันทึกรายจ่าย ---
with st.expander("✍️ เพิ่มรายการใหม่", expanded=True):
    c1, c2 = st.columns([2, 1])
    item_name = c1.text_input("ซื้ออะไร:", placeholder="เช่น ค่าข้าว", key="item_name")
    # ตรงนี้ก็แก้ให้ขยับทีละ 1 บาทเหมือนกันครับ
    item_price = c2.number_input("กี่บาท:", min_value=0.0, step=1.0, format="%.0f", key="item_price")
    
    if st.button("✅ บันทึกรายจ่าย"):
        if item_name and item_price > 0:
            new_record = pd.DataFrame([[datetime.now().date(), item_name, item_price]], columns=['วันที่', 'รายการ', 'จำนวน'])
            st.session_state.money_logs = pd.concat([st.session_state.money_logs, new_record], ignore_index=True)
            st.toast(f"บันทึก {item_name} แล้ว!")

# --- 4. สรุปยอดและ YouTube ---
today_data = st.session_state.money_logs[st.session_state.money_logs['วันที่'] == datetime.now().date()]
total_spent = today_data['จำนวน'].sum()
balance = user_budget - total_spent

st.markdown(f"""
    <div class="status-card" style="background-color: {'#003311' if balance >= 0 else '#440000'};">
        <h2 style="margin:0;">ใช้ไป: {total_spent:,.0f} / {user_budget:,.0f}</h2>
        <h3 style="color: #00FFCC;">คงเหลือ: {balance:,.0f} บาท</h3>
    </div>
""", unsafe_allow_html=True)

st.write("---")
st.subheader("🎵 ฟังเพลงบำบัดใจ")
yt_playlist = "https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
st.markdown(f'<iframe width="100%" height="315" src="{yt_playlist}" frameborder="0" allowfullscreen style="border-radius:20px;"></iframe>', unsafe_allow_html=True)
