
มันเป็นภาษาแบบนี้อ่านไ่มออกครับ

อ๋อครับ เห็นจากรูปแล้ว ภาษาไทยในหน้าแอปเพี้ยนจริง ครับ ไม่ใช่แค่ฟอนต์อย่างเดียว แต่มีโอกาสสูงว่าไฟล์ที่เอาขึ้น GitHub ถูกตีความ encoding ผิด ทำให้ข้อความอย่าง ชื่อเจ้าของนา กลายเป็นตัวอักษรประหลาด

ผมทำไฟล์แก้ให้ใหม่แล้ว โดย:

🇹🇭 บังคับข้อความภาษาไทยให้ไม่เพี้ยนจาก encoding

ใช้ฟอนต์ที่รองรับภาษาไทย

ยังคงฟังก์ชันเดิมทั้งหมด

ใช้กับ GitHub + Streamlit ได้

ไฟล์ที่แก้แล้ว
ดาวน์โหลด Ta_app_thai_fixed.py

ให้ทำแบบนี้ครับ:

ลบ Ta_app.py ตัวเก่าใน GitHub

เอาไฟล์นี้ขึ้นไป

เปลี่ยนชื่อเป็น Ta_app.py

logo1.png วางไว้ข้าง ๆ กัน

กด Deploy/Reboot แอป

อีกอย่างหนึ่ง: จากรูปผมเห็นว่าหน้าแอปเดิมมีข้อความเพี้ยนหลายตำแหน่ง ดังนั้นผมแนะนำให้ใช้ไฟล์ใหม่นี้ทั้งไฟล์เลย อย่าเอาโค้ดเก่ามาผสมครับ

ถ้าหลังจากเปลี่ยนแล้ว ภาษาไทยกลับมาอ่านได้ปกติ ขั้นต่อไปผมจะจัดเรื่อง “ลากหมุดได้จริงบนมือถือ + GPS ใช้งานจริง + ใบสรุปสวย ๆ” ให้ต่อครับ 🌾📍 


Ta_app_thai_fixed.py
โค้ด


File "/mount/src/taww101/Ta_app.py", line 12
  จาก pathlib นำเข้า Path
      ^
SyntaxError: invalid syntax

ใช่ครับ ปัญหานี้ ไม่ใช่ Shapely แล้ว แต่ไฟล์ที่อยู่บน GitHub ของคุณถูกเปลี่ยนคำสั่ง Python เป็นภาษาไทย เช่น

จาก pathlib นำเข้า Path
Python อ่านไม่ได้ จึงขึ้น SyntaxError ครับ

ผมตรวจไฟล์ใหม่แล้ว และไฟล์ที่แก้ ผ่านการตรวจ Syntax ของ Python แล้ว ไม่มีปัญหาที่บรรทัด from pathlib import Path ครับ

ดาวน์โหลด Ta_app_thai_fixed.py

ให้ทำแบบนี้เลย
ใน GitHub:

เปิด Ta_app.py

กด Edit

ลบโค้ดเก่าทั้งหมด

เปิดไฟล์ Ta_app_thai_fixed.py ที่ผมให้

คัดลอก ทั้งหมด ไปวางใน Ta_app.py

กด Commit changes

กลับ Streamlit แล้วกด Reboot app

อย่าแก้คำสั่ง Python เป็นภาษาไทยเด็ดขาด เช่นต้องเป็น:

from pathlib import Path
import streamlit as st
ไม่ใช่:

จาก pathlib นำเข้า Path
นำเข้า streamlit เป็น st
อีกอย่างครับ จากรูปก่อนหน้านี้ภาษาไทยก็เพี้ยนด้วย ผมจึงทำไฟล์ใหม่ให้ ตัวคำสั่ง Python เป็นมาตรฐาน และข้อความภาษาไทยถูกเก็บอย่างปลอดภัย แล้วครับ

ถ้าต้องการให้จบทีเดียว ผมแนะนำว่า ใช้ไฟล์ใหม่ทั้งไฟล์ ไม่เอาโค้ดเก่ามาผสม ครับ 🌾👍


Ta_app_thai_fixed.py
โค้ด


File "/mount/src/taww101/Ta_app.py", line 12
  จาก pathlib นำเข้า Path
      ^
SyntaxError: invalid syntax

