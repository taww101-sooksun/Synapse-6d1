import json
import firebase_admin
from firebase_admin import credentials, db
import streamlit as st

# ฟังก์ชันสำหรับเริ่มต้นระบบ Firebase อย่างปลอดภัย
def init_firebase():
    # ตรวจสอบก่อนว่าเคยตั้งค่าแอปไปหรือยัง ถ้ายังไม่เคยให้สร้างใหม่
    if not firebase_admin._apps:
        try:
            # 1. ดึงข้อความ JSON จาก st.secrets
            secret_text = st.secrets["firebase"]["text"]
            
            # 2. แปลงข้อความให้เป็น Dictionary
            cred_dict = json.loads(secret_text)
            
            # 🔥 [แก้บั๊ก จุดที่ 1] บังคับแปลงรหัส \n ใน private_key ให้ถูกต้อง ป้องกัน InvalidPadding
            if "private_key" in cred_dict:
                cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
            
            # 3. โหลดใบรับรอง Credential
            cred = credentials.Certificate(cred_dict)
            
            # 4. สตาร์ทแอปเชื่อมต่อฐานข้อมูล (ใส่ URL ของโปรเจกต์ sooksun-101)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://sooksun-101-default-rtdb.firebaseio.com/' 
            })
            st.success("เชื่อมต่อ Firebase สำเร็จแล้วเพื่อนต๊ะ!")
            
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการโหลดคีย์: {e}")
    else:
        # ถ้าแอปเคยรันไปแล้วให้ไปดึงตัวเดิมมาใช้ ไม่ต้องสตาร์ทใหม่ (ป้องกันแอปดับ)
        firebase_admin.get_app()

# เรียกใช้งานฟังก์ชันจัดการระบบก่อนทำอย่างอื่น
init_firebase()

# --- หลังจากนี้ค่อยเขียนโค้ดหน้าตาแอป ---
st.title("REGISTER AGENT ⚠️")
agent_name = st.text_input("ENTER AGENT NAME", value="Ta101")

if st.button("บันทึกข้อมูล Agent"):
    try:
        # ตัวอย่างการส่งข้อมูลเข้า Firebase Realtime Database
        ref = db.reference("agents")
        ref.child(agent_name).set({
            "status": "Active",
            "slogan": "อยู่นิ่งๆ ไม่เจ็บตัว"
        })
        st.success(f"บันทึกรหัส {agent_name} เข้าฐานข้อมูลเรียบร้อย!")
    except Exception as e:
        st.error(f"ไม่สามารถเข้าถึงฐานข้อมูลคลาวด์ได้: {e}")
