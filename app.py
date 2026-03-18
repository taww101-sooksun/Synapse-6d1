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

st.set_page_config(page_title="SYNAPSE", layout="wide")

# --- 2. FIREBASE ---
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
    except: st.error("Firebase Key Error")

# --- 3. SESSION STATE ---
if 'lat' not in st.session_state: st.session_state.lat = 13.7056 # เริ่มต้นที่อ่อนนุช
if 'lon' not in st.session_state: st.session_state.lon = 100.6015

# --- 4. AUDIO PLAYER (เปลี่ยนลิงก์สำรองเพื่อทดสอบ) ---
def synapse_audio_player():
    # ผมใส่ลิงก์เพลงทดสอบที่โหลดติดง่ายกว่าให้ก่อนครับ ถ้าติดแล้วค่อยเปลี่ยนเป็นเพลงพี่
    link = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    st.sidebar.markdown(f"""
        <div style="background:#111; padding:10px; border-radius:10px; border:1px solid #00f2fe; text-align:center;">
            <p style="color:#00f2fe; font-size:12px;">🎵 SYSTEM AUDIO</p>
            <audio controls loop style="width:100%;">
                <source src="{link}" type="audio/mpeg">
            </audio>
        </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN UI ---
with st.sidebar:
    if logo_exists: st.image(logo_path)
    synapse_audio_player()
    st.title("CONTROL")
    user = st.text_input("ID", "AGENT_X")

t1, t2 = st.tabs(["🚀 แกนหลัก", "🛰️ เรดาร์"])

with t1:
    st.header(f"ยินดีต้อนรับ, {user}")
    # ระบบ GPS แบบบังคับดึงค่า
    st.components.v1.html(f"""
        <div style="background:#000; color:#00f2fe; padding:20px; border:1px solid #333; border-radius:10px; font-family:monospace;">
            📍 พิกัดปัจจุบัน: <span id="pos">กำลังจับสัญญาณ...</span>
        </div>
        <script>
            function getLocation() {{
                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(
                        (p) => {{
                            document.getElementById('pos').innerText = p.coords.latitude.toFixed(6) + ", " + p.coords.longitude.toFixed(6);
                        }},
                        (e) => {{ document.getElementById('pos').innerText = "กรุณาเปิด GPS และอนุญาตสิทธิ์"; }},
                        {{ enableHighAccuracy: true }}
                    );
                }}
            }}
            setInterval(getLocation, 2000);
        </script>
    """, height=120)
    
    st.warning("⚠️ ถ้าเลขข้างบนขยับแล้ว ให้พิมพ์เลข 6 หลักมาใส่ช่องข้างล่างนี้ครับ")
    c1, c2 = st.columns(2)
    st.session_state.lat = c1.number_input("ละติจูด (Lat)", value=st.session_state.lat, format="%.6f")
    st.session_state.lon = c2.number_input("ลองจิจูด (Lon)", value=st.session_state.lon, format="%.6f")
    if st.button("📢 UPDATE RADAR"):
        st.success("อัปเดตพิกัดไปหน้าเรดาร์แล้ว!")

with t2:
    st.subheader("🛰️ เรดาร์ตรวจจับ")
    # แผนที่ดาวเทียม Google Hybrid
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=17, 
                   tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Marker([st.session_state.lat, st.session_state.lon], tooltip="คุณอยู่ที่นี่").add_to(m)
    st_folium(m, width="100%", height=500)
