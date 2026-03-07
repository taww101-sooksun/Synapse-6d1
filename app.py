import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import time
import streamlit.components.v1 as components

# --- 1. SETTING & DARK MODE (Green Glow) ---
st.set_page_config(page_title="SYNAPSE COMMAND", layout="wide", page_icon="🛰️")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #00ff00; }
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(0, 30, 0, 0.4);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00ff00;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
    }
    .my-msg { text-align: right; color: #00ff00; background: rgba(0,255,0,0.1); padding: 10px; border-radius: 10px; margin-bottom: 5px; border-right: 4px solid #00ff00; }
    .other-msg { text-align: left; color: #ffffff; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; margin-bottom: 5px; border-left: 4px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FIREBASE CONNECTION (ป้องกันพังด้วย Try-Except) ---
if not firebase_admin._apps:
    try:
        if "firebase" in st.secrets:
            fb_dict = dict(st.secrets["firebase"])
            fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
            creds = credentials.Certificate(fb_dict)
            
            # ความจริง: URL นี้ต้องตรงกับใน Firebase Console ของคุณเป๊ะๆ
            firebase_admin.initialize_app(creds, {
                'databaseURL': 'https://sooksun1-default-rtdb.asia-southeast1.firebasedatabase.app/'
            })
            st.toast("📡 เชื่อมต่อฐานข้อมูลสำเร็จ", icon="✅")
        else:
            st.error("🔑 ไม่พบข้อมูล 'firebase' ใน Streamlit Secrets")
    except Exception as e:
        st.error(f"⚠️ Firebase Connection Error: {e}")

# --- 3. AGORA CONFIG (ข้อมูลที่คุณให้มา) ---
AGORA_APP_ID = "84d8f5f05b0c49e181837f40d7688967"
AGORA_TOKEN = "007eJxTYDjNVVmy0Oluq8PFx7OrOp1l86+W2W9aez+Ir2Fz8pT1+TEKDBYmKRZppmkGpkkGySaWqYYWhhbG5mkmBinmZhYWlmbmcRFrMhsCGRkc/rcxMTJAIIivwOCcn1eWr+voqRtQlJ+Vmlyia2BmamRqqmtgbmBsZGBkxsAAAF8oJtY="
CHANNEL_NAME = "Synapse_Main"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🛰️ COMMAND PANEL")
    my_id = st.text_input("รหัส (ID):", value="Ta101")
    st.write("---")
    st.subheader("🎵 SYNAPSE PLAYER")
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    components.html(
        f'<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list={playlist_id}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
        height=220
    )
    st.caption("🎧 'อยู่นิ่งๆ ไม่เจ็บตัว' | BY Ta101")

# --- 5. CORE SYSTEM (Tabs) ---
st.title("SYNAPSE COMMAND CENTER")
tabs = st.tabs(["🚀 RADAR & GPS", "💬 CHAT ROOM", "📞 TELE-CALL"])

# TAB 1: RADAR & GPS (ป้องกัน Error NotFound)
with tabs[0]:
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        st.success(f"📍 พิกัดปัจจุบัน: {lat}, {lon}")
        if st.button("🛰️ บันทึกพิกัดลงเรดาร์"):
            try:
                db.reference(f'users/{my_id}').update({
                    'lat': lat, 'lon': lon, 'last_update': time.time()
                })
                st.toast("พิกัดถูกบันทึกแล้ว!", icon="🛰️")
            except Exception as e:
                st.error(f"ไม่สามารถบันทึกได้: เช็กการตั้งค่า Database URL")

    # แผนที่ดาวเทียม (Folium) ไม่ต้องผูกบัตร
    st.subheader("🌐 GLOBAL RADAR MAP")
    m = folium.Map(location=[13.75, 100.5], zoom_start=10, tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google")
    try:
        users_data = db.reference('users').get()
        if users_data:
            for name, info in users_data.items():
                if 'lat' in info and 'lon' in info:
                    # ถ้าอัปเดตล่าสุดไม่เกิน 10 นาที ให้เป็นสีเขียว
                    is_active = (time.time() - info.get('last_update', 0)) < 600
                    color = 'green' if is_active else 'red'
                    folium.Marker([info['lat'], info['lon']], tooltip=name, icon=folium.Icon(color=color)).add_to(m)
    except: pass
    st_folium(m, width="100%", height=400)

# TAB 2: CHAT ROOM
with tabs[1]:
    st.subheader("💬 ENCRYPTED CHAT")
    try:
        chat_ref = db.reference('chats/main_room')
        msgs = chat_ref.order_by_child('timestamp').limit_to_last(15).get() or {}
        
        with st.container(height=350):
            for m_id, m_val in sorted(msgs.items(), key=lambda x: x[1].get('timestamp', 0)):
                css = "my-msg" if m_val.get('user') == my_id else "other-msg"
                st.markdown(f"<div class='{css}'><b>{m_val.get('user')}</b>: {m_val.get('text')}</div>", unsafe_allow_html=True)
        
        with st.form("send_chat", clear_on_submit=True):
            col1, col2 = st.columns([8, 2])
            txt = col1.text_input("พิมพ์ข้อความ...", label_visibility="collapsed")
            if col2.form_submit_button("ส่ง 🚀") and txt:
                chat_ref.push({'user': my_id, 'text': txt, 'timestamp': time.time()})
                st.rerun()
    except:
        st.warning("⚠️ ระบบแชตขัดข้อง: ตรวจสอบการเชื่อมต่อฐานข้อมูล")

# TAB 3: TELE-CALL (Agora READY)
with tabs[2]:
    st.subheader("📞 AGORA REAL-TIME CALL")
    # โค้ด HTML/JS เรียกใช้ Agora SDK แบบสมบูรณ์
    agora_ui = f"""
    <div id="video-box" style="width: 100%; height: 450px; background: #000; border: 2px solid #00ff00; border-radius: 10px; overflow: hidden; position: relative;">
        <div id="local-view" style="width: 100%; height: 100%;"></div>
        <div style="position: absolute; bottom: 10px; left: 10px; color: #00ff00; background: rgba(0,0,0,0.6); padding: 5px;">LIVE | {my_id}</div>
    </div>
    <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.11.0.js"></script>
    <script>
        async function runCall() {{
            const client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            try {{
                await client.join("{AGORA_APP_ID}", "{CHANNEL_NAME}", "{AGORA_TOKEN}", null);
                const [audio, video] = await AgoraRTC.createMicrophoneAndCameraTracks();
                video.play('local-view');
                await client.publish([audio, video]);
                console.log("Agora Connected!");
            }} catch (err) {{
                console.error("Agora Failed:", err);
            }}
        }}
        runCall();
    </script>
    """
    components.html(agora_ui, height=500)
    st.info(f"🟢 สถานะ: กำลังเชื่อมต่อช่อง {CHANNEL_NAME}")
