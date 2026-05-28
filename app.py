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
    
    # 2. สร้างแผนที่แบบสว่าง มีชื่อถนน มีชื่อสถานที่ชัดเจนด้วย Folium
    # โดยตั้งค่าให้ดึงแผนที่มาตรฐานแบบ OpenStreetMap (สว่างและเห็นเส้นทางชัด)
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles="OpenStreetMap")
    
    # ปักหมุดตรงจุดที่เราอยู่ พร้อมป้ายบอก
    folium.Marker(
        [lat, lon], 
        popup="ตำแหน่งจริงของคุณ ณ วินาทีนี้",
        tooltip="คุณอยู่ที่นี่"
    ).add_to(m)
    
    # สั่งวาดแผนที่ลงหน้าแอป SYNAPSE
    st_folium(m, width=700, height=500)

else:
    st.info("กำลังรับสัญญาณดาวเทียมเพื่อระบุตำแหน่งพิกัดจริง...")
