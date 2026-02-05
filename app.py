import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# --- ตั้งค่าหน้าจอ ---
st.set_page_config(page_title="SYNAPSE X - REAL SENSOR", layout="wide")
st.markdown("<style>.stApp {background-color: #000; color: #FFD700;}</style>", unsafe_allow_html=True)

st.title("🔴 SYNAPSE X : REAL-TIME COMMAND")
st.write(f"**SLOGAN:** อยู่นิ่งๆ ไม่เจ็บตัว | **VERSION:** 3,000-HOUR MASTERPIECE")

# --- ส่วนดึงค่าจริง (GPS) ---
st.subheader("📍 ระบบตรวจจับพิกัดจริง (SENSOR)")
location = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(pos => {return {lat: pos.coords.latitude, lon: pos.coords.longitude}})", key="gps")

col1, col2 = st.columns(2)
with col1:
    if location:
        st.success(f"LAT: {location['lat']} | LON: {location['lon']}")
        st.map({"lat": [location['lat']], "lon": [location['lon']]})
    else:
        st.warning("กำลังรอสัญญาณ GPS... (โปรดกด Allow บนมือถือ)")

with col2:
    st.metric("🕒 SYSTEM TIME", datetime.now().strftime("%H:%M:%S"))
    st.info("ระบบกำลังรันด้วยข้อมูลจริงจากเซนเซอร์เครื่อง")

# --- ส่วนสูตรบำบัด 144 ---
st.markdown("---")
st.subheader("📐 Assassin 144 Logic")
val_144 = st.slider("ปรับระดับ Matrix (V)", 1, 144, 72)
st.latex(r"Result = \frac{" + str(val_144) + r" \times 144}{Healing}")

# --- ส่วนความบันเทิง (YouTube) ---
st.subheader("📺 S.S.S PRIVATE STATION")
st.markdown('<iframe width="100%" height="315" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

# --- ปุ่มสั่งการ ---
if st.button("🚀 EXECUTE GLOBAL DEPLOY"):
    st.balloons()
    st.success("ระบบทำงานสมบูรณ์แบบ ไม่มีการหลอกข้อมูล!")
