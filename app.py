import streamlit as st

st.set_page_config(page_title="Image Searcher", layout="wide")

# ส่วนที่ 1: ค้นหารูปภาพ (ดึงจาก API จริง)
st.title("🔍 ค้นหารูปภาพจากคีย์เวิร์ด")
st.write("พิมพ์สิ่งที่อยากค้นหา แล้วแอปจะดึงรูปจาก Unsplash มาให้ครับ")

query = st.text_input("ค้นหารูปภาพอะไรดี?", placeholder="เช่น: retro computer, cyberpunk, cat")

if query:
    # แก้ไข: สร้าง Direct Link ที่ใช้งานได้จริง
    # เราจะใช้คำค้นหาไปใส่ใน URL ของ Unsplash Source
    img_url_1 = f"https://source.unsplash.com/featured/800x600?{query.replace(' ', ',')}&sig=1"
    img_url_2 = f"https://source.unsplash.com/featured/800x600?{query.replace(' ', ',')}&sig=2"

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ผลลัพธ์ที่ 1")
        st.image(img_url_1, caption=f"รูปภาพเกี่ยวกับ: {query}", use_container_width=True)
        st.code(img_url_1, language="text")

    with col2:
        st.subheader("ผลลัพธ์ที่ 2")
        st.image(img_url_2, caption=f"รูปภาพเกี่ยวกับ: {query}", use_container_width=True)
        st.code(img_url_2, language="text")

st.divider()

# ส่วนที่ 2: Image Link Previewer (ตรวจเช็คลิงก์ที่มีอยู่แล้ว)
st.title("🖼️ Image Link Previewer")

image_url = st.text_input(
    label="วางลิงก์รูปภาพ (Direct Link) ที่นี่:",
    placeholder="ตัวอย่าง: https://images.unsplash.com/photo-..."
)

if st.button("แสดงรูปภาพ"):
    if image_url:
        try:
            st.image(image_url, caption="ภาพจากลิงก์ของคุณ", use_container_width=True)
            st.success("โหลดรูปภาพสำเร็จ!")
        except Exception as e:
            [span_5](start_span)st.error("ไม่สามารถโหลดรูปภาพได้: กรุณาตรวจสอบว่าเป็น Direct Link ที่ลงท้ายด้วยนามสกุลไฟล์ภาพ")[span_5](end_span)
    else:
        st.warning("กรุณาใส่ลิงก์รูปภาพก่อนกดปุ่มครับ")
