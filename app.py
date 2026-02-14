import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage

# --- 1. เชื่อมต่อ Firebase ---
if not firebase_admin._apps:
    # ทุกบรรทัดที่อยู่ภายใต้ 'if' ต้องมีย่อหน้าเข้าไปเท่ากันทั้งหมด
    cred_info = dict(st.secrets["firebase_service_account"])
    cred_info["private_key"] = cred_info["private_key"].replace("\\n", "\n")
    cred = credentials.Certificate(cred_info)
    
    # เชื่อมต่อทั้งฐานข้อมูลและที่เก็บไฟล์
    firebase_admin.initialize_app(cred, {
        'storageBucket': st.secrets["firebase_config"]["storageBucket"]
    })

# บรรทัดที่ออกมาอยู่นอก 'if' ต้องกลับมาชิดซ้ายสุด
db = firestore.client()
bucket = storage.bucket(st.secrets["firebase_config"]["storageBucket"])
