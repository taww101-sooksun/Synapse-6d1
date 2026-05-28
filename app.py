import streamlit as st
import pdk  # เป็นแพ็คเกจย่อยของ pydeck ที่มีติดมากับ Streamlit อยู่แล้ว
from streamlit_geolocation import streamlit_geolocation

location = streamlit_geolocation()

if location and location['latitude'] is not None:
    lat = location['latitude']
    lon = location['longitude']
    
    # สร้างข้อมูลพิกัดในรูปแบบที่ pydeck เข้าใจ
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=16, # ระดับความซูม
        pitch=0
    )
    
    # วาดแผนที่กราฟิกความละเอียดสูง (สไตล์ถนนและสถานที่ชัดเจน)
    r = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v11', # ใช้สไตล์ถนนที่คมชัดของ Mapbox
        initial_view_state=view_state
    )
    
    st.pydeck_chart(r)
