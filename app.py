import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# ป้องกันการ Initialize ซ้ำ
if not firebase_admin._apps:
    try:
        # ดึงค่าจาก Secrets
        cred_info = dict(st.secrets["firebase_service_account"])
        
        # จัดการ Newline (\n) ให้ Firebase SDK อ่านเข้าใจ
        cred_info["private_key"] = cred_info["private_key"].replace("\\n", "\n")
        
        cred = credentials.Certificate(cred_info)
        firebase_admin.initialize_app(cred)
        st.success("🔥 เชื่อมต่อ Firebase สำเร็จ! สบายตัวแล้วครับ")
    except Exception as e:
        st.error(f"❌ โอ๊ะ! ยังติดปัญหาอยู่นิดหน่อย: {e}")

# ตัวแปรสำหรับใช้งานฐานข้อมูล
db = firestore.client()
