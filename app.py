import numpy as np
import streamlit as st
import google.generativeai as genai
import json
import time

# --- 1. ตั้งค่าดีไซน์ตามโลโก้ (ม่วง-ดำ-เขียวมินต์) ---
st.set_page_config(page_title="SYNAPSE 6D Pro", page_icon="💎", layout="centered")

# CSS สำหรับปรับจูนหน้าตาให้ Pro ตามสไตล์คุณ
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; } 
    h1, h2, h3 { color: #B266FF !important; text-shadow: 2px 2px 4px #000000; }
    .stMetric { background-color: #1E1E1E; border-radius: 10px; padding: 15px; border: 1px solid #B266FF; }
    .stButton>button { 
        background-color: #00CC99; 
        color: white; border-radius: 25px; width: 100%; font-weight: bold; height: 50px;
        box-shadow: 0px 4px 15px rgba(0, 204, 153, 0.3);
    }
    .stTextArea textarea { background-color: #1E1E1E; color: white; border: 1px solid #B266FF; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ตั้งค่าระบบ AI (ดึงผ่าน Secrets เพื่อความปลอดภัย) ---
try:
    # ดึงค่าจาก Streamlit Secrets ที่คุณตั้งไว้ (กุญแจซุกซุน-101)
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("🚨 ระบบหา API Key ไม่เจอ! กรุณาตั้งค่าใน Streamlit Secrets ก่อนนะครับ")
    st.stop()

# --- 3. ระบบวิเคราะห์และสร้างเสียงบำบัด ---
class UltimateAIsystem:
    def analyze_emotion(self, text):
        """วิเคราะห์อารมณ์และแปลงเป็นค่า Matrix"""
        try:
            # สั่งให้ Gemini วิเคราะห์เป็น JSON เพื่อเอาไปคำนวณต่อ
            prompt = f"""
            วิเคราะห์อารมณ์จากข้อความ: '{text}' 
            ตอบเป็น JSON รูปแบบนี้เท่านั้น: 
            {{'v': 0.0-1.0, 'a': 0.0-1.0, 'chords': 'ชื่อคอร์ดที่เข้ากับอารมณ์'}}
            """
            response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            return json.loads(response.text)
        except:
            # ถ้า AI พลาด ให้ใช้ค่ามาตรฐาน (Safe Mode)
            return {"v": 0.5, "a": 0.5, "chords": "Cmaj7, Gmaj7"}

    def synthesize_sound(self, v):
        """สร้างคลื่นเสียง 432Hz เพื่อปรับสมดุลพลังงาน"""
        t = np.linspace(0, 5, 44100 * 5)
        # ใช้ 432Hz เป็นฐาน และเปลี่ยนตามค่าความสุข (v)
        base_freq = 432 * (0.5 + v)
        wave = 0.4 * np.sin(2 * np.pi * base_freq * t) 
        
        # ใส่ Envelope ป้องกันเสียงกระชาก (Fade in/out)
        envelope = np.ones_like(t)
        fade = 44100 // 2
        envelope[:fade] = np.linspace(0, 1, fade)
        envelope[-fade:] = np.linspace(1, 0, fade)
        
        return (np.clip(wave * envelope, -0.9, 0.9) * 32767).astype(np.int16)

# --- 4. หน้าจอใช้งาน (UI) ---
st.title("💎 SYNAPSE : 6D ENERGY PRO")
st.subheader("ระบบปรับจูนพลังงานระดับเซลล์ของคุณ")

system = UltimateAIsystem()
user_input = st.text_area("บอกความรู้สึกของคุณวันนี้ให้ระบบรับรู้:", placeholder="เช่น เหนื่อย ล้า หรือต้องการพลังงาน...")

if st.button("🚀 ACTIVATE ENERGY (เริ่มการบำบัด)"):
    if user_input:
        with st.spinner("ระบบกำลังคำนวณ Matrix และปรับจูนคลื่นความถี่..."):
            # 1. AI วิเคราะห์อารมณ์
            data = system.analyze_emotion(user_input)
            
            # 2. สร้างเสียงบำบัดจากค่าที่วิเคราะห์ได้
            audio = system.synthesize_sound(data['v'])
            time.sleep(1.5) # หน่วงเวลาให้ดูสมจริง
            
            # 3. แสดงผลลัพธ์
            st.subheader(f"🎨 สภาวะพลังงานปัจจุบัน (Intensity: {data.get('v', 0.5)})")
            c1, c2 = st.columns(2)
            c1.metric("ความสว่างเซลล์ (Light)", f"{data.get('v', 0.5)*100:.1f}%")
            c2.metric("ความเข้มข้น (Contrast)", f"{data.get('a', 0.5)*100:.1f}%")
            
            st.subheader(f"🔊 เสียงบำบัดพลังงาน: {data.get('chords', 'Healing Waves')}")
            st.audio(audio, format='audio/wav', sample_rate=44100)
            
            st.success("ปรับจูนพลังงานเรียบร้อยแล้ว ยินดีด้วยครับ")
            st.markdown(f"---")
            st.caption(f"🛡️ สโลแกนของคุณ: **อยู่นิ่งๆ ไม่เจ็บตัว**")
    else:
        st.warning("กรุณากรอกความรู้สึกก่อนกดปุ่ม ACTIVATE นะครับ")
