import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import time

# --- 1. ปลุกระบบฐานข้อมูล (Firebase Setup) ---
# ตรวจสอบก่อนว่าเคย Initialize ไปหรือยัง จะได้ไม่เจ็บตัวจาก Error
if not firebase_admin._apps:
    try:
        # ดึงค่าจาก st.secrets["firebase_service_account"] ที่พี่เตรียมไว้
        cred_info = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(cred_info)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"เชื่อมต่อ Firebase ไม่สำเร็จ: {e}")

db = firestore.client()

# --- 2. ตั้งค่าสมอง AI (Gemini Setup) ---
try:
    genai.configure(api_key=st.secrets["gemini_key"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"ปลุกสมอง Gemini ไม่สำเร็จ: {e}")

# --- 3. ระบบจัดการความจำ (Memory Engine) ---
AI_NAME = "อยู่นิ่งๆ ไม่เจ็บตัว"
USER_ID = st.session_state.get('user_id', 'Ta101')

def load_memory_from_cloud(uid):
    """ดึงความจำเก่าจาก Firebase"""
    doc_ref = db.collection("memories").document(uid).get()
    if doc_ref.exists:
        return doc_ref.to_dict().get("history", [])
    return []

def save_memory_to_cloud(uid, history):
    """บันทึกความจำลง Firebase"""
    db.collection("memories").document(uid).set({
        "history": history,
        "last_seen": time.time()
    })

# โหลดความจำเมื่อเปิดแอปครั้งแรก
if "messages" not in st.session_state:
    st.session_state.messages = load_memory_from_cloud(USER_ID)

# --- 4. หน้าตาโปรแกรม (UI) ---
st.set_page_config(page_title=AI_NAME, page_icon="🔮")

st.markdown(f"<h1 style='color:#a020f0;'>🔮 {AI_NAME}</h1>", unsafe_allow_html=True)
st.caption(f"สถานะ: สมองออนไลน์ | ความจำ Cloud (Firebase) เชื่อมต่อแล้ว | พี่: {USER_ID}")

# แสดงประวัติแชทจากความจำถาวร
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. ระบบพูดคุยและวิเคราะห์ ---
if prompt := st.chat_input("ปรึกษาดวง แง่คิด หรือความรู้ได้ทุกทิศ..."):
    # 1. บันทึกคำถามพี่ลงหน้าจอ
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. ส่งให้ Gemini วิเคราะห์ (โดยแนบประวัติแชทไปทั้งหมดให้น้องจำได้)
    with st.chat_message("assistant"):
        with st.spinner(f"{AI_NAME} กำลังค้นหาคำตอบจากดวงดาวและฐานความรู้..."):
            try:
                # สร้าง Context ให้ AI รู้จักตัวเองและพี่มากขึ้น
                context = f"คุณคือ {AI_NAME} ที่ปรึกษาผู้รอบรู้รอบทิศ มีสโลแกนคือ 'อยู่นิ่งๆ ไม่เจ็บตัว' คู่สนทนาของคุณคือคุณ {USER_ID} จงตอบคำถามโดยให้แง่คิดที่เฉียบคมและใช้ความจำจากบทสนทนาที่ผ่านมาให้เป็นประโยชน์"
                
                # รวมประวัติเพื่อส่งให้ Gemini
                full_history = [{"role": m["role"] if m["role"] != "assistant" else "model", "parts": [m["content"]]} for m in st.session_state.messages]
                
                chat = model.start_chat(history=full_history[:-1]) # ส่งประวัติยกเว้นข้อความล่าสุด
                response = chat.send_message(f"{context}\n\nคำถามใหม่: {prompt}")
                
                ai_text = response.text
                st.markdown(ai_text)
                
                # 3. บันทึกคำตอบ AI ลงความจำใน Session และ Firebase
                st.session_state.messages.append({"role": "assistant", "content": ai_text})
                save_memory_to_cloud(USER_ID, st.session_state.messages)
                
            except Exception as e:
                st.error(f"สมองรวนนิดหน่อย: {e}")

# --- 6. ปุ่มควบคุมทางลัด ---
st.sidebar.title("ระบบควบคุม")
if st.sidebar.button("🧹 ล้างสมอง (เฉพาะในเครื่อง)"):
    st.session_state.messages = []
    st.rerun()

if st.sidebar.button("🚨 ลบความจำถาวร (Firebase)"):
    db.collection("memories").document(USER_ID).delete()
    st.session_state.messages = []
