import streamlit as st
# โค้ดส่วนนี้เป็นตัวอย่างการดึงปลั๊กอินพิกัด
from streamlit_geolocation import streamlit_geolocation

st.title("📍 ระบบตรวจสอบพิกัดจริงบนโลก (โกหกไม่ได้)")

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
