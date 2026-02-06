import streamlit as st
import streamlit.components.v1 as components

st.subheader("🎨 REAL-TIME COLOR & BRIGHTNESS SCANNER")
st.write("สถานะ: ดึงค่าแสงและสีดิบจากเลนส์กล้อง (ไม่มีการบล็อก)")

color_js = """
<div style="background-color: #111; color: #FFD700; padding: 20px; border: 2px solid #FFD700; border-radius: 15px; text-align: center;">
    <video id="v_color" style="width: 100%; max-width: 300px; border-radius: 10px;" autoplay playsinline></video>
    <canvas id="c_color" style="display:none;"></canvas>
    
    <div style="margin-top: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div style="background: #222; padding: 10px; border-radius: 10px;">
            <small>ความสว่างเฉลี่ย</small>
            <h2 id="br_val">0</h2>
        </div>
        <div style="background: #222; padding: 10px; border-radius: 10px;">
            <small>โทนสีหลัก</small>
            <div id="color_box" style="width: 30px; height: 30px; margin: 5px auto; border: 1px solid #fff;"></div>
        </div>
    </div>
    <p id="rgb_text" style="font-family: monospace; color: #00ffff; margin-top: 10px;">RGB: 0, 0, 0</p>
</div>

<script>
    async function startColorScan() {
        const v = document.getElementById('v_color');
        const c = document.getElementById('c_color');
        const ctx = c.getContext('2d');
        
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            v.srcObject = stream;
            
            setInterval(() => {
                c.width = v.videoWidth;
                c.height = v.videoHeight;
                ctx.drawImage(v, 0, 0, 1, 1); // ดึงค่าแค่พิกเซลเดียวเพื่อหาค่าเฉลี่ย
                const [r, g, b] = ctx.getImageData(0, 0, 1, 1).data;
                
                const brightness = Math.round((r + g + b) / 3);
                document.getElementById('br_val').innerText = brightness;
                document.getElementById('rgb_text').innerText = `R:${r} G:${g} B:${b}`;
                document.getElementById('color_box').style.backgroundColor = `rgb(${r},${g},${b})`;
            }, 100);
        } catch (e) { alert("กรุณาอนุญาตให้เข้าถึงกล้อง"); }
    }
    startColorScan();
</script>
"""

components.html(color_js, height=500)

st.write("**ความจริงที่ได้:**")
st.write("- **ความสว่าง:** 0 (มืดสนิท) ถึง 255 (ขาวจัด)")
st.write("- **RGB:** ค่าสีจริงที่กล้องเห็น ถ้าส่องไปที่น้ำแข็งต้องได้สีออกฟ้า/ขาว")
