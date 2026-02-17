import streamlit as st

def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D; text-align:center;'>🔴 RED MEDIA HUB</h1>", unsafe_allow_html=True)
    
    if st.button("⬅️ กลับหน้าหลัก"):
        st.session_state.page = "home"
        st.rerun()

    # --- ส่วนดึงข้อมูลแบบปลอดภัย ---
    try:
        # ลองดึงแบบเรียงลำดับก่อน
        posts = db.collection('posts_red').order_by('time', direction='DESCENDING').limit(20).stream()
        
        # ถ้าไม่มี Error จะทำต่อที่นี่
        for doc in posts:
            p = doc.to_dict()
            st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; margin-bottom:10px; border-left:5px solid #FF4D4D;">
                    <b style="color:#FFD700;">👤 {p.get('user')}</b>
                    <p>{p.get('text', '')}</p>
                </div>
            """, unsafe_allow_html=True)
            if p.get('media'):
                if "youtube" in p.get('media'): st.video(p.get('media'))
                else: st.image(p.get('media'))

    except Exception as e:
        # ถ้าแดง (Error) ให้โชว์คำเตือนแทน และลองดึงแบบไม่เรียงลำดับ
        st.warning("🔄 ระบบกำลังจัดเรียงฟีด (Index Build)... ระหว่างนี้จะแสดงโพสต์แบบสุ่มไปก่อนครับ")
        posts = db.collection('posts_red').limit(10).stream()
        for doc in posts:
            p = doc.to_dict()
            st.write(f"👤 {p.get('user')}: {p.get('text')}")

# อย่าลืมเช็คการตั้งค่า Secrets ใน Streamlit Cloud ด้วยนะครับว่าชื่อตรงกับที่เรียกในโค้ดไหม
