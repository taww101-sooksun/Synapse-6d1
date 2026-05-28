import streamlit as st
from streamlit_geolocation import streamlit_geolocation
# เพิ่มเครื่องมือทำแผนที่สว่างและละเอียด (ต้องใส่ใน requirements.txt ด้วยนะ)
import folium
from streamlit_folium import st_folium

st.title("📍 ศูนย์สั่งการพิกัดพื้นที่จริง")

location = streamlit_geolocation()

if location and location['latitude'] is not None:
    lat = location['latitude']
    lon = location['longitude']
    
    st.success("จับพิกัดความจริงได้สำเร็จ!")
    
    # 1. แสดงตัวเลขพิกัดที่โกหกไม่ได้
    st.write(f"🌐 **พิกัดตรงนี้คือ:** {lat}, {lon}")
    st.write("📌 **พื้นที่ปัจจุบันของคุณ:** ตำบลนาโพธิ์ อำเภอเมืองร้อยเอ็ด จังหวัดร้อยเอ็ด")
    
# เปลี่ยนบรรทัดสร้างแผนที่เดิม ให้กลายเป็นแผนที่ดาวเทียม Google Maps ชัดๆ
m = folium.Map(
    location=[lat, lon], 
    zoom_start=18, # ซูมเข้าไปลึกๆ ระดับ 18-19 จะเห็นหลังคาบ้านชัดเจน
    tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", # ลิงก์ดึงภาพดาวเทียม Google
    attr="Google Satellite"
)

