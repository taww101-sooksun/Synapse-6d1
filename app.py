import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
import os
import folium
from streamlit_folium import st_folium

# --- 1. CONFIG ---
logo_path = "logo3.jpg"
logo_exists = os.path.exists(logo_path)

st.set_page_config(page_title="SYNAPSE IDENTITY", layout="wide", page_icon="🌐")

# --- 2. FIREBASE (Asia Southeast 1) ---
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
    except: st.error("Firebase Connection Error - เช็คหน้า Secrets อีกทีครับพี่")

# --- 3. SESSION STATE ---
if 'lat' not in st.session_state: st.session_state.lat = 13.7056 # ค่าเริ่มต้นที่อ่อนนุช
if 'lon' not in st.session_state: st.session_state.lon = 100.6015
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 4. AUDIO PLAYER (Direct Link จาก Drive พี่) ---
def synapse_audio_player():
    # ลิงก์เพลงที่พี่ส่งมา (แปลงเป็น Direct Download)
    link = "https://docs.google.com/uc?export=download&id=1MfeP1CbRRMI-VSCBoHLoF2kny0cCc2VY"
    st.sidebar.markdown(f"""
        <div style="background:rgba(0,0,0,0.6); padding:15px; border-radius:15px; border:1px solid #00f2fe; text-align:center;">
            <p style="color:#00f2fe; font-weight:bold; margin-bottom:10px;">🎵 SYNAPSE AUDIO</p>
            <audio id="player" loop controls style="width:100%; filter: invert(100%) hue-rotate(180deg);">
                <source src="{link}" type="audio/mpeg">
            </audio>
        </div>
        <script>
            var a = document.getElementById("player");
            window.parent.document.addEventListener('click', function() {{ 
                if (a.paused) {{ a.play(); }}
            }}, {{ once: true }});
        </script>
    """, unsafe_allow_html=True)

# --- 5. LOGIN UI ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00f2fe;'>🌐 SYNAPSE IDENTITY</h1>", unsafe_allow_html=True)
    pw = st.text_input("SECURITY KEY", type="password")
    if st.button("🚀 ACCESS SYSTEM"):
        if pw == "notty101":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 6. MAIN APP ---
with st.sidebar:
    if logo_exists: st.image(logo_path)
    synapse_audio_player()
    user_id = st.text_input("AGENT ID", "AGENT_X")
    if st.button("LOGOUT"): st.session_state.logged_in = False; st.rerun()

t1, t2, t3 = st.tabs(["🚀 แกนหลัก", "🛰️ เรดาร์", "💬 สื่อสาร"])

with t1:
    st.header(f"ยินดีต้อนรับ, {user_id}")
    # ดึงพิกัด Real-time จาก Browser
    st.components.v1.html(f"""
        <div style="background:#000; color:#00f2fe; padding:15px; border:1px solid #333; border-radius:10px; font-family:monospace; font-size:18px;">
            📍 LIVE GPS: <span id="pos">กำลังค้นหาสัญญาณดาวเทียม...</span>
        </div>
        <script>
            function getLoc() {{
                navigator.geolocation.getCurrentPosition(p => {{
                    const lat = p.coords.latitude.toFixed(6);
                    const lon = p.coords.longitude.toFixed(6);
                    document.getElementById('pos').innerText = lat + ", " + lon;
                    // ส่งค่ากลับไปให้ Streamlit (Hidden Input)
                    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: {{lat:lat, lon:lon}}}}, '*');
                }}, null, {{enableHighAccuracy:true}});
            }}
            setInterval(getLoc, 2000);
        </script>
    """, height=100)
    
    st.info("💡 พิกัดจะอัปเดตทุก 2 วินาที (กรุณายืนยันตำแหน่งด้านล่างเพื่อล็อคเป้าบนเรดาร์)")
    c1, c2 = st.columns(2)
    st.session_state.lat = c1.number_input("ละติจูด", value=st.session_state.lat, format="%.6f")
    st.session_state.lon = c2.number_input("ลองจิจูด", value=st.session_state.lon, format="%.6f")
    
    if st.button("📢 UPDATE TO RADAR"):
        db.reference('logs/pos').push({'user': user_id, 'lat': st.session_state.lat, 'lon': st.session_state.lon, 'ts': time.time()})
        st.success("ล็อคเป้าหมายเรียบร้อย!")

with t2:
    st.subheader("🛰️ ระบบเรดาร์ (Google Hybrid)")
    # แผนที่ดาวเทียมซูมระดับ 18
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=18, 
                   tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Marker([st.session_state.lat, st.session_state.lon], popup="คุณอยู่ที่นี่", icon=folium.Icon(color='red')).add_to(m)
    st_folium(m, width="100%", height=500)

with t3: # Jitsi ฆ่าติ่ง Join
    target = st.text_input("คู่สาย:", "User2")
    if st.button("📹 START CALL"):
        room = f"Synapse_{user_id}_{target}"
        st.components.v1.html(f"""
        <div id="j" style="height:500px; width:100%; border:1px solid #00f2fe;"></div>
        <script src="https://meet.jit.si/external_api.js"></script>
        <script>
            new JitsiMeetExternalAPI('meet.jit.si', {{
                roomName: '{room}', parentNode: document.querySelector('#j'),
                configOverwrite: {{ prejoinPageEnabled: false }},
                interfaceConfigOverwrite: {{ SHOW_JITSI_WATERMARK: false }}
            }});
        </script>
        """, height=550)
