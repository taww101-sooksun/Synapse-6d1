import streamlit as st
import os
import base64

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="MUSIC 6D PRO", layout="wide", initial_sidebar_state="collapsed")
# --- 2. แต่งหน้าตาให้เท่ (UI) ---
st.set_page_config(page_title="SYNAPSE 6D Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stButton>button { 
        background-color: #FF0000; color: white; border-radius: 10px; 
        height: 60px; font-weight: bold; border: 2px solid #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Music 6D อยู่นิ้งๆไม่เจ็บตัว")
st.write('สโลแกน: "อยู่นิ่งๆ ไม่เจ็บตัว"')
# 2. คาถา CSS ล็อกพิกัด (บังคับรูปอยู่ข้างในเท่านั้น)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    header, footer, [data-testid="stToolbar"] {visibility:hidden !important;}
    
    /* สร้างกรอบทีวี */
    .tv-box {
        border: 15px solid #FF0000;
        border-right: 15px solid #0000FF;
        border-bottom: 15px solid #0000FF;
        border-radius: 40px;
        width: 100%;
        height: 350px;
        background-color: #000;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        box-shadow: 0 0 30px #FF0000;
    }

    /* บังคับรูปในกรอบ */
    .tv-box img {
        width: 100%;
        height: 100%;
        object-fit: contain; /* ปรับให้รูปพอดีกรอบ ไม่เบี้ยว */
    }

    /* ตัวหนังสือวิ่ง */
    .run-text {
        background: #111;
        border: 2px solid #0000FF;
        border-radius: 10px;
        padding: 10px;
        color: #FF0000;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ส่วนดึงรูป globe.jpg แบบ Base64 (ไม้ตาย) ---
def display_globe():
    if os.path.exists("globe.jpg"):
        with open("globe.jpg", "rb") as f:
            data = base64.b64encode(f.read()).decode()
        # ยัดรูปเข้าไปใน div .tv-box โดยตรง
        st.markdown(f'<div class="tv-box"><img src="data:image/jpeg;base64,{data}"></div>', unsafe_allow_html=True)
    else:
        # ถ้าไม่มีรูป ให้โชว์คำเตือนในกรอบ
        st.markdown('<div class="tv-box"><h2 style="color:red;">ไม่พบไฟล์ globe.jpg</h2></div>', unsafe_allow_html=True)

# --- 4. แสดงผลหน้าจอหลัก ---
display_globe()

st.markdown('<div class="run-text"><marquee scrollamount="10">อยู่นิ่งๆ ไม่เจ็บตัว... สถานีเพลง 6D เปิดเอาเองนะครับ จะลงเพลงไว้ให้ยาวๆ 24 ช.ม!</marquee></div>', unsafe_allow_html=True)

# --- 5. ส่วนของเพื่อน (รูปจะอยู่ล่างสุดจริงๆ) ---
st.write("---")
st.subheader("📸 มุมเพื่อนโชว์รูป")
friend_files = st.file_uploader("ส่งรูปมาโชว์ตรงนี้", type=['jpg','png','jpeg'], accept_multiple_files=True)

if friend_files:
    for f in friend_files:
        st.image(f, use_container_width=True)

# --- 6. คลังเพลง (ดึงจาก GitHub) ---
st.write("### 💿 รายการเพลงของ อยู่นิ้งๆไม่เจ็บตัว")
music_files = [f for f in os.listdir('.') if f.endswith('.mp3')]

if music_files:
    song = st.selectbox("เลือกเพลง:", music_files)
    st.audio(song)
else:
    st.error("⚠️ อย่าลืมลงเพลง .mp3 ในหน้าแรกของ GitHub นะครับ")
if friend_files:
    for f in friend_files:
        st.image(f, use_container_width=True)
# --- 3. ระบบเลือกเพลงและเล่นต่อเนื่อง ---
if 'track_index' not in st.session_state:
    st.session_state.track_index = 0

current_track = playlist[st.session_state.track_index]

st.subheader(f"▶️ กำลังบรรเลง: {current_track['title']}")

# --- 6. คลังเพลง (ดึงจาก GitHub) ---
st.write("### 💿 รายการเพลงของ อยู่นิ้งๆไม่เจ็บตัว")
music_files = [f for f in os.listdir('.') if f.endswith('.mp3')]

col1, col2 = st.columns(2)
with col1:
    if st.button("⏮️ เพลงก่อนหน้า"):
        st.session_state.track_index = (st.session_state.track_index - 1) % len(playlist)
        st.rerun()
with col2:
    if st.button("ถัดไป ⏭️"):
        st.session_state.track_index = (st.session_state.track_index + 1) % len(playlist)
        st.rerun()
st.write("#### *สโลแกน: อยู่นิ่งๆ ไม่เจ็บตัว*")
