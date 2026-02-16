import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components

# --- 1. การเชื่อมต่อ Firebase ---
if not firebase_admin._apps:
    try:
        cred_info = dict(st.secrets["firebase_service_account"])
        if "\\n" in cred_info["private_key"]:
            cred_info["private_key"] = cred_info["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(cred_info)
        firebase_admin.initialize_app(cred, {'storageBucket': st.secrets["firebase_config"]["storageBucket"]})
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

db = firestore.client()
bucket = storage.bucket()

# --- 2. ฟังก์ชันจัดการธีม (ปรับสีเข้มขึ้นตามสั่ง) ---
def get_thai_time():
    return datetime.utcnow() + timedelta(hours=7)

def set_room_theme(room_id):
    themes = {
        "home":  {
            # ปรับสีหน้าหลักให้เข้มและชัดเจนขึ้น (Darker Gradient)
            "bg": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)", 
            "text": "#E0E0E0", 
            "accent": "#00d2ff"
        },
        "red":   {"bg": "linear-gradient(180deg, #660000, #990000)", "text": "#FFFFFF", "accent": "#FF0000"},
        "blue":  {"bg": "linear-gradient(180deg, #000033, #000066)", "text": "#FFFFFF", "accent": "#0084FF"},
        "green": {"bg": "linear-gradient(180deg, #003300, #006600)", "text": "#FFFFFF", "accent": "#25D366"},
        "black": {"bg": "linear-gradient(180deg, #000000, #1a1a1a)", "text": "#FFFFFF", "accent": "#555555"}
    }
    cfg = themes.get(room_id, themes["home"])
    st.markdown(f"""
        <style>
        .stApp {{ background: {cfg['bg']}; color: {cfg['text']}; }}
        h1, h2, h3, p, span, label, .stMarkdown {{ color: {cfg['text']} !important; }}
        .post-box {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px; border-radius: 15px; margin-bottom: 20px;
        }}
        .stButton>button {{
            background-color: {cfg['accent']}; color: white !important;
            border-radius: 20px; font-weight: bold; width: 100%;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 3. ระบบหลักของแต่ละห้อง ---
def render_social_room(room_id, room_name):
    set_room_theme(room_id)
    st.title(f"🚀 {room_name} Room")
    # ... (ส่วนการแสดงโพสต์และไลค์เหมือนเดิมที่คุณท่านมี) ...

# --- 4. การประมวลผลหน้าจอ ---
if 'user' not in st.session_state:
    set_room_theme("home")
    st.title("🛡️ เข้าสู่ระบบ")
    u_name = st.text_input("ระบุชื่อผู้ใช้")
    if st.button("ตกลง"):
        if u_name:
            st.session_state.user = u_name
            db.collection('users').document(u_name).set({'last_active': get_thai_time()}, merge=True)
            st.rerun()
else:
    with st.sidebar:
        st.header(f"👤 {st.session_state.user}")
        menu = st.radio("เลือกเมนู", ["หน้าหลัก", "YouTube (Red)", "Facebook (Blue)", "Line (Green)", "X (Black)"])
        if st.button("ออกจากระบบ"):
            del st.session_state.user
            st.rerun()

    if menu == "หน้าหลัก":
        set_room_theme("home")
        
        # แสดงโลโก้
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try: st.image("logo.jpg", use_container_width=True)
            except: st.warning("กรุณาตรวจสอบไฟล์ logo.jpg")

        st.markdown("<h1 style='text-align: center;'>Firebase Social 2026</h1>", unsafe_allow_html=True)
        
        # --- ฝัง Playlist YouTube (ใส่เพิ่มให้ตามคำขอ) ---
        st.subheader("🎵 เพลย์ลิสต์พิเศษสำหรับคุณ")
        st.video("https://youtube.com/playlist?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO&si=BGiqmOiqhccE7538")
        
        st.markdown("---")
        
        # --- คำบรรยายการใช้งานแต่ละห้อง ---
        st.subheader("📖 คู่มือการใช้งานแต่ละห้อง")
        with st.container():
            st.markdown("""
            * 🔴 **YouTube Room:** พื้นที่แบ่งปันวิดีโอที่คุณชื่นชอบ พูดคุยและคอมเมนต์แลกเปลี่ยนมุมมองกับเพื่อนๆ
            * 🔵 **Facebook Room:** ห้องสื่อสารเต็มรูปแบบ **รองรับการโทรฟรี** และวิดีโอคอลแบบ Peer-to-Peer
            * 🟢 **Line Room:** เน้นการส่งต่อความรู้สึกผ่านรูปภาพและข้อความที่รวดเร็ว ในบรรยากาศสบายๆ
            * ⚫ **X (Black) Room:** พื้นที่สำหรับข่าวสารที่กระชับ รวดเร็ว และทันเหตุการณ์
            """)
            
        st.info("💡 **เคล็ดลับ:** หากต้องการโทรหาเพื่อน ให้ไปที่ห้อง Facebook แล้วเลือกชื่อเพื่อนจากรายการได้ทันทีครับ!")

    else:
        mapping = {"YouTube (Red)": ("red", "YouTube"), "Facebook (Blue)": ("blue", "Facebook"), 
                   "Line (Green)": ("green", "Line"), "X (Black)": ("black", "X")}
        render_social_room(*mapping[menu])
