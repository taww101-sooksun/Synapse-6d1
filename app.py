import streamlit as st
from datetime import datetime
import uuid

# --- ฟังก์ชันดึงข้อมูลโพสต์จาก Firebase ---
def fetch_red_posts():
    # ดึงโพสต์เรียงตามเวลาล่าสุด (ดันฟีดไปเรื่อยๆ ตามที่คุณต้องการ)
    posts_ref = db.collection('posts_red').order_by('time', direction='DESCENDING').limit(50)
    return posts_ref.stream()

def render_red_room():
    st.markdown("<h1 style='color:#FF4D4D; text-align:center;'>🔴 RED PUBLIC FEED</h1>", unsafe_allow_html=True)
    
    if st.button("⬅️ กลับหน้าศูนย์บัญชาการ"):
        st.session_state.page = "home"
        st.rerun()

    # --- 1. ส่วนการโพสต์ (Write to Firebase) ---
    with st.expander("📝 สร้างโพสต์ใหม่ (แชร์วิดีโอ/รูปภาพ)"):
        with st.form("form_red", clear_on_submit=True):
            msg = st.text_area("คุณกำลังคิดอะไรอยู่?")
            media_url = st.text_input("แปะลิงก์ YouTube หรือลิงก์รูปภาพ")
            
            if st.form_submit_button("🚀 ปล่อยโพสต์"):
                if msg or media_url:
                    # บันทึกลง Firestore
                    db.collection('posts_red').add({
                        'user': st.session_state.user,
                        'text': msg,
                        'media': media_url,
                        'likes': [],
                        'time': datetime.now() # ใช้เวลาปัจจุบันเป็นตัวดันฟีด
                    })
                    st.success("โพสต์สำเร็จ!")
                    st.rerun()

    st.divider()

    # --- 2. ส่วนแสดงฟีด (Read from Firebase) ---
    docs = fetch_red_posts()
    
    for doc in docs:
        p = doc.to_dict()
        pid = doc.id
        
        # กล่องโพสต์
        st.markdown(f"""
            <div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:15px; border:1px solid #444; margin-bottom:15px;">
                <b style="color:#FFD700;">👤 {p.get('user')}</b> 
                <small style="color:#666; margin-left:10px;">{p.get('time').strftime('%Y-%m-%d %H:%M') if p.get('time') else ''}</small>
                <p style="margin-top:10px;">{p.get('text')}</p>
            </div>
        """, unsafe_allow_html=True)

        # แสดงสื่อ (วิดีโอ/รูป)
        m = p.get('media', '')
        if "youtube.com" in m or "youtu.be" in m:
            st.video(m)
        elif m.startswith("http"):
            st.image(m, use_container_width=True)

        # --- 3. ระบบ Like & Comment ---
        likes = p.get('likes', [])
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.button(f"❤️ {len(likes)}", key=f"like_{pid}"):
                ref = db.collection('posts_red').document(pid)
                if st.session_state.user in likes:
                    ref.update({'likes': firestore.ArrayRemove([st.session_state.user])})
                else:
                    ref.update({'likes': firestore.ArrayUnion([st.session_state.user])})
                st.rerun()
        
        with col2:
            if st.button("💬", key=f"comment_{pid}"):
                st.session_state.view_comments = pid # เก็บ ID ไว้เพื่อเปิดหน้าคอมเมนต์

        st.markdown("<hr style='border:0.5px solid #222;'>", unsafe_allow_html=True)
