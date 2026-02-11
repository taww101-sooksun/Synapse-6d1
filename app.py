<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Math-Elastic Healer</title>
    <style>
        body { background: #080808; color: #0f0; font-family: 'Courier New', monospace; height: 100vh; margin: 0; display: flex; flex-direction: column; overflow: hidden; }
        
        /* HEADER & CANVAS */
        .top-section { position: relative; height: 200px; background: #000; border-bottom: 2px solid #0f0; }
        canvas { width: 100%; height: 100%; display: block; }
        
        .overlay-info { 
            position: absolute; top: 10px; left: 10px; 
            background: rgba(0,0,0,0.7); padding: 10px; border: 1px solid #0f0;
        }
        
        /* CONTROLS */
        .controls { padding: 15px; display: flex; gap: 10px; justify-content: center; background: #111; flex-wrap: wrap; }
        button { 
            background: #000; color: #0f0; border: 1px solid #0f0; padding: 10px 20px; 
            cursor: pointer; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;
            transition: 0.2s;
        }
        button:hover { background: #0f0; color: #000; box-shadow: 0 0 15px #0f0; }
        button.rec.active { background: #f00; border-color: #f00; color: #fff; animation: pulse 1s infinite; }
        
        input[type="file"] { display: none; }
        .file-btn { border: 1px dashed #666; color: #888; }

        /* 144 GRID VISUALIZER */
        .grid-wrapper { flex: 1; overflow: auto; padding: 10px; background: #050505; position: relative; }
        .grid { 
            display: grid; grid-template-columns: repeat(12, 1fr); gap: 2px; 
            min-width: 800px; padding-bottom: 50px;
        }
        .cell { 
            height: 40px; background: #111; border: 1px solid #222; 
            display: flex; align-items: center; justify-content: center; 
            font-size: 0.7em; color: #333; transition: 0.05s;
        }
        .cell.active { background: #0f0; color: #000; box-shadow: 0 0 15px #0f0; z-index: 10; transform: scale(1.2); }
        .cell.base-note { border-color: #fff; background: #222; color: #fff; }

        @keyframes pulse { 0% {box-shadow: 0 0 0 #f00;} 50% {box-shadow: 0 0 20px #f00;} 100% {box-shadow: 0 0 0 #f00;} }
    </style>
</head>
<body>

<div class="top-section">
    <canvas id="visualizer"></canvas>
    <div class="overlay-info">
        <h2 style="margin:0">MATH-ELASTIC ENGINE</h2>
        <div id="status">รอคำสั่ง: อัดเสียง C4 (โด) เพื่อเริ่มคำนวณ...</div>
        <div style="font-size:0.8em; color:#888; margin-top:5px;">
            MATH: f = f0 * 2^(n/12) <br>
            STRETCH: Granular Loop
        </div>
    </div>
</div>

<div class="controls">
    <button id="btnRec" class="rec" onclick="toggleRec()">1. อัดเสียงต้นแบบ (Base Voice)</button>
    <label class="file-btn" style="padding: 10px 20px; display: inline-block; cursor: pointer;">
        2. เลือกเพลง MP3
        <input type="file" id="mp3Input" accept="audio/*">
    </label>
    <button onclick="startEngine()">3. เริ่มระบบคำนวณ (Start Math)</button>
    <button onclick="stopAll()" style="border-color:#555; color:#555;">Stop</button>
</div>

<div class="grid-wrapper">
    <div class="grid" id="grid">
        </div>
</div>

<script>
    const NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const status = document.getElementById('status');
    const grid = document.getElementById('grid');
    const canvas = document.getElementById('visualizer');
    const ctx = canvas.getContext('2d');

    let audioCtx;
    let masterGain;
    
    // User Voice Data
    let userBuffer = null; // เสียงต้นฉบับ
    let baseNoteIndex = 60; // C4 (Middle C) เป็นค่ามาตรฐานในการคำนวณ
    
    // MP3 Data
    let mp3Source, mp3Buffer;
    let mp3Analyser;
    
    // System State
    let isRecording = false;
    let isRunning = false;
    let mediaRecorder, chunks = [];
    let animationId;

    // 1. สร้างตาราง 144
    function initGrid() {
        grid.innerHTML = '';
        for(let i=0; i<144; i++) {
            const note = NOTES[i%12];
            const oct = Math.floor(i/12);
            const div = document.createElement('div');
            div.className = 'cell';
            div.id = `cell-${i}`;
            div.innerHTML = `${note}${oct}`;
            if(i === 60) div.classList.add('base-note'); // Highlight C4
            grid.appendChild(div);
        }
    }
    initGrid();

    // 2. ระบบเสียง & REC
    function initAudio() {
        if(!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if(audioCtx.state === 'suspended') audioCtx.resume();
        masterGain = audioCtx.createGain();
        masterGain.connect(audioCtx.destination);
    }

    async function toggleRec() {
        initAudio();
        const btn = document.getElementById('btnRec');
        
        if(!isRecording) {
            // Start Rec
            try {
                const stream = await navigator.mediaDevices.getUserMedia({audio: true});
                mediaRecorder = new MediaRecorder(stream);
                chunks = [];
                mediaRecorder.ondataavailable = e => chunks.push(e.data);
                mediaRecorder.onstop = async () => {
                    const blob = new Blob(chunks);
                    const buf = await blob.arrayBuffer();
                    userBuffer = await audioCtx.decodeAudioData(buf);
                    status.innerHTML = "✅ ได้ข้อมูลเสียงแล้ว! <br>ระบบคำนวณคณิตศาสตร์พร้อมแปลงเป็น 144 เสียง";
                    status.style.color = "#0f0";
                    btn.classList.remove('active');
                    btn.innerText = "บันทึกใหม่ (Re-Record)";
                };
                mediaRecorder.start();
                isRecording = true;
                btn.classList.add('active');
                btn.innerText = "กำลังอัด... (ร้อง C4 ยาวๆ)";
                status.innerText = "🎙️ กำลังเก็บตัวอย่างเสียง...";
            } catch(e) { alert("Mic Error"); }
        } else {
            // Stop Rec
            mediaRecorder.stop();
            isRecording = false;
        }
    }

    // 3. โหลด MP3
    document.getElementById('mp3Input').onchange = async (e) => {
        const file = e.target.files[0];
        if(!file) return;
        status.innerText = "⏳ กำลังถอดรหัสเพลง MP3...";
        initAudio();
        const ab = await file.arrayBuffer();
        mp3Buffer = await audioCtx.decodeAudioData(ab);
        status.innerText = "พร้อมเดินเครื่อง! กดปุ่มเริ่มระบบ";
    };

    // 4. THE MATH ENGINE (หัวใจหลัก)
    function startEngine() {
        if(!userBuffer || !mp3Buffer) { alert("กรุณาอัดเสียง และ เลือกเพลงก่อนครับ"); return; }
        if(isRunning) return;
        
        isRunning = true;
        
        // เล่น MP3
        mp3Source = audioCtx.createBufferSource();
        mp3Source.buffer = mp3Buffer;
        const mp3Gain = audioCtx.createGain();
        mp3Gain.gain.value = 0.8; // ลดเสียงเพลงลงนิดนึง ให้เสียงเราเด่น
        
        // ตัววิเคราะห์ความถี่ (Frequency Analyzer)
        mp3Analyser = audioCtx.createAnalyser();
        mp3Analyser.fftSize = 2048;
        
        mp3Source.connect(mp3Gain);
        mp3Gain.connect(mp3Analyser);
        mp3Gain.connect(audioCtx.destination);
        mp3Source.start();

        status.innerText = "🚀 กำลังคำนวณและยืดหดเสียงแบบ Real-time...";
        
        visualizeAndTrigger();
    }

    // 5. Logic การคำนวณและการ Trigger เสียง
    function visualizeAndTrigger() {
        if(!isRunning) return;
        
        const bufferLength = mp3Analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        mp3Analyser.getByteFrequencyData(dataArray);

        // วาดกราฟ
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        const barWidth = (canvas.width / bufferLength) * 2.5;
        let x = 0;

        // หาความถี่เด่น (Dominant Frequency) เพื่อ Trigger โน้ตที่ตรงกัน
        let maxVal = 0;
        let maxIndex = 0;

        for(let i = 0; i < bufferLength; i++) {
            const barHeight = dataArray[i];
            
            // Visual
            ctx.fillStyle = `rgb(0, ${barHeight + 100}, 0)`;
            ctx.fillRect(x, canvas.height - barHeight/2, barWidth, barHeight/2);
            x += barWidth + 1;

            if(barHeight > maxVal) { maxVal = barHeight; maxIndex = i; }
        }

        // --- MATH MAGIC STARTS HERE ---
        // ถ้าเสียงดังพอ (มีทำนอง)
        if(maxVal > 180) { 
            // 1. คำนวณความถี่ (Hz) จาก Index
            const nyquist = audioCtx.sampleRate / 2;
            const targetFreq = maxIndex * (nyquist / bufferLength);

            // 2. กรองย่านความถี่มนุษย์ (80Hz - 1000Hz)
            if(targetFreq > 80 && targetFreq < 1000) {
                
                // 3. แปลง Hz เป็น Note Number (0-143)
                // สูตร: Note = 12 * log2(Freq / 440) + 69
                const midiNum = 12 * (Math.log(targetFreq / 440) / Math.log(2)) + 69;
                let gridIndex = Math.round(midiNum); // ปัดเศษเป็นจำนวนเต็ม
                
                // Map MIDI to Grid (MIDI 0 is C-1, Grid starts usually around MIDI 12 or 24)
                // ปรับ Offset ให้ตรงกับตารางเรา
                gridIndex = gridIndex + 12; 

                // Limit
                if(gridIndex < 0) gridIndex = 0;
                if(gridIndex > 143) gridIndex = 143;

                // 4. Trigger เสียงผู้ใช้ที่ช่องนั้น
                triggerCalculatedVoice(gridIndex, maxVal);
            }
        }

        animationId = requestAnimationFrame(visualizeAndTrigger);
    }

    // ฟังก์ชันยืดหดเสียง (Elastic Voice)
    // นี่คือส่วนที่ใช้คณิตศาสตร์ปรับเสียงเราให้ตรงกับช่อง 144
    function triggerCalculatedVoice(targetIndex, velocity) {
        
        // Highlight Visual
        const cell = document.getElementById(`cell-${targetIndex}`);
        if(cell) {
            cell.classList.add('active');
            setTimeout(() => cell.classList.remove('active'), 150);
        }

        // เล่นเสียง
        const src = audioCtx.createBufferSource();
        src.buffer = userBuffer;
        
        // *** MATH FORMULA: Pitch Shifting ***
        // คำนวณระยะห่างจากเสียงต้นฉบับ (C4 = Index 60)
        // สมมติเราอัดเสียง C4 ไว้ที่ index 60
        // แต่เพลงเล่นโน้ต G4 (index 67) -> เราต้องเร่งความเร็ว
        const semitoneDiff = targetIndex - baseNoteIndex; // เช่น 67 - 60 = 7 semitones
        
        // สูตร PlaybackRate: rate = 2 ^ (semitones / 12)
        const rate = Math.pow(2, semitoneDiff / 12);
        
        src.playbackRate.value = rate; // ยืด/หดเสียงตามสูตร
        
        // Envelope (Fade In/Out เร็วๆ เพื่อไม่ให้เสียงกระตุก)
        const gain = audioCtx.createGain();
        src.connect(gain);
        gain.connect(audioCtx.destination);
        
        // ความดังตามความแรงของเพลง
        const vol = (velocity / 255) * 0.8; 
        
        gain.gain.setValueAtTime(0, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(vol, audioCtx.currentTime + 0.05); // Attack
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3); // Release (Short Sustain)

        src.start();
    }

    function stopAll() {
        if(mp3Source) mp3Source.stop();
        isRunning = false;
        cancelAnimationFrame(animationId);
        status.innerText = "ระบบหยุดทำงาน";
    }

</script>
</body>
</html>
