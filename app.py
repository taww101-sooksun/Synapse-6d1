import streamlit as st
import streamlit.components.v1 as components

import os
import json
import base64
import mimetypes
from pathlib import Path


# =====================================================
# SYNAPSE NEON MUSIC STUDIO
# =====================================================

APP_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="SYNAPSE NEON MUSIC",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# HIDE STREAMLIT INTERFACE
# =====================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}

header {visibility:hidden;}

footer {visibility:hidden;}

.stApp {
    background:#03030a;
}

.block-container {
    padding:0 !important;
    margin:0 !important;
    max-width:100% !important;
}

[data-testid="stSidebar"] {
    display:none;
}

iframe {
    border:none !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD LOGO
# =====================================================

logo_path = APP_DIR / "671.jpg"
if not logo_path.exists():
    logo_path = APP_DIR / "logo1.jpg"

logo_data = ""

if logo_path.exists():

    with open(logo_path, "rb") as f:

        logo_data = base64.b64encode(
            f.read()
        ).decode("utf-8")


if logo_data:

    logo_url = "data:image/jpeg;base64," + logo_data

else:

    logo_url = ""


# =====================================================
# LOAD MUSIC FROM SAME FOLDER
# =====================================================

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".ogg",
    ".m4a",
    ".aac",
    ".flac"
}

music_files = sorted([
    p for p in APP_DIR.iterdir()
    if p.is_file()
    and p.suffix.lower() in AUDIO_EXTENSIONS
])


music_library = []

for path in music_files:

    try:

        mime = mimetypes.guess_type(
            path.name
        )[0]

        if not mime:
            mime = "audio/mpeg"

        with open(path, "rb") as f:

            encoded = base64.b64encode(
                f.read()
            ).decode("utf-8")

        music_library.append({

            "name": path.stem,

            "type": mime,

            "src": (
                "data:"
                + mime
                + ";base64,"
                + encoded
            )

        })

    except Exception:

        pass


tracks_json = json.dumps(
    music_library,
    ensure_ascii=False
)

logo_json = json.dumps(logo_url)


# =====================================================
# HTML START
# =====================================================

