import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import time
import datetime
import streamlit.components.v1 as components

# --- 1. SETTING & UI THEME ---
st.set_page_config(page_title="SYNAPSE COMMAND", layout="wide", page_icon="🛰️")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #00ff00; }
    /* กล่อง Container หลัก */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(0, 30, 0, 0.4);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00ff00;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
        margin-bottom: 10px;
    }
    /* สไตล์ข้อความแชท */
    .my-msg { text-align: right; color: #00ff00; background: rgba(0,255,0,0.1); padding: 10px; border-radius: 10px; margin-bottom: 5px; border-right: 4px solid #00ff00; }
    .other-msg { text-align: left; color: #ffffff; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; margin-bottom: 5px; border-left: 4px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FIREBASE CONNECTION ---
if not firebase_admin._apps:
    try:
        if "firebase" in st.secrets:
            fb_dict = dict(st.secrets["firebase"])
            # แก้ไขเรื่อง Private Key ให้รองรับรูปแบบบรรทัดใหม่
            if "private_key" in fb_dict:
                fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
            
            creds = credentials.Certificate(fb_dict)
            firebase_admin.initialize_app(creds, {
                'databaseURL': 'https://sooksun1-default-rtdb.asia-southeast1.firebasedatabase.app/'
            })
            st.toast("📡 ระบบเชื่อมต่อฐานข้อมูลสำเร็จ", icon="✅")
        else:
            st.error("🔑 ไม่พบข้อมูล 'firebase' ใน Secrets! (กรุณาตั้งค่าใน Streamlit Cloud)")
    except Exception as e:
        st.error(f"⚠️ Firebase Connection Error: {e}")

# --- 3. CONFIG & PARAMETERS ---
AGORA_APP_ID = "84d8f5f05b0c49e181837f40d7688967"
AGORA_TOKEN = "007eJxTYDjNVVmy0Oluq8PFx7OrOp1l86+W2W9aez+Ir2Fz8pT1+TEKDBYmKRZppmkGpkkGySaWqYYWhhbG5mkmBinmZhYWlmbmcRFrMhsCGRkc/rcxMTJAIIivwOCcn1eWr+voqRtQlJ+Vmlyia2BmamRqqmtgbmBsZGBkxsAAAF8oJtY="
CHANNEL_NAME = "Synapse_Main"

# --- 4. SIDEBAR PANEL ---
with st.sidebar:
    st.title("🛰️ COMMAND PANEL")
    my_id = st.text_input("ระบุรหัส (ID):", value="Ta101")
    st.divider()
    
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

# --- TAB 1: RADAR & GPS ---
with tabs[0]:
    loc = get_geolocation()
    if loc and 'coords' in loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        st.success(f"📍 พิกัดปัจจุบัน: {lat}, {lon}")
        if st.button("🛰️ บันทึกพิกัดลงเรดาร์"):
            try:
                db.reference(f'users/{my_id}').update({
                    'lat': lat, 
                    'lon': lon, 
                    'last_update': time.time(),
                    'time_str': datetime.datetime.now().strftime("%H:%M")
                })
                st.toast("บันทึกพิกัดแล้ว!", icon="🛰️")
            except Exception as e:
                st.error(f"Database Error: {e}")
    else:
        st.info("💡 กรุณากดยอมรับการเข้าถึง Location เพื่อเปิดระบบเรดาร์")

    st.subheader("🌐 GLOBAL RADAR MAP")
    # ตั้งค่าเริ่มต้นที่กรุงเทพฯ
    m = folium.Map(location=[13.75, 100.5], zoom_start=10, tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google Satellite")
    
    try:
        users_data = db.reference('users').get()
        if users_data:
            for name, info in users_data.items():
                if 'lat' in info and 'lon' in info:
                    # เช็คสถานะ Active (ภายใน 10 นาที)
                    is_active = (time.time() - info.get('last_update', 0)) < 600
                    status_color = 'green' if is_active else 'red'
                    folium.Marker(
                        [info['lat'], info['lon']], 
                        popup=f"{name} ({info.get('time_str', '??')})",
                        tooltip=f"User: {name}",
                        icon=folium.Icon(color=status_color, icon='info-sign')
                    ).add_to(m)
    except:
        pass
    
    st_folium(m, width="100%", height=400)

# --- TAB 2: CHAT ROOM ---
with tabs[1]:
    st.subheader("💬 ENCRYPTED CHAT")
    try:
        chat_ref = db.reference('chats/main_room')
        msgs_data = chat_ref.order_by_child('timestamp').limit_to_last(20).get()
        
        # ส่วนแสดงข้อความ
        with st.container(height=400):
            if msgs_data:
                # เรียงข้อความตามเวลา (Firebase บางทีคืนค่าเป็น Dict ที่ไม่เรียง)
                sorted_msgs = sorted(msgs_data.items(), key=lambda x: x[1].get('timestamp', 0))
                for m_id, m_val in sorted_msgs:
                    u_name = m_val.get('user', 'Unknown')
                    u_text = m_val.get('text', '')
                    css_class = "my-msg" if u_name == my_id else "other-msg"
                    st.markdown(f"<div class='{css_class}'><b>{u_name}</b>: {u_text}</div>", unsafe_allow_html=True)
            else:
                st.caption("ยังไม่มีข้อความ... เริ่มคุยกันเลย")

        # ส่วนส่งข้อความ
        with st.form("send_chat", clear_on_submit=True):
            c1, c2 = st.columns([8, 2])
            chat_input = c1.text_input("พิมพ์ข้อความ...", label_visibility="collapsed")
            if c2.form_submit_button("ส่ง 🚀") and chat_input:
                chat_ref.push({
                    'user': my_id,
                    'text': chat_input,
                    'timestamp': time.time()
                })
                st.rerun()
    except Exception as e:
        st.warning(f"ระบบแชทขัดข้อง: {e}")

# --- TAB 3: TELE-CALL (Agora Integration) ---
with tabs[2]:
    st.subheader("📞 AGORA REAL-TIME CALL")
    st.warning("⚠️ โปรดทราบ: กล้องจะทำงานเมื่อเข้าถึงผ่าน https:// เท่านั้น")
    
    # Agora HTML/JS Component
    agora_ui = f"""
    <div id="video-box" style="width: 100%; height: 450px; background: #000; border: 2px solid #00ff00; border-radius: 10px; overflow: hidden; position: relative;">
        <div id="local-view" style="width: 100%; height: 100%;"></div>
        <div style="position: absolute; bottom: 10px; left: 10px; color: #00ff00; background: rgba(0,0,0,0.6); padding: 5px; font-family: monospace;">
            📡 LIVE_STREAM_ID: {my_id}
        </div>
    </div>
    <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.11.0.js"></script>
    <script>
        async function startCall() {{
            const client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            try {{
                await client.join("{AGORA_APP_ID}", "{CHANNEL_NAME}", "{AGORA_TOKEN}", null);
                const [audioTrack, videoTrack] = await AgoraRTC.createMicrophoneAndCameraTracks();
                videoTrack.play('local-view');
                await client.publish([audioTrack, videoTrack]);
                console.log("Joined and Published!");
            }} catch (e) {{
                console.error("Agora Error:", e);
            }}
        }}
        startCall();
    </script>
    """
    components.html(agora_ui, height=500)
    st.info(f"🟢 สถานะ: กำลังสแตนด์บายในช่อง {CHANNEL_NAME}")

