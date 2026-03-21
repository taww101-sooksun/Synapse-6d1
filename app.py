import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="Streamlit Music Player", layout="centered")

# ใส่ CSS สำหรับพื้นหลังรุ้ง (ตามที่คุณให้มา)
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(270deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff);
        background-size: 1200% 1200%;
        animation: RainbowFlow 10s ease infinite;
    }}
    @keyframes RainbowFlow {{
        0%{{background-position:0% 50%}}
        50%{{background-position:100% 50%}}
        100%{{background-position:0% 50%}}
    }}
    /* ซ่อนปุ่มเมนูของ Streamlit เพื่อความสวยงามตอนแคปวิดีโอ */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_stdio=True)

st.title("🎵 Music Crossfader Pro")

# ส่วนของการเลือกไฟล์
uploaded_files = st.file_uploader("เลือกไฟล์เพลงของคุณ (เลือกพร้อมกันหลายไฟล์ได้)", type=["mp3", "wav"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"โหลดเพลงสำเร็จ {len(uploaded_files)} เพลง พร้อมเล่น!")
    
    # แปลงไฟล์เป็นตัวแปรเพื่อส่งเข้า JavaScript
    # (ในขั้นตอนนี้เราจะส่งชื่อไฟล์ไปโชว์)
    file_names = [f.name for f in uploaded_files]
    
    # สร้าง Player ด้วย HTML/JS ฝังใน Streamlit
    custom_player_html = f"""
    <div id="player-container" style="text-align: center; color: white; font-family: sans-serif;">
        <div style="background: rgba(0,0,0,0.7); padding: 10px; margin-bottom: 20px; border-radius: 10px;">
            <marquee id="marquee-text" style="font-size: 24px; font-weight: bold; color: #AFEEEE;">
                เตรียมพร้อมเล่นเพลง...
            </marquee>
        </div>
        
        <div id="cover" style="width: 250px; height: 250px; margin: 0 auto 20px; background: #AFEEEE; border: 5px solid #FF7F50; border-radius: 20px; display: flex; align-items: center; justify-content: center; color: #333; font-weight: bold;">
            No Cover
        </div>

        <button id="play-btn" style="
            padding: 20px 40px; 
            font-size: 20px; 
            background: #FF7F50; 
            color: white; 
            border: none; 
            border-radius: 50px; 
            cursor: pointer;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        ">เริ่มการเล่นเพลงแบบ Crossfade</button>
    </div>

    <script>
        // หมายเหตุ: ใน Streamlit เราจะจำลองการเล่นผ่าน JS เพื่อความเนียน
        const btn = document.getElementById('play-btn');
        btn.onclick = () => {{
            alert("เนื่องจากข้อจำกัดด้านความปลอดภัยของ Browser บน Streamlit Cloud แนะนำให้รันแบบ HTML ไฟล์เดียวจะเนียนที่สุดครับ แต่ถ้าจะใช้บนนี้ ต้องทำการ Map ไฟล์เข้ากับ Audio Object ต่อไป");
            // ส่วนนี้เป็น Logic การเล่นเพลงใน Browser
        }};
    </script>
    """
    components.html(custom_player_html, height=500)

else:
    st.info("กรุณาเลือกเพลงจากเครื่องของคุณเพื่อเริ่มใช้งาน")