html = r"""

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width,
initial-scale=1.0,
maximum-scale=1.0,
user-scalable=no">


<style>

* {
    box-sizing:border-box;
    margin:0;
    padding:0;
}

html,body {

    width:100%;
    height:100%;

    overflow:hidden;

    background:#02020a;

    font-family:Arial,sans-serif;

    color:white;

}

#studio {

    position:relative;

    width:100%;

    height:100dvh;

    max-height:100dvh;

    overflow:hidden;

    background:
    radial-gradient(
        circle at 50% 45%,
        #10132b 0%,
        #050611 45%,
        #010107 100%
    );

}


/* BACKGROUND GRID */

.grid {

    position:absolute;

    inset:0;

    background-image:

    linear-gradient(
        rgba(0,255,255,.07) 1px,
        transparent 1px
    ),

    linear-gradient(
        90deg,
        rgba(0,255,255,.07) 1px,
        transparent 1px
    );

    background-size:35px 35px;

    opacity:.65;

}


/* SCAN LINES */

.scan {

    position:absolute;

    inset:0;

    pointer-events:none;

    background:repeating-linear-gradient(

        0deg,

        transparent,

        transparent 3px,

        rgba(255,255,255,.035) 4px

    );

    z-index:10;

}


/* PARTICLES */

#particles {

    position:absolute;

    width:100%;

    height:100%;

    inset:0;

}


/* HEADER */

.header {

    position:absolute;

    top:clamp(12px,2.5vh,24px);

    left:clamp(12px,3vw,24px);

    right:22px;

    display:flex;

    justify-content:space-between;

    align-items:center;

    z-index:5;

}

.brand {

    font-size:clamp(25px,7vw,42px);

    font-weight:900;

    letter-spacing:8px;

    color:#a7faff;

    text-shadow:

    0 0 8px #00eaff,

    0 0 25px #008cff,

    0 0 55px #00d9ff;

}

.subtitle {

    font-size:9px;

    letter-spacing:4px;

    color:#9aa8c8;

    margin-top:6px;

}

.status {

    text-align:right;

    font-size:10px;

    letter-spacing:3px;

    color:#f8dc65;

    line-height:2;

}


/* TOP SPECTRUM */

#spectrum {

    position:absolute;

    top:clamp(100px,18vh,150px);

    left:3%;

    width:94%;

    height:120px;

}


/* MAIN VISUALIZER */

.visualizer {

    position:absolute;

    width:min(88vw,510px);

    height:min(88vw,510px);

    max-height:510px;

    max-width:510px;

    left:50%;

    top:48%;

    transform:translate(-50%,-50%);

    display:flex;

    align-items:center;

    justify-content:center;

}


/* CIRCULAR CANVAS */

#visual {

    position:absolute;

    width:100%;

    height:100%;

    inset:0;

}


/* LOGO */

.logo-box {

    width:38%;

    aspect-ratio:1/1;

    border-radius:50%;

    overflow:hidden;

    position:relative;

    z-index:3;

    display:flex;

    justify-content:center;

    align-items:center;

    background:#03030a;

    border:3px solid #c5faff;

    box-shadow:

    0 0 12px #00eaff,

    0 0 35px #008cff,

    0 0 65px #a000ff,

    inset 0 0 25px #004cff;

    animation:logoPulse 3s infinite alternate;

}

.logo-box img {

    width:100%;

    height:100%;

    object-fit:cover;

}

.logo-text {

    font-size:24px;

    font-weight:900;

    color:#00eaff;

    text-shadow:0 0 20px cyan;

}

@keyframes logoPulse {

    from {

        transform:scale(.96);

        box-shadow:0 0 15px cyan;

    }

    to {

        transform:scale(1.04);

        box-shadow:

        0 0 35px cyan,

        0 0 65px purple;

    }

}


/* SIDE METERS */

.meter {

    position:absolute;

    top:42%;

    z-index:4;

    font-size:11px;

    letter-spacing:2px;

    color:#a8b9e5;

    text-shadow:0 0 10px cyan;

}

.left-meter {

    left:20px;

}

.right-meter {

    right:20px;

    text-align:right;

}

.meter strong {

    display:block;

    font-size:24px;

    margin-top:7px;

    color:#fff;

}


/* TRACK INFO */

.track-info {

    position:absolute;

    bottom:clamp(145px,21vh,185px);

    left:20px;

    right:20px;

    text-align:center;

    z-index:5;

}

.track-title {

    font-size:16px;

    font-weight:bold;

    color:#fff;

    text-shadow:0 0 15px cyan;

    white-space:nowrap;

    overflow:hidden;

    text-overflow:ellipsis;

}

.track-sub {

    font-size:10px;

    color:#9ba7c9;

    letter-spacing:3px;

    margin-top:6px;

}


/* PLAYER CONTROL */

.controls {

    position:absolute;

    bottom:clamp(12px,2vh,24px);

    left:0;

    right:0;

    z-index:6;

    text-align:center;

}

.buttons {

    display:flex;

    justify-content:center;

    align-items:center;

    gap:clamp(9px,2.8vw,18px);

}

.btn {

    width:clamp(40px,11vw,48px);

    height:clamp(40px,11vw,48px);

    border-radius:50%;

    border:1px solid #00eaff;

    background:rgba(0,20,45,.8);

    color:#fff;

    font-size:18px;

    box-shadow:0 0 15px rgba(0,220,255,.5);

    cursor:pointer;

}

.btn.play {

    width:clamp(54px,14vw,62px);

    height:clamp(54px,14vw,62px);

    font-size:24px;

    background:linear-gradient(
        135deg,
        #006aff,
        #9b00ff,
        #ff0080
    );

    border:2px solid white;

    box-shadow:

    0 0 20px #00eaff,

    0 0 40px #8b00ff;

}

.btn:active {

    transform:scale(.9);

}


/* PROGRESS */

.progress-area {

    margin:15px auto 0;

    width:85%;

}

#progress {

    width:100%;

    accent-color:#00eaff;

}

.time {

    display:flex;

    justify-content:space-between;

    font-size:10px;

    color:#9da9c9;

}


/* LIBRARY */

.library {

    position:absolute;

    top:18px;

    right:22px;

    z-index:9;

}

.library button {

    background:#11172b;

    color:#00eaff;

    border:1px solid #00eaff;

    border-radius:8px;

    padding:7px 12px;

}

#playlist {

    display:none;

    position:absolute;

    top:35px;

    right:0;

    width:230px;

    max-height:250px;

    overflow-y:auto;

    background:rgba(5,8,25,.97);

    border:1px solid #00eaff;

    box-shadow:0 0 25px #004cff;

    padding:8px;

}

.song {

    padding:10px;

    font-size:12px;

    border-bottom:1px solid #29304d;

    cursor:pointer;

    color:white;

}

.song:hover {

    color:#00ffff;

    background:#142344;

}



.theme-dock {position:absolute;left:50%;top:clamp(82px,13vh,125px);transform:translateX(-50%);z-index:8;display:flex;gap:6px;padding:6px 8px;border:1px solid rgba(130,220,255,.35);border-radius:24px;background:rgba(3,7,20,.72);backdrop-filter:blur(8px);}
.theme-dock button {width:28px;height:28px;border-radius:50%;border:1px solid rgba(255,255,255,.35);background:rgba(20,25,45,.8);color:white;font-size:14px;cursor:pointer;}
.theme-dock button:active {transform:scale(.9);}
@media(max-height:700px){.visualizer{top:48%;width:min(74vw,55vh);height:min(74vw,55vh)} #spectrum{height:85px;top:110px}.track-info{bottom:125px}.controls{bottom:8px}.buttons{gap:8px}.progress-area{margin-top:8px}}

/* RESPONSIVE */

@media(max-width:500px) {

    .visualizer {

        width:88vw;

        height:88vw;

        top:46%;

    }

    .meter {

        font-size:9px;

    }

    .meter strong {

        font-size:18px;

    }

    .left-meter {

        left:12px;

    }

    .right-meter {

        right:12px;

    }

    .track-info {

        bottom:150px;

    }

}

</style>

</head>


<body>

<div id="studio">

<div class="grid"></div>

<canvas id="particles"></canvas>

<div class="scan"></div>


<div class="header">

<div>

<div class="brand">SYNAPSE</div>

<div class="subtitle">

NEON MUSIC STUDIO / SOUND SYSTEM

</div>

</div>

<div class="status">

● AUDIO<br>

● NEON SYSTEM<br>

● READY

</div>

</div>


<canvas id="spectrum"></canvas>


<div class="meter left-meter">

BASS ENERGY

<strong id="bass">000</strong>

AUDIO INPUT

<br><br>

<span id="state">STANDBY</span>

</div>


<div class="meter right-meter">

TREBLE ENERGY

<strong id="treble">000</strong>

STEREO CHANNEL

<br><br>

<span> L / R ACTIVE </span>

</div>


<div class="visualizer">

<canvas id="visual"></canvas>

<div class="logo-box">

<img id="logo" style="display:none">

<div id="logoFallback" class="logo-text">

SYNAPSE

</div>

</div>

</div>


<div class="library">

<button onclick="toggleLibrary()">

♫ SONGS

</button>

<div id="playlist"></div>

</div>

<div class="theme-dock">
<button onclick="setTheme(0)" title="Neon spectrum">🌈</button>
<button onclick="setTheme(1)" title="Ice blue">🔵</button>
<button onclick="setTheme(2)" title="Purple pulse">🟣</button>
<button onclick="setTheme(3)" title="Solar gold">🟡</button>
<button onclick="setTheme(4)" title="Matrix green">🟢</button>
<button onclick="fullScreenMode()" title="Fullscreen">⛶</button>
</div>


<div class="track-info">

<div class="track-title" id="trackName">

SYNAPSE NEON MUSIC STUDIO

</div>

<div class="track-sub">

SOUND FREQUENCY / VISUAL EXPERIENCE

</div>

</div>


<div class="controls">

<div class="buttons">

<button class="btn" onclick="previousTrack()">

◀

</button>

<button class="btn play" onclick="togglePlay()" id="playBtn">

▶

</button>

<button class="btn" onclick="stopMusic()">

■

</button>

<button class="btn" onclick="nextTrack()">

▶▶

</button>

</div>


<div class="progress-area">

<input type="range"
id="progress"
min="0"
max="1000"
value="0"
oninput="seekMusic(this.value)">

<div class="time">

<span id="currentTime">00:00</span>

<span id="duration">00:00</span>

</div>

</div>

</div>


<audio id="audio" preload="metadata"></audio>

</div>

</body>

"""
# =====================================================
# JAVASCRIPT ENGINE
# =====================================================

