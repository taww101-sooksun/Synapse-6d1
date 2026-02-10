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
        width: 100%; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ดึง API Key ของ Gemini (กุญแจซุกซุนที่คุณมีอยู่แล้ว) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("🚨 ระบบหา API Key ไม่เจอใน Secrets!")
    st.stop()

# --- 3. หน้าจอ UI ---
st.title("💎 SYNAPSE 6D : ENERGY")
st.subheader("ระบบวิเคราะห์พลังงานและเสียงบำบัด")

user_input = st.text_input("บอกความรู้สึกของคุณ:", "วันนี้ฉันเหนื่อยนิดหน่อย")

if st.button("🚀 ACTIVATE ENERGY"):
    if user_input:
        with st.spinner("AI กำลังวิเคราะห์สภาวะของคุณ..."):
            # ขั้นตอนที่ 1: ให้ Gemini วิเคราะห์อารมณ์และแต่งคำแนะนำ
            prompt = f"จากข้อความ '{user_input}' ช่วยวิเคราะห์อารมณ์และให้กำลังใจสั้นๆ เป็นภาษาไทย 1-2 ประโยค"
            response = model.generate_content(prompt)
            healing_text = response.text

            # ขั้นตอนที่ 2: ใช้ gTTS สร้างเสียงพูด (ฟรีและนิ่ง)
            try:
                tts = gTTS(text=healing_text, lang='th')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                
                # แสดงผล
                st.info(f"💬 AI วิเคราะห์ว่า: {healing_text}")
                st.audio(audio_fp, format='audio/mp3')
                st.success("ปรับจูนพลังงานเสียงเรียบร้อยแล้ว")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการสร้างเสียง: {e}")
    else:
        st.warning("กรุณาใส่ข้อความก่อนกด Activate ครับ")

st.caption("🛡️ สโลแกน: อยู่นิ่งๆ ไม่เจ็บตัว | ขุมพลัง Gemini + gTTS")
