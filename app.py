import streamlit as st

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="SYNAPSE - Image Finder", layout="wide")

# ส่วนหัวของแอปตามสไตล์คุณ
st.title("🔍 SYNAPSE: Search & Preview")
st.write("อยู่นิ่งๆ ไม่เจ็บตัว - ค้นหารูปภาพที่ใช้งานได้จริง")

# --- ส่วนที่ 1: ค้นหารูปภาพใหม่ ---
st.subheader("1. ค้นหารูปภาพจากคีย์เวิร์ด")
query = st.text_input("พิมพ์สิ่งที่อยากค้นหา (ภาษาอังกฤษ):", placeholder="เช่น: cyberpunk, retro, nature")

if query:
    # ใช้ Unsplash Source API เพื่อดึงรูปมาแสดงทันที
    img_url_1 = f"https://images.unsplash.com/photo-1501504905953-f875d0234446?q=80&w=1000&auto=format&fit=crop" # รูปตัวอย่างถาวรกรณี API เปลี่ยน
    # ในการใช้งานจริง แนะนำใช้ระบบสุ่มจากคีย์เวิร์ด
    search_link = f"https://source.unsplash.com/featured/800x600?{query.replace(' ', ',')}"
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(search_link, caption=f"ผลลัพธ์สำหรับ: {query}", use_container_width=True)
    with col2:
        st.info("คัดลอกลิงก์ด้านล่างไปใช้งาน")
        st.code(search_link, language="text")

st.divider()

# --- ส่วนที่ 2: ตรวจสอบลิงก์ที่มีอยู่แล้ว ---
st.subheader("2. Image Link Previewer")
image_url = st.text_input(
    label="วางลิงก์รูปภาพ (Direct Link) ที่นี่:",
    placeholder="https://example.com/image.jpg"
)

if st.button("แสดงรูปภาพ"):
    if image_url:
        try:
            # จัดระเบียบการย่อหน้าให้เป๊ะตามหลัก Python
            st.image(image_url, caption="ภาพจากลิงก์ของคุณ", use_container_width=True)
            st.success("โหลดรูปภาพสำเร็จ!")
        except Exception as e:
            st.error("ไม่สามารถโหลดรูปภาพได้: โปรดตรวจสอบว่าเป็น Direct Link ที่ถูกต้อง")
    else:
        st.warning("กรุณาใส่ลิงก์รูปภาพก่อนกดปุ่มครับ")

# ส่วน Footer
st.caption("พัฒนาโดย Bas/Ta | 'อยู่นิ่งๆ ไม่เจ็บตัว'")
