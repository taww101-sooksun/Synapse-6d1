import streamlit as st

# --- 1. ตั้งค่าหน้าตาแอป (UI Customization) ---
st.set_page_config(page_title="BigBoss Healing Station", layout="centered")

# แต่ง CSS ให้หล่อเท่แบบช่างใหญ่
st.markdown("""
    <style>
    /* พื้นหลังและกรอบแอป */
    .stApp {
        background: linear-gradient(180deg, #0f0f0f 0%, #1a0033 100%);
        color: #e0e0e0;
    }
    
    /* กรอบหัวข้อ */
    .main-header {
        background: rgba(139, 0, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #8B00FF;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(139, 0, 255, 0.3);
    }

    /* ตัววิ่งสโลแกน */
    .marquee {
        color: #8B00FF;
        font-weight: bold;
        font-size: 1.2rem;
        border-top: 1px solid #333;
        border-bottom: 1px solid #333;
        padding: 5px 0;
    }

    /* ตกแต่งปุ่มและ Selectbox */
    .stSelectbox label { color: #BB86FC !important; font-size: 1.1rem; }
    
    /* ปรับแต่ง Audio Player */
    audio { width: 100%; filter: invert(100%) hue-rotate(275deg) brightness(1.5); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ส่วนหัวของแอป ---
st.markdown("""
    <div class="main-header">
        <h1 style='margin:0; color:#BB86FC;'>🎵 สถานีบำบัดใจ 🎵</h1>
        <p style='margin:5px 0 0 0; color:#888;'>ศูนย์รวมร่องเพลง... บรรเทาทุกข์</p>
    </div>
    """, unsafe_allow_html=True)

# ตัววิ่งสโลแกนประจำตัว
st.markdown('<marquee class="marquee">อยู่นิ่งๆ ไม่เจ็บตัว... ยินดีต้อนรับทุกท่านสู่สถานีบำบัดใจโดย ช่างใหญ่ ...</marquee>', unsafe_allow_html=True)

st.write("")

# --- 3. คลังเพลง (ใส่เพิ่มตรงนี้ได้เลยครับ) ---
SONGS = {
    "🎧 01. การเดินทางของฉัน": "https://github.com/leehunna789-boop/blank-app/raw/refs/heads/main/%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%94%E0%B8%B4%E0%B8%99%E0%B8%97%E0%B8%B2%E0%B8%87%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B8%89%E0%B8%B1%E0%B8%99.mp3",
    # "🎧 02. ชื่อเพลงต่อไป": "ลิงก์เพลง",
}

# --- 4. ส่วนเครื่องเล่นเพลง ---
st.subheader("📻 เลือกฟังร่องเพลงที่ท่านชอบ")
selected_song = st.selectbox("", list(SONGS.keys()), label_visibility="collapsed")

st.info(f"📍 กำลังเล่น: {selected_song}")
st.audio(SONGS[selected_song])

st.write("")
st.write("---")

# --- 5. ส่วนพูดคุย (แบบง่าย ไม่ต้องเก็บลงฐานข้อมูล) ---
with st.expander("💬 ฝากข้อความถึงช่างใหญ่"):
    user_msg = st.text_input("พิมพ์ข้อความ:")
    if st.button("ส่งความรู้สึก"):
        st.success("ข้อความของท่านถูกส่งถึงใจช่างใหญ่แล้ว! (ระบบจำลอง)")

# ส่วนท้าย
st.markdown("<p style='text-align:center; color:#555;'>Created by BigBoss Station © 2026</p>", unsafe_allow_html=True)
