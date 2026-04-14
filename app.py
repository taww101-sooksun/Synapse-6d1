import streamlit as st
from PIL import Image
import streamlit as st

# ใส่ URL ของรูปภาพที่ต้องการ
st.image("https://example.com", caption="คำอธิบายใต้ภาพ")

# เปิดไฟล์ภาพที่อยู่ในโฟลเดอร์เดียวกับโค้ด
image = Image.open('my_picture.png')
st.image(image, caption='รูปภาพจากเครื่อง', use_container_width=True)
