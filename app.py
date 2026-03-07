import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import time
import streamlit.components.v1 as components

# --- 1. SETTING & DARK MODE STYLE ---
st.set_page_config(page_title="SYNAPSE COMMAND", layout="wide", page_icon="🛰️")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #00ff00; }
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(0, 30, 0, 0.3);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00ff00;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
    }
    .my-msg { text-align: right; color: #00ff00; background: rgba(0,255,0,0.1); padding: 10px; border-radius: 10px; margin-bottom: 5px; border-right: 4px solid #00ff00; }
    .other-msg { text-align: left; color: #ffffff; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; margin-bottom: 5px; border-left: 4px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FIREBASE CONNECTION (ใช้ Service Account ที่คุณให้มา) ---
if not firebase_admin._apps:
    try:
        # ดึงจาก Secrets (ต้องไปแปะในหน้า Dashboard ของ Streamlit ก่อน)
        fb_dict = dict(st.secrets["firebase"])
        fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
        
        creds = credentials.Certificate(fb_dict)
        firebase_admin.initialize_app(creds, {
            'databaseURL': 'https://sooksun1-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
    except Exception as e:
        st.error(f"⚠️ Firebase Connection Error: {e}")

# --- 3. AGORA CONFIG (ข้อมูลล่าสุดของคุณ) ---
AGORA_APP_ID = "84d8f5f05b0c49e181837f40d7688967"
AGORA_TOKEN = "007eJxTYDjNVVmy0Oluq8PFx7OrOp1l86+W2W9aez+Ir2Fz8pT1+TEKDBYmKRZppmkGpkkGySaWqYYWhhbG5mkmBinmZhYWlmbmcRFrMhsCGRkc/rcxMTJAIIivwOCcn1eWr+voqRtQlJ+Vmlyia2BmamRqqmtgbmBsZGBkxsAAAF8oJtY="
CHANNEL_NAME = "Synapse_Main"

# --- 4. SIDEBAR PANEL ---
with st.sidebar:
    st.title("🛰️ COMMAND PANEL")
    my_id = st.text_input("ระบุตัวตน (ID):", value="Ta101")
    st.write("---")
    st.subheader("🎵 SYNAPSE PLAYER")
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    components.html(
        f'<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list={playlist_id}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
        height=220
    )
    st.caption("🎧 'อยู่นิ่งๆ ไม่เจ็บตัว' | BY Ta101")

# --- 5. MAIN INTERFACE ---
st.title("SYNAPSE COMMAND CENTER")
tabs = st.tabs(["🚀 RADAR & GPS", "💬 CHAT ROOM", "📞 TELE-CALL"])

# TAB 1: RADAR & GPS
with tabs[0]:
    st.subheader("📍 LIVE TRACKING")
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        st.success(f"พิกัดปัจจุบัน: {lat}, {lon}")
        if st.button("🛰️ บันทึกตำแหน่งลงเรดาร์"):
            db.reference(f'users/{my_id}').update({
                'lat': lat, 'lon': lon, 'last_update': time.time()
            })
            st.toast("อัปเดตตำแหน่งแล้ว!", icon="✅")
    
    # แสดงแผนที่ (Google Hybrid)
    m = folium.Map(location=[13.75, 100.5], zoom_start=12, tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google")
    try:
        users = db.reference('users').get() or {}
        for name, info in users.items():
            if 'lat' in info:
                color = 'green' if (time.time() - info.get('last_update', 0)) < 600 else 'red'
                folium.Marker([info['lat'], info['lon']], tooltip=name, icon=folium.Icon(color=color)).add_to(m)
    except: pass
    st_folium(m, width="100%", height=400)

# TAB 2: CHAT ROOM
with tabs[1]:
    st.subheader("💬 ENCRYPTED CHAT")
    chat_ref = db.reference('chats/main_room')
    
    # แสดงข้อความ 15 ข้อความล่าสุด
    messages = chat_ref.order_by_child('timestamp').limit_to_last(15).get() or {}
    with st.container(height=300):
        for mid, msg in sorted(messages.items(), key=lambda x: x[1].get('timestamp', 0)):
            css_class = "my-msg" if msg.get('user') == my_id else "other-msg"
            st.markdown(f"<div class='{css_class}'><b>{msg.get('user')}</b>: {msg.get('text')}</div>", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([8, 2])
        msg_input = col1.text_input("พิมพ์ข้อความ...", label_visibility="collapsed")
        if col2.form_submit_button("ส่ง 🚀") and msg_input:
            chat_ref.push({'user': my_id, 'text': msg_input, 'timestamp': time.time()})
            st.rerun()

# TAB 3: TELE-CALL (Agora Integration)
with tabs[2]:
    st.subheader("📞 AGORA VIDEO CALL")
    agora_js = f"""
    <div id="video-container" style="width: 100%; height: 450px; background: #000; border: 2px solid #00ff00; border-radius: 10px; overflow: hidden;">
        <div id="local-player" style="width: 100%; height: 100%;"></div>
    </div>
    <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.11.0.js"></script>
    <script>
        async function start() {{
            const client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            await client.join("{AGORA_APP_ID}", "{CHANNEL_NAME}", "{AGORA_TOKEN}", null);
            const [audio, video] = await AgoraRTC.createMicrophoneAndCameraTracks();
            video.play('local-player');
            await client.publish([audio, video]);
        }}
        start();
    </script>
    """
    components.html(agora_js, height=500)
    st.info(f"Connected to Channel: {CHANNEL_NAME}")
