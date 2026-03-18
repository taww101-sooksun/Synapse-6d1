import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

# --- 1. CONFIG & LOGO ---
logo_path = "logo2.jpg"
logo_exists = os.path.exists(logo_path)

st.set_page_config(
    page_title="SYNAPSE IDENTITY", 
    page_icon=logo_path if logo_exists else "logo2.jpg", 
    layout="wide"
)

# --- 2. INITIALIZE FIREBASE (Asia Southeast 1) ---
if not firebase_admin._apps:
    try:
        fb_data = st.secrets["firebase"]
        fb_config = {
            "type": fb_data["type"],
            "project_id": fb_data["project_id"],
            "private_key_id": fb_data["private_key_id"],
            "private_key": fb_data["private_key"].replace('\\n', '\n'),
            "client_email": fb_data["client_email"],
            "client_id": fb_data["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": fb_data["client_x509_cert_url"]
        }
        cred = credentials.Certificate(fb_config)
        target_url = "https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/"
        firebase_admin.initialize_app(cred, {'databaseURL': target_url})
        st.toast("✅ SYNAPSE CORE CONNECTED")
    except Exception as e:
        st.error(f"🚨 Connection Error: {e}")
        st.stop()

# --- 3. AUDIO PLAYER FUNCTION ---
def synapse_audio_player():
    link = "https://docs.google.com/uc?export=download&id=1AhClqXudsgLtFj7CofAUqPqfX8YW1T7a"
    st.sidebar.markdown(f"""
        <div style="background:rgba(0,0,0,0.5); padding:15px; border-radius:15px; border:1px solid {st.session_state.get('theme_color', '#00f2fe')}; text-align:center;">
            <p style="color:{st.session_state.get('theme_color', '#00f2fe')}; font-weight:bold; margin-bottom:10px;">🎵 SYNAPSE AUDIO</p>
            <audio id="audio-player" loop controls style="width:100%; filter: invert(100%) hue-rotate(180deg) brightness(1.5);">
                <source src="{link}" type="audio/mpeg">
            </audio>
        </div>
        <script>
            var audio = document.getElementById("audio-player");
            window.parent.document.addEventListener('click', function() {{ 
                if (audio.paused) {{ audio.play(); }}
            }}, {{ once: true }});
        </script>
    """, unsafe_allow_html=True)

# --- 4. CHAT LOGIC ---
def private_chat_logic(my_name, target_name, p_msg=None):
    try:
        pair = sorted([my_name, target_name])
        room_id = f"priv_{pair[0]}_{pair[1]}"
        ref = db.reference(f'private_rooms/{room_id}')
        if p_msg:
            ref.push({'name': my_name, 'msg': p_msg, 'ts': time.time()})
        raw_p_msgs = ref.get()
        if raw_p_msgs:
            msgs = list(raw_p_msgs.values()) if isinstance(raw_p_msgs, dict) else [m for m in raw_p_msgs if m]
            return sorted(msgs, key=lambda x: x.get('ts', 0))[-15:]
    except: return []
    return []

# --- 5. MULTI-LANGUAGE ---
LANG_DATA = {
    "TH": {"welcome": "ยินดีต้อนรับ", "core": "🚀🖲 แกนหลัก", "radar": "🛰️📡 เรดาร์", "comms": "💬📝 สื่อสาร", "sys": "🧹 ระบบ", "lat": "ละติจูด", "lon": "ลองติจูด", "manual": "คู่มือ"},
    "EN": {"welcome": "Welcome", "core": "🚀🖲 CORE", "radar": "🛰️📡 RADAR", "comms": "💬📝 COMMS", "sys": "🧹 SYSTEM", "lat": "LATITUDE", "lon": "LONGITUDE", "manual": "MANUAL"},
    "JP": {"welcome": "ようこそ", "core": "🚀🖲 コア", "radar": "🛰️📡 レーダー", "comms": "💬📝 通信", "sys": "🧹 システム", "lat": "緯度", "lon": "経度", "manual": "マニュアル"},
    "CN": {"welcome": "欢迎", "core": "🚀🖲 核心", "radar": "🛰️📡 雷达", "comms": "💬📝 通讯", "sys": "🧹 系统", "lat": "纬度", "lon": "经度", "manual": "手册"},
    "MM": {"welcome": "ကြိုဆိုပါတယ်", "core": "🚀🖲 အဓိက", "radar": "🛰️📡 ရေဒါ", "comms": "💬📝 ဆက်သွယ်ရေး", "sys": "🧹 စနစ်", "lat": "လတ္တီတွဒ်", "lon": "လောင်ဂျီတွဒ်", "manual": "လမ်းညွှန်"},
    "LA": {"welcome": "ຍິນດີຕ້ອນຮັບ", "core": "🚀🖲 ແກນຫຼັກ", "radar": "🛰️📡 ເຣດາ", "comms": "💬📝 ສື່ສານ", "sys": "🧹 ລະບົບ", "lat": "ລະຕິຈູด", "lon": "ລောင်ຕິຈູດ", "manual": "ຄູ່ມື"}
}

# --- 6. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_name' not in st.session_state: st.session_state.user_name = "AGENT_X"
if 'theme_color' not in st.session_state: st.session_state.theme_color = "#00f2fe"
if 'lang' not in st.session_state: st.session_state.lang = "TH"

# --- 7. LOGIN UI ---
if not st.session_state.logged_in:
    if logo_exists: st.image(logo_path, width=400)
    st.markdown(f"<h1 style='text-align:center; color:{st.session_state.theme_color};'>🌐 SYNAPSE IDENTITY</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        pw = st.text_input("SECURITY KEY", type="password")
        if st.button("🚀 ENTER SYSTEM"):
            if pw == "ta101":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("❌ Access Denied")
    st.stop()

# --- 8. MAIN APP ---
L = LANG_DATA[st.session_state.lang]
st.markdown(f"<style>.stApp {{ background: #000; color: {st.session_state.theme_color}; }}</style>", unsafe_allow_html=True)

with st.sidebar:
    if logo_exists: st.image(logo_path, use_column_width=True)
    st.title("🌐 CONTROL")
    synapse_audio_player()
    st.session_state.user_name = st.text_input("ID", st.session_state.user_name)
    st.session_state.lang = st.selectbox("LANGUAGE", list(LANG_DATA.keys()))
    st.session_state.theme_color = st.color_picker("THEME COLOR", st.session_state.theme_color)
    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.rerun()

# --- 9. TABS ---
tabs = st.tabs([L["core"], L["radar"], L["comms"], L["sys"]])

with tabs[0]: # แกนหลัก (GPS แม่นยำสูง)
    st.header(f"{L['welcome']}, {st.session_state.user_name}")
    st.components.v1.html(f"""
        <div style="background:rgba(0,0,0,0.8); color:{st.session_state.theme_color}; padding:15px; border-radius:10px; border:1px solid {st.session_state.theme_color}; font-family:monospace;">
            <div style="display:flex; justify-content:space-between;">
                <div>📍 GPS: <span id="g">...</span></div>
                <div>⏰ TIME: <span id="t">00:00:00</span></div>
            </div>
        </div>
        <script>
            const options = {{ enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }};
            setInterval(() => {{
                navigator.geolocation.getCurrentPosition(p => {{
                    document.getElementById('g').innerText = p.coords.latitude.toFixed(6) + ", " + p.coords.longitude.toFixed(6);
                }}, null, options);
                document.getElementById('t').innerText = new Date().toLocaleTimeString('th-TH');
            }}, 1000);
        </script>
    """, height=100)
    if st.button("📢 BROADCAST SIGNAL"):
        db.reference('logs/activity').push({'user': st.session_state.user_name, 'ts': time.time()})
        st.toast("Signal Broadcasted!")

with tabs[1]: # เรดาร์ (Google Hybrid)
    st.subheader(L["radar"])
    col_a, col_b = st.columns(2)
    lat_v = col_a.number_input(L["lat"], value=13.7500, format="%.6f")
    lon_v = col_b.number_input(L["lon"], value=100.5100, format="%.6f")
    
    m = folium.Map(location=[lat_v, lon_v], zoom_start=18, 
                   tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Marker([lat_v, lon_v], icon=folium.Icon(color='red')).add_to(m)
    st_folium(m, width="100%", height=500)

with tabs[2]: # สื่อสาร (Jitsi ฆ่าติ่ง Join)
    st.subheader(L["comms"])
    target = st.text_input("แชทกับใคร:", value="User2")
    if st.button("📹 VIDEO CALL START"):
        room_name = f"Synapse_{st.session_state.user_name}_{target}"
        st.components.v1.html(f"""
        <div id="jitsi-container" style="height: 500px; width: 100%; border: 2px solid {st.session_state.theme_color}; border-radius: 10px;"></div>
        <script src="https://meet.jit.si/external_api.js"></script>
        <script>
            const options = {{
                roomName: '{room_name}', parentNode: document.querySelector('#jitsi-container'),
                configOverwrite: {{ prejoinPageEnabled: false, disableDeepLinking: true, startWithAudioMuted: false, startWithVideoMuted: false }},
                interfaceConfigOverwrite: {{ SHOW_JITSI_WATERMARK: false, TOOLBAR_BUTTONS: ['microphone', 'camera', 'hangup'] }},
                userInfo: {{ displayName: '{st.session_state.user_name}' }}
            }};
            new JitsiMeetExternalAPI('meet.jit.si', options);
        </script>
        """, height=550)
    
    st.markdown("---")
    msgs = private_chat_logic(st.session_state.user_name, target)
    for m in msgs: st.write(f"**{m['name']}**: {m['msg']}")
    with st.form("chat_f", clear_on_submit=True):
        txt = st.text_input("พิมพ์ข้อความ...")
        if st.form_submit_button("ส่ง"):
            private_chat_logic(st.session_state.user_name, target, txt)
            st.rerun()

with tabs[3]: # ระบบ
    st.subheader(f"📖 {L['manual']}")
    st.write('Philosophy: "อยู่นิ่งๆ ไม่เจ็บตัว"')
    if st.button("REBOOT CORE"):
        st.cache_resource.clear()
        st.rerun()
