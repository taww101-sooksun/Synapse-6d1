import streamlit as st
import folium  # ต้องมีบรรทัดนี้ ไม่งั้นมันจะฟ้อง Error บรรทัดที่ 7 ทันที
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation

# ... แล้วค่อยตามด้วยโค้ดตั้งค่าแผนที่ด้านล่าง ...

import streamlit as st
# โค้ดส่วนนี้เป็นตัวอย่างการดึงปลั๊กอินพิกัด
from streamlit_geolocation import streamlit_geolocation

st.title("📍 ระบบตรวจสอบพิกัดจริงบนโลก (โกหกไม่ได้)")
# เปลี่ยนบรรทัดสร้างแผนที่เดิม ให้กลายเป็นแผนที่ดาวเทียม Google Maps ชัดๆ
m = folium.Map(
    location=[lat, lon], 
    zoom_start=18, # ซูมเข้าไปลึกๆ ระดับ 18-19 จะเห็นหลังคาบ้านชัดเจน
    tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", # ลิงก์ดึงภาพดาวเทียม Google
    attr="Google Satellite"
)

# สั่งให้แอปดึงพิกัดจากชิป GPS หรือสัญญาณอินเทอร์เน็ตของอุปกรณ์
location = streamlit_geolocation()

# ตรวจสอบว่าได้ค่ามาหรือยัง
if location and location['latitude'] is not None:
    lat = location['latitude']
    lon = location['longitude']
    
    st.success("จับสัญญาณพิกัดได้สำเร็จ!")
    st.write(f"**ละติจูด (Latitude):** {lat}")
    st.write(f"**ลองติจูด (Longitude):** {lon}")
    
    # เอาตัวเลขพิกัดความจริงนี้ ไปเปิดบนแผนที่โลกให้เห็นตำแหน่งเลย
    st.map(data=[{"lat": lat, "lon": lon}])

else:
    st.info("กำลังรอการอนุญาตเข้าถึงพิกัด GPS จากอุปกรณ์ของคุณ...")
