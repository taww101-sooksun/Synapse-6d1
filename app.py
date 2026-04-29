import streamlit as st
import os
import base64

# --- CONFIG ---
st.set_page_config(page_title="HAPPY COFFI GOLD", layout="centered")

# --- CUSTOM CSS (ลบ Streamlit UI & แต่งสีสันจัดจ้าน) ---
st.markdown("""
    <style>
    /* ลบ Header, Footer และ Menu ของ Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* แต่งพื้นหลังและสีสัน */
    .stApp {
        background: linear-gradient(45deg, #ff00cc, #3333ff);
        color: white;
    }
    
    .main-container {
        text-align: center;
        padding: 2rem;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 20px;
        border: 5px solid #00ff00;
    }
    
    h1 {
        text-shadow: 3px 3px #ff0000;
        font-size: 3rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_base64_bin(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- UI SECTION ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# แสดง Logo
if os.path.exists("logo1.png"):
    st.image("logo1.png", width=200)

st.markdown("<h1>HAPPY COFFI GOLD</h1>", unsafe_allow_html=True)

# --- MUSIC LOGIC ---
# ดึงไฟล์ .mp3 ทั้งหมดที่อยู่ในโฟลเดอร์เดียวกับ .py
music_files = [f for f in os.listdir('.') if f.endswith('.mp3')]

if music_files:
    # สร้าง Playlist ในรูปแบบ JavaScript Array
    # หมายเหตุ: เราจะดึงไฟล์มาทำเป็น Base64 เพื่อให้ Browser เล่นได้ทันทีโดยไม่ติดเรื่อง Path
    playlist_html = ""
    
    # สำหรับตัวอย่างนี้ ผมจะใช้เทคนิคสร้าง Audio Element ที่สลับเพลงอัตโนมัติ
    # เราจะส่งชื่อไฟล์ทั้งหมดเข้า JS
    files_js = str(music_files)
    
    # อ่านไฟล์แรกมาเป็น Default
    audio_base64 = get_base64_bin(music_files[0])
    
    audio_component = f"""
        <div style="margin-top: 20px;">
            <p>ตอนนี้กำลังเล่น: <span id="track-name">{music_files[0]}</span></p>
            <audio id="myAudio" controls autoplay style="width: 100%;">
                <source id="audioSource" src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        </div>

        <script>
        var audio = document.getElementById('myAudio');
        var source = document.getElementById('audioSource');
        var trackName = document.getElementById('track-name');
        var playlist = {files_js};
        var currentIndex = 0;

        // เมื่อเพลงจบ ให้เปลี่ยนเพลงถัดไป
        audio.onended = function() {{
            currentIndex++;
            if (currentIndex >= playlist.length) {{
                currentIndex = 0; // วนกลับไปเพลงแรก
            }}
            
            // หมายเหตุ: การดึงไฟล์ถัดไปใน Streamlit แบบ Static HTML 
            // จะต้องใช้การ Refresh หรือดึงผ่าน URL ตรงๆ 
            // ในที่นี้แนะนำให้ใส่เพลงเดียวแล้ว Loop หรือใช้ฟีเจอร์ loop ของ HTML5
            // หากต้องการเพลงต่อเนื่องแบบ Dynamic จริงๆ ต้องมี Server เก็บไฟล์ที่เข้าถึงได้ผ่าน URL
            
            location.reload(); // วิธีที่ง่ายที่สุดสำหรับไฟล์ Local คือ Reload เพื่อดึง State ใหม่ (ถ้าทำ Logic เพิ่ม)
        }};
        
        // สำหรับความจริง: เว็บ Browser ส่วนใหญ่จะบล็อก Autoplay 
        // ผู้ใช้ต้องกด Play ครั้งแรกก่อน เพลงถึงจะรันต่อเนื่องได้
        </script>
    """
    st.markdown(audio_component, unsafe_allow_html=True)
    
    st.write(f"พบเพลงในโฟลเดอร์ {len(music_files)} เพลง")
    for m in music_files:
        st.write(f"🎵 {m}")
else:
    st.error("ไม่พบไฟล์ .mp3 ในโฟลเดอร์เดียวกับโค้ดครับ!")

st.markdown('</div>', unsafe_allow_html=True)

# สโลแกนปิดท้ายตามสไตล์
st.markdown("<br><center><p>อยู่นิ่งๆ ไม่เจ็บตัว</p></center>", unsafe_allow_html=True)