เข้าใจแล้วครับ — ตอนนี้ Streamlit ยังรัน Ta_app.py ตัวเก่าที่อยู่ใน GitHub อยู่ ไม่ได้รันไฟล์ที่ผมแก้ให้ครับ

Error นี้ยืนยันเลย:

จาก pathlib นำเข้า Path
มันต้องเป็น:

from pathlib import Path
ผมตรวจไฟล์ใหม่ของผมด้วย Python แล้ว ผ่าน Syntax Check เรียบร้อย และในไฟล์ไม่มีคำสั่ง จาก pathlib นำเข้า Path ครับ

ทำตามนี้แบบตรง ๆ ครับ
ใน GitHub Repository taww101:

เข้าไฟล์ Ta_app.py

กดปุ่ม ✏️ Edit this file

กด Ctrl+A / เลือกโค้ดทั้งหมด

ลบของเดิมออกให้หมด

เอาโค้ดจากไฟล์นี้ไปแทนทั้งหมด:

ดาวน์โหลด Ta_app_thai_fixed.py

ใน GitHub ตั้งชื่อไฟล์เป็น Ta_app.py

กด Commit changes

กลับ Streamlit → Reboot app

สำคัญมาก
อย่าแก้บรรทัด Python เองเป็นภาษาไทยเด็ดขาดครับ เช่น

❌ ผิด

จาก pathlib นำเข้า Path
✅ ถูก

from pathlib import Path
และ

❌

นำเข้า streamlit เป็น st
✅

import streamlit as st
ส่วนข้อความที่แสดงบนหน้าจอเป็นภาษาไทยได้ตามปกติ ไม่ต้องแปลคำสั่ง Python ครับ

ถ้าคุณต้องการ ผมสามารถทำให้ต่อเป็น โค้ดเวอร์ชันสุดท้ายที่ไม่ใช้คำสั่งภาษาไทยในตัวโค้ดเลย และเน้นมือถือโดยเฉพาะ เพื่อเอาไปวาง GitHub แบบคัดลอกครั้งเดียวจบได้ครับ.


Ta_app_thai_fixed.py
โค้ด


ไม่ได้เลือกไฟล์ใด
ไลบรารี
/
Ta_app_thai_fixed.py


1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
# -*- coding: utf-8 -*-
# Ta_app.py
# \u0e41\u0e2d\u0e1b\u0e27\u0e31\u0e14\u0e1e\u0e37\u0e49\u0e19\u0e17\u0e35\u0e48\u0e19\u0e32 + \u0e1b\u0e31\u0e01\u0e2b\u0e21\u0e38\u0e14 + \u0e04\u0e33\u0e19\u0e27\u0e13\u0e04\u0e48\u0e32\u0e1a\u0e23\u0e34\u0e01\u0e32\u0e23
# \u0e15\u0e49\u0e2d\u0e07\u0e21\u0e35\u0e44\u0e1f\u0e25\u0e4c logo1.png \u0e2d\u0e22\u0e39\u0e48\u0e42\u0e1f\u0e25\u0e40\u0e14\u0e2d\u0e23\u0e4c\u0e40\u0e14\u0e35\u0e22\u0e27\u0e01\u0e31\u0e1a\u0e44\u0e1f\u0e25\u0e4c\u0e19\u0e35\u0e49
#
# \u0e15\u0e34\u0e14\u0e15\u0e31\u0e49\u0e07:
#   pip install streamlit streamlit-folium folium shapely
# \u0e23\u0e31\u0e19:
#   streamlit run Ta_app.py

import math
from pathlib import Path

import folium
import streamlit as st
from folium.plugins import LocateControl
from shapely.geometry import Polygon
from streamlit_folium import st_folium



st.markdown("""
<style>
html, body, [class*="css"], .stApp, button, input, textarea, select {
    font-family: "Noto Sans Thai", "Tahoma", "Arial", sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Ta App - \u0e27\u0e31\u0e14\u0e1e\u0e37\u0e49\u0e19\u0e17\u0e35\u0e48\u0e19\u0e32",
    page_icon="\U0001f33e",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# \u0e15\u0e31\u0e49\u0e07\u0e04\u0e48\u0e32\u0e1e\u0e37\u0e49\u0e19\u0e10\u0e32\u0e19
# ----------------------------
PLOW_RATE = 250.0
MILL_RATE = 350.0
RAI_M2 = 1600.0
