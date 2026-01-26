import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. ตั้งค่าการเชื่อมต่อ Google Sheets ---
# ช่างใหญ่ต้องนำ URL ของไฟล์ Sheet (ไม่ใช่โฟลเดอร์) มาใส่ตรงนี้ครับ
# ลิงก์ที่ลงท้ายด้วย /edit#gid=0
SHEET_URL = "https://docs.google.com/spreadsheets/d/1zuCTvb2qqn-4Yy62eZzpTK0Qg8ouIV43/edit#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

def get_permanent_id(name):
    # อ่านข้อมูลปัจจุบันจาก Sheets
    df = conn.read(spreadsheet=SHEET_URL, usecols=[0, 1])
    df = df.dropna()

    # ตรวจสอบว่าชื่อนี้มีในระบบหรือยัง
    existing_user = df[df['name'] == name]
    
    if not existing_user.empty:
        # ถ้าเจอชื่อเดิม ส่งเลขเดิมกลับไป
        return int(existing_user.iloc[0]['user_number'])
    else:
        # ถ้าเป็นชื่อใหม่ ให้รันเลขต่อจากลำดับล่าสุด
        if len(df) == 0:
            new_id = 1
        else:
            new_id = int(df['user_number'].max()) + 1
        
        # บันทึกคนใหม่ลง Sheets
        new_data = pd.DataFrame([{"name": name, "user_number": new_id}])
        updated_df = pd.concat([df, new_data], ignore_index=True)
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        return new_id

# --- 2. หน้าจอเข้าสู่ระบบ ---
if "my_id" not in st.session_state:
    st.title("🔐 เข้าสู่สถานีบำบัดใจ")
    name_input = st.text_input("กรุณาใส่ชื่อของคุณ (เพื่อดึงหมายเลขประจำตัวถาวร):")
    
    if st.button("ตกลง"):
        if name_input:
            with st.spinner('กำลังตรวจสอบทะเบียน...'):
                user_id = get_permanent_id(name_input)
                st.session_state.my_id = user_id
                st.session_state.my_name = name_input
                st.rerun()
        else:
            st.error("กรุณาพิมพ์ชื่อก่อนครับ")
    st.stop()

# --- 3. หน้าหลักของแอปหลังจากล็อคอินแล้ว ---
my_id = st.session_state.my_id
my_name = st.session_state.my_name

st.sidebar.markdown(f"### 👤 ข้อมูลสมาชิก")
st.sidebar.write(f"ชื่อ: **{my_name}**")
st.sidebar.subheader(f"ลำดับที่: {my_id}")

st.title(f"🎵 ยินดีต้อนรับกลับมา หมายเลข {my_id}")
st.write("สถานีบำบัดใจ 100 เพลง พร้อมให้บริการคุณแล้วครับ")

# --- ตรงนี้ใส่เครื่องเล่นเพลง 100 เพลง และ แชต ที่เราทำไว้ก่อนหน้านี้ได้เลย ---
