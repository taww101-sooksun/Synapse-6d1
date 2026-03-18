import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import time
import os

# --- 1. SET UP & THEME ---
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="wide", page_icon="🛰️")

if 'theme_color' not in st.session_state:
    st.session_state.theme_color = "#00f2fe" 

with st.sidebar:
    st.markdown("### 🎨 SYNAPSE CUSTOMIZE")
    st.session_state.theme_color = st.color_picker("เลือกสีนีออนของคุณ", st.session_state.theme_color)
    st.write(f"สถานะระบบ: ONLINE")
    st.write("---")
    st.write('**สโลแกน:** "อยู่นิ่งๆ ไม่เจ็บตัว"')
    
    # --- 2. 🎵 ระบบเสียง (ยักษ์ในตัวฉัน) ---
    st.markdown("### 🎵 AUDIO SYSTEM")
    music_url = "https://docs.google.com/uc?export=download&id=1AhClqXudsgLtFj7CofAUqPqfX8YW1T7a"
    st.audio(music_url, format="audio/mpeg", loop=True)

# ฉีด CSS ตามสีที่พี่เลือก
st.markdown(f"""
    <style>
    .stApp {{ background: #000; color: {st.session_state.theme_color}; }}
    .stButton>button {{ 
        border: 1px solid {st.session_state.theme_color} !important; 
        color: {st.session_state.theme_color} !important; 
        background-color: transparent !important;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 🛰️ เชื่อมต่อ FIREBASE ---
if not firebase_admin._apps:
    try:
        fb_dict = dict(st.secrets["firebase"])
        fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
        creds = credentials.Certificate(fb_dict)
        firebase_admin.initialize_app(creds, {'databaseURL': 'https://notty-101-default-rtdb.asia-southeast1.firebasedatabase.app/'})
    except:
        st.error("🚨 ตรวจสอบ Firebase Secrets ใน Setting")

st.title("🛰️ SYNAPSE COMMAND CENTER")

# --- 4. 🚀 ระบบดึงพิกัดจริงด้วย JS_EVAL ---
loc = get_geolocation()

tabs = st.tabs(["🚀 CORE (แกนหลัก)", "🛰️ RADAR (เรดาร์)"])

with tabs[0]:
    col1, col2 = st.columns([1, 1])
    with col1:
        my_id = st.text_input("ระบุชื่อรหัสของคุณ:", value="Ta101")
        
        if loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            st.success(f"📍 ตรวจพบพิกัดจริง: {lat}, {lon}")
            
            if st.button("🛰️ บันทึกพิกัดลงฐานข้อมูล"):
                db.reference(f'users/{my_id}').update({
                    'lat': lat, 'lon': lon, 'last_update': time.time()
                })
                st.balloons()
                st.toast("บันทึกพิกัดสำเร็จ!")
        else:
            st.warning("🚨 กรุณากด 'อนุญาต' (Allow) การเข้าถึงตำแหน่งบนเบราว์เซอร์ เพื่อให้พิกัดตรงจุด")

with tabs[1]:
    st.subheader("🛰️ ระบบเรดาร์ตรวจจับพิกัดดาวเทียม")
    all_users = db.reference('users').get()
    
    # ตั้งค่าแผนที่เริ่มต้น (ถ้าไม่มีพิกัดเรา ให้ไปอ่อนนุชก่อน)
    view_lat, view_lon = 13.7056, 100.6015
    if all_users and my_id in all_users:
        view_lat = all_users[my_id].get('lat', view_lat)
        view_lon = all_users[my_id].get('lon', view_lon)

    # แผนที่ดาวเทียม Google Satellite (lyrs=y)
    m = folium.Map(location=[view_lat, view_lon], zoom_start=18, 
                   tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", 
                   attr="Google Satellite")

    if all_users:
        for name, info in all_users.items():
            if 'lat' in info and 'lon' in info:
                # 🔵 ตัวคุณ (Ta101) | 🔴 คนอื่น
                color = 'blue' if name == my_id else 'red'
                folium.Marker(
                    [info['lat'], info['lon']], 
                    tooltip=f"ID: {name}",
                    popup=f"พิกัด: {info['lat']}, {info['lon']}",
                    icon=folium.Icon(color=color, icon='star')
                ).add_to(m)
        
    st_folium(m, width="100%", height=600)
