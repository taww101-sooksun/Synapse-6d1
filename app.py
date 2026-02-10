import streamlit as st
import google.generativeai as genai

# --- 1. ตั้งค่า API Key จาก Secrets ---
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("❌ ไม่พบ API Key! กรุณาตั้งค่าใน Secrets (GEMINI_API_KEY)")
    st.stop()

# --- 2. การตกแต่ง UI ให้ดูแน่นและเข้มสะใจ ---
st.markdown("""
    <style>
    .stApp { background-color: #000033; color: white; }
    .stButton>button { 
        background-color: #990000; color: white; border: 2px solid white; 
        font-weight: bold; border-radius: 10px; height: 3em;
    }
    .stTextArea>div>div>textarea { background-color: #001a00; color: white; border: 2px solid white; border-radius: 10px; }
    .music-player-box { background-color: #000066; padding: 20px; border-radius: 15px; border: 2px solid #00FF00; margin-bottom: 20px; }
    h1, h2, h3 { text-shadow: 2px 2px #000000; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. เครื่องเล่นเพลงหน้ากลาง (ไม่หายแน่นอน!) ---
st.markdown('<div class="music-player-box">', unsafe_allow_html=True)
st.markdown("### 🎧 เครื่องเล่นเพลงบำบัด (SYNAPSE PLAYER)")
try:
    st.audio("music.mp3", loop=True)
    st.caption("🎵 เพลงกำลังเล่นวนลูปเพื่อความผ่อนคลายของคุณ...")
except:
    st.warning("⚠️ โปรดอัปโหลดไฟล์ music.mp3")
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. โครงสร้าง 4 หน้าหลัก พร้อมปุ่มเสริม ---
tabs = st.tabs(["📝 ระบายใจ", "🎸 เลือกแนว", "🎵 รับบทเพลง", "💬 ปรับทุกข์"])

with tabs[0]:
    st.header("พื้นที่ระบายความในใจ")
    col1, col2 = st.columns([4, 1])
    with col1:
        user_thought = st.text_area("ปลดปล่อยความรู้สึกออกมาให้หมด...", height=300, placeholder="พิมพ์ที่นี่...")
    with col2:
        st.button("🗑️ ล้าง")
        st.button("🔥 เผาทิ้ง")
        st.write(f"ตัวนับ: {len(user_thought)} อักษร")
    
    st.markdown("---")
    st.write("เลือกอารมณ์ตอนนี้:")
    st.button("😭 เศร้า", key="sad")
    st.button("😡 โกรธ", key="angry")

with tabs[1]:
    st.header("เลือกท่วงทำนองที่จะเยียวยา")
    genre = st.selectbox("สไตล์เพลง:", ["หมอลำ", "Pop", "Rock", "Rap", "เพื่อชีวิต", "ลูกทุ่ง"])
    
    col3, col4 = st.columns(2)
    with col3:
        st.button("🔊 ฟังตัวอย่างเสียง")
    with col4:
        st.button("🎲 สุ่มแนวเพลง")
    
    st.info("💡 แต่ละแนวเพลงจะมีคอร์ดและอารมณ์ที่ต่างกันไปตามที่คุณเลือก")

with tabs[2]:
    st.header("บทเพลงบำบัดของคุณ")
    if st.button("✨ ให้ 'อยู่นิ่งๆ ไม่เจ็บตัว' แต่งเพลง"):
        if user_thought:
            with st.spinner("AI กำลังสร้างสรรค์ผลงาน..."):
                # ฟังก์ชันเรียก AI (เหมือนเดิม)
                prompt = f"แต่งเพลงแนว {genre} จากข้อความ: {user_thought} พร้อมใส่คอร์ด"
                result = model.generate_content(prompt).text
                st.code(result, language='text')
                
                # ปุ่มฟังก์ชันเสริมหน้าผลลัพธ์
                c1, c2, c3 = st.columns(3)
                c1.button("📋 ก๊อปปี้เนื้อ")
                c2.button("📸 บันทึกภาพ")
                c3.button("🔄 แต่งใหม่")
                
                st.markdown("---")
                st.write("🔓 ปลดล็อคดาวน์โหลดโดยการกดติดตาม:")
                col_s1, col_s2, col_s3 = st.columns(3)
                col_s1.button("🔵 Facebook")
                col_s2.button("📸 Instagram")
                col_s3.button("🎵 TikTok")
        else:
            st.warning("กรุณาพิมพ์ข้อความระบายใจก่อนครับ")

with tabs[3]:
    st.header("คุยกับ 'อยู่นิ่งๆ ไม่เจ็บตัว'")
    # ระบบแชท (เหมือนเดิมแต่ขยายหน้าจอให้กว้างขึ้น)
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
        
    if p := st.chat_input("คุยได้ทุกเรื่อง..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        
        reply = model.generate_content(f"ตอบในฐานะเพื่อนบำบัด: {p}").text
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"): st.write(reply)
