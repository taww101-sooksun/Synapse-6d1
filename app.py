import streamlit as st

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="Social App Demo", page_icon="📱")

# --- CSS เพื่อแต่งสีตามธีม (Inject CSS) ---
def local_css(color_code):
    st.markdown(f"""
    <style>
    .stButton>button {{
        color: white;
        background-color: {color_code};
        border-color: {color_code};
    }}
    div[data-testid="stMetricValue"] {{
        color: {color_code};
    }}
    h1, h2, h3 {{
        color: {color_code} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ส่วนจัดการ State (จำค่า Login, Like, Follow) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'phone_number' not in st.session_state:
    st.session_state.phone_number = ""
# สร้างตัวแปรเก็บสถานะติดตามของแต่ละสี
for color in ['Red', 'Blue', 'Green', 'Black']:
    if f'follow_{color}' not in st.session_state:
        st.session_state[f'follow_{color}'] = False

# --- 1. หน้า Login ---
if not st.session_state.logged_in:
    st.title("🔒 เข้าสู่ระบบ")
    
    phone = st.text_input("กรอกเบอร์โทรศัพท์", placeholder="08x-xxx-xxxx")
    
    if st.button("ขอรหัส OTP เพื่อเข้าใช้งาน"):
        if phone:
            st.session_state.phone_number = phone
            st.session_state.logged_in = True
            st.rerun() # รีเฟรชหน้าเพื่อเข้าหน้าหลัก
        else:
            st.warning("กรุณากรอกเบอร์โทรศัพท์")
            
    st.markdown("---")
    st.caption('"อยู่นิ่งๆ ไม่เจ็บตัว"') # สโลแกนของคุณ

# --- 2. หน้าหลัก (หลังจาก Login แล้ว) ---
else:
    st.sidebar.success(f"ผู้ใช้งาน: {st.session_state.phone_number}")
    if st.sidebar.button("ออกจากระบบ"):
        st.session_state.logged_in = False
        st.rerun()

    # สร้าง 4 แท็บ ตามสีที่ขอ
    tab1, tab2, tab3, tab4 = st.tabs(["🔴 แดง", "🔵 น้ำเงิน", "🟢 เขียว", "⚫ ดำ"])

    # ฟังก์ชันสำหรับวาดหน้าจอของแต่ละสี
    def draw_page(color_name, theme_color_hex, icon):
        # ใส่สีให้ปุ่มและหัวข้อเฉพาะในส่วนนี้
        local_css(theme_color_hex)
        
        st.header(f"{icon} หน้าสี{color_name}")
        
        # พื้นที่จำลอง Video/Image
        st.image("https://placehold.co/600x400/EEE/31343C?text=VIDEO+CONTENT", caption=f"วิดีโอ/รูปภาพ โซนสี{color_name}")

        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        
        with col1:
            if st.button(f"👍 Like", key=f"like_{color_name}"):
                st.toast(f"คุณถูกใจโพสต์ในโซนสี{color_name}!")

        with col2:
            if st.button(f"↗️ Share", key=f"share_{color_name}"):
                st.toast("แชร์เรียบร้อยแล้ว!")
        
        with col3:
            # ปุ่มติดตาม (เช็คสถานะว่ากดไปหรือยัง)
            is_following = st.session_state[f'follow_{color_name}']
            btn_text = "ติดตามแล้ว" if is_following else "ติดตาม"
            
            if st.button(btn_text, key=f"btn_follow_{color_name}"):
                st.session_state[f'follow_{color_name}'] = not st.session_state[f'follow_{color_name}']
                st.rerun()

        st.text_area("💬 พิมพ์ใจความของคุณ...", key=f"comment_{color_name}")
        st.info(f"คุณกำลังอยู่ในโซน: **{color_name} Zone**")

    # --- เรียกใช้งานแต่ละแท็บ ---
    with tab1:
        draw_page("Red", "#FF4B4B", "🔥") # สีแดง Streamlit

    with tab2:
        draw_page("Blue", "#1E90FF", "💧") # สีน้ำเงิน

    with tab3:
        draw_page("Green", "#2E8B57", "🌿") # สีเขียว

    with tab4:
        draw_page("Black", "#000000", "🌙") # สีดำ
