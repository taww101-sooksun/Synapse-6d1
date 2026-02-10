import streamlit as st
import google.generativeai as genai
import numpy as np
import io
from gtts import gTTS

# --- 1. ตั้งค่าดีไซน์ SYNAPSE 6D ---
st.set_page_config(page_title="SYNAPSE 6D Pro", page_icon="💎")
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    h1 { color: #B266FF !important; text-shadow: 2px 2px 4px #000000; }
    .stButton>button { 
        background-color: #00CC99; color: white; border-radius: 20px; 
        width: 100%; font-weight: bold; height: 50px;
    }
    .stTextInput input { background-color: #1E1E1E; color: white; border: 1px solid #B266FF; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ดึง API Key และแก้บั๊ก NotFound ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # ใช้ชื่อรุ่นแบบ Full Path เพื่อป้องกัน Error 'NotFound'
    # หาก gemini-1.5-flash ยังไม่ได้ ให้ลองเปลี่ยนเป็น 'gemini-pro'
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"🚨 ตั้งค่า API ไม่สำเร็จ: {e}")
    st.stop()

# --- 3. หน้าจอ UI ---
st.title("💎 SYNAPSE 6D : ENERGY")
st.subheader("ระบบวิเคราะห์พลังงานและเสียงบำบัด")

user_input = st.text_input("วันนี้คุณรู้สึกอย่างไร?", placeholder="พิมพ์ความรู้สึกของคุณที่นี่...")

if st.button("🚀 ACTIVATE ENERGY"):
    if user_input:
        with st.spinner("ระบบกำลังเชื่อมต่อสมองกล AI..."):
            try:
                # ขั้นตอนที่ 1: ให้ Gemini วิเคราะห์อารมณ์
                prompt = f"จากข้อความ '{user_input}' ช่วยวิเคราะห์อารมณ์และให้กำลังใจสั้นๆ เป็นภาษาไทย 1-2 ประโยค"
                response = model.generate_content(prompt)
                healing_text = response.text

                # ขั้นตอนที่ 2: ใช้ gTTS สร้างเสียงพูด (ฟรีและเสถียร)
                tts = gTTS(text=healing_text, lang='th')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                
                # แสดงผลลัพธ์
                st.markdown("---")
                st.write(f"💬 **AI วิเคราะห์สภาวะคุณ:**")
                st.info(healing_text)
                
                st.write("🎙️ **เสียงบำบัดจากระบบ:**")
                st.audio(audio_fp, format='audio/mp3')
                
                st.success("ปรับจูนพลังงานเรียบร้อยแล้ว")
                
            except Exception as e:
                # ถ้ายัง NotFound อีก จะแจ้งให้เปลี่ยนรุ่นโมเดล
                st.error(f"เกิดข้อผิดพลาด: {e}")
                st.warning("คำแนะนำ: หากขึ้น NotFound ลองเปลี่ยนชื่อโมเดลในโค้ดเป็น 'gemini-pro' ดูครับ")
    else:
        st.warning("กรุณาใส่ข้อมูลความรู้สึกก่อนครับ")

st.caption("🛡️ สโลแกน: อยู่นิ่งๆ ไม่เจ็บตัว | ขับเคลื่อนด้วย Gemini & gTTS")
