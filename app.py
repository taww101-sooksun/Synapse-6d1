import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. ดีไซน์หน้าจอ (ดำ-เขียว-มน) ---
st.set_page_config(page_title="SYNAPSE Money", layout="centered")
st.markdown("""
    <สไตล์>
    .stApp { background-color: #0A0A0A; color: white; }
    /*ความร้อนระอุช่องให้จิ้มง่ายมันจะขึ้นทันที */
    .stNumberInput input {
        ขอบโค้งมน: 15 พิกเซล !สำคัญ;
        background-color: #121212 !important;
        สี: #00FFCC !สำคัญ;
        ขอบ: 3px ทึบ #00FFCC !สำคัญ;
        ความสูง: 50 พิกเซล !สำคัญ;
        ขนาดตัวอักษร: 20 พิกเซล !สำคัญ;
    }
    .status-card {
        ระยะห่างภายใน: 25 พิกเซล;
        ขอบโค้งมน: 25 พิกเซล;
        จัดแนวข้อความ: กึ่งกลาง;
        ระยะขอบล่าง: 20 พิกเซล;
        ขอบ: ทึบ 2 พิกเซล #00FFCC;
        # --- [ สลิปสไตล์ธนาคาร SYNAPSE ] ---
st.markdown("""
    <style>
         
        bank-slip {
        background: linear-gradient(180deg, #0044cc; 0%, #0A0A0A; 100%);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #00FFCC;
        color: white;
        font-family: 'Tahoma', sans-serif;
    }
    .slip-header { border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

if st.button("📱 ดูสลิปธนาคารส่วนตัว"):
    today = datetime.now().date()
    today_data = st.session_state.logs[st.session_state.logs['วันที่'] == today]
    
    if not today_data.empty:
        total = today_data['จำนวน'].sum()
        st.markdown(f"""
            <div class="bank-slip">
                <div class="slip-header">
                    <h3 style='margin:0;'>🏦 SYNAPSE BANK</h3>
                    <p style='font-size:12px;'>บันทึกสำเร็จ | {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                </div>
                <center>
                    <p style='margin:0;'>ยอดใช้จ่ายรวมวันนี้</p>
                    <h1 style='color: #00FFCC;'>฿ {total:,.2f}</h1>
                </center>
                <div style='font-size:14px; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px;'>
                    {"".join([f"• {row['รายการ']}: {row['จำนวน']:,.2f} บาท<br>" for index, row in today_data.iterrows()])}
                </div>
                <p style='text-align:center; font-size:12px; margin-top:10px;'>--- "อยู่นิ่งๆ ไม่เจ็บตัว" ---</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("ยังไม่มีรายการบันทึกของวันนี้ครับคุณพ่อ")
        # --- [ ส่วนเสริม: ออกใบสรุป Slip ] ---
if not st.session_state.logs.empty:
    st.write("---")
    if st.button("📄 ออกใบสรุป (Slip) ของวันนี้"):
        today = datetime.now().date()
        today_data = st.session_state.logs[st.session_state.logs['วันที่'] == today]
        
        if not today_data.empty:
            total = today_data['จำนวน'].sum()
            # สร้างหน้าตา Slip แบบนิ่งๆ เท่ๆ
            st.markdown(f"""
                <div style="background-color: #f0f2f6; color: #333; padding: 20px; border-radius: 10px; font-family: 'Courier New', Courier, monospace; border: 2px dashed #999;">
                    <center>
                        <h2 style="color: #000;">STATION: อยู่นิ่งๆ ไม่เจ็บตัว</h2>
                        <p>วันที่: {today}</p>
                        <hr style="border-top: 1px dashed #bbb;">
                    </center>
                    <table style="width: 100%;">
                        {"".join([f"<tr><td>{row['รายการ']}</td><td style='text-align:right;'>{row['จำนวน']:,.2f}</td></tr>" for index, row in today_data.iterrows()])}
                    </table>
                    <hr style="border-top: 1px dashed #bbb;">
                    <h3 style="text-align: center;">ยอดรวมใช้ไป: {total:,.2f} บาท</h3>
                    <center><p>-- บันทึกเรียบร้อย ไม่เจ็บตัวแน่นอน --</p></center>
                </div>
            """, unsafe_allow_html=True)
            st.balloons() # ฉลองที่ออกสลิปสำเร็จ!
        else:
            st.warning("วันนี้ยังไม่มีข้อมูลให้ออกสลิปครับคุณพ่อ")

        


    }
    </style>
""" , unsafe_allow_html= True )

# --- 2. ระบบเทคนิค ---
ถ้า 'money_logs'  ไม่ อยู่ใน st.session_state :
    เซนต์เซสชั่น_สถานะmoney_logs = pd. DataFrame ( columns= [ 'วันที่' , 'รายการ' , 'จำนวน' ] )

เซนต์markdown ( "<h2 style='text-align: center; color: #00FFCC;'>💰 บันทึกงบรายวัน</h2>" , unsafe_allow_html= True )

# --- [ จุดแก้ให้คุณพ่อ ] ---
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
