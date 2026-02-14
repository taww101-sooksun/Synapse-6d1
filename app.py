import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. ฟังก์ชันเชื่อมต่อ Firebase
def init_firebase():
    if not firebase_admin._apps:
        try:
            # ดึงค่าจาก Secrets
            cred_info = dict(st.secrets["firebase_service_account"])
            
            # แก้ไขเรื่องเครื่องหมายขึ้นบรรทัดใหม่ (\n) ในรหัสลับ
            cred_info["private_key"] = cred_info["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(cred_info)
            firebase_admin.initialize_app(cred)
            return True
        except Exception as e:
            st.error(f"❌ เชื่อมต่อไม่สำเร็จ: {e}")
            return False
    return True

# 2. เริ่มทำงาน
if init_firebase():
    st.success("✅ ยินดีด้วย! แอปเชื่อมต่อ Firebase สำเร็จแล้ว")
    db = firestore.client()
    # --- โค้ดสำหรับลองเพิ่มข้อมูล ---
st.divider()
st.subheader("📝 ทดลองบันทึกข้อมูล")

# สร้างช่องกรอกชื่อ
name_input = st.text_input("พิมพ์ชื่อที่คุณต้องการบันทึก:")

if st.button("บันทึกข้อมูล"):
    if name_input:
        # บันทึกลง Collection ชื่อ 'test_users'
        db.collection("test_users").add({
            "name": name_input,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        st.balloons()
        st.success(f"บันทึกชื่อ '{name_input}' เรียบร้อยแล้ว!")
    else:
        st.warning("กรุณาพิมพ์ชื่อก่อนกดบันทึกนะครับ")

# --- โค้ดสำหรับดึงข้อมูลมาโชว์ ---
st.divider()
st.subheader("📊 ข้อมูลทั้งหมดในฐานข้อมูล")

users_ref = db.collection("test_users").order_by("timestamp", direction=firestore.Query.DESCENDING)
docs = users_ref.stream()

for doc in docs:
    user_data = doc.to_dict()
    st.write(f"🔹 {user_data.get('name')} (เมื่อ: {user_data.get('timestamp')})")

    
    # --- คุณสามารถเขียนโค้ดต่อจากบรรทัดนี้ได้เลย ---
    st.write("พร้อมใช้งานฐานข้อมูล Notty-101 แล้วครับ")
