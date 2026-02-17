import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- 1. ตั้งค่าการเชื่อมต่อ (Safe Connection) ---
if not firebase_admin._apps:
    try:
        # ดึงข้อมูลจาก st.secrets ที่คุณตั้งค่าไว้
        cred_dict = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"⚠️ เชื่อมต่อ Firebase ไม่สำเร็จ: {e}")
        st.info("ตรวจสอบว่าได้ใส่ค่าใน Settings > Secrets บน Streamlit Cloud หรือยัง?")
        st.stop()

db = firestore.client()

# --- 2. ฟังก์ชันห้องสีแดง (Red Room) ---
def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D; text-align:center;'>🔴 RED PUBLIC FEED</h1>", unsafe_allow_html=True)
    
    if st.button("⬅️ กลับหน้าศูนย์บัญชาการ"):
        st.session_state.page = "home"
        st.rerun()

    # ส่วนโพสต์ใหม่
    with st.expander("📝 สร้างโพสต์ใหม่"):
        with st.form("form_red", clear_on_submit=True):
            msg = st.text_area("เขียนข้อความ...")
            media_url = st.text_input("ลิงก์ YouTube หรือรูปภาพ")
            if st.form_submit_button("🚀 ปล่อยโพสต์"):
                if msg or media_url:
                    db.collection('posts_red').add({
                        'user': st.session_state.user,
                        'text': msg,
                        'media': media_url,
                        'likes': [],
                        'time': datetime.now()
                    })
                    st.success("โพสต์สำเร็จ!")
                    st.rerun()

    st.divider()

    # ส่วนแสดงฟีด (ดึงข้อมูลจริง)
    try:
        posts = db.collection('posts_red').order_by('time', direction='DESCENDING').limit(20).stream()
        for doc in posts:
            p = doc.to_dict()
            pid = doc.id
            
            st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; border:1px solid #444; margin-bottom:10px;">
                    <b style="color:#FFD700;">👤 {p.get('user')}</b>
                    <p>{p.get('text', '')}</p>
                </div>
            """, unsafe_allow_html=True)
            
            m = p.get('media', '')
            if "youtube.com" in m or "youtu.be" in m:
                st.video(m)
            elif m.startswith("http"):
                st.image(m, use_container_width=True)
                
            # ปุ่ม Like
            likes = p.get('likes', [])
            if st.button(f"❤️ {len(likes)}", key=f"like_{pid}"):
                ref = db.collection('posts_red').document(pid)
                if st.session_state.user in likes:
                    ref.update({'likes': firestore.ArrayRemove([st.session_state.user])})
                else:
                    ref.update({'likes': firestore.ArrayUnion([st.session_state.user])})
                st.rerun()
    except Exception as e:
        st.warning("ยังไม่มีโพสต์ในขณะนี้ หรือตั้งค่า Index ใน Firebase ยังไม่เสร็จ")

# --- 3. ส่วนควบคุมแอป ---
if 'user' not in st.session_state:
    # ถ้ายังไม่ Login ให้ไปหน้า Login (โค้ดเก่าที่คุณมี)
    st.title("🛡️ Synapse Login")
    u = st.text_input("Username")
    if st.button("เข้าสู่ระบบ"):
        st.session_state.user = u
        st.session_state.page = "home"
        st.rerun()
else:
    if st.session_state.get('page') == "red":
        render_red_room()
    else:
        # เรียกหน้าหลักที่มีโลโก้และปุ่ม 5 สี
        from your_home_file import render_home # หรือใส่โค้ด render_home() ไว้ที่นี่
        render_home()
