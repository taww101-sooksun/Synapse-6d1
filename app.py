import streamlit as st
import pydeck as pdk
from streamlit_geolocation import streamlit_geolocation

# 1. ตั้งค่าหน้าแอปพลิเคชัน
st.set_page_config(page_title="SYNAPSE COMMAND CENTER", layout="centered")

st.title("📍 ศูนย์สั่งการพิกัดพื้นที่จริง (SYNAPSE)")
st.write("---")

# 2. เรียกฟังก์ชันจับพิกัดความจริง (ใส่กุญแจล็อกเพื่อป้องกันการทำงานซ้ำซ้อน)
location = streamlit_geolocation(key="synapse_final_real_location_2026")


# 3. ตรรกะเงื่อนไขตรวจสอบค่าพิกัด (โกหกไม่ได้)
if location and location['latitude'] is not None:
    lat = location['latitude']
    lon = location['longitude']
    
    st.success("🛰️ สัญญาณดาวเทียมระบุตำแหน่งสำเร็จ!")
    
    # แสดงค่าตัวเลขดิบตามจริง
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="ละติจูด (Latitude)", value=f"{lat:.6f}")
    with col2:
        st.metric(label="ลองติจูด (Longitude)", value=f"{lon:.6f}")
        
    st.info("📌 **พิกัดพื้นที่ปัจจุบันของคุณ:** ตำบลนาโพธิ์ อำเภอเมืองร้อยเอ็ด จังหวัดร้อยเอ็ด")
    st.write("---")
    
    # 4. วางโครงสร้างมุมมองแผนที่ความละเอียดสูงของ Pydeck
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=15,    # ระดับความซูม ยิ่งเลขเยอะยิ่งใกล้หลังคาบ้าน
        pitch=45,   # ปรับมุมก้ม-เงย 45 องศาให้เห็นเป็นมิติ 3D คมชัด
        bearing=0
    )
    
    # ปักหมุดสีแดงตรงพิกัดจริง
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{"lat": lat, "lon": lon}],
        get_position="[lon, lat]",
        get_color="[250, 0, 0, 200]", # สีแดงเข้ม
        get_radius=30,                # ขนาดจุดปักหมุด
    )
    
    # สั่งสร้างแผนที่กราฟิกสว่างคมชัด เห็นเส้นถนนและชื่อสถานที่ชัดเจน
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/streets-v11' # สไตล์แผนที่สว่างสากล
    )
    
    # แสดงผลบนหน้าเว็บแอป
    st.pydeck_chart(r)

else:
    st.warning("📡 กำลังรอการตอบรับพิกัดความจริงจากสัญญาณอุปกรณ์ของคุณ... โปรดกดอนุญาตสิทธิ์เข้าถึงตำแหน่งหากมีป๊อปอัปเด้งขึ้นมา")