html += r"""

<script>

const tracks = __TRACKS__;

const logoURL = __LOGO__;

const audio = document.getElementById("audio");

const playBtn = document.getElementById("playBtn");

const trackName = document.getElementById("trackName");

const playlist = document.getElementById("playlist");

const progress = document.getElementById("progress");

let currentTrack = 0;

let audioContext = null;

let analyser = null;

let sourceNode = null;

let frequencyData = null;

let playing = false;

let shuffle = false;

let pulse = 0;


const logo = document.getElementById("logo");

if (logoURL) {

    logo.src = logoURL;

    logo.style.display = "block";

    document.getElementById(
        "logoFallback"
    ).style.display = "none";

}


/* =====================================
   AUDIO ENGINE
===================================== */

function setupAudio() {

    if (audioContext) return;

    audioContext = new (
        window.AudioContext ||
        window.webkitAudioContext
    )();

    analyser = audioContext.createAnalyser();

    analyser.fftSize = 512;

    analyser.smoothingTimeConstant = 0.82;

    sourceNode = audioContext.createMediaElementSource(
        audio
    );

    sourceNode.connect(analyser);

    analyser.connect(audioContext.destination);

    frequencyData = new Uint8Array(
        analyser.frequencyBinCount
    );

}


/* =====================================
   LOAD TRACK
===================================== */

function loadTrack(index, autoplay=true) {

    if (!tracks.length) {

        trackName.innerText = "NO MUSIC FILE FOUND";

        return;

    }

    currentTrack = (
        index + tracks.length
    ) % tracks.length;

    audio.src = tracks[currentTrack].src;

    trackName.innerText = tracks[currentTrack].name;

    progress.value = 0;

    if (autoplay) {

        playMusic();

    }

    renderPlaylist();

}


/* =====================================
   PLAY
===================================== */

async function playMusic() {

    if (!tracks.length) return;

    try {

        setupAudio();

        if (audioContext.state === "suspended") {

            await audioContext.resume();

        }

        await audio.play();

        playing = true;

        playBtn.innerText = "Ⅱ";

        document.getElementById(
            "state"
        ).innerText = "PLAYING";

    } catch(e) {

        document.getElementById(
            "state"
        ).innerText = "PRESS PLAY";

    }

}


function togglePlay() {

    if (!tracks.length) return;

    if (audio.paused) {

        playMusic();

    } else {

        audio.pause();

        playing = false;

        playBtn.innerText = "▶";

        document.getElementById(
            "state"
        ).innerText = "PAUSED";

    }

}


/* =====================================
   STOP
===================================== */

function stopMusic() {

    audio.pause();

    audio.currentTime = 0;

    playing = false;

    playBtn.innerText = "▶";

    document.getElementById(
        "state"
    ).innerText = "STOPPED";

}


/* =====================================
   NEXT / PREVIOUS
===================================== */

function nextTrack() {

    let next = currentTrack + 1;

    if (shuffle && tracks.length > 1) {

        next = Math.floor(
            Math.random() * tracks.length
        );

    }

    loadTrack(next, true);

}


function previousTrack() {

    if (audio.currentTime > 3) {

        audio.currentTime = 0;

        return;

    }

    loadTrack(currentTrack - 1, true);

}


audio.addEventListener("ended", nextTrack);


/* =====================================
   PLAYLIST
===================================== */

function toggleLibrary() {

    playlist.style.display =
        playlist.style.display === "block"
        ? "none"
        : "block";

}


function renderPlaylist() {

    playlist.innerHTML = "";

    tracks.forEach((track, index) => {

        const item = document.createElement("div");

        item.className = "song";

        item.innerText =
            (index + 1) + ". " + track.name;

        item.onclick = function() {

            loadTrack(index, true);

            playlist.style.display = "none";

        };

        playlist.appendChild(item);

    });

}


/* =====================================
   TIME / PROGRESS
===================================== */

function formatTime(seconds) {

    if (!Number.isFinite(seconds)) {

        return "00:00";

    }

    let minutes = Math.floor(seconds / 60);

    let secs = Math.floor(seconds % 60);

    return (
        String(minutes).padStart(2,"0")
        + ":"
        + String(secs).padStart(2,"0")
    );

}


function seekMusic(value) {

    if (audio.duration) {

        audio.currentTime =
            (value / 1000) * audio.duration;

    }

}


audio.addEventListener("timeupdate", function() {

    if (audio.duration) {

        progress.value =
            (audio.currentTime / audio.duration) * 1000;

        document.getElementById(
            "currentTime"
        ).innerText = formatTime(audio.currentTime);

        document.getElementById(
            "duration"
        ).innerText = formatTime(audio.duration);

    }

});



const themeSets = [
 ["#00eaff","#a000ff","#ff007a","#ffd700","#00ff88","#ffffff"],
 ["#00d9ff","#0077ff","#6aeaff","#a8f4ff","#ffffff","#4a8cff"],
 ["#d000ff","#7b2cff","#ff35df","#a86bff","#00eaff","#ffffff"],
 ["#ffd000","#ff8c00","#ff3d00","#fff27a","#ffcc44","#ffffff"],
 ["#00ff66","#00cc88","#66ff00","#00eaff","#aaff44","#ffffff"]
];
let themeIndex=0;
let colors=[...themeSets[0]];
function setTheme(n){themeIndex=n; colors.splice(0,colors.length,...themeSets[n]); document.documentElement.style.setProperty('--accent',colors[0]); document.getElementById('state').innerText=playing?'PLAYING':'THEME '+(n+1)+' ACTIVE';}
function fullScreenMode(){const el=document.getElementById('studio');if(!document.fullscreenElement){el.requestFullscreen?.();}else{document.exitFullscreen?.();}}

/* =====================================
   VISUALIZER
===================================== */

const canvas = document.getElementById("visual");

const ctx = canvas.getContext("2d");

const spectrumCanvas =
    document.getElementById("spectrum");

const sctx = spectrumCanvas.getContext("2d");


function resizeCanvas() {

    const box = canvas.getBoundingClientRect();

    const dpr = Math.min(
        window.devicePixelRatio || 1,
        2
    );

    canvas.width = box.width * dpr;

    canvas.height = box.height * dpr;

    ctx.setTransform(dpr,0,0,dpr,0,0);

    const sw = spectrumCanvas.getBoundingClientRect();

    spectrumCanvas.width = sw.width * dpr;

    spectrumCanvas.height = sw.height * dpr;

    sctx.setTransform(dpr,0,0,dpr,0,0);

}


window.addEventListener("resize", resizeCanvas);

resizeCanvas();


/* =====================================
   DRAW CIRCULAR ENERGY
===================================== */

function drawVisual() {

    const w = canvas.clientWidth;

    const h = canvas.clientHeight;

    const cx = w / 2;

    const cy = h / 2;

    const baseRadius = Math.min(w,h) * .31;

    ctx.clearRect(0,0,w,h);

    let bass = 0;

    let treble = 0;

    if (analyser && playing) {

        analyser.getByteFrequencyData(
            frequencyData
        );

        for (let i=0;i<35;i++) {

            bass += frequencyData[i];

        }

        for (
            let i=frequencyData.length-35;
            i<frequencyData.length;
            i++
        ) {

            treble += frequencyData[i];

        }

        bass = bass / 35;

        treble = treble / 35;

    } else {

        pulse += .025;

        bass = 15 + Math.sin(pulse) * 8;

        treble = 10 + Math.cos(pulse) * 6;

    }

    document.getElementById("bass").innerText =
        String(Math.round(bass)).padStart(3,"0");

    document.getElementById("treble").innerText =
        String(Math.round(treble)).padStart(3,"0");


    /* MULTI LAYER RINGS */

    for (let layer=0;layer<5;layer++) {

        ctx.beginPath();

        const color = colors[layer];

        for (let i=0;i<=240;i++) {

            const angle =
                i / 240 * Math.PI * 2;

            let data = 0;

            if (analyser && playing) {

                const index = Math.floor(
                    i / 240 * frequencyData.length
                );

                data = frequencyData[index] / 255;

            } else {

                data = Math.sin(
                    angle * 8 + pulse
                ) * .12;

            }

            const radius =
                baseRadius
                + layer * 12
                + data * (25 + bass * .15);

            const x = cx + Math.cos(angle) * radius;

            const y = cy + Math.sin(angle) * radius;

            if (i===0) {

                ctx.moveTo(x,y);

            } else {

                ctx.lineTo(x,y);

            }

        }

        ctx.closePath();

        ctx.strokeStyle = color;

        ctx.lineWidth = layer===0 ? 3 : 1.5;

        ctx.shadowColor = color;

        ctx.shadowBlur = 15 + bass * .08;

        ctx.stroke();

    }


    /* OUTER ENERGY BARS */

    for (let i=0;i<100;i++) {

        const angle =
            i / 100 * Math.PI * 2;

        let value = 0;

        if (analyser && playing) {

            value =
                frequencyData[i % frequencyData.length] / 255;

        } else {

            value =
                Math.abs(Math.sin(pulse + i * .2)) * .25;

        }

        const r1 = baseRadius + 65;

        const r2 = r1 + 8 + value * 45;

        const x1 = cx + Math.cos(angle) * r1;

        const y1 = cy + Math.sin(angle) * r1;

        const x2 = cx + Math.cos(angle) * r2;

        const y2 = cy + Math.sin(angle) * r2;

        ctx.beginPath();

        ctx.moveTo(x1,y1);

        ctx.lineTo(x2,y2);

        ctx.strokeStyle = colors[i % colors.length];

        ctx.lineWidth = 2;

        ctx.shadowBlur = 8;

        ctx.shadowColor = colors[i % colors.length];

        ctx.stroke();

    }

}


/* =====================================
   TOP SPECTRUM
===================================== */

function drawSpectrum() {

    const w = spectrumCanvas.clientWidth;

    const h = spectrumCanvas.clientHeight;

    sctx.clearRect(0,0,w,h);

    const bars = 65;

    const gap = 4;

    const barWidth = (w - gap * bars) / bars;

    for (let i=0;i<bars;i++) {

        let value = 0;

        if (analyser && playing) {

            const index = Math.floor(
                i / bars * frequencyData.length
            );

            value = frequencyData[index] / 255;

        } else {

            value =
                Math.abs(Math.sin(pulse + i * .3)) * .2;

        }

        const barHeight = 5 + value * h * .85;

        const x = i * (barWidth + gap);

        const y = h - barHeight;

        const gradient = sctx.createLinearGradient(
            0,y,0,h
        );

        gradient.addColorStop(0,"#ff00cc");

        gradient.addColorStop(.45,"#00eaff");

        gradient.addColorStop(1,"#0066ff");

        sctx.fillStyle = gradient;

        sctx.shadowColor = "#00eaff";

        sctx.shadowBlur = 10;

        sctx.fillRect(
            x,y,barWidth,barHeight
        );

    }

}


/* =====================================
   PARTICLES
===================================== */

const pCanvas = document.getElementById("particles");

const pctx = pCanvas.getContext("2d");

let particles = [];


function resizeParticles() {

    pCanvas.width = pCanvas.clientWidth;

    pCanvas.height = pCanvas.clientHeight;

}


resizeParticles();

window.addEventListener(
    "resize",
    resizeParticles
);


for (let i=0;i<100;i++) {

    particles.push({

        x:Math.random(),

        y:Math.random(),

        size:Math.random()*3+1,

        speed:Math.random()*.0008+.0002,

        color:colorsRandom()

    });

}


function colorsRandom() {

    const colors = [

        "#00ffff",

        "#ff00cc",

        "#00ff66",

        "#ffcc00",

        "#ffffff",

        "#0066ff"

    ];

    return colors[
        Math.floor(Math.random()*colors.length)
    ];

}


function drawParticles() {

    const w = pCanvas.width;

    const h = pCanvas.height;

    pctx.clearRect(0,0,w,h);

    particles.forEach(p => {

        p.y -= p.speed * h;

        if (p.y < 0) {

            p.y = 1;

            p.x = Math.random();

        }

        pctx.beginPath();

        pctx.arc(
            p.x*w,
            p.y*h,
            p.size,
            0,
            Math.PI*2
        );

        pctx.fillStyle = p.color;

        pctx.shadowColor = p.color;

        pctx.shadowBlur = 12;

        pctx.fill();

    });

}


/* =====================================
   ANIMATION LOOP
===================================== */

function animate() {

    if (analyser && playing) {

        analyser.getByteFrequencyData(
            frequencyData
        );

    }

    drawVisual();

    drawSpectrum();

    drawParticles();

    requestAnimationFrame(animate);

}


/* =====================================
   START
===================================== */

if (tracks.length > 0) {

    loadTrack(0,false);

    document.getElementById(
        "state"
    ).innerText = "LIBRARY READY";

} else {

    document.getElementById(
        "state"
    ).innerText = "NO MUSIC";

    trackName.innerText =
        "ADD MUSIC TO APP FOLDER";

}


renderPlaylist();

animate();


</script>

</html>

"""


# =====================================================
# INSERT DATA
# =====================================================

html = html.replace(
    "__TRACKS__",
    tracks_json
)

html = html.replace(
    "__LOGO__",
    logo_json
)


# =====================================================
# DISPLAY
# =====================================================

components.html(
    html,
    height=850,
    scrolling=False
)
