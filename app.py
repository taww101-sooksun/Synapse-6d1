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
    
    # --- คุณสามารถเขียนโค้ดต่อจากบรรทัดนี้ได้เลย ---
    st.write("พร้อมใช้งานฐานข้อมูล Notty-101 แล้วครับ")
