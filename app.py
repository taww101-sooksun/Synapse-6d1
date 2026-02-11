# ก่อนรันต้องติดตั้ง: pip install gTTS
from gtts import gTTS
import os

def generate_real_vocal(text, lang='th'):
    # 1. แปลงข้อความเป็นเสียงมนุษย์
    tts = gTTS(text=text, lang=lang)
    
    # 2. บันทึกเป็นไฟล์มิติ
    filename = "matrix_vocal.mp3"
    tts.save(filename)
    
    print(f"--- ระบบกำลังรันเสียงร้องจริง: '{text}' ---")
    return filename

# --- ป้อนข้อมูลรหัสและสโลแกนของคุณ ---
my_lyrics = "หก แปด ศูนย์ สอง เจ็ด สอง หนึ่ง ศูนย์ แปด แปด. หก หนึ่ง สอง สี่ สี่ สอง ห้า สอง. อยู่นิ่งๆ ไม่เจ็บตัว"

# รันโค้ด
audio_file = generate_real_vocal(my_lyrics)

# หมายเหตุ: หากรันใน Google Colab ใช้คำสั่งนี้เพื่อฟัง:
# from IPython.display import Audio
# Audio(audio_file, autoplay=True)
