# MATRIX_V2: Lightweight Truth Engine
# Slogan: "อยู่นิ่งๆ ไม่เจ็บตัว"

import time

# [1] ฐานข้อมูล 252 ตัวเลข (จำลองโครงสร้าง Matrix)
db_252 = list(range(1, 253)) 

# [2] กุญแจ 42 ตัวอักษร + 2 เครื่องหมาย
keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnop" + "+=" 

# [3] ตัวแปรเสริม 12 อย่าง (Input Variables)
aux_vars = [1.02, 0.98, 1.00, 1.05, 0.99, 1.01, 1.03, 0.97, 1.00, 1.04, 1.02, 0.96]

def decode_matrix_v2():
    print(f"--- เริ่มต้นการถอดรหัส ณ เวลา: {time.strftime('%H:%M:%S')} ---")
    
    # คำนวณความเชื่อมโยง (Numerical Connection)
    # ยึดค่าความจริงจากตัวเลข 252 ตัว หารด้วยมิติทั้ง 6
    base_truth = sum(db_252) / len(aux_vars)
    
    # มิติ 6 ด่าน (The 6 Gates)
    gates = ["Stability", "Filtering", "Reflection", "Equilibrium", "Silence", "Unity"]
    results = {}

    for i, gate in enumerate(gates):
        # คำนวณค่ามิติโดยใช้กุญแจและตัวแปรเสริม
        gate_value = (base_truth * aux_vars[i]) / len(keys)
        results[gate] = round(gate_value, 4)
        
    return results

# รันผลลัพธ์เพื่อแสดงค่าข้อมูลจริง
output_data = decode_matrix_v2()

print(f"ผลลัพธ์มิติทั้ง 6 (Gate Values):")
for gate, value in output_data.items():
    print(f"  > {gate}: {value}")

# ค่าสัมผัส (Scent Output) ที่สอดคล้องกับเวลา
print(f"\nสถานะสัมผัสปัจจุบัน: {round(sum(aux_vars), 2)} (ค่าความบริสุทธิ์ของกลิ่น)")
