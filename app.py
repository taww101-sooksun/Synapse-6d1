import streamlit as st
import streamlit as st

st.set_page_config(page_title="Image Searcher", layout="wide")

st.title("🔍 ค้นหารูปภาพจากคีย์เวิร์ด")
st.write("พิมพ์สิ่งที่อยากค้นหา (ภาษาอังกฤษจะแม่นยำกว่า) แล้วแอปจะดึงรูปที่ชัดที่สุดมาให้ครับ")

# 1. ช่องกรอกคำค้นหา
query = st.text_input("ค้นหารูปภาพอะไรดี?", placeholder="เช่น: retro computer, cyberpunk, cat")

if query:
    # สร้างลิงก์ค้นหาจาก Unsplash Source (วิธีที่ง่ายและชัดที่สุด)
    # รูปแบบ: https://unsplash.com?<keyword>
    # หมายเหตุ: ปัจจุบัน Unsplash เปลี่ยนมาใช้ระบบใหม่ แนะนำใช้ลิงก์ด้านล่างนี้แทนครับ
    search_url = f"https://unsplash.com{query}"
    
    # ลิงก์สำหรับดึงรูปสุ่มตามคีย์เวิร์ดที่ชัดระดับ HD
    random_image_url = f"https://loremflickr.com{query.replace(' ', ',')}"

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ผลลัพธ์ที่ 1")
        st.image(random_image_url, caption=f"รูปภาพเกี่ยวกับ: {query}", use_container_width=True)
        st.code(random_image_url, language="text") # โชว์ลิงก์ให้ก๊อปไปใช้ต่อได้

    with col2:
        st.subheader("ผลลัพธ์ที่ 2")
        # ใช้บริการค้นหาของ Unsplash แบบระบุขนาดชัดๆ
        alt_image_url = f"https://boringavatars.com{query}" # ตัวอย่างบริการอื่น
        st.info("คุณสามารถคัดลอกลิงก์ด้านซ้ายไปใส่ในโค้ดหลักของคุณได้เลยครับ")

# ส่วนคำแนะนำ
with st.expander("💡 วิธีหาลิงก์ภาพที่ชัดที่สุดด้วยตัวเอง"):
    st.markdown("""
    1. ไปที่เว็บ [Unsplash.com](https://unsplash.com) หรือ [Pexels.com](https://pexels.com)
    2. ค้นหารูปที่ชอบ แล้วคลิกเข้าไปดูรูปขนาดใหญ่
    3. **คลิกขวาที่รูป** -> เลือก **'คัดลอกที่อยู่รูปภาพ' (Copy Image Address)**
    4. ลิงก์ที่ได้จะมีความละเอียดสูงและนำมาใส่ในแอปได้ทันที
    """)

# ตั้งชื่อหัวข้อแอป
st.title("🖼️ Image Link Previewer")

# สร้างช่องกรอกข้อความสำหรับใส่ URL ของรูปภาพ
image_url = st.text_input(
    label="วางลิงก์รูปภาพ (Direct Link) ที่นี่:",
    placeholder="ตัวอย่าง: https://example.com"
)

# สร้างปุ่มสำหรับกดเพื่อแสดงรูป
if st.button("แสดงรูปภาพ"):
    if image_url:
        try:
            # ใช้ st.image เพื่อแสดงผลรูปจาก URL
            st.image(image_url, caption="ภาพจากลิงก์ของคุณ", use_container_width=True)
            st.success("โหลดรูปภาพสำเร็จ!")
        except Exception as e:
            # แจ้งเตือนหากลิงก์ไม่ถูกต้อง หรือไม่ใช้ไฟล์รูปภาพ
            st.error(f"ไม่สามารถโหลดรูปภาพได้: กรุณาตรวจสอบว่าลิงก์ถูกต้องและลงท้ายด้วย .jpg, .png หรือ .webp")
    else:
        st.warning("กรุณาใส่ลิงก์รูปภาพก่อนกดปุ่มครับ")

# คำแนะนำเพิ่มเติม
st.info("💡 เคล็ดลับ: ลิงก์ที่ใช้ต้องเป็น 'Direct Link' ที่คลิกแล้วเห็นแค่รูปภาพเท่านั้น")
