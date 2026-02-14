import streamlit as st
import firebase_admin  # <--- ต้องมีบรรทัดนี้แบบเต็มๆ ด้วย
from firebase_admin import credentials, firestore, storage

# --- 1. เชื่อมต่อ Firebase ---
if not firebase_admin._apps:  # บรรทัดนี้จะเลิก Error ทันที
    # ... code ส่วนที่เหลือ ...
# --- 1. เชื่อมต่อ Firebase ---
if not firebase_admin._apps:
    # ดึงค่าจาก Secrets
    service_account_info = st.secrets["firebase_service_account"]
    
    # สร้าง Credentials โดยตรงจาก Dictionary (Streamlit จัดการเรื่อง \n ให้เองในระดับหนึ่ง)
    # แต่ถ้ายังมีปัญหาเรื่องคีย์ ให้ใช้ dict() ครอบตามเดิมได้ครับ
    cred = credentials.Certificate(dict(service_account_info))
    
    # ดึงชื่อ Bucket มาเตรียมไว้
    bucket_name = st.secrets["firebase_config"]["storageBucket"]
    
    # เชื่อมต่อแอป
    firebase_admin.initialize_app(cred, {
        'storageBucket': bucket_name
    })

# ประกาศตัวแปรใช้งาน
db = firestore.client()
# ระบุชื่อ bucket ย้ำลงไปในฟังก์ชันเพื่อความชัวร์
bucket = storage.bucket(st.secrets["firebase_config"]["storageBucket"])
