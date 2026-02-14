import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage

# --- 1. เชื่อมต่อ Firebase ---
# ตรวจสอบว่ามีการเชื่อมต่ออยู่แล้วหรือไม่เพื่อป้องกัน Error
if not firebase_admin._apps:
    try:
        # ดึงข้อมูลจาก Streamlit Secrets
        cred_info = dict(st.secrets["firebase_service_account"])
        
        # จัดการเรื่องตัวอักษรขึ้นบรรทัดใหม่ใน Private Key
        if "\\n" in cred_info["private_key"]:
            cred_info["private_key"] = cred_info["private_key"].replace("\\n", "\n")
        
        cred = credentials.Certificate(cred_info)
        
        # เชื่อมต่อ Firebase พร้อมระบุ Storage Bucket
        firebase_admin.initialize_app(cred, {
            'storageBucket': st.secrets["firebase_config"]["storageBucket"]
        })
    except Exception as e:
        st.error(f"ไม่สามารถเชื่อมต่อ Firebase ได้: {e}")

# เรียกใช้งาน Client
try:
    db = firestore.client()
    # ระบุชื่อ bucket โดยตรงเพื่อให้มั่นใจว่าหาเจอ
    bucket = storage.bucket(st.secrets["firebase_config"]["storageBucket"])
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลด Service: {e}")

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
            padding: 15px; 
            border-radius: 15px; 
            border: 1px solid rgba(255,255,255,0.2); 
            margin-bottom: 20px; 
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 3. ระบบล็อกอินด้วยเบอร์ ---
if 'user' not in st.session_state:
    apply_style("ดำเงา")
    st.title("📱 Notty-101 Login")
    phone = st.text_input("ใส่เบอร์โทรของคุณ:", placeholder="08xxxxxxxx")
    if st.button("เข้าสู่ระบบ"):
        if len(phone) >= 10:
            st.session_state.user = phone
            st.rerun()
        else:
            st.warning("กรุณาใส่เบอร์โทรให้ถูกต้อง")
else:
    # --- 4. เมนูเลือกห้องหน้าหลัก ---
    if 'room' not in st.session_state:
        st.session_state.room = 'main'

    with st.sidebar:
        st.write(f"👤 ผู้ใช้งาน: **{st.session_state.user}**")
        st.divider()
        if st.button("🏠 หน้าหลัก"): st.session_state.room = 'main'
        if st.button("🔴 ห้องแดง"): st.session_state.room = 'red'
        if st.button("🔵 ห้องน้ำเงิน"): st.session_state.room = 'blue'
        if st.button("🟢 ห้องเขียว"): st.session_state.room = 'green'
        if st.button("🟣 ห้องม่วง"): st.session_state.room = 'purple'
        st.divider()
        if st.button("🚪 ออกจากระบบ"): 
            del st.session_state.user
            st.rerun()

    # --- 5. แสดงผลตามห้อง ---
    room = st.session_state.room
    color_map = {
        'main': 'ดำเงา', 
        'red': 'แดงเงา', 
        'blue': 'น้ำเงินเงา', 
        'green': 'เขียวเงา', 
        'purple': 'ม่วงเงา'
    }
    apply_style(color_map[room])

    if room == 'main':
        st.title("🏠 ยินดีต้อนรับสู่เมนูหลัก")
        st.subheader(f"สวัสดีครับคุณ {st.session_state.user}")
        st.write("เลือกห้องสีด้านข้างเพื่อเริ่มเลื่อนฟีดครับ")
    else:
        st.title(f"🖼️ ฟีดห้อง{color_map[room]}")
        
        # ส่วนโพสต์ข้อความ
        with st.expander("📝 สร้างโพสต์ใหม่"):
            msg = st.text_area("เขียนข้อความ...", height=100)
            if st.button("ส่งโพสต์"):
                if msg:
                    try:
                        db.collection(f"feed_{room}").add({
                            "user": st.session_state.user,
                            "text": msg,
                            "time": firestore.SERVER_TIMESTAMP
                        })
                        st.success("โพสต์สำเร็จ!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"โพสต์ไม่สำเร็จ: {e}")

        # ส่วนแสดงฟีด (เลื่อนดูโพสต์)
        try:
            posts = db.collection(f"feed_{room}").order_by("time", direction=firestore.Query.DESCENDING).stream()
            
            count = 0
            for p in posts:
                d = p.to_dict()
                st.markdown(f"""
                <div class="post-card">
                    <small style="color: #ccc;">👤 {d.get('user', 'ไม่ระบุตัวตน')}</small>
                    <p style="font-size:1.1rem; margin-top: 10px;">{d.get('text', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                count += 1
            
            if count == 0:
                st.info("ยังไม่มีโพสต์ในห้องนี้ เริ่มเขียนเป็นคนแรกเลย!")
        except Exception as e:
            st.error(f"โหลดฟีดไม่ได้: {e}")
