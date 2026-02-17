import streamlit as st
import streamlit.components.v1 as components

def render_home():
    # CSS ตกแต่งให้สมกับความเป็นเจ้าของ Synapse
    st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle, #001219 0%, #000000 100%); }
        .logo-center { display: flex; justify-content: center; padding: 20px; }
        .logo-img { 
            width: 280px; border-radius: 15px; 
            border: 2px solid #D4AF37; 
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.5); 
        }
        /* ปรับสไตล์ปุ่ม 5 สี */
        .stButton>button { height: 60px; border-radius: 10px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    # 1. แสดงโลโก้ที่เป็นความจริงของคุณ
    st.markdown('<div class="logo-center">', unsafe_allow_html=True)
    # ลิงก์ตรงจาก GitHub ที่คุณพิสูจน์ให้เห็นแล้ว
    logo_url = "https://raw.githubusercontent.com/taww101-sooksun/Synapse-6d1/main/logo.jpg"
    st.image(logo_url, width=280)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. YouTube Playlist (ตัวจริงที่ต้องการ)
    st.write("---")
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    components.html(f"""
        <iframe width="100%" height="315" 
        src="https://www.youtube.com/embed/videoseries?list={playlist_id}" 
        frameborder="0" allowfullscreen style="border-radius:12px; border:1px solid #333;"></iframe>
    """, height=330)

    # 3. ปุ่มเข้าห้อง 5 สี (Grid)
    st.write("---")
    st.subheader("🌐 ระบบศูนย์บัญชาการ Synapse")
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        if st.button("🔴 RED (Media)", use_container_width=True): st.session_state.page = "red"; st.rerun()
    with row1_col2:
        if st.button("🔵 BLUE (Voice)", use_container_width=True): st.session_state.page = "blue"; st.rerun()
    with row1_col3:
        if st.button("🟢 GREEN (Secret)", use_container_width=True): st.session_state.page = "green"; st.rerun()
    with row2_col1:
        if st.button("⚫ BLACK (X-Room)", use_container_width=True): st.session_state.page = "black"; st.rerun()
    with row2_col2:
        if st.button("🟣 PURPLE (VIP)", use_container_width=True): st.session_state.page = "purple"; st.rerun()

# รันระบบ
if 'user' in st.session_state:
    render_home()
