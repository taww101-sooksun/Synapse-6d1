import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation

# 1. ตั้งค่าหน้าแอป
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="centered")
st.title("📍 ศูนย์สั่งการพิกัดพื้นที่จริง (SYNAPSE - ดาวเทียม)")
st.write("---")

# 2. เรียกฟังก์ชันจับพิกัดความจริง (ใส่กุญแจแยกเพื่อป้องกันระบบซ้ำซ้อน)
location = streamlit_geolocation(key="synapse_google_satellite_location_2026")

# 3. ต้องเช็คเงื่อนไขและสร้างตัวแปรก่อน ถึงจะเอาไปใช้ในแผนที่ได้ (ห้ามสลับลำดับ)
if location and location['latitude'] is not None:
    # สร้างตัวแปรแกะค่าพิกัดจริงออกมารองรับไว้ก่อน
    lat = location['latitude']
    lon = location['longitude']
    
    st.success("🛰️ สัญญาณดาวเทียมระบุตำแหน่งสำเร็จ!")
    st.write(f"🌐 **พิกัดปัจจุบันของคุณ:** {lat}, {lon}")
    st.info("📌 **พื้นที่ปัจจุบันของคุณ:** ตำบลนาโพธิ์ อำเภอเมืองร้อยเอ็ด จังหวัดร้อยเอ็ด")
    st.write("---")
    
    # 4. พอมีตัวแปร lat, lon แล้ว ถึงจะสั่งสร้างแผนที่ดาวเทียม Google Maps ชัดๆ ได้
    m = folium.Map(
        location=[lat, lon], # คอมพิวเตอร์อ่านตรงนี้จะรู้ทันทีว่า lat, lon คืออะไรเพราะสร้างไว้ด้านบนแล้ว
        zoom_start=18,        # ซูมลึกระดับเห็นหลังคาบ้าน
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", # ภาพดาวเทียมผสมชื่อถนนของ
