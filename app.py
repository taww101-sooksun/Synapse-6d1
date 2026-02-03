import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. ตั้งค่าและดีไซน์ (CSS) ---
st.set_page_config(page_title="SYNAPSE Money", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0A0A0A; color: white; }
    /* ปรับช่องกรอกให้จิ้มง่าย แป้นพิมพ์ขึ้นทันที */
    .stNumberInput input, .stTextInput input {
        border-radius: 15px !important;
        background-color: #121212 !important;
        color: #00FFCC !important;
        border: 2px solid #00FFCC !important;
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
    .bank-slip {
        background: linear-gradient(180deg, #0044cc 0%, #0A0A0A 100%);
        padding: 25px;
        border-radius: 25px;
        border: 1px solid #00FFCC;
        color: white;
        font-family: 'Tahoma', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. ระบบฐานข้อมูล (Session State) ---
if 'logs' not in st.session_state:
    st.session_state.logs = pd.DataFrame(columns=['วันที่', 'รายการ', 'จำนวน'])

# --- 3. ส่วนหัวและตั้งงบ ---
st.markdown("<h2 style='text-align: center; color: #00FFCC;'>💰 บันทึกงบรายวัน</h2>", unsafe_allow_html=True)

# ช่องพิมพ์งบ (จิ้มแล้วพิมพ์เลข 300 ได้เลย)
user_budget = st.number_input("📌 ตั้งงบวันนี้ (บาท):", min_value=0.0, value=300.0, step=1.0, format="%.0f", key="budget_main")

# --- 4. ฟังก์ชันบันทึกข้อมูล (แบบมีปฏิทินและแนบรูปสลิป) ---
with st.expander("✍️ บันทึกรายการใหม่ / แนบสลิป", expanded=True):
    u_date = st.date_input("📅 วันที่:", value=datetime.now().date(), key="input_date")
    u_item = st.text_input("📝 รายการ:", placeholder="ซื้ออะไรไปบ้าง...", key="input_item")
    u_price = st.number_input("💵 จำนวนเงิน (บาท):", min_value=0.0, step=1.0, format="%.0f", key="input_price")
    
    # ช่องแนบรูปสลิปเงินออก
    u_file = st.file_uploader("📸 แนบรูปสลิป (ถ้ามี)", type=["jpg", "png", "jpeg"], key="input_file")
    
    if st.button("✅ บันทึกข้อมูลลงเครื่อง"):
        if u_item and u_price > 0:
            new_row = pd.DataFrame([[u_date, u_item, u_price]], columns=['วันที่', 'รายการ', 'จำนวน'])
            st.session_state.logs = pd.concat([st.session_state.logs, new_row], ignore_index=True)
            st.success(f"บันทึก {u_item} เรียบร้อย!")
            if u_file: st.image(u_file, width=150, caption="สลิปที่บันทึก")
        else:
            st.warning("กรุณากรอกข้อมูลให้ครบครับคุณพ่อ")

# --- 5. สรุปยอดและไฟจราจร ---
today_data = st.session_state.logs[st.session_state.logs['วันที่'] == datetime.now().date()]
total_spent = today_data['จำนวน'].sum()
balance = user_budget - total_spent

st.markdown(f"""
    <div class="status-card" style="background-color: {'#003311' if balance >= 0 else '#440000'};">
        <h2 style="margin:0;">ใช้ไป: {total_spent:,.0f} / {user_budget:,.0f}</h2>
        <h3 style="color: #00FFCC;">คงเหลือ: {balance:,.0f} บาท</h3>
        <p>"อยู่นิ่งๆ ไม่เจ็บตัว"</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. ดูสลิปธนาคารย้อนหลัง ---
if not today_data.empty:
    if st.button("📱 ดูสลิปสรุปวันนี้ (แบบธนาคาร)"):
        st.markdown(f"""
            <div class="bank-slip">
                <center>
                    <h3 style='margin:0;'>🏦 SYNAPSE BANK</h3>
                    <p style='font-size:12px;'>บันทึกสำเร็จ | {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                    <hr>
                    <p style='margin:0;'>ยอดรวมวันนี้</p>
                    <h1 style='color: #00FFCC;'>฿ {total_spent:,.2f}</h1>
                    <div style='text-align:left; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px;'>
                        {"".join([f"• {row['รายการ']}: {row['จำนวน']:,.0f} บาท<br>" for i, row in today_data.iterrows()])}
                    </div>
                </center>
            </div>
        """, unsafe_allow_html=True)

# --- 7. YouTube ---
st.write("---")
st.subheader("🎵 ฟังเพลงบำบัดใจ")
yt_url = "https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
st.markdown(f'<iframe width="100%" height="315" src="{yt_url}" frameborder="0" allowfullscreen style="border-radius:20px; border: 1px solid #00FFCC;"></iframe>', unsafe_allow_html=True)

st.markdown("<br><center><p style='color: #444;'>SYNAPSE Smart Finance v2.0</p></center>", unsafe_allow_html=True)
