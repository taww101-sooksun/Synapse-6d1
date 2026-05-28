import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import streamlit as st
# อิมพอร์ต pydeck เข้ามาตรงๆ ตัวเต็ม
import pydeck as pdk 
from streamlit_geolocation import streamlit_geolocation

st.title("📍 ศูนย์สั่งการพิกัดพื้นที่จริง (ระบบ Pydeck)")

location = streamlit_geolocation()

if location and location['latitude'] is not None:
    lat = location['latitude']
    lon = location['longitude']
    
    st.success("จับพิกัดความจริงได้สำเร็จ!")
    st.write(f"🌐 **พิกัดปัจจุบัน:** {lat}, {lon}")
    
    # วางโครงสร้างมุมมองแผนที่ (ตั้งค่าพิกัดความจริงของเราลงไป)
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=15,    # ระดับความซูม ยิ่งเยอะยิ่งใกล้หลังคาบ้าน
        pitch=45,   # ปรับมุมก้ม-เงย (ใส่ 45 จะเห็นเป็นมิติ 3D แบบเอียงๆ สวยมาก)
        bearing=0   # มุมหันหน้าทิศเหนือทิศใต้
    )
    
    # สั่งวาดแผนที่ความละเอียดสูง
    r = pdk.Deck(
        initial_view_state=view_state,
        # ใช้สไตล์แผนที่แบบสว่าง เห็นถนนและชื่อสถานที่ชัดเจนของ Mapbox
        map_style='mapbox://styles/mapbox/streets-v11', 
    )
    
    # แสดงผลบนหน้าจอแอป SYNAPSE
    st.pydeck_chart(r)

else:
    st.info("กำลังรับสัญญาณดาวเทียมเพื่อระบุตำแหน่งพิกัดจริง...")

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
