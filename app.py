import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime
import uuid
# from PIL import Image # ไม่จำเป็นต้อง import PIL สำหรับ st.image หากแค่แสดงผล

# --- 1. ตั้งค่าและเชื่อมต่อ Firebase ---
if "firebase_service_account" not in st.secrets:
    st.error("ไม่พบการตั้งค่า Secrets! กรุณาสร้างไฟล์ .streamlit/secrets.toml")
    st.stop()

if not firebase_admin._apps:
    try:
        cred_info = dict(st.secrets["firebase_service_account"])
        # แก้ไข private_key ที่อาจมีการขึ้นบรรทัดใหม่
        if "\\n" in cred_info["private_key"]:
            cred_info["private_key"] = cred_info["private_key"].replace("\\n", "\n")
        
        cred = credentials.Certificate(cred_info)
        firebase_admin.initialize_app(cred, {
            'storageBucket': st.secrets["firebase_config"]["storageBucket"]
        })
    except Exception as e:
        st.error(f"เชื่อมต่อ Firebase ไม่ได้: {e}")
        st.stop()

db = firestore.client()
try:
    bucket = storage.bucket()
except Exception as e:
    st.error(f"ไม่พบ Storage Bucket หรือเกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
    st.stop()


# --- 2. จัดการ State (หน้าและ User) ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'user' not in st.session_state: st.session_state.user = ''

# --- 3. ฟังก์ชันตกแต่ง CSS (เปลี่ยนสีตามห้อง) ---
def set_theme(room_color):
    themes = {
        "home": ("#ffffff", "#000000"), # พื้นขาว ตัวดำ
        "red": ("#800000", "#ffffff"),  # พื้นแดงเลือดหมู ตัวขาว (ตัวอย่าง: YouTube)
        "blue": ("#000080", "#ffffff"), # พื้นน้ำเงินเข้ม ตัวขาว (ตัวอย่าง: Facebook)
        "green": ("#006400", "#ffffff"),# พื้นเขียวแก่ ตัวขาว (ตัวอย่าง: Line)
        "black": ("#000000", "#ffffff") # พื้นดำ ตัวขาว (ตัวอย่าง: Twitter/X)
    }
    bg, text = themes.get(room_color, ("#ffffff", "#000000"))
    
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {bg}; }}
        h1, h2, h3, p, span, div, label {{ color: {text} !important; }}
        .stButton>button {{
            border-radius: 20px;
            background-color: white;
            color: black;
            border: 1px solid #ccc;
            padding: 0.5rem 1rem;
            cursor: pointer;
        }}
        .post-box {{
            border: 1px solid {text};
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            background-color: rgba(255,255,255,0.1); /* สีพื้นหลังของกล่องโพสต์จะจางๆ */
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. ฟังก์ชันสำหรับห้องแชท (Reusable) ---
def render_room(room_id, room_name_th):
    # กำหนดธีมตามห้อง
    set_theme(room_id)

    st.title(f"ห้อง{room_name_th}")
    
    if st.button("⬅️ กลับหน้าหลัก"):
        st.session_state.page = 'home'
        st.rerun()

    # --- ส่วนโพสต์ ---
    with st.expander("📝 เขียนโพสต์ใหม่ / อัปโหลดรูป", expanded=False): # เปลี่ยนเป็น expanded=False เพื่อไม่ให้เปิดตลอด
        with st.form(f"post_form_{room_id}"):
            msg = st.text_area("คุยอะไรกันดี...")
            media = st.file_uploader("รูป/วิดีโอ", type=['png','jpg','mp4','mov'])
            submitted = st.form_submit_button("โพสต์เลย")
            
            if submitted and (msg or media):
                media_url, media_type = None, None
                if media:
                    with st.spinner("กำลังอัปโหลด..."):
                        ext = media.name.split('.')[-1]
                        # สร้าง path ใน Storage bucket: room_id/uuid.ext
                        fname = f"{room_id}/{uuid.uuid4()}.{ext}" 
                        blob = bucket.blob(fname)
                        blob.upload_from_string(media.getvalue(), content_type=media.type)
                        blob.make_public() # ทำให้ไฟล์สามารถเข้าถึงได้ผ่าน URL สาธารณะ
                        media_url = blob.public_url
                        media_type = 'video' if 'video' in media.type else 'image'
                
                db.collection(f'posts_{room_id}').add({
                    'user': st.session_state.user,
                    'text': msg,
                    'media_url': media_url,
                    'media_type': media_type,
                    'likes': [], # เก็บรายชื่อคนกดไลค์
                    'timestamp': firestore.SERVER_TIMESTAMP # ใช้ timestamp จากเซิร์ฟเวอร์ Firebase
                })
                st.success("โพสต์แล้ว!")
                st.rerun() # รีโหลดหน้าเพื่อแสดงโพสต์ใหม่

    # --- ส่วนแสดงฟีด ---
    # ดึงโพสต์จาก Firestore เรียงตาม timestamp ล่าสุดอยู่บนสุด
    docs = db.collection(f'posts_{room_id}').order_by('timestamp', direction='DESCENDING').stream()
    
    for doc in docs:
        d = doc.to_dict()
        did = doc.id # Document ID ของโพสต์
        likes = d.get('likes', [])
        is_liked = st.session_state.user in likes # ตรวจสอบว่า user ปัจจุบันกดไลค์โพสต์นี้หรือไม่
        
        st.markdown(f'<div class="post-box">', unsafe_allow_html=True) # เริ่มกล่องโพสต์
        
        # แสดงชื่อผู้ใช้และเวลา
        timestamp_str = d.get('timestamp').strftime('%d %b %Y, %H:%M') if d.get('timestamp') else ''
        st.caption(f"👤 {d.get('user')} • {timestamp_str}")
        
        st.write(d.get('text')) # แสดงข้อความโพสต์
        
        if d.get('media_url'): # ถ้ามีไฟล์มีเดีย
            if d.get('media_type') == 'video':
                st.video(d.get('media_url'))
            else:
                st.image(d.get('media_url'))
        
        # ปุ่ม Like & Share
        c1, c2, c3 = st.columns([1, 1, 4])
        with c1:
            like_label = f"❤️ {len(likes)}" if is_liked else f"🤍 {len(likes)}"
            if st.button(like_label, key=f"like_{did}"): # key ต้องไม่ซ้ำกันในแต่ละปุ่ม
                ref = db.collection(f'posts_{room_id}').document(did)
                if is_liked: # ถ้าเคยไลค์แล้ว ให้ลบออกจาก array
                    ref.update({'likes': firestore.ArrayRemove([st.session_state.user])})
                else: # ถ้ายังไม่ไลค์ ให้เพิ่มเข้าใน array
                    ref.update({'likes': firestore.ArrayUnion([st.session_state.user])})
                st.rerun() # รีโหลดหน้าเพื่อแสดงผลการไลค์
        with c2:
            if st.button("🔗 แชร์", key=f"share_{did}"):
                st.toast("จำลอง: คัดลอกลิงก์เรียบร้อย!") # แสดงข้อความชั่วคราว
        
        # --- เพิ่มส่วนคอมเมนต์ตรงนี้ ---
        # **จะแสดงเฉพาะห้องสีแดง (YouTube) เป็นตัวอย่าง**
        if room_id == 'red': 
            st.markdown("---") # เส้นคั่น
            st.subheader("ความคิดเห็น")

            # แสดงคอมเมนต์ที่มีอยู่
            comments_ref = db.collection(f'posts_{room_id}').document(did).collection('comments').order_by('timestamp', direction='ASCENDING')
            comments_docs = comments_ref.stream()
            for comment_doc in comments_docs:
                comment_data = comment_doc.to_dict()
                comment_timestamp_str = comment_data.get('timestamp').strftime('%d %b %Y, %H:%M') if comment_data.get('timestamp') else ''
                st.write(f"**{comment_data.get('user')}**: {comment_data.get('comment_text')}")
                st.caption(f"เมื่อ: {comment_timestamp_str}")

            # ฟอร์มสำหรับเพิ่มคอมเมนต์ใหม่
            with st.form(f"comment_form_{did}", clear_on_submit=True): # clear_on_submit ล้างฟอร์มหลังจากส่ง
                comment_text = st.text_area("เพิ่มความคิดเห็น...", key=f"comment_input_{did}") # key สำหรับ text_area
                comment_submitted = st.form_submit_button("แสดงความคิดเห็น")
                if comment_submitted and comment_text:
                    db.collection(f'posts_{room_id}').document(did).collection('comments').add({
                        'user': st.session_state.user,
                        'comment_text': comment_text,
                        'timestamp': firestore.SERVER_TIMESTAMP
                    })
                    st.success("แสดงความคิดเห็นแล้ว!")
                    st.rerun() # รีโหลดหน้าเพื่อแสดงคอมเมนต์ใหม่
        
        st.markdown('</div>', unsafe_allow_html=True) # ปิดกล่องโพสต์


# --- 5. การจัดการหน้าและ User ใน Main App ---

# ส่วน sidebar สำหรับตั้งชื่อ user
with st.sidebar:
    st.header("ตั้งค่า")
    user_input = st.text_input("ชื่อผู้ใช้ของคุณ:", value=st.session_state.user)
    if user_input:
        st.session_state.user = user_input
        st.success(f"สวัสดี, {st.session_state.user}!")
    else:
        st.warning("กรุณากรอกชื่อผู้ใช้!")

    st.markdown("---")
    st.caption("เลือกห้องที่คุณต้องการเข้า:")
    if st.session_state.user: # ถ้ามีชื่อผู้ใช้แล้วถึงจะแสดงปุ่มห้อง
        if st.button("ห้อง YouTube (แดง)"):
            st.session_state.page = 'red'
            st.rerun()
        if st.button("ห้อง Facebook (น้ำเงิน)"):
            st.session_state.page = 'blue'
            st.rerun()
        if st.button("ห้อง Line (เขียว)"):
            st.session_state.page = 'green'
            st.rerun()
        if st.button("ห้อง X (ดำ)"):
            st.session_state.page = 'black'
            st.rerun()
    else:
        st.info("กรุณากรอกชื่อผู้ใช้ในช่องด้านบนเพื่อเลือกห้อง")


# แสดงผลหน้าตาม st.session_state.page
if st.session_state.page == 'home':
    set_theme('home') # กำหนดธีมสีขาวสำหรับหน้าหลัก
    st.title("ยินดีต้อนรับสู่ Firebase Social App!")
    st.markdown("---")
    
    # เพิ่มโลโก้
    try:
        st.image("logo.jpg", width=200) # แสดงโลโก้
    except FileNotFoundError:
        st.warning("ไม่พบไฟล์ 'logo.jpg' โปรดตรวจสอบพาธหรือวางไฟล์ในไดเรกทอรีเดียวกัน.")
    
    st.write("เลือกชื่อผู้ใช้ของคุณทางซ้ายมือ แล้วเลือกห้องที่คุณต้องการจะเข้าร่วม")
    st.write("แอปพลิเคชันนี้สาธิตการใช้งาน Firebase Firestore และ Firebase Storage ร่วมกับ Streamlit")
    st.markdown("---")
    st.subheader("คุณสมบัติ:")
    st.markdown("- โพสต์ข้อความและอัปโหลดรูป/วิดีโอ")
    st.markdown("- กดไลค์โพสต์")
    st.markdown("- แสดงความคิดเห็น (เฉพาะห้อง YouTube)")

elif st.session_state.page == 'red':
    render_room('red', 'YouTube')
elif st.session_state.page == 'blue':
    render_room('blue', 'Facebook')
elif st.session_state.page == 'green':
    render_room('green', 'Line')
elif st.session_state.page == 'black':
    render_room('black', 'X')

