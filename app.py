import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime

# --- 1. เชื่อมต่อ Firebase ---
if not firebase_admin._apps:
    try:
        cred_info = dict(st.secrets["firebase_service_account"])
        if "\\n" in cred_info["private_key"]:
            cred_info["private_key"] = cred_info["private_key"].replace("\\n", "\n")
        
        cred = credentials.Certificate(cred_info)
        firebase_admin.initialize_app(cred, {
            'storageBucket': st.secrets["firebase_config"]["storageBucket"]
        })
    except Exception as e:
        st.error(f"การเชื่อมต่อล้มเหลว: {e}")

db = firestore.client()
bucket = storage.bucket(st.secrets["firebase_config"]["storageBucket"])

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
        .post-card {{ 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 15px; 
            border: 1px solid rgba(255,255,255,0.2); 
            margin-bottom: 20px; 
        }}
        img {{ border-radius: 10px; margin-top: 10px; }}
        </style>
    """, unsafe_allow_html=True)

# --- 3. ระบบล็อกอิน ---
if 'user' not in st.session_state:
    apply_style("ดำเงา")
    st.title("📱 Notty-101 Login")
    phone = st.text_input("ใส่เบอร์โทรของคุณ:")
    if st.button("เข้าสู่ระบบ"):
        if len(phone) >= 10:
            st.session_state.user = phone
            st.rerun()
else:
    # --- 4. เมนูเลือกห้อง ---
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

    room = st.session_state.room
    color_map = {'main':'ดำเงา', 'red':'แดงเงา', 'blue':'น้ำเงินเงา', 'green':'เขียวเงา', 'purple':'ม่วงเงา'}
    apply_style(color_map[room])

    if room == 'main':
        st.title("🏠 หน้าหลัก")
        st.write("เลือกห้องสีด้านข้างเพื่อดูฟีด")
    else:
        st.title(f"🖼️ ฟีดห้อง{color_map[room]}")
        
        # --- 5. ส่วนโพสต์ (ข้อความ + รูปภาพ) ---
        with st.expander("📝 สร้างโพสต์ใหม่ (ใส่รูปได้)"):
            msg = st.text_area("เขียนข้อความ...")
            uploaded_file = st.file_uploader("เลือกรูปภาพ...", type=["jpg", "jpeg", "png"])
            
            if st.button("โพสต์"):
                if msg or uploaded_file:
                    image_url = None
                    # ถ้ามีการอัปโหลดรูป
                    if uploaded_file:
                        with st.spinner('กำลังอัปโหลดรูปภาพ...'):
                            file_path = f"posts/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
                            blob = bucket.blob(file_path)
                            blob.upload_from_string(uploaded_file.read(), content_type=uploaded_file.type)
                            blob.make_public()
                            image_url = blob.public_url
                    
                    # บันทึกข้อมูลลง Firestore
                    db.collection(f"feed_{room}").add({
                        "user": st.session_state.user,
                        "text": msg,
                        "image": image_url,
                        "time": firestore.SERVER_TIMESTAMP
                    })
                    st.success("โพสต์เรียบร้อย!")
                    st.rerun()

        # --- 6. ส่วนแสดงฟีด ---
        posts = db.collection(f"feed_{room}").order_by("time", direction=firestore.Query.DESCENDING).stream()
        for p in posts:
            d = p.to_dict()
            with st.container():
                st.markdown(f'<div class="post-card">', unsafe_allow_html=True)
                st.write(f"👤 **{d.get('user')}**")
                if d.get('text'):
                    st.write(d.get('text'))
                if d.get('image'):
                    st.image(d.get('image'), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
