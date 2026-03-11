import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import time
import datetime
import streamlit.components.v1 as components

# --- 1. UI THEME (Cyberpunk Green) ---
st.set_page_config(page_title="SYNAPSE COMMAND", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #00ff00; }
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(0, 30, 0, 0.4);
        padding: 15px; border-radius: 10px; border: 1px solid #00ff00;
    }
    .my-msg { text-align: right; color: #00ff00; background: rgba(0,255,0,0.1); padding: 8px; border-radius: 10px; margin-bottom: 5px; border-right: 4px solid #00ff00; }
    .other-msg { text-align: left; color: #ffffff; background: rgba(255,255,255,0.1); padding: 8px; border-radius: 10px; margin-bottom: 5px; border-left: 4px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONNECT FIREBASE (แบบใช้ URL ตรงๆ ไม่ต้องเรียก Secret เยอะ) ---
# ความจริง: ถ้าคุณตั้ง Rules ใน Firebase เป็น true ทั้งหมด คุณแทบไม่ต้องใช้กุญแจเลยในบางกรณี
if not firebase_admin._apps:
    try:
        # ถ้ามี Secrets ก็ใช้ ถ้าไม่มีก็ปล่อยผ่านให้ระบบลองเชื่อมต่อดู
        if "firebase" in st.secrets:
            fb_dict = dict(st.secrets["firebase"])
            fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
            creds = credentials.Certificate(fb_dict)
            firebase_admin.initialize_app(creds, {'databaseURL': fb_dict["databaseURL"]})
        else:
            st.warning("⚠️ ยังไม่ได้ใส่กุญแจ Firebase ใน Secrets (ระบบอาจบันทึกข้อมูลไม่ได้)")
    except Exception as e:
        st.error(f"Error: {e}")

# --- 3. MAIN APP ---
st.title("🛰️ SYNAPSE COMMAND")

# Sidebar: แค่ใส่ชื่อ ID ก็พอ ไม่ต้องใช้รหัสผ่าน
with st.sidebar:
    my_id = st.text_input("USER ID:", value="Ta101")
    st.divider()
    st.write("🎵 **AUTO PLAYER**")
    # ใส่ YouTube Playlist แบบไม่ต้องกดรหัส
    components.html('<iframe width="100%" height="180" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allow="autoplay"></iframe>', height=200)

tabs = st.tabs(["🚀 RADAR", "💬 CHAT", "📞 CALL"])

with tabs[0]: # RADAR
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        if st.button("🛰️ บันทึกพิกัด"):
            db.reference(f'users/{my_id}').update({'lat': lat, 'lon': lon, 'last_update': time.time()})
            st.toast("บันทึกพิกัดแล้ว!")
    
    m = folium.Map(location=[13.75, 100.5], zoom_start=10, tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google")
    try:
        users = db.reference('users').get()
        if users:
            for name, info in users.items():
                folium.Marker([info['lat'], info['lon']], tooltip=name).add_to(m)
    except: pass
    st_folium(m, width="100%", height=400)

with tabs[1]: # CHAT
    chat_ref = db.reference('chats/main_room')
    with st.container(height=300):
        try:
            msgs = chat_ref.order_by_child('timestamp').limit_to_last(15).get()
            if msgs:
                for m_id, m_val in sorted(msgs.items(), key=lambda x: x[1].get('timestamp', 0)):
                    css = "my-msg" if m_val.get('user') == my_id else "other-msg"
                    st.markdown(f"<div class='{css}'><b>{m_val.get('user')}</b>: {m_val.get('text')}</div>", unsafe_allow_html=True)
        except: st.write("เริ่มแชทเลย...")
    
    with st.form("chat", clear_on_submit=True):
        txt = st.text_input("พิมพ์ข้อความ...")
        if st.form_submit_button("ส่ง") and txt:
            chat_ref.push({'user': my_id, 'text': txt, 'timestamp': time.time()})
            st.rerun()

with tabs[2]: # CALL (Agora)
    st.write("🟢 ระบบ Video Call พร้อมใช้งาน (ไม่ต้องใช้รหัส)")
    agora_html = f"""
    <div id="v-box" style="width:100%; height:400px; background:#000; border:1px solid #00ff00;"></div>
    <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.11.0.js"></script>
    <script>
        async function start() {{
            const client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            await client.join("84d8f5f05b0c49e181837f40d7688967", "Synapse_Main", "007eJxTYDjNVVmy0Oluq8PFx7OrOp1l86+W2W9aez+Ir2Fz8pT1+TEKDBYmKRZppmkGpkkGySaWqYYWhhbG5mkmBinmZhYWlmbmcRFrMhsCGRkc/rcxMTJAIIivwOCcn1eWr+voqRtQlJ+Vmlyia2BmamRqqmtgbmBsZGBkxsAAAF8oJtY=", null);
            const [a, v] = await AgoraRTC.createMicrophoneAndCameraTracks();
            v.play('v-box');
            await client.publish([a, v]);
        }}
        start();
    </script>
    """
    components.html(agora_html, height=450)
