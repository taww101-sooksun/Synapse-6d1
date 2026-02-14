import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage

# --- 1. เชื่อมต่อ Firebase ---
if not firebase_admin._apps:
    cred_info = dict(st.secrets["firebase_service_account"])
    cred_info["private_key"] = cred_info["private_key"].replace("\\n", "\n")
    cred = credentials.Certificate(cred_info)
    # เชื่อมต่อทั้งฐานข้อมูลและที่เก็บไฟล์
    firebase_admin.initialize_app(cred, {
        'storageBucket': st.secrets["firebase_config"]["storageBucket"]
    })

db = firestore.client()
bucket = storage.bucket()

# --- 2. ฟังก์ชันตกแต่งสีเงา ---
def apply_style(color_name):
    gradients = {
        "แดงเงา": "linear-gradient(180deg, #ff4b4b, #600000)",
        "น้ำเงินเงา": "linear-gradient(180deg, #1e90ff, #000040)",
        "เขียวเงา": "linear-gradient(180deg, #32cd32, #003000)",
        "ม่วงเงา": "linear-gradient(180deg, #da70d6, #300040)",
        "ดำเงา": "linear-gradient(180deg, #404040, #000000)"
    }
    st.markdown(f"""
        <style>
        .stApp {{ background: {gradients[color_name]}; color: white; }}
        h1, h2, h3, p, label {{ color: white !important; }}
        .post-card {{ background: rgba(255,255,255,0.1); padding: 15px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.2); margin-bottom: 20px; }}
        </style>
    """, unsafe_allow_html=True)

# --- 3. ระบบล็อกอินด้วยเบอร์ ---
if 'user' not in st.session_state:
    apply_style("ดำเงา")
    st.title("📱 Notty-101 Login")
    phone = st.text_input("ใส่เบอร์โทรของคุณ:")
    if st.button("เข้าสู่ระบบ"):
        if len(phone) >= 10:
            st.session_state.user = phone
            st.rerun()
else:
    # --- 4. เมนูเลือกห้องหน้าหลัก ---
    if 'room' not in st.session_state:
        st.session_state.room = 'main'

    with st.sidebar:
        st.write(f"👤 {st.session_state.user}")
        if st.button("🏠 หน้าหลัก"): st.session_state.room = 'main'
        if st.button("🔴 ห้องแดง"): st.session_state.room = 'red'
        if st.button("🔵 ห้องน้ำเงิน"): st.session_state.room = 'blue'
        if st.button("🟢 ห้องเขียว"): st.session_state.room = 'green'
        if st.button("🟣 ห้องม่วง"): st.session_state.room = 'purple'
        if st.button("🚪 ออกจากระบบ"): 
            del st.session_state.user
            st.rerun()

    # --- 5. แสดงผลตามห้อง ---
    room = st.session_state.room
    color_titles = {'main':'ดำเงา', 'red':'แดงเงา', 'blue':'น้ำเงินเงา', 'green':'เขียวเงา', 'purple':'ม่วงเงา'}
    apply_style(color_titles[room])

    if room == 'main':
        st.title("🏠 ยินดีต้อนรับสู่เมนูหลัก")
        st.write("เลือกห้องสีด้านข้างเพื่อเริ่มเลื่อนฟีดครับ")
    else:
        st.title(f"🖼️ ฟีดห้อง{color_titles[room]}")
        
        # ส่วนโพสต์
        with st.expander("📝 สร้างโพสต์ใหม่"):
            msg = st.text_area("เขียนข้อความ...")
            if st.button("โพสต์"):
                if msg:
                    db.collection(f"feed_{room}").add({
                        "user": st.session_state.user,
                        "text": msg,
                        "time": firestore.SERVER_TIMESTAMP
                    })
                    st.success("โพสต์ติดแล้ว!")
                    st.rerun()

        # ส่วนเลื่อนฟีด
        posts = db.collection(f"feed_{room}").order_by("time", direction=firestore.Query.DESCENDING).stream()
        for p in posts:
            d = p.to_dict()
            st.markdown(f"""<div class="post-card">
                <small>👤 {d.get('user')}</small>
                <p style="font-size:1.2rem;">{d.get('text')}</p>
            </div>""", unsafe_allow_html=True)
