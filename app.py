import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage

# ดึงข้อมูลจาก "ตู้เซฟ" (Secrets) ที่คุณใส่ไฟล์ JSON ลงไป
if not firebase_admin._apps:
    cred_dict = dict(st.secrets["firebase_service_account"]) # ชื่อต้องตรงกับที่คุณตั้งใน Secrets
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'storageBucket': f"{cred_dict['project_id']}.appspot.com"
    })

db = firestore.client()
