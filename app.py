import streamlit as st
import streamlit.components.v1 as components

def render_home():
    # --- 1. CSS สำหรับหน้าหลัก (Center Logo & Grid Buttons) ---
    st.markdown("""
        <style>
        /* จัดการ Layout ของโลโก้ */
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding-top: 20px;
            margin-bottom: 30px;
        }
        .logo-img {
            width: 150px; /* ปรับขนาดโลโก้ได้ที่นี่ */
            border-radius: 50%;
            border: 3px solid #FFD700;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
        }
        
        /* สไตล์หัวข้อ */
        .home-title {
            text-align: center;
            color: #FFD700;
            font-size: 24px;
            letter-spacing: 3px;
            margin-bottom: 20px;
        }

        /* ปุ่ม 5 ห้อง (Grid 5 สี) */
        .stButton>button {
            height: 100px !important;
            font-size: 18px !important;
            font-weight: bold !important;
            border-radius: 15px !important;
            transition: transform 0.3s, box-shadow 0.3s !important;
        }
        .stButton>button:hover {
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- 2. แสดงโลโก้ตรงกลาง ---
    # หมายเหตุ: คุณต้องมีไฟล์ logo.jpg อยู่ในโฟลเดอร์เดียวกับไฟล์โค้ด
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image("logo.jpg", width=150) # หรือใช้ CSS class logo-img ครอบ
    except:
        st.markdown('<div style="color:gray;">(รอใส่ไฟล์ logo.jpg)</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<h2 class="home-title">SYNAPSE COMMAND CENTER</h2>', unsafe_allow_html=True)

    # --- 3. เพลย์ลิสต์ YouTube ---
    st.markdown("### 🎬 Synapse Playlist")
    # ใช้ iFrame เพื่อดึงเพลย์ลิสต์ตามลิงก์ที่คุณให้มา
    playlist_url = "https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    components.html(f"""
        <iframe width="100%" height="350" src="{playlist_url}" 
        frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen style="border-radius:15px; border:1px solid #D4AF37;"></iframe>
    """, height=360)

    st.write("---")

    # --- 4. ปุ่ม 5 ห้อง 5 สี ---
    st.subheader("📂 เลือกมิติการเข้าถึง")
    
    # แบ่งเป็นแถวเพื่อให้ปุ่มดูสวยงาม (แถวบน 3 ปุ่ม แถวล่าง 2 ปุ่ม หรือตามเหมาะสม)
    col1, col2, col3 = st.columns(3)
    col4, col5, _ = st.columns([1, 1, 1])

    with col1:
        if st.button("🔴 RED\nMedia", key="btn_red"):
            st.session_state.page = "red"; st.rerun()
    with col2:
        if st.button("🔵 BLUE\nVoice", key="btn_blue"):
            st.session_state.page = "blue"; st.rerun()
    with col3:
        if st.button("🟢 GREEN\nSecret", key="btn_green"):
            st.session_state.page = "green"; st.rerun()
    with col4:
        if st.button("⚫ BLACK\nMatrix", key="btn_black"):
            st.session_state.page = "black"; st.rerun()
    with col5:
        # เพิ่มห้องที่ 5 สีม่วง (Purple Luxury)
        if st.button("🟣 PURPLE\nVIP", key="btn_purple"):
            st.session_state.page = "purple"; st.rerun()

    # ปุ่ม Logout อยู่ล่างสุดแบบเนียนๆ
    st.write("")
    if st.button("🚪 Exit Protocol"):
        del st.session_state.user
        st.rerun()

# --- ส่วนควบคุมในไฟล์หลัก ---
if 'user' in st.session_state:
    if st.session_state.get('page') == "home":
        render_home()
