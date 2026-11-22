import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import mimetypes
import json

# =========================================================
# SYNAPSE NEON MUSIC SYSTEM
# =========================================================

APP_DIR = Path(__file__).resolve().parent
LOGO_FILE = APP_DIR / "logo1.jpg"

AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac"
}

st.set_page_config(
    page_title="SYNAPSE NEON MUSIC",
    page_icon="🎵",
    layout="wide"
)

# =========================================================
# HIDE STREAMLIT
# =========================================================

st.markdown("""
<style>
html, body {
    margin:0!important;
    padding:0!important;
    overflow:hidden!important;
    background:#02030a!important;
}
header, footer, #MainMenu,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebar"],
.stDeployButton {
    display:none!important;
}
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    padding:0!important;
    margin:0!important;
    background:#02030a!important;
}
.block-container {
    padding:0!important;
    margin:0!important;
    max-width:100%!important;
}
iframe {
    border:none!important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGO
# =========================================================

logo_base64 = ""

if LOGO_FILE.exists():
    logo_base64 = base64.b64encode(
        LOGO_FILE.read_bytes()
    ).decode("utf-8")

# =========================================================
# MUSIC FROM SAME DIRECTORY AS Ta_app.py
# =========================================================

music_list = []

for file in sorted(APP_DIR.iterdir(), key=lambda x: x.name.lower()):
    if file.is_file() and file.suffix.lower() in AUDIO_EXTENSIONS:
        try:
            raw = file.read_bytes()
            mime = mimetypes.guess_type(file.name)[0] or "audio/mpeg"

            music_list.append({
                "name": file.stem,
                "type": mime,
                "data": base64.b64encode(raw).decode("ascii")
            })
        except Exception:
            pass

music_json = json.dumps(music_list, ensure_ascii=False)

# =========================================================
# HTML START
# =========================================================

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing:border-box;
}

html, body {
    margin:0;
    width:100%;
    height:100%;
    overflow:hidden;
    background:#02030a;
    font-family:Arial,sans-serif;
}

:root {
    --c1:#00eaff;
    --c2:#bd00ff;
    --c3:#ff1744;
    --c4:#ffd700;
    --c5:#ffffff;
    --c6:#00ff88;
}

#screen {
    width:100%;
    height:100vh;
    height:100dvh;
    overflow:hidden;
    position:relative;
    background:
      radial-gradient(circle at 50% 50%,
      #17172d 0%,
      #080916 45%,
      #02030a 100%);
}

/* BACKGROUND */

canvas {
    pointer-events:none;
}

#stars, #particles, #grid {
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
}

#grid {
    opacity:.16;
}

.scan {
    position:absolute;
    inset:0;
    z-index:30;
    pointer-events:none;
    background:repeating-linear-gradient(
      0deg,
      transparent 0px,
      transparent 3px,
      rgba(255,255,255,.08) 4px
    );
}

.vignette {
    position:absolute;
    inset:0;
    z-index:31;
    pointer-events:none;
    background:radial-gradient(
      circle,
      transparent 40%,
      rgba(0,0,0,.35) 75%,
      #000 130%
    );
}

/* HEADER */

.header {
    position:absolute;
    top:3%;
    left:4%;
    right:4%;
    display:flex;
    justify-content:space-between;
    z-index:10;
}

.brand {
    font-size:clamp(22px,5vw,38px);
    font-weight:900;
    letter-spacing:.28em;
    color:var(--c1);
    text-shadow:0 0 10px var(--c1),0 0 35px var(--c2);
}

.subbrand {
    color:#a8b3c9;
    font-size:8px;
    letter-spacing:.35em;
    margin-top:5px;
}

.status {
    text-align:right;
    color:var(--c4);
    font-size:9px;
    letter-spacing:.2em;
    line-height:2;
}

.dot {
    display:inline-block;
    width:7px;
    height:7px;
    background:var(--c3);
    border-radius:50%;
    box-shadow:0 0 12px var(--c3);
    animation:blink 1s infinite;
}

@keyframes blink {
    50% {opacity:.15;}
}

/* CORNERS */

.corner {
    position:absolute;
    width:38px;
    height:38px;
    z-index:5;
}

.tl {
    top:13%;
    left:2%;
    border-top:2px solid var(--c1;
    border-left:2px solid var(--c1);
}

.tr {
    top:13%;
    right:2%;
    border-top:2px solid var(--c3);
    border-right:2px solid var(--c3);
}

.bl {
    bottom:4%;
    left:2%;
    border-bottom:2px solid var(--c4);
    border-left:2px solid var(--c4);
}

.br {
    bottom:4%;
    right:2%;
    border-bottom:2px solid var(--c2);
    border-right:2px solid var(--c2);
}

/* CENTER CORE */

.core {
    position:absolute;
    width:min(76vw,66vh);
    height:min(76vw,66vh);
    max-width:620px;
    max-height:620px;
    left:50%;
    top:48%;
    transform:translate(-50%,-50%);
    z-index:6;
}

.ring {
    position:absolute;
    inset:0;
    border-radius:50%;
    pointer-events:none;
}

.r1 {
    border:1px dashed var(--c1);
    box-shadow:0 0 15px var(--c1);
    animation:spin 30s linear infinite;
}

.r2 {
    inset:5%;
    border:2px solid var(--c2);
    box-shadow:0 0 15px var(--c2);
    animation:spinback 22s linear infinite;
}

.r3 {
    inset:10%;
    border:1px dotted var(--c4);
    animation:spin 17s linear infinite;
}

.r4 {
    inset:15%;
    border:2px double var(--c5);
    opacity:.6;
    animation:spinback 12s linear infinite;
}

.r5 {
    inset:21%;
    border:1px dashed var(--c3);
    box-shadow:0 0 12px var(--c3);
    animation:spin 8s linear infinite;
}

.r6 {
    inset:27%;
    border:2px solid var(--c1);
    box-shadow:inset 0 0 12px var(--c1);
    animation:spinback 5s linear infinite;
}

@keyframes spin {
    to {transform:rotate(360deg);}
}

@keyframes spinback {
    to {transform:rotate(-360deg);}
}

#orbit {
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
}

/* LOGO */

.logo {
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    width:34%;
    height:34%;
    border-radius:50%;
    overflow:hidden;
    background:#000;
    border:3px solid var(--c4);
    box-shadow:
      0 0 12px var(--c4),
      0 0 30px var(--c1),
      0 0 70px var(--c2);
    animation:pulse 2.8s infinite;
    display:flex;
    justify-content:center;
    align-items:center;
}

.logo img {
    width:100%;
    height:100%;
    object-fit:contain;
}

@keyframes pulse {
    50% {
        box-shadow:
          0 0 25px var(--c4),
          0 0 55px var(--c1),
          0 0 100px var(--c2);
    }
}

/* SIDE METERS */

.side {
    position:absolute;
    width:19%;
    top:27%;
    z-index:9;
}

.left {
    left:3%;
}

.right {
    right:3%;
    text-align:right;
}

.label {
    font-size:8px;
    color:var(--c1);
    letter-spacing:.2em;
    margin-bottom:10px;
}

.bars {
    height:65px;
    display:flex;
    align-items:flex-end;
    gap:2px;
}

.right .bars {
    justify-content:flex-end;
}

.bars span {
    flex:1;
    max-width:7px;
    height:5%;
    background:var(--c1);
    box-shadow:0 0 7px var(--c1);
}

.right .bars span {
    background:var(--c3);
    box-shadow:0 0 7px var(--c3);
}

.number {
    color:var(--c4);
    font-size:20px;
    margin-top:8px;
    text-shadow:0 0 12px var(--c4);
}

.info {
    font-size:7px;
    color:#8b9bb8;
    letter-spacing:.16em;
    line-height:2;
    margin-top:10px;
}

/* TOP BARS */

.topBars {
    position:absolute;
    top:18%;
    left:24%;
    right:24%;
    height:45px;
    display:flex;
    align-items:flex-end;
    justify-content:center;
    gap:2px;
    z-index:5;
}

.topBars span {
    flex:1;
    max-width:8px;
    height:5%;
    background:var(--c4);
    box-shadow:0 0 8px var(--c4);
}

/* WAVE */

.wave {
    position:absolute;
    top:39%;
    left:5%;
    right:5%;
    height:12%;
    z-index:7;
}

#wave {
    width:100%;
    height:100%;
}

/* BOTTOM SPECTRUM */

.spectrum {
    position:absolute;
    left:3%;
    right:3%;
    bottom:25%;
    height:10%;
    z-index:8;
    display:flex;
    justify-content:center;
    align-items:flex-end;
    gap:2px;
}

.spectrum span {
    flex:1;
    max-width:10px;
    height:3%;
    background:var(--c1);
    box-shadow:0 0 8px var(--c1);
}

/* TRACK */

.track {
    position:absolute;
    bottom:17%;
    left:5%;
    right:5%;
    text-align:center;
    z-index:12;
}

.trackTitle {
    color:white;
    font-size:clamp(10px,2.5vw,17px);
    letter-spacing:.12em;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
    text-shadow:0 0 12px var(--c1);
}

.trackCaption {
    color:var(--c4);
    font-size:8px;
    letter-spacing:.35em;
    margin-bottom:8px;
}

/* COLOR PANEL */

.colors {
    position:absolute;
    top:12%;
    left:50%;
    transform:translateX(-50%);
    width:95%;
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    gap:5px;
    z-index:20;
    background:rgba(0,0,0,.65);
    border:1px solid #30344a;
    padding:5px;
}

.colors label {
    display:flex;
    align-items:center;
    gap:2px;
    color:#9baac5;
    font-size:7px;
}

.colors input {
    width:21px;
    height:18px;
    border:0;
    padding:0;
    background:transparent;
}

/* PLAYER */

.player {
    position:absolute;
    bottom:2%;
    left:4%;
    right:4%;
    z-index:20;
    text-align:center;
}

.buttons {
    display:flex;
    justify-content:center;
    align-items:center;
    flex-wrap:wrap;
    gap:4px;
}

button {
    color:var(--c1);
    background:rgba(2,5,15,.9);
    border:1px solid var(--c1);
    border-radius:3px;
    padding:7px 9px;
    font-size:8px;
    letter-spacing:.1em;
    box-shadow:0 0 8px rgba(0,234,255,.2);
}

button:active {
    background:var(--c1);
    color:#000;
}

#play {
    color:var(--c4);
    border-color:var(--c4);
}

.progress {
    width:78%;
    height:3px;
    margin:8px auto 5px;
    background:#252c40;
}

#fill {
    width:0%;
    height:100%;
    background:linear-gradient(90deg,var(--c1),var(--c2),var(--c3),var(--c4));
    box-shadow:0 0 12px var(--c1);
}

.time {
    font-size:8px;
    color:#aab5cb;
}

.message {
    font-size:8px;
    color:var(--c4);
    margin-top:5px;
}

.fullscreen {
    position:absolute;
    right:3%;
    bottom:11%;
    z-index:25;
}

/* MOBILE */

@media(max-width:700px) {
    .core {
        width:min(78vw,55vh);
        height:min(78vw,55vh);
        top:48%;
    }

    .side {
        top:28%;
        width:19%;
    }

    .bars {
        height:52px;
    }

    .info {
        font-size:6px;
    }

    .topBars {
        top:19%;
    }

    .spectrum {
        bottom:25%;
        height:9%;
    }

    .track {
        bottom:17%;
    }

    .player {
        bottom:2%;
    }

    .colors {
        top:12%;
    }

    button {
        padding:6px 7px;
        font-size:7px;
    }

    .fullscreen {
        bottom:11%;
    }
}

@media(max-height:650px) {
    .core {
        width:min(58vh,62vw);
        height:min(58vh,62vw);
        top:43%;
    }

    .side {
        top:21%;
    }

    .track {
        bottom:13%;
    }

    .spectrum {
        bottom:22%;
    }

    .player {
        bottom:1%;
    }

    .colors {
        top:10%;
    }
}

</style>
</head>

<body>
<div id="screen">

<canvas id="stars"></canvas>
<canvas id="particles"></canvas>
<canvas id="grid"></canvas>

<div class="scan"></div>
<div class="vignette"></div>

<div class="corner tl"></div>
<div class="corner tr"></div>
<div class="corner bl"></div>
<div class="corner br"></div>

<div class="header">
    <div>
        <div class="brand">SYNAPSE</div>
        <div class="subbrand">NEON MUSIC SYSTEM / SOUND & VISUAL THERAPY</div>
    </div>
    <div class="status">
        <span class="dot"></span> AUDIO<br>
        <span id="sys">SYSTEM READY</span>
    </div>
</div>

<div class="topBars" id="topBars"></div>

<div class="side left">
    <div class="label">LOW FREQUENCY</div>
    <div class="bars" id="bassBars"></div>
    <div class="number" id="bassNum">000</div>
    <div class="info">BASS ENERGY<br>SUB WAVE<br><span id="bassStatus">STANDBY</span></div>
</div>

<div class="side right">
    <div class="label">HIGH FREQUENCY</div>
    <div class="bars" id="trebleBars"></div>
    <div class="number" id="trebleNum">000</div>
    <div class="info">TREBLE ENERGY<br>STEREO CHANNEL<br><span id="trebleStatus">STANDBY</span></div>
</div>

<div class="core">

    <div class="ring r1"></div>
    <div class="ring r2"></div>
    <div class="ring r3"></div>
    <div class="ring r4"></div>
    <div class="ring r5"></div>
    <div class="ring r6"></div>

    <canvas id="orbit"></canvas>

    <div class="logo" id="logo">
        <span style="color:#00eaff;font-weight:bold">SYNAPSE</span>
    </div>

</div>

<div class="wave">
    <canvas id="wave"></canvas>
</div>

<div class="spectrum" id="spectrum"></div>

<div class="track">
    <div class="trackCaption">NEURAL AUDIO / NOW PLAYING</div>
    <div class="trackTitle" id="trackName">SYNAPSE MUSIC SYSTEM</div>
</div>

<div class="colors">
    <label>RING<input type="color" id="col1" value="#00eaff"></label>
    <label>ORBIT<input type="color" id="col2" value="#bd00ff"></label>
    <label>WAVE<input type="color" id="col3" value="#ffffff"></label>
    <label>BASS<input type="color" id="col4" value="#ffd700"></label>
    <label>BAR<input type="color" id="col5" value="#ff1744"></label>
    <label>STAR<input type="color" id="col6" value="#00ff88"></label>
</div>

<div class="player">
    <div class="buttons">
        <button onclick="prev()">◀ PREV</button>
        <button id="play" onclick="playPause()">▶ PLAY</button>
        <button onclick="stopAudio()">■ STOP</button>
        <button onclick="next()">NEXT ▶</button>
        <button onclick="shuffle()">SHUFFLE</button>
        <button onclick="repeat()">REPEAT</button>
    </div>

    <div class="progress">
        <div id="fill"></div>
    </div>

    <div class="time">
        <span id="now">00:00</span> /
        <span id="total">00:00</span>
    </div>

    <div class="message" id="msg">SYSTEM READY</div>
</div>

<button class="fullscreen" onclick="fullScreen()">⛶ FULL SCREEN</button>

</div><script>

// =========================================================
// MUSIC DATA
// =========================================================

const MUSIC = __MUSIC__;
const LOGO_DATA = "__LOGO__";

// =========================================================
// COLOR SYSTEM
// =========================================================

const C = {
    c1:"#00eaff",
    c2:"#bd00ff",
    c3:"#ffffff",
    c4:"#ffd700",
    c5:"#ff1744",
    c6:"#00ff88"
};

function setColor(key,value) {
    C[key] = value;
    document.documentElement.style.setProperty("--"+key,value);
}

[
    ["col1","c1"],
    ["col2","c2"],
    ["col3","c3"],
    ["col4","c4"],
    ["col5","c5"],
    ["col6","c6"]
].forEach(([id,key]) => {
    document.getElementById(id).addEventListener("input",e=>{
        setColor(key,e.target.value);
    });
});

// =========================================================
// LOGO
// =========================================================

if(LOGO_DATA.length > 10) {
    document.getElementById("logo").innerHTML =
        `<img src="data:image/jpeg;base64,${LOGO_DATA}">`;
}

// =========================================================
// CREATE BARS
// =========================================================

const spectrum = document.getElementById("spectrum");
const topBars = document.getElementById("topBars");
const bassBars = document.getElementById("bassBars");
const trebleBars = document.getElementById("trebleBars");

for(let i=0;i<90;i++) {
    spectrum.appendChild(document.createElement("span"));
}

for(let i=0;i<40;i++) {
    topBars.appendChild(document.createElement("span"));
}

for(let i=0;i<20;i++) {
    bassBars.appendChild(document.createElement("span"));
    trebleBars.appendChild(document.createElement("span"));
}

// =========================================================
// AUDIO
// =========================================================

const audio = new Audio();
audio.preload = "auto";

let audioContext = null;
let analyser = null;
let sourceNode = null;
let freq = null;
let waveData = null;

let current = 0;
let isPlaying = false;
let isShuffle = false;
let isRepeat = false;

function initAudio() {
    if(!audioContext) {
        const AC = window.AudioContext || window.webkitAudioContext;

        if(!AC) {
            document.getElementById("msg").textContent =
                "BROWSER AUDIO NOT SUPPORTED";
            return;
        }

        audioContext = new AC();

        analyser = audioContext.createAnalyser();
        analyser.fftSize = 512;
        analyser.smoothingTimeConstant = 0.8;

        sourceNode = audioContext.createMediaElementSource(audio);

        sourceNode.connect(analyser);
        analyser.connect(audioContext.destination);

        freq = new Uint8Array(analyser.frequencyBinCount);
        waveData = new Uint8Array(analyser.fftSize);
    }

    if(audioContext.state === "suspended") {
        audioContext.resume();
    }
}

function timeFormat(sec) {
    if(!Number.isFinite(sec)) return "00:00";

    const m = Math.floor(sec/60);
    const s = Math.floor(sec%60);

    return String(m).padStart(2,"0")+":"+
           String(s).padStart(2,"0");
}

// =========================================================
// TRACK LOADING
// =========================================================

function loadTrack(index,autoplay=false) {
    if(!MUSIC.length) {
        document.getElementById("msg").textContent =
            "NO MUSIC FILE FOUND";
        return;
    }

    current = (index+MUSIC.length)%MUSIC.length;

    const track = MUSIC[current];

    audio.src = "data:"+track.type+";base64,"+track.data;
    audio.load();

    document.getElementById("trackName").textContent = track.name;
    document.getElementById("msg").textContent =
        "TRACK "+(current+1)+" / "+MUSIC.length;

    if(autoplay) startAudio();
}

function startAudio() {
    if(!MUSIC.length) {
        document.getElementById("msg").textContent =
            "ADD MUSIC BESIDE Ta_app.py";
        return;
    }

    initAudio();

    if(!audio.src) {
        loadTrack(current,false);
    }

    audio.play().then(()=>{
        isPlaying = true;
        document.getElementById("play").textContent = "❚❚ PAUSE";
        document.getElementById("sys").textContent = "PLAYING";
        document.getElementById("bassStatus").textContent = "ACTIVE";
        document.getElementById("trebleStatus").textContent = "ACTIVE";
        document.getElementById("msg").textContent = "AUDIO SYSTEM ACTIVE";
    }).catch(()=>{
        document.getElementById("msg").textContent =
            "PRESS PLAY TO START";
    });
}

function playPause() {
    if(!MUSIC.length) return;

    initAudio();

    if(audio.paused) {
        startAudio();
    } else {
        audio.pause();
        isPlaying = false;

        document.getElementById("play").textContent = "▶ PLAY";
        document.getElementById("sys").textContent = "PAUSED";
    }
}

function stopAudio() {
    audio.pause();
    audio.currentTime = 0;
    isPlaying = false;

    document.getElementById("play").textContent = "▶ PLAY";
    document.getElementById("sys").textContent = "STOPPED";
}

function next() {
    if(!MUSIC.length) return;

    if(isShuffle && MUSIC.length>1) {
        let n=current;

        while(n===current) {
            n=Math.floor(Math.random()*MUSIC.length);
        }

        loadTrack(n,true);
    } else {
        loadTrack(current+1,true);
    }
}

function prev() {
    if(!MUSIC.length) return;

    if(audio.currentTime>3) {
        audio.currentTime=0;
    } else {
        loadTrack(current-1,true);
    }
}

function shuffle() {
    isShuffle=!isShuffle;

    document.getElementById("msg").textContent =
        isShuffle ? "SHUFFLE MODE ON" : "SHUFFLE MODE OFF";
}

function repeat() {
    isRepeat=!isRepeat;
    audio.loop=isRepeat;

    document.getElementById("msg").textContent =
        isRepeat ? "REPEAT MODE ON" : "REPEAT MODE OFF";
}

audio.addEventListener("ended",()=>{
    if(!isRepeat) next();
});

audio.addEventListener("timeupdate",()=>{
    document.getElementById("now").textContent =
        timeFormat(audio.currentTime);

    document.getElementById("total").textContent =
        timeFormat(audio.duration);

    if(audio.duration>0) {
        document.getElementById("fill").style.width =
            (audio.currentTime/audio.duration*100)+"%";
    }
});

// =========================================================
// FULL SCREEN
// =========================================================

function fullScreen() {
    const el=document.getElementById("screen");

    if(!document.fullscreenElement) {
        if(el.requestFullscreen) el.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

// =========================================================
// CANVAS
// =========================================================

const orbit=document.getElementById("orbit");
const octx=orbit.getContext("2d");

const waveCanvas=document.getElementById("wave");
const wctx=waveCanvas.getContext("2d");

function resizeCanvas(canvas) {
    const rect=canvas.getBoundingClientRect();
    const dpr=Math.min(window.devicePixelRatio||1,2);

    canvas.width=Math.max(1,rect.width*dpr);
    canvas.height=Math.max(1,rect.height*dpr);

    canvas.getContext("2d").setTransform(dpr,0,0,dpr,0,0);
}

function resizeAll() {
    resizeCanvas(orbit);
    resizeCanvas(waveCanvas);
    resizeBG();
}

window.addEventListener("resize",resizeAll);

// =========================================================
// AUDIO DATA
// =========================================================

let tick=0;
let bass=0;
let treble=0;
let mid=0;

function average(arr,a,b) {
    let sum=0;
    let count=0;

    for(let i=a;i<b;i++) {
        sum+=arr[i];
        count++;
    }

    return count ? sum/count : 0;
}

// =========================================================
// ANIMATION ENGINE
// =========================================================

function animate() {
    requestAnimationFrame(animate);

    tick+=0.015;

    if(analyser && isPlaying) {
        analyser.getByteFrequencyData(freq);
        analyser.getByteTimeDomainData(waveData);

        const n=freq.length;

        bass=average(freq,0,Math.floor(n*0.15));
        mid=average(freq,Math.floor(n*0.15),Math.floor(n*0.55));
        treble=average(freq,Math.floor(n*0.55),n);
    } else {
        bass=8+Math.random()*10;
        mid=5+Math.random()*8;
        treble=5+Math.random()*10;
    }

    document.getElementById("bassNum").textContent =
        Math.round(bass).toString().padStart(3,"0");

    document.getElementById("trebleNum").textContent =
        Math.round(treble).toString().padStart(3,"0");

    updateBars();
    drawOrbit();
    drawWave();
}

// =========================================================
// SPECTRUM
// =========================================================

function updateBars() {
    const bars=spectrum.children;

    for(let i=0;i<bars.length;i++) {
        let v;

        if(analyser && isPlaying) {
            const idx=Math.floor(i/bars.length*freq.length);
            v=Math.max(3,freq[idx]/255*100);
        } else {
            v=5+Math.random()*25;
        }

        bars[i].style.height=v+"%";

        const hue=(i/bars.length*360+tick*25)%360;

        bars[i].style.background=`hsl(${hue},100%,65%)`;
        bars[i].style.boxShadow=`0 0 10px hsl(${hue},100%,60%)`;
    }

    for(let i=0;i<topBars.children.length;i++) {
        let v;

        if(analyser && isPlaying) {
            const idx=Math.floor(i/topBars.children.length*freq.length);
            v=Math.max(3,freq[idx]/255*100);
        } else {
            v=5+Math.random()*25;
        }

        topBars.children[i].style.height=v+"%";
    }

    for(let i=0;i<bassBars.children.length;i++) {
        const b=analyser && isPlaying
            ?freq[i]/255*100
            :Math.random()*75;

        const t=analyser && isPlaying
            ?freq[freq.length-1-i]/255*100
            :Math.random()*75;

        bassBars.children[i].style.height=Math.max(4,b)+"%";
        trebleBars.children[i].style.height=Math.max(4,t)+"%";
    }
}

// =========================================================
// CIRCULAR VISUALIZER
// =========================================================

function drawOrbit() {
    const rect=orbit.getBoundingClientRect();
    const w=rect.width;
    const h=rect.height;

    octx.clearRect(0,0,w,h);
    octx.save();
    octx.translate(w/2,h/2);

    const base=Math.min(w,h)*0.35;

    for(let layer=0;layer<6;layer++) {
        octx.beginPath();

        const points=260;

        for(let i=0;i<=points;i++) {
            const angle=i/points*Math.PI*2;

            let d;

            if(analyser && isPlaying) {
                const idx=Math.floor(i/points*freq.length);
                d=freq[idx]/255;
            } else {
                d=Math.sin(angle*12+tick+layer)*0.12;
            }

            const r=base+layer*9+d*(22+bass*0.15);
            const rot=tick*(layer%2 ? 1:-1);

            const x=Math.cos(angle+rot)*r;
            const y=Math.sin(angle+rot)*r;

            if(i===0) octx.moveTo(x,y);
            else octx.lineTo(x,y);
        }

        octx.closePath();

        const color=[
            C.c1,C.c2,C.c3,C.c4,C.c5,C.c6
        ][layer];

        octx.strokeStyle=color;
        octx.globalAlpha=.75-layer*.08;
        octx.lineWidth=layer===0 ? 2:1;
        octx.shadowBlur=15;
        octx.shadowColor=color;
        octx.stroke();
    }

    // ORBITING LIGHTS

    for(let i=0;i<36;i++) {
        const a=tick*(i%2 ? 1:-1)+i*Math.PI*2/36;
        const r=base+25+Math.sin(tick*3+i)*12;

        octx.beginPath();
        octx.arc(
            Math.cos(a)*r,
            Math.sin(a)*r,
            2+bass/55,
            0,
            Math.PI*2
        );

        const color=i%3===0 ? C.c4 : i%3===1 ? C.c1 : C.c5;

        octx.fillStyle=color;
        octx.shadowBlur=20;
        octx.shadowColor=color;
        octx.fill();
    }

    // RADAR

    const a=tick*.8;

    octx.beginPath();
    octx.moveTo(0,0);
    octx.arc(0,0,base*1.55,a,a+.3);
    octx.closePath();

    octx.fillStyle=C.c1;
    octx.globalAlpha=.08;
    octx.fill();

    octx.restore();
}

// =========================================================
// WAVEFORM
// =========================================================

function drawWave() {
    const rect=waveCanvas.getBoundingClientRect();
    const w=rect.width;
    const h=rect.height;

    wctx.clearRect(0,0,w,h);

    const colors=[C.c1,C.c2,C.c3,C.c4];

    for(let layer=0;layer<4;layer++) {
        wctx.beginPath();

        for(let x=0;x<w;x++) {
            let v;

            if(analyser && isPlaying) {
                const idx=Math.floor(x/w*waveData.length);
                v=(waveData[idx]-128)/128;
            } else {
                v=Math.sin(x*.03+tick+layer)*.2;
            }

            const y=h/2+v*h*.35+
                Math.sin(x*.015+tick+layer)*(layer+1)*3;

            if(x===0) wctx.moveTo(x,y);
            else wctx.lineTo(x,y);
        }

        wctx.strokeStyle=colors[layer];
        wctx.globalAlpha=.8-layer*.12;
        wctx.lineWidth=layer===0 ? 2:1;
        wctx.shadowBlur=15;
        wctx.shadowColor=colors[layer];
        wctx.stroke();
    }
}

// =========================================================
// PARTICLE SYSTEM
// =========================================================

const particlesCanvas=document.getElementById("particles");
const pctx=particlesCanvas.getContext("2d");
let particles=[];

function resizeBG() {
    const w=innerWidth;
    const h=innerHeight;

    particlesCanvas.width=w;
    particlesCanvas.height=h;

    document.getElementById("stars").width=w;
    document.getElementById("stars").height=h;

    document.getElementById("grid").width=w;
    document.getElementById("grid").height=h;

    particles=[];

    for(let i=0;i<130;i++) {
        particles.push({
            x:Math.random()*w,
            y:Math.random()*h,
            r:Math.random()*2.5+.5,
            dx:(Math.random()-.5)*.5,
            dy:(Math.random()-.5)*.5,
            hue:Math.random()*360,
            alpha:Math.random()
        });
    }

    drawGrid();
}

function drawGrid() {
    const canvas=document.getElementById("grid");
    const g=canvas.getContext("2d");

    g.clearRect(0,0,canvas.width,canvas.height);
    g.strokeStyle=C.c1;
    g.lineWidth=.5;

    for(let x=0;x<canvas.width;x+=35) {
        g.beginPath();
        g.moveTo(x,0);
        g.lineTo(x,canvas.height);
        g.stroke();
    }

    for(let y=0;y<canvas.height;y+=35) {
        g.beginPath();
        g.moveTo(0,y);
        g.lineTo(canvas.width,y);
        g.stroke();
    }
}

function particleLoop() {
    requestAnimationFrame(particleLoop);

    pctx.clearRect(0,0,particlesCanvas.width,particlesCanvas.height);

    const star=document.getElementById("stars");
    const sctx=star.getContext("2d");

    sctx.clearRect(0,0,star.width,star.height);

    for(const p of particles) {
        p.x+=p.dx*(1+bass/30);
        p.y+=p.dy*(1+bass/30);

        if(p.x<0) p.x=particlesCanvas.width;
        if(p.x>particlesCanvas.width) p.x=0;
        if(p.y<0) p.y=particlesCanvas.height;
        if(p.y>particlesCanvas.height) p.y=0;

        p.alpha+=(Math.random()-.5)*.05;
        p.alpha=Math.max(.15,Math.min(1,p.alpha));

        const color=`hsla(${p.hue},100%,65%,${p.alpha})`;

        pctx.beginPath();
        pctx.arc(p.x,p.y,p.r+bass/90,0,Math.PI*2);
        pctx.fillStyle=color;
        pctx.shadowBlur=18;
        pctx.shadowColor=color;
        pctx.fill();

        sctx.beginPath();
        sctx.arc(p.x,p.y,p.r,0,Math.PI*2);
        sctx.fillStyle=color;
        sctx.fill();
    }
}

// =========================================================
// START
// =========================================================

resizeAll();
particleLoop();
animate();

if(MUSIC.length>0) {
    document.getElementById("msg").textContent=
        MUSIC.length+" MUSIC FILES READY";

    document.getElementById("sys").textContent=
        "LIBRARY READY";

    loadTrack(0,false);
} else {
    document.getElementById("msg").textContent=
        "ADD MP3 FILE BESIDE Ta_app.py";

    document.getElementById("sys").textContent=
        "NO MUSIC FOUND";
}

</script>
</body>
</html>
"""

# =========================================================
# INSERT DATA SAFELY
# =========================================================

html = html.replace("__MUSIC__", music_json)
html = html.replace("__LOGO__", logo_base64)

# =========================================================
# DISPLAY
# =========================================================

st.iframe(
    html,
    height=850,
    width="stretch"
)
