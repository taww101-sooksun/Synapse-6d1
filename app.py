import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. ตั้งค่าพื้นฐาน ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1zjKmVhshtYGoM3OQS5V3D_DaB1u-_TkFQCzn9jmlQaU/edit?usp=sharing"

st.set_page_config(page_title="BigBoss Healing Station", layout="wide")

# ปรับหน้าตาให้หล่อๆ แบบช่างใหญ่
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; border: 4px solid #8B00FF; border-radius: 20px; }
    h1, h2, h3, p, label { color: white !important; }
    .stButton>button { background-color: #8B00FF; color: white; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# เชื่อมต่อ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def get_permanent_id(name):
    try:
        # พยายามอ่านข้อมูลจาก Google Sheets
        df = conn.read(spreadsheet=SHEET_URL, ttl=0) # ttl=0 คือให้อ่านสดๆ ตลอด
        df = df.dropna(how='all')
    except:
        # ถ้าอ่านไม่ได้ ให้สร้างตารางเปล่าขึ้นมา
        df = pd.DataFrame(columns=['name', 'user_number'])
    
    # ตรวจสอบว่าชื่อนี้มีหรือยัง
    existing_user = df[df['name'].astype(str) == str(name)]
    
    if not existing_user.empty:
        return int(existing_user.iloc[0]['user_number'])
    else:
        # ถ้ายังไม่มี ให้รันเลขใหม่
        if len(df) == 0:
            new_id = 1
        else:
            new_id = int(pd.to_numeric(df['user_number']).max()) + 1
        
        # เพิ่มชื่อใหม่
        new_row = pd.DataFrame([{"name": name, "user_number": new_id}])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        
        # ส่งกลับไปบันทึกที่ Google Sheets
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        return new_id

# --- 2. ระบบลงชื่อเข้าใช้ ---
if "my_id" not in st.session_state:
    st.markdown("<h2 style='text-align:center;'>🔐 เข้าสู่สถานีบำบัดใจ</h2>", unsafe_allow_html=True)
    st.write("---")
    name_input = st.text_input("ระบุชื่อของคุณ (เพื่อรับหมายเลขประจำตัว):")
    
    if st.button("เข้าสู่สถานี 🚀"):
        if name_input:
            try:
                with st.spinner('กำลังจดทะเบียนหมายเลขของคุณ...'):
                    user_id = get_permanent_id(name_input)
                    st.session_state.my_id = user_id
                    st.session_state.my_name = name_input
                    st.rerun()
            except Exception as e:
                st.error(f"ใจเย็นๆ ครับช่างใหญ่ เหมือน Google Sheets จะยังไม่เปิดสิทธิ์ Editor ให้แอปครับ")
                st.info("วิธีแก้: กดปุ่ม 'แชร์' ใน Sheets -> เปลี่ยนเป็น 'ทุกคนที่มีลิงก์' -> เลือก 'เอดีเตอร์'")
        else:
            st.warning("กรุณาใส่ชื่อก่อนครับ")
    st.stop()

# --- 3. หน้าสถานีเมื่อเข้าสำเร็จ ---
my_id = st.session_state.my_id
my_name = st.session_state.my_name

st.sidebar.success(f"คุณคือสมาชิกหมายเลข: {my_id}")
st.sidebar.markdown(f"**ชื่อ:** {my_name}")

st.markdown(f"<h2 style='text-align:center;'>🎵 สถานีหมายเลข {my_id} ยินดีต้อนรับ</h2>", unsafe_allow_html=True)
st.write("---")

# คลังเพลง (ช่างใหญ่เพิ่มลิงก์ต่อได้เลยครับ)
SONGS = {
    "01. การเดินทางของฉัน": "https://github.com/leehunna789-boop/blank-app/raw/refs/heads/main/%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%94%E0%B8%B4%E0%B8%99%E0%B8%97%E0%B8%B2%E0%B8%87%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B8%89%E0%B8%B1%E0%B8%99.mp3",
}

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📻 เพลงบำบัดใจ")
    selected = st.selectbox("เลือกเพลง:", list(SONGS.keys()))
    st.audio(SONGS[selected])
    st.divider()
    st.write("📢 *อยู่นิ่งๆ ไม่เจ็บตัว โดย ช่างใหญ่*")

with col2:
    st.subheader("💬 สนทนาธรรม")
    st.write("ยินดีต้อนรับสมาชิกใหม่ทุกท่าน!")
    # ส่วนนี้สามารถพัฒนาต่อเป็นแชทจริงได้ในอนาคตครับ
