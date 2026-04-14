import streamlit as st

st.set_page_config(page_title="Image Searcher", layout="wide")

# ส่วนหัวของแอป
st.title("🔍 ค้นหารูปภาพระดับ HD")
st.write("พิมพ์สิ่งที่ต้องการค้นหา เพื่อดึงรูปภาพมาใช้ในโปรเจกต์ของคุณ")

# 1. ช่องกรอกคำค้นหา
query = st.text_input("ค้นหารูปภาพอะไรดี?", placeholder="เช่น: nature, technology, abstract")

if query:
    # ใช้ Unsplash Source API เพื่อดึงรูปภาพโดยตรง (Direct Link)
    # ขนาด 800x600 px
    image_url_1 = f"https://source.unsplash.com/featured/800x600?{query}&1"
    image_url_2 = f"https://source.unsplash.com/featured/800x600?{query}&2"

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ผลลัพธ์ที่ 1")
        st.image(image_url_1, caption=f"Keyword: {query}", use_container_width=True)
        st.code(image_url_1, language="text")

    if image_url:
          try:
        st.image(image_url, caption="ภาพจากลิงก์ของคุณ", use_container_width=True)
        st.success("โหลดรูปภาพสำเร็จ!")  # เขียนแค่แบบนี้พอครับ
    except Exception as e:
        st.error(f"ไม่สามารถโหลดรูปภาพได้: {e}")


st.divider()

# 2. ส่วน Preview จากลิงก์ที่คุณมีอยู่แล้ว
st.title("🖼️ Image Link Previewer")
image_url_input = st.text_input("วางลิงก์รูปภาพ (Direct Link) ที่นี่:", placeholder="https://example.com/image.jpg")

if st.button("ตรวจสอบรูปภาพ"):
    if image_url_input:
        try:
            st.image(image_url_input, caption="ตัวอย่างรูปภาพจากลิงก์", use_container_width=True)
            [span_4](start_span)st.success("โหลดรูปภาพสำเร็จ!")[span_4](end_span)
        except:
            [span_5](start_span)st.error("ไม่สามารถโหลดรูปภาพได้: โปรดตรวจสอบว่าเป็น Direct Link (.jpg, .png, .webp)")[span_5](end_span)
