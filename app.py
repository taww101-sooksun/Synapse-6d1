import streamlit as st
import requests
from streamlit_js_eval import get_geolocation
from datetime import datetime
import pytz
from firebase_admin import credentials, db, storage
import firebase_admin
import folium
from streamlit_folium import st_folium
import uuid

# --- 1. INITIALIZE FIREBASE ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="wide")

if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/',
            'storageBucket': 'notty-101.firebasestorage.app' 
        })
    except Exception as e:
        st.error(f"Firebase Connection Error: {e}")

bucket = storage.bucket()

# --- 2. SECURITY GATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center;'>🔐 SYNAPSE ACCESS CONTROL</h2>", unsafe_allow_html=True)
    try: st.image("logo2.jpg", width=200)
    except: pass
    with st.form("Login"):
        u_id = st.text_input("Enter your ID / ใส่ ID")
        u_pw = st.text_input("Password", type="password")
        if st.form_submit_button("UNLOCK SYSTEM"):
            if u_pw == "99999999" and u_id: 
                st.session_state.authenticated = True
                st.session_state.my_id = u_id.strip()
                st.rerun()
    st.stop()

my_id = st.session_state.my_id

# --- 3. CUSTOM STYLE ---
st.markdown("""
    <style>
    .stApp { background: #0f0c29; color: white; }
    .chat-container { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; height: 500px; overflow-y: auto; }
    .bubble-me { background: #0078ff; padding: 10px; border-radius: 15px 15px 0 15px; margin: 10px 0; margin-left: auto; width: fit-content; max-width: 80%; }
    .bubble-them { background: #333; padding: 10px; border-radius: 15px 15px 15px 0; margin: 10px 0; width: fit-content; max-width: 80%; }
    .media-content { border-radius: 10px; margin-top: 5px; max-width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR & LOGO ---
with st.sidebar:
    try: st.image("logo2.jpg", use_container_width=True)
    except: st.title("S Y N A P S E")
    st.write(f"🟢 **Online:** {my_id}")
    
    all_users = db.reference('/users').get()
    friend_list = [u for u in all_users.keys() if u != my_id] if all_users else []
    target_chat = st.selectbox("💬 เลือกเพื่อนสนทนา:", ["-- เลือกเพื่อน --"] + friend_list)
    
    st.divider()
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# --- 5. CHAT LOGIC ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📍 Satellite Tracking")
    location = get_geolocation()
    if location:
        coords = location.get('coords', {})
        lat, lon = coords.get('latitude'), coords.get('longitude')
        if lat and lon:
            m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
            folium.Marker([lat, lon]).add_to(m)
            st_folium(m, width=350, height=300)

with col2:
    if target_chat != "-- เลือกเพื่อน --":
        st.subheader(f"Talking to: {target_chat}")
        
        chat_room_id = "_".join(sorted([my_id, target_chat]))
        chat_ref = db.reference(f'/chats/{chat_room_id}')

        # ดึงและเรียงข้อความ (แก้ Error ที่คุณเจอ)
        raw_msgs = chat_ref.get()
        msgs = []
        if raw_msgs:
            # แปลงเป็น List และ Sort ใน Python
            msgs = sorted(raw_msgs.values(), key=lambda x: x.get('timestamp', 0))
            msgs = msgs[-20:] # เอา 20 อันล่าสุด

        # แสดงข้อความใน Container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for m in msgs:
            is_me = m['sender'] == my_id
            cls = "bubble-me" if is_me else "bubble-them"
            
            with st.chat_message("user" if is_me else "assistant"):
                st.write(f"**{m['sender']}**")
                if m.get('text'): st.write(m['text'])
                
                # แสดงรูปภาพหรือวิดีโอ
                if m.get('type') == 'image':
                    st.image(m['url'], use_container_width=True)
                elif m.get('type') == 'video':
                    st.video(m['url'])
                
                st.caption(m.get('time', ''))

        # ส่วนส่งข้อมูล
        with st.form("chat_form", clear_on_submit=True):
            msg_text = st.text_input("พิมพ์ข้อความ...")
            uploaded_file = st.file_uploader("ส่งรูปหรือวิดีโอ", type=['jpg','png','mp4','mov'])
            
            if st.form_submit_button("SEND 🚀"):
                new_msg = {
                    'sender': my_id,
                    'timestamp': datetime.now().timestamp(),
                    'time': datetime.now().strftime('%H:%M'),
                    'type': 'text'
                }
                
                if uploaded_file:
                    # อัปโหลดไป Firebase Storage
                    file_id = f"{uuid.uuid4()}_{uploaded_file.name}"
                    blob = bucket.blob(f"chat_media/{file_id}")
                    blob.upload_from_file(uploaded_file)
                    blob.make_public()
                    
                    new_msg['url'] = blob.public_url
                    new_msg['type'] = 'image' if uploaded_file.type.startswith('image') else 'video'
                
                if msg_text:
                    new_msg['text'] = msg_text
                
                if msg_text or uploaded_file:
                    chat_ref.push(new_msg)
                    st.rerun()
    else:
        st.info("กรุณาเลือกเพื่อนเพื่อเริ่มการสนทนา")

# --- 6. MUSIC ---
st.write("---")
with st.expander("🎵 Therapy Music"):
    st.markdown('<iframe width="100%" height="150" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0"></iframe>', unsafe_allow_html=True)
