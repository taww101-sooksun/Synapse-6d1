import streamlit as st
import os

# ตั้งค่าหน้าแอป
st.set_page_config(page_title="SYNAPSE MP3 PLAYER", layout="centered")

# --- 1. ค้นหาไฟล์ MP3 ในโฟลเดอร์เดียวกัน ---
current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
mp3_files = [f for f in os.listdir(current_dir) if f.endswith('.mp3')]

# --- 2. ส่วนควบคุมและปรับแต่ง (Sidebar) ---
st.sidebar.header("🎨 ปรับแต่งเครื่องเล่น")

# ปรับสีสัน
theme_color = st.sidebar.color_picker("เลือกสีหลักของแอป", "#00FFCC")
text_color = st.sidebar.color_picker("เลือกสีตัวหนังสือ", "#FFFFFF")

# ปรับเอฟเฟกต์กรอบไฟนีออน
neon_glow = st.sidebar.slider("ความฟุ้งของไฟนีออน (px)", 5, 30, 15)

# ตัวเลือกข้อความวิ่ง
marquee_text = st.sidebar.text_input("พิมพ์ข้อความวิ่งสวยๆ", "ยินดีต้อนรับสู่ SYNAPSE COMMAND CENTER - อยู่นิ่งๆ ไม่เจ็บตัว...")
marquee_speed = st.sidebar.slider("ความเร็วข้อความวิ่ง", 1, 20, 10)

# ส่วนปรับเสียง (Simulated Equalizer สำหรับหน้าตาแอป)
st.sidebar.subheader("🎚️ ปรับแต่งเสียง (EQ)")
bass = st.sidebar.slider("เสียงต่ำ (Bass)", 0, 100, 50)
mid = st.sidebar.slider("เสียงกลาง (Mid)", 0, 100, 50)
treble = st.sidebar.slider("เสียงสูง (Treble)", 0, 100, 50)


# --- 3. ระบบตกแต่งสไตล์ด้วย CSS (Custom CSS) ---
custom_css = f"""
<style>
    /* สไตล์กรอบแอปนีออน */
    .main-player-box {{
        border: 2px solid {theme_color};
        border-radius: 15px;
        padding: 25px;
        background-color: #111111;
        box-shadow: 0 0 {neon_glow}px {theme_color};
        color: {text_color};
        text-align: center;
        margin-bottom: 20px;
    }}
    /* สไตล์ข้อความวิ่ง */
    .marquee-box {{
        background: #000000;
        color: {theme_color};
        padding: 8px;
        border-radius: 5px;
        font-weight: bold;
        border: 1px solid {theme_color};
        overflow: hidden;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# --- 4. หน้าตาเครื่องเล่นเพลง (UI) ---

# โลโก้และชื่อแอป
st.markdown(f"""
<div class='main-player-box'>
    <h1 style='color: {theme_color}; margin-bottom: 5px;'>🎧 MP3 PLAYER</h1>
    <p style='font-style: italic; opacity: 0.8;'>สโลแกน: อยู่นิ่งๆ ไม่เจ็บตัว</p>
</div>
""", unsafe_allow_html=True)

# แสดงข้อความวิ่ง
if marquee_text:
    st.markdown(f"""
    <div class='marquee-box'>
        <marquee scrollamount='{marquee_speed}'>{marquee_text}</marquee>
    </div>
    <br>
    """, unsafe_allow_html=True)

# กล่องเลือกเพลง
st.subheader("🎵 เลือกเพลงที่ต้องการเล่น")
if mp3_files:
    selected_song = st.selectbox("ไฟล์ MP3 ในโฟลเดอร์ของคุณ:", mp3_files)
    
    # ดึงไฟล์เพลงมาเตรียมเล่น
    song_path = os.path.join(current_dir, selected_song)
    
    # แสดงเครื่องเล่นเพลงมาตรฐานของ HTML5 (รันได้จริงชัวร์ๆ บนเบราว์เซอร์มือถือ)
    with open(song_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    
    st.success(f"กำลังพร้อมเล่นเพลง: {selected_song}")
else:
    st.warning("⚠️ ไม่พบไฟล์ .mp3 ในโฟลเดอร์นี้ กรุณาเอาไฟล์เพลงมาวางไว้โฟลเดอร์เดียวกับโค้ดก่อนนะครับ")


# --- 5. ปุ่มเอฟเฟกต์ต่างๆ (Sound Effects Board) ---
st.write("---")
st.subheader("🎹 ปุ่มซาวด์เอฟเฟกต์ (กดขำๆ หรือเอาไว้เล่นจังหวะ)")

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🚨 Airhorn"):
        st.toast("บี๊บๆๆๆ! (เอฟเฟกต์ Airhorn)")
with col2:
    if st.button("💥 Explosion"):
        st.toast("ตู้มมม! (เอฟเฟกต์ระเบิด)")
with col3:
    if st.button("🎵 Scratch"):
        st.toast("ฟึ่ดฟั่ด! (เอฟเฟกต์ดีเจสแครช)")
with col4:
    if st.button("👏 Applause"):
        st.toast("แปะๆๆๆ! (เสียงปรบมือ)")


# แสดงสถานะ EQ ที่ปรับไว้ (ให้เห็นค่าที่เปลี่ยนไปจริง)
st.write("---")
st.caption(f"📊 สถานะเสียงปัจจุบัน -> Bass: {bass}% | Mid: {mid}% | Treble: {treble}%")
