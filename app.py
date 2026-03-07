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

# --- 2. FIREBASE CONNECTION ---
if not firebase_admin._apps:
    try:
        if "firebase" in st.secrets:
            fb_dict = dict(st.secrets["firebase"])
            # จัดการเรื่องขึ้นบรรทัดใหม่ของ Private Key ให้ถูกต้อง
            fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
            creds = credentials.Certificate(fb_dict)
            
            # เชื่อมต่อด้วย URL ของคุณจริงๆ
            firebase_admin.initialize_app(creds, {
                'databaseURL': 'https://sooksun1-default-rtdb.asia-southeast1.firebasedatabase.app/'
            })
            st.toast("📡 เชื่อมต่อฐานข้อมูลสำเร็จ", icon="✅")
        else:
            st.error("🔑 ไม่พบข้อมูล 'firebase' ใน Streamlit Secrets")
    except Exception as e:
        st.error(f"⚠️ Firebase Connection Error: {e}")

# --- 3. SIDEBAR ---
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

# --- 4. CORE SYSTEM (Tabs) ---
st.title("SYNAPSE COMMAND CENTER")
tabs = st.tabs(["🚀 RADAR & GPS", "💬 LIVE CHAT"])

# TAB 1: RADAR & GPS
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
                st.error(f"⚠️ Error: {e}")
        
        # แสดงแผนที่ 
        m = folium.Map(location=[lat, lon], zoom_start=15, tiles="CartoDB dark_matter")
        folium.Marker([lat, lon], popup=f"Me: {my_id}", icon=folium.Icon(color='green')).add_to(m)
        st_folium(m, width=700, height=400)
    else:
        st.info("⏳ กำลังค้นหาสัญญาณดาวเทียม... (อย่าลืมกด Allow Location บนเบราว์เซอร์ด้วยนะ)")

# TAB 2: LIVE CHAT ROOM
with tabs[1]:
    st.subheader("💬 REAL-TIME CHAT")
    
    # เช็คว่าต่อ Firebase ติดแล้วค่อยดึงข้อมูลมาแสดง
    if firebase_admin._apps:
        chat_ref = db.reference('chat')
        
        # กล่องพิมพ์ข้อความ
        with st.container():
            msg_input = st.text_input("พิมพ์ข้อความที่นี่...", key="chat_in")
            if st.button("ส่งข้อความ") and msg_input:
                chat_ref.push({
                    'user': my_id,
                    'msg': msg_input,
                    'time': time.time()
                })
                st.rerun()

        st.write("---")
        
        # ดึง 10 ข้อความล่าสุดมาแสดง
        try:
            messages = chat_ref.order_by_child('time').limit_to_last(10).get()
            if messages:
                # เรียงเวลาให้ชัวร์ว่าข้อความเก่าอยู่บน ข้อความใหม่อยู่ล่าง
                sorted_msgs = sorted(messages.values(), key=lambda x: x.get('time', 0))
                for val in sorted_msgs:
                    cls = "my-msg" if val['user'] == my_id else "other-msg"
                    st.markdown(f'<div class="{cls}"><b>{val["user"]}</b>: {val["msg"]}</div>', unsafe_allow_html=True)
            else:
                st.caption("ยังไม่มีข้อความในระบบ เริ่มทักทายได้เลย!")
        except Exception as e:
            st.error(f"ไม่สามารถดึงข้อความได้: {e}")
    else:
        st.warning("⚠️ ระบบแชตยังไม่พร้อมใช้งาน (เช็คการตั้งค่า Firebase)")
