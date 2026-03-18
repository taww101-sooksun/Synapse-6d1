import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
import os
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

# --- 1. CONFIG & THEME ---
logo_path = "logo3.jpg"
logo_exists = os.path.exists(logo_path)

st.set_page_config(page_title="SYNAPSE IDENTITY", layout="wide")

if 'theme_color' not in st.session_state: st.session_state.theme_color = "#00f2fe"

# --- 2. FIREBASE CONNECTION ---
if not firebase_admin._apps:
    try:
        fb_data = st.secrets["firebase"]
        fb_config = {
            "type": fb_data["type"], "project_id": fb_data["project_id"],
            "private_key_id": fb_data["private_key_id"],
            "private_key": fb_data["private_key"].replace('\\n', '\n'),
            "client_email": fb_data["client_email"], "client_id": fb_data["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": fb_data["client_x509_cert_url"]
        }
        cred = credentials.Certificate(fb_config)
        firebase_admin.initialize_app(cred, {'databaseURL': "https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/"})
    except: st.error("Firebase Error")

# --- 3. CHAT LOGIC (ระบบแชตดึงค่าจาก Firebase) ---
def get_private_messages(my_id, target_id):
    try:
        pair = sorted([my_id, target_id])
        room_id = f"chat_{pair[0]}_{pair[1]}"
        ref = db.reference(f'private_messages/{room_id}')
        msgs = ref.get()
        if msgs:
            return sorted(msgs.values(), key=lambda x: x['ts'])[-20:] # ดึง 20 ข้อความล่าสุด
    except: return []
    return []

def send_private_message(my_id, target_id, text):
    if text.strip():
        pair = sorted([my_id, target_id])
        room_id = f"chat_{pair[0]}_{pair[1]}"
        db.reference(f'private_messages/{room_id}').push({
            'sender': my_id, 'msg': text, 'ts': time.time()
        })

# --- 4. MAIN APP ---
st.markdown(f"<style>.stApp {{ background: #000; color: {st.session_state.theme_color}; }}</style>", unsafe_allow_html=True)

with st.sidebar:
    if logo_exists: st.image(logo_path)
    st.title("🌐 CONTROL")
    my_name = st.text_input("รหัสของคุณ (ID):", "Ta101")
    target_name = st.text_input("คุยกับใคร (Target ID):", "User2")
    st.session_state.theme_color = st.color_picker("THEME COLOR", st.session_state.theme_color)
    st.write('*"อยู่นิ่งๆ ไม่เจ็บตัว"*')

tabs = st.tabs(["🚀 แกนหลัก", "🛰️ เรดาร์", "💬 สื่อสาร & คอล"])

# --- TAB 1: CORE (พิกัดจริง) ---
with tabs[0]:
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        st.success(f"📍 พิกัดปัจจุบันของคุณ: {lat}, {lon}")
        if st.button("🛰️ บันทึกพิกัดจริงลงระบบ"):
            db.reference(f'users/{my_name}').update({'lat': lat, 'lon': lon, 'ts': time.time()})
            st.toast("พิกัดถูกบันทึกแล้ว!")

# --- TAB 2: RADAR (แผนที่ดาวเทียม) ---
with tabs[1]:
    all_users = db.reference('users').get()
    view_lat, view_lon = 13.7056, 100.6015 # อ่อนนุช
    if all_users and my_name in all_users:
        view_lat, view_lon = all_users[my_name]['lat'], all_users[my_name]['lon']

    m = folium.Map(location=[view_lat, view_lon], zoom_start=18, 
                   tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    if all_users:
        for name, info in all_users.items():
            color = 'blue' if name == my_name else 'red'
            folium.Marker([info['lat'], info['lon']], tooltip=name, icon=folium.Icon(color=color)).add_to(m)
    st_folium(m, width="100%", height=500)

# --- TAB 3: COMMS (แชต & คอล) ---
with tabs[2]:
    col1, col2 = st.columns([1, 1])
    
    with col1: # ส่วนของวิดีโอคอล
        st.subheader("📹 ระบบวิดีโอคอล")
        if st.button("🚀 เริ่มการคอล (Video Call)"):
            # สร้างห้องคอลแบบ P2P ผ่าน Jitsi
            room_id = f"Synapse_{sorted([my_name, target_name])[0]}_{sorted([my_name, target_name])[1]}"
            st.components.v1.html(f"""
                <div id="jitsi-container" style="height: 450px; width: 100%; border: 2px solid {st.session_state.theme_color}; border-radius: 10px;"></div>
                <script src="https://meet.jit.si/external_api.js"></script>
                <script>
                    const options = {{
                        roomName: '{room_id}',
                        parentNode: document.querySelector('#jitsi-container'),
                        configOverwrite: {{ prejoinPageEnabled: false }},
                        interfaceConfigOverwrite: {{ SHOW_JITSI_WATERMARK: false }},
                        userInfo: {{ displayName: '{my_name}' }}
                    }};
                    const api = new JitsiMeetExternalAPI('meet.jit.si', options);
                </script>
            """, height=470)

    with col2: # ส่วนของแชต
        st.subheader(f"💬 แชตกับ: {target_name}")
        # แสดงข้อความแชต
        messages = get_private_messages(my_name, target_name)
        chat_container = st.container()
        with chat_container:
            for m in messages:
                align = "right" if m['sender'] == my_name else "left"
                color = st.session_state.theme_color if m['sender'] == my_name else "#fff"
                st.markdown(f"""
                    <div style="text-align: {align}; margin-bottom: 10px;">
                        <span style="background: rgba(255,255,255,0.1); padding: 8px 12px; border-radius: 10px; border-left: 3px solid {color};">
                            <b>{m['sender']}</b>: {m['msg']}
                        </span>
                    </div>
                """, unsafe_allow_html=True)
        
        # ช่องพิมพ์ข้อความ
        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input("พิมพ์ข้อความ...")
            if st.form_submit_button("ส่ง"):
                send_private_message(my_name, target_name, user_msg)
                st.rerun()
