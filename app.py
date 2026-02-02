import streamlit as st
import google.generativeai as genai
import numpy as np

# --- 1. ตั้งค่าดีไซน์ตามโลโก้ SYNAPSE ---
st.set_page_config(page_title="SYNAPSE 6D Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .lyrics-board {
        background-color: #1E1E1E; padding: 20px; border-radius: 15px; 
        border: 1px solid #00CC99; color: #00FFCC; min-height: 150px;
        font-family: 'monospace';
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ตั้งค่า AI (อย่าลืมใส่ Key ของคุณพ่อนะครับ) ---
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. หน้าจอหลัก ---
st.title("💎 SYNAPSE : STAY STILL & HEAL")
st.write("สโลแกน: **'อยู่นิ่งๆ ไม่เจ็บตัว'**") [cite: 2025-12-20]

col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 ระบบออมเงิน (Budget 300.-)")
    spent = st.number_input("วันนี้ใช้ไปเท่าไหร่?", min_value=0)
    if spent > 300:
        st.error(f"เกินงบ! จ่ายเกินไป {spent-300} บาท")
    else:
        st.success(f"ยังนิ่งอยู่! เหลือเงิน {300-spent} บาท") [cite: 2025-12-20]

    st.write("---")
    st.subheader("📺 ความบันเทิง (YouTube)")
    yt_url = st.text_input("วางลิงก์ YouTube ที่คุณพ่อชอบที่นี่:", "https://www.youtube.com/watch?v=Rvmvt7gscIM")
    if yt_url:
        st.video(yt_url) # แสดงวิดีโอในแอปเลย [cite: 2025-12-20]

with col2:
    st.subheader("🧘 กระดานขยี้ใจความ (5-6 บรรทัด)")
    note = st.text_area("ใส่ใจความสั้นๆ:")
    
    if st.button("🚀 GENERATE (ขยี้ใจความ)"):
        if note:
            with st.spinner("กำลังขยี้..."):
                # สั่ง AI ขยี้สั้นๆ 5-6 บรรทัดตามสั่ง [cite: 2025-12-20]
                prompt = f"ขยี้ข้อความ '{note}' เป็นคำคมบำบัดให้กำลังใจ 5-6 บรรทัด มีคำว่า 'อยู่นิ่งๆ ไม่เจ็บตัว' ด้วย" [cite: 2025-12-20]
                response = model.generate_content(prompt)
                
                st.markdown(f"""
                    <div class="lyrics-board">
                        {response.text}
                    </div>
                """, unsafe_allow_html=True)
                st.balloons() # ฉลองความสำเร็จแบบนิ่งๆ [cite: 2025-12-20]
