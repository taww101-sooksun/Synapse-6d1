import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. ตั้งค่าพื้นฐาน ---
# ลิงก์ที่ช่างใหญ่ส่งมา ผมใส่ให้เรียบร้อยแล้วครับ
SHEET_URL = "https://docs.google.com/spreadsheets/d/1zjKmVhshtYGoM3OQS5V3D_DaB1u-_TkFQCzn9jmlQaU/edit?usp=sharing"

st.set_page_config(page_title="BigBoss Healing Station", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; border: 4px solid #8B00FF; border-radius: 20px; }
    h1, h2, h3, p { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# เชื่อมต่อกับ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def get_permanent_id(name):
    # อ่านข้อมูลทะเบียนสมาชิก
    df = conn.read(spreadsheet=SHEET_URL, usecols=[0, 1])
    df = df.dropna()
    
    # ตรวจสอบว่าชื่อนี้มีในทะเบียนหรือยัง
    existing_user = df[df['name'].astype(str) == str(name)]
    
    if not existing_user.empty:
        # ถ้าเคยมาแล้ว คืนเลขเดิมให้
        return int(existing_user.iloc[0]['user_number'])
    else:
        # ถ้ามาครั้งแรก ให้เลขลำดับถัดไป
        if len(df) == 0:
            new_id = 1
        else:
            new_id = int(df['user_number'].max()) + 1
        
        # จดบันทึกลงสมุดทะเบียนถาวร
        new_row = pd.DataFrame([{"name": name, "user_number": new_id}])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        return new_id

# --- 2. ระบบลงชื่อเข้าใช้ (Login) ---
if "my_id" not in st.session_state:
    st.markdown("<h2 style='text-align:center;'>🔐 เข้าสู่สถานีบำบัดใจ</h2>", unsafe_allow_html=True)
    st.write("---")
    name_input = st.text_input("ระบุชื่อของคุณ (เพื่อรับหมายเลขประจำตัวถาวร):")
    
    if st.button("เข้าสู่สถานี 🚀"):
        if name_input:
            with st.spinner('กำลังค้นหาหมายเลขของคุณ...'):
                user_id = get_permanent_id(name_input)
                st.session_state.my_id = user_id
                st.session_state.my_name = name_input
                st.rerun()
        else:
            st.warning("กรุณาใส่ชื่อก่อนครับช่างใหญ่")
    st.stop()

# --- 3. หน้าสถานีเมื่อเข้าสำเร็จ ---
my_id = st.session_state.my_id
my_name = st.session_state.my_name

st.sidebar.markdown(f"### 👤 สมาชิก")
st.sidebar.success(f"คุณ: **{my_name}**")
st.sidebar.info(f"หมายเลขประจำตัว: **{my_id}**")

# คลังเพลง 100 เพลง (ใส่เพลงแรกให้แล้วครับ)
SONGS = {
    "01. การเดินทางของฉัน": "https://github.com/leehunna789-boop/blank-app/raw/refs/heads/main/%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%94%E0%B8%B4%E0%B8%99%E0%B8%97%E0%B8%B2%E0%B8%87%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B8%89%E0%B8%B1%E0%B8%99.mp3",
}

st.markdown(f"<h2 style='text-align:center;'>🎵 สถานีหมายเลข {my_id} ยินดีต้อนรับ</h2>", unsafe_allow_html=True)
st.write("---")

col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("📻 เลือกฟังเพลงบำบัดใจ")
    selected = st.selectbox("ค้นหาจาก 100 เพลง:", list(SONGS.keys()))
    st.audio(SONGS[selected])
    st.success(f"กำลังเล่น: {selected}")
    st.divider()
    st.write("📜 *ปรัชญา: อยู่นิ่งๆ ไม่เจ็บตัว*")

with col_right:
    st.subheader("💬 สภากาแฟ")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    # แสดงแชท
    for m in st.session_state.messages:
        st.write(f"**{m['name']} (#{m['id']})**: {m['text']}")

    # ช่องส่งแชท
    with st.form("chat", clear_on_submit=True):
        msg = st.text_input("พิมพ์อะไรหน่อย...")
        if st.form_submit_button("ส่ง"):
            st.session_state.messages.append({"name": my_name, "id": my_id, "text": msg})
            st.rerun()
