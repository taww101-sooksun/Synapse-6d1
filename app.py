import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import os

# --- 1. SETUP UI & THEME (ตัวเชื่อมหน้าตา) ---
def setup_ui_theme():
    if 'theme_color' not in st.session_state:
        st.session_state.theme_color = "#00f2fe"
    
    st.set_page_config(page_title="SYNAPSE ULTIMATE", layout="wide", page_icon="🌐")
    
    # ฉีด CSS นีออน
    st.markdown(f"""
        <style>
        .stApp {{ background: #000; color: {st.session_state.theme_color}; }}
        .stButton>button {{ 
            border: 1px solid {st.session_state.theme_color} !important; 
            color: {st.session_state.theme_color} !important; 
            background: transparent !important; width: 100%;
        }}
        .chat-box {{ 
            border-left: 3px solid {st.session_state.theme_color}; 
            padding: 10px; margin: 5px; background: rgba(255,255,255,0.05); 
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 2. AUDIO LOGIC (ตัวเชื่อมเพลง) ---
def play_background_music():
    with st.sidebar:
        st.markdown("### 🎵 SYSTEM AUDIO")
        # ลิงก์เพลง "ยักษ์ในตัวฉัน" ที่พี่ใช้แล้วติด
        music_url = "https://docs.google.com/uc?export=download&id=1AhClqXudsgLtFj7CofAUqPqfX8YW1T7a"
        st.audio(music_url, format="audio/mpeg", loop=True)
        st.session_state.theme_color = st.color_picker("ปรับสีระบบ", st.session_state.theme_color)
        st.write('*"อยู่นิ่งๆ ไม่เจ็บตัว"*')

# --- 3. FIREBASE & GPS LOGIC (ตัวเชื่อมสมอง) ---
def init_firebase():
    if not firebase_admin._apps:
        try:
            fb_dict = dict(st.secrets["firebase"])
            fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
            creds = credentials.Certificate(fb_dict)
            firebase_admin.initialize_app(creds, {'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/'})
        except: pass

def sync_user_location(name, lat, lon):
    db.reference(f'users/{name}').update({
        'lat': lat, 'lon': lon, 'last_update': time.time()
    })

# --- 4. MAIN PROGRAM (ตัวเชื่อมโครงสร้าง) ---
setup_ui_theme()
init_firebase()
play_background_music()

if 'my_id' not in st.session_state: st.session_state.my_id = "Ta101"

tab1, tab2, tab3 = st.tabs(["🚀 CORE", "🛰️ RADAR", "💬 COMMS"])

with tab1:
    st.header("SYSTEM INITIATE")
    name = st.text_input("ระบุชื่อรหัสของคุณ:", st.session_state.my_id)
    st.session_state.my_id = name
    
    # ใช้ JS_EVAL ดึงพิกัดจริง (อ่อนนุชตรงเป๊ะ)
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        st.success(f"📍 ตรวจพบตำแหน่งจริง: {lat}, {lon}")
        if st.button("🛰️ UPDATE SIGNAL"):
            sync_user_location(name, lat, lon)
            st.balloons()
    else:
        st.warning("🚨 กรุณากด 'Allow' เพื่อให้แผนที่ตรงจุด")

with tab2:
    st.subheader("🛰️ STRATEGIC RADAR")
    all_users = db.reference('users').get()
    
    # ถ้ามีพิกัดเรา ให้เปิดแผนที่ตรงที่เราอยู่
    v_lat, v_lon = 13.7056, 100.6015 # อ่อนนุช
    if all_users and name in all_users:
        v_lat, v_lon = all_users[name].get('lat', v_lat), all_users[name].get('lon', v_lon)

    m = folium.Map(location=[v_lat, v_lon], zoom_start=18, 
                   tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google")
    
    if all_users:
        for u_name, info in all_users.items():
            color = 'blue' if u_name == name else 'red'
            folium.Marker([info['lat'], info['lon']], tooltip=u_name, 
                          icon=folium.Icon(color=color, icon='star')).add_to(m)
    st_folium(m, width="100%", height=500)

with tab3:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("📹 VIDEO CALL")
        # ระบบฆ่าติ่ง Join และซ่อนแอป Jitsi
        if st.button("🚀 INITIATE CALL"):
            room = f"SYN_{int(time.time())}"
            st.components.v1.html(f"""
                <div id="j" style="height:450px; width:100%; border:1px solid {st.session_state.theme_color}; border-radius:10px;"></div>
                <script src="https://meet.jit.si/external_api.js"></script>
                <script>
                    new JitsiMeetExternalAPI('meet.jit.si', {{
                        roomName: '{room}', parentNode: document.querySelector('#j'),
                        configOverwrite: {{ prejoinPageEnabled: false, disableDeepLinking: true }},
                        interfaceConfigOverwrite: {{ SHOW_JITSI_WATERMARK: false, TOOLBAR_BUTTONS: ['microphone', 'camera', 'hangup'] }}
                    }});
                </script>
            """, height=470)

    with c2:
        st.subheader("💬 PRIVATE CHAT")
        target = st.text_input("คุยกับ:", "User2")
        # ดึงแชตจาก Firebase (Simplified)
        chat_ref = db.reference(f'chats/{name}_{target}')
        if st.button("ส่งข้อความ"):
            # เพิ่ม Logic ส่งแชตตรงนี้
            pass
        st.write("ระบบแชตกำลังรอการเชื่อมต่อ...")

