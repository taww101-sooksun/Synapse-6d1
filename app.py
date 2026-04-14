import streamlit as st

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
