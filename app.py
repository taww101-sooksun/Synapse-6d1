import torch
import numpy as np
import librosa
import soundfile as sf
from fairseq import checkpoint_utils

# --- 1. ตั้งค่าพื้นฐาน (Config) ---
device = "cuda" if torch.cuda.is_available() else "cpu" # ถ้าในมือถือมักจะเป็น cpu
is_half = False # มือถือส่วนใหญ่ต้องปิด Half precision ไม่งั้น error

# --- 2. ฟังก์ชันโหลด Hubert (ตัวแปลงเสียงเป็น Code) ---
def load_hubert(hubert_path):
    print(f"กำลังโหลด Hubert จาก: {hubert_path}")
    models, _, _ = checkpoint_utils.load_model_ensemble_and_task(
        [hubert_path],
        suffix="",
    )
    hubert_model = models[0]
    hubert_model = hubert_model.to(device)
    if is_half:
        hubert_model = hubert_model.half()
    else:
        hubert_model = hubert_model.float()
    hubert_model.eval()
    return hubert_model

# --- 3. ฟังก์ชันโหลดโมเดลเสียง RVC (.pth) ---
def get_vc(model_path):
    print(f"กำลังโหลดโมเดลเสียงจาก: {model_path}")
    cpt = torch.load(model_path, map_location="cpu")
    tgt_sr = cpt["config"][-1] # ค่า Sample Rate ของโมเดล
    cpt["config"][-3] = cpt["weight"]["emb_g.weight"].shape[0] # แก้ config ให้ตรงกับ weight
    net_g = cpt["net_g"] # นี่คือตัว Neural Network (สมอง)
    net_g = net_g.to(device)
    if is_half:
        net_g = net_g.half()
    else:
        net_g = net_g.float()
    net_g.eval()
    vc = net_g
    return vc, tgt_sr

# --- 4. ฟังก์ชันแปลงเสียง (Inference Core) ---
def rvc_convert(model_path, hubert_path, input_audio_path, f0_up_key=0):
    # f0_up_key: ปรับคีย์เสียง (0 = ปกติ, 12 = สูงขึ้น 1 octave, -12 = ต่ำลง)
    
    # 4.1 โหลดของ
    hubert_model = load_hubert(hubert_path)
    net_g, tgt_sr = get_vc(model_path)
    
    # 4.2 โหลดเสียงเรา
    print(f"กำลังอ่านไฟล์เสียง: {input_audio_path}")
    audio, sr = librosa.load(input_audio_path, sr=16000) # RVC บังคับ input 16k
    
    # 4.3 แปลงเสียงเป็น Tensor
    audio_opt = torch.from_numpy(audio).to(device)
    if is_half: audio_opt = audio_opt.half()
    else: audio_opt = audio_opt.float()
    
    # 4.4 ส่งเข้า Hubert เพื่อดึง Feature
    feats = audio_opt.unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        padding_mask = torch.BoolTensor(feats.shape).fill_(False)
        inputs = {
            "source": feats,
            "padding_mask": padding_mask,
            "output_layer": 9, # ปกติใช้ layer 9 หรือ 12
        }
        logits = hubert_model.extract_features(**inputs)
        feats = hubert_model.final_proj(logits[0])
    
    # 4.5 ส่งเข้า VC Model (แปลงเนื้อเสียง)
    # ตรงนี้ต้องมีการคำนวณ Pitch (F0) ด้วยถ้าเป็นโมเดลร้องเพลง แต่ขอตัดแบบง่ายสุดให้ก่อน
    # เพื่อให้รันผ่านบนมือถือ
    
    print("กำลังประมวลผลแปลงเสียง... (ขั้นตอนนี้กินเครื่องหนักสุด)")
    with torch.no_grad():
         # สั่งโมเดลทำงาน (Output ออกมาเป็น Audio)
         # หมายเหตุ: โค้ดส่วนนี้ย่อมา ของจริงต้องมี f0 prediction ถ้าจะเอาเนียนกริบ
         audio_out = net_g.infer(feats, torch.LongTensor([feats.shape[1]]).to(device))
         
    output_audio = audio_out[0][0, 0].data.cpu().float().numpy()
    
    return output_audio, tgt_sr

# --- ส่วนสั่งงาน (EXECUTE) ---
if __name__ == "__main__":
    try:
        # ใส่ชื่อไฟล์ของคุณตรงนี้
        my_model = "my_voice_model.pth"      # ไฟล์โมเดลที่ฝึกเสร็จแล้ว
        my_hubert = "hubert_base.pt"         # ไฟล์ Hubert
        my_input = "test_input.wav"          # เสียงของคุณ
        
        # เริ่มกระบวนการ
        out_audio, out_sr = rvc_convert(my_model, my_hubert, my_input, f0_up_key=0)
        
        # บันทึกไฟล์
        sf.write("output_final.wav", out_audio, out_sr)
        print("สำเร็จ! ได้ไฟล์ output_final.wav แล้ว")
        
    except Exception as e:
        print("Error! เกิดข้อผิดพลาด:")
        print(e)
        print("คำแนะนำ: เช็คว่าลง library ครบไหม (torch, fairseq, librosa)")
