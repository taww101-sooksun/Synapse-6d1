import numpy as np
import simpleaudio as sa # หรือใช้ IPython.display.Audio ถ้าอยู่ใน Colab

def generate_matrix_sound(duration=5):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 1. ความถี่ฐานระบบ (147 Hz) - ความนิ่ง
    core_tone = np.sin(147 * 2 * np.pi * t)
    
    # 2. ความถี่ทองคำ (135.42 Hz) - ความมั่งคั่ง
    gold_tone = np.sin(135.42 * 2 * np.pi * t)
    
    # 3. ความถี่ความรัก (528 Hz) - ความปลอดภัย (เบาลงหน่อยเพื่อให้ไม่หนวกหู)
    love_tone = np.sin(528 * 2 * np.pi * t) * 0.3
    
    # รวมคลื่นเสียง (Mixed Mode)
    # เราใช้การเฉลี่ยเพื่อไม่ให้คลื่นเสียงพีคจนลำโพงแตก (ป้องกันการ "เจ็บตัว")
    mixed_tone = (core_tone + gold_tone + love_tone) * 0.2
    
    # แปลงเป็นฟอร์แมต 16-bit PCM
    audio = (mixed_tone * 32767).astype(np.int16)
    
    return audio

# สถานะ: พร้อมรันความถี่
print("--- RUNNING: Stillness Frequencies (147Hz, 135.42Hz, 528Hz) ---")
# play_obj = sa.play_buffer(generate_matrix_sound(), 1, 2, 44100)
# play_obj.wait_done()
