import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json
import mimetypes
import random

# =========================================================
# SYNAPSE NEON MUSIC STUDIO - MAXIMAL EDITION
# =========================================================

APP_DIR = Path(__file__).resolve().parent
LOGO_PATH = APP_DIR / "logo1.jpg"

SUPPORTED_AUDIO = {
    ".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac"
}

st.set_page_config(
    page_title="SYNAPSE NEON MUSIC STUDIO",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# HIDE STREAMLIT UI
# =========================================================

st.markdown("""
<style>
#MainMenu,
header,
footer,
.stDeployButton,
[data-testid="stSidebar"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    display: none !important;
}

html, body {
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    background: #02030a !important;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #02030a !important;
    margin: 0 !important;
    padding: 0 !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

iframe {
    border: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# READ LOGO
# =========================================================

logo_b64 = ""

if LOGO_PATH.exists():
    logo_b64 = base64.b64encode(
        LOGO_PATH.read_bytes()
    ).decode("utf-8")

# =========================================================
# AUTO READ MUSIC FROM SAME FOLDER
# =========================================================

music_files = sorted(
    [
        p for p in APP_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_AUDIO
    ],
    key=lambda p: p.name.lower()
)

tracks = []

for file_path in music_files:
    try:
        raw = file_path.read_bytes()
        mime = mimetypes.guess_type(file_path.name)[0]

        if not mime:
            mime = "audio/mpeg"

        tracks.append({
            "name": file_path.stem,
            "filename": file_path.name,
            "type": mime,
            "data": base64.b64encode(raw).decode("ascii")
        })
    except Exception:
        pass

music_json = json.dumps(tracks, ensure_ascii=False)

# =========================================================
# VISUALIZER HTML
# =========================================================

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: #02030a;
    overflow: hidden;
    font-family: Arial, Helvetica, sans-serif;
}

:root {
    --c1: #00eaff;
    --c2: #bd00ff;
    --c3: #ff1744;
    --c4: #ffd700;
    --c5: #ffffff;
    --c6: #00ff88;
}

#screen {
    position: relative;
    width: 100%;
    height: 100vh;
    min-height: 520px;
    overflow: hidden;
    isolation: isolate;

    background:
        radial-gradient(ellipse at 50% 50%,
        #10152a 0%,
        #080916 38%,
        #02030a 80%);
}

/* BACKGROUND FX */

#starCanvas,
#particleCanvas,
#gridCanvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

#gridCanvas {
    opacity: 0.17;
}

.scanlines {
    position: absolute;
    inset: 0;
    z-index: 30;
    pointer-events: none;
    opacity: 0.10;

    background: repeating-linear-gradient(
        to bottom,
        transparent 0px,
        transparent 2px,
        #fff 3px,
        transparent 4px
    );
}

.vignette {
    position: absolute;
    inset: 0;
    z-index: 29;
    pointer-events: none;

    background:
        radial-gradient(
            ellipse at center,
            transparent 35%,
            rgba(0,0,0,0.15) 65%,
            rgba(0,0,0,0.8) 100%
        );
}

/* HEADER */

.header {
    position: absolute;
    top: 2%;
    left: 3%;
    right: 3%;
    z-index: 20;

    display: flex;
    justify-content: space-between;
    align-items: center;
}

.brand {
    font-size: clamp(17px, 3vw, 34px);
    font-weight: 900;
    letter-spacing: 0.35em;

    color: var(--c1);

    text-shadow:
        0 0 5px var(--c1),
        0 0 20px var(--c1),
        0 0 50px var(--c2);
}

.brandSub {
    font-size: 8px;
    letter-spacing: 0.45em;
    color: #9aa8c7;
    margin-top: 5px;
}

.headerRight {
    text-align: right;
    color: var(--c4);
    font-size: 10px;
    letter-spacing: 0.2em;
    line-height: 1.8;
}

.liveDot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--c3);
    box-shadow: 0 0 15px var(--c3);
    animation: blink 1s infinite;
}

@keyframes blink {
    50% { opacity: 0.15; }
}

/* HUD CORNERS */

.corner {
    position: absolute;
    width: 50px;
    height: 50px;
    z-index: 4;
    opacity: 0.8;
}

.tl {
    top: 12%;
    left: 2%;
    border-top: 2px solid var(--c1);
    border-left: 2px solid var(--c1);
}

.tr {
    top: 12%;
    right: 2%;
    border-top: 2px solid var(--c3);
    border-right: 2px solid var(--c3);
}

.bl {
    bottom: 5%;
    left: 2%;
    border-bottom: 2px solid var(--c4);
    border-left: 2px solid var(--c4);
}

.br {
    bottom: 5%;
    right: 2%;
    border-bottom: 2px solid var(--c2);
    border-right: 2px solid var(--c2);
}

/* CENTRAL CORE */

.core {
    position: absolute;
    left: 50%;
    top: 47%;
    transform: translate(-50%, -50%);

    width: min(68vw, 68vh);
    height: min(68vw, 68vh);

    max-width: 620px;
    max-height: 620px;

    z-index: 6;
}

.ring {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    pointer-events: none;
}

.ring1 {
    inset: 1%;
    border: 1px dashed var(--c1);
    box-shadow: 0 0 12px var(--c1);
    opacity: 0.55;
    animation: rotate 36s linear infinite;
}

.ring2 {
    inset: 5%;
    border: 2px solid var(--c2);
    box-shadow: 0 0 15px var(--c2), inset 0 0 12px var(--c2);
    opacity: 0.5;
    animation: rotateReverse 23s linear infinite;
}

.ring3 {
    inset: 10%;
    border: 1px dotted var(--c4);
    opacity: 0.8;
    animation: rotate 16s linear infinite;
}

.ring4 {
    inset: 15%;
    border: 3px double var(--c5);
    opacity: 0.4;
    animation: rotateReverse 11s linear infinite;
}

.ring5 {
    inset: 20%;
    border: 1px dashed var(--c3);
    box-shadow: 0 0 15px var(--c3);
    opacity: 0.6;
    animation: rotate 8s linear infinite;
}

.ring6 {
    inset: 25%;
    border: 2px solid var(--c1);
    opacity: 0.6;
    animation: rotateReverse 5s linear infinite;
}

@keyframes rotate {
    to { transform: rotate(360deg); }
}

@keyframes rotateReverse {
    to { transform: rotate(-360deg); }
}

#orbitCanvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
}

/* LOGO */

.logoBox {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    width: 31%;
    height: 31%;

    border-radius: 50%;
    overflow: hidden;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #02030a;
    border: 3px solid var(--c4);

    box-shadow:
        0 0 10px var(--c4),
        0 0 30px var(--c1),
        0 0 70px var(--c2),
        inset 0 0 25px var(--c1);

    animation: logoPulse 3s ease-in-out infinite;
}

.logoBox img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

@keyframes logoPulse {
    0%,100% {
        transform: translate(-50%, -50%) scale(0.98);
    }
    50% {
        transform: translate(-50%, -50%) scale(1.04);
    }
}

/* SIDE METERS */

.side {
    position: absolute;
    top: 25%;
    width: 20%;
    z-index: 10;
}

.sideLeft {
    left: 2%;
}

.sideRight {
    right: 2%;
    text-align: right;
}

.title {
    font-size: 9px;
    letter-spacing: 0.3em;
    color: var(--c1);
    text-shadow: 0 0 10px var(--c1);
    margin-bottom: 12px;
}

.meter {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 100px;
}

.sideRight .meter {
    justify-content: flex-end;
}

.meter span {
    width: 5px;
    flex: 1;
    max-width: 9px;
    height: 5%;
    border-radius: 2px 2px 0 0;
    background: var(--c1);
    box-shadow: 0 0 8px var(--c1);
}

.sideRight .meter span {
    background: var(--c3);
    box-shadow: 0 0 8px var(--c3);
}

.value {
    color: var(--c4);
    font-size: clamp(15px, 2.2vw, 25px);
    margin-top: 10px;
    text-shadow: 0 0 15px var(--c4);
}

.smallText {
    font-size: 8px;
    color: #8d9cb7;
    letter-spacing: 0.18em;
    line-height: 2;
    margin-top: 12px;
}

/* TOP MINI BARS */

.miniTop {
    position: absolute;
    left: 25%;
    right: 25%;
    top: 16%;
    height: 50px;
    z-index: 5;
    display: flex;
    align-items: flex-end;
    gap: 2px;
    justify-content: center;
}

.miniTop span {
    flex: 1;
    max-width: 7px;
    height: 5%;
    background: var(--c4);
    box-shadow: 0 0 8px var(--c4);
}

/* BOTTOM SPECTRUM */

.spectrum {
    position: absolute;
    left: 3%;
    right: 3%;
    bottom: 24%;
    height: 13%;
    z-index: 8;

    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 2px;
}

.spectrum span {
    flex: 1;
    min-width: 1px;
    max-width: 12px;
    height: 3%;
    border-radius: 2px 2px 0 0;
}

/* WAVE */

.waveArea {
    position: absolute;
    left: 4%;
    right: 4%;
    top: 39%;
    height: 13%;
    z-index: 7;
}

#waveCanvas {
    width: 100%;
    height: 100%;
}

/* TRACK INFO */

.trackPanel {
    position: absolute;
    left: 5%;
    right: 5%;
    bottom: 16%;
    text-align: center;
    z-index: 12;
}

.trackName {
    font-size: clamp(12px, 2vw, 20px);
    letter-spacing: 0.15em;
    color: white;
    text-shadow: 0 0 12px var(--c1), 0 0 25px var(--c2);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.trackSub {
    color: var(--c4);
    font-size: 8px;
    letter-spacing: 0.4em;
    margin-bottom: 8px;
}

/* CONTROL PANEL */

.controlPanel {
    position: absolute;
    bottom: 2%;
    left: 5%;
    right: 5%;
    z-index: 20;
    text-align: center;
}

.buttons {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 5px;
}

button {
    border: 1px solid var(--c1);
    background: rgba(2, 7, 18, 0.88);
    color: var(--c1);

    padding: 7px 11px;
    border-radius: 3px;

    font-size: 9px;
    letter-spacing: 0.12em;

    box-shadow: 0 0 8px rgba(0,234,255,0.2);
    cursor: pointer;
}

button:active,
button:hover {
    color: #000;
    background: var(--c1);
    box-shadow: 0 0 20px var(--c1);
}

#playBtn {
    border-color: var(--c4);
    color: var(--c4);
}

#playBtn:hover {
    background: var(--c4);
    color: black;
}

.progress {
    height: 3px;
    margin: 10px auto 5px;
    width: 75%;
    background: #283044;
    overflow: hidden;
}

#progressFill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, var(--c1), var(--c2), var(--c3), var(--c4));
    box-shadow: 0 0 12px var(--c1);
}

.time {
    font-size: 8px;
    color: #9ba9c4;
    letter-spacing: 0.15em;
}

.message {
    color: var(--c4);
    font-size: 8px;
    margin-top: 6px;
}

/* COLOR CONTROL */

.colorPanel {
    position: absolute;
    z-index: 50;
    top: 12%;
    left: 50%;
    transform: translateX(-50%);

    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 4px;

    background: rgba(0,0,0,0.7);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 5px;
    padding: 5px;
}

.colorPanel label {
    color: #8b9bb6;
    font-size: 7px;
    letter-spacing: 0.1em;
    display: flex;
    align-items: center;
    gap: 3px;
}

.colorPanel input {
    width: 20px;
    height: 18px;
    padding: 0;
    border: 0;
    background: none;
}

/* FULLSCREEN */

.fullBtn {
    position: absolute;
    right: 3%;
    bottom: 2%;
    z-index: 60;
}

/* RESPONSIVE */

@media (max-width: 700px) {

    .core {
        width: min(78vw, 54vh);
        height: min(78vw, 54vh);
        top: 48%;
    }

    .side {
        top: 28%;
        width: 19%;
    }

    .meter {
        height: 60px;
    }

    .side .smallText {
        font-size: 6px;
    }

    .miniTop {
        top: 18%;
    }

    .spectrum {
        bottom: 24%;
        height: 10%;
    }

    .trackPanel {
        bottom: 16%;
    }

    .controlPanel {
        bottom: 2%;
    }

    .colorPanel {
        top: 12%;
        width: 94%;
    }

    button {
        padding: 6px 8px;
        font-size: 8px;
    }

    .fullBtn {
        bottom: 11%;
    }

    .brandSub {
        letter-spacing: 0.22em;
    }
}

@media (max-height: 600px) {
    .core {
        width: min(55vh, 60vw);
        height: min(55vh, 60vw);
        top: 44%;
    }

    .side {
        top: 20%;
    }

    .spectrum {
        bottom: 23%;
        height: 12%;
    }

    .trackPanel {
        bottom: 13%;
    }

    .controlPanel {
        bottom: 1%;
    }

    .colorPanel {
        top: 11%;
    }
}

</style>
</head>

<body>

<div id="screen">

<canvas id="starCanvas"></canvas>
<canvas id="particleCanvas"></canvas>
<canvas id="gridCanvas"></canvas>

<div class="scanlines"></div>
<div class="vignette"></div>

<div class="corner tl"></div>
<div class="corner tr"></div>
<div class="corner bl"></div>
<div class="corner br"></div>

<!-- HEADER -->

<div class="header">
    <div>
        <div class="brand">SYNAPSE</div>
        <div class="brandSub">SOUND & VISUAL THERAPY / NEON SYSTEM</div>
    </div>

    <div class="headerRight">
        <span class="liveDot"></span> AUDIO SYSTEM<br>
        <span id="systemStatus">STANDBY</span>
    </div>
</div>

<!-- TOP SPECTRUM -->

<div class="miniTop" id="miniTop"></div>

<!-- SIDE LEFT -->

<div class="side sideLeft">
    <div class="title">LOW FREQUENCY</div>
    <div class="meter" id="bassMeter"></div>

    <div class="value" id="bassValue">000</div>

    <div class="smallText">
        BASS ENERGY<br>
        SUB WAVE / CHANNEL A<br>
        <span id="bassStatus">STANDBY</span>
    </div>
</div>

<!-- SIDE RIGHT -->

<div class="side sideRight">
    <div class="title">HIGH FREQUENCY</div>
    <div class="meter" id="trebleMeter"></div>

    <div class="value" id="trebleValue">000</div>

    <div class="smallText">
        TREBLE ENERGY<br>
        STEREO / CHANNEL B<br>
        <span id="trebleStatus">STANDBY</span>
    </div>
</div>

<!-- CORE -->

<div class="core" id="core">

    <div class="ring ring1"></div>
    <div class="ring ring2"></div>
    <div class="ring ring3"></div>
    <div class="ring ring4"></div>
    <div class="ring ring5"></div>
    <div class="ring ring6"></div>

    <canvas id="orbitCanvas"></canvas>

    <div class="logoBox" id="logoBox">
        <div style="color:var(--c1);font-weight:900;">SYNAPSE</div>
    </div>
</div>

<!-- WAVE -->

<div class="waveArea">
    <canvas id="waveCanvas"></canvas>
</div>

<!-- BOTTOM SPECTRUM -->

<div class="spectrum" id="spectrum"></div>

<!-- TRACK -->

<div class="trackPanel">
    <div class="trackSub">NOW PLAYING / NEURAL AUDIO</div>
    <div class="trackName" id="trackName">SYNAPSE NEON MUSIC STUDIO</div>
</div>

<!-- COLOR SELECTORS -->

<div class="colorPanel">
    <label>RING <input type="color" value="#00eaff" id="color1"></label>
    <label>ORBIT <input type="color" value="#bd00ff" id="color2"></label>
    <label>WAVE <input type="color" value="#ffffff" id="color3"></label>
    <label>BASS <input type="color" value="#ffd700" id="color4"></label>
    <label>BAR <input type="color" value="#ff1744" id="color5"></label>
    <label>PARTICLE <input type="color" value="#00ff88" id="color6"></label>
</div>

<!-- CONTROLS -->

<div class="controlPanel">

    <div class="buttons">
        <button onclick="prevTrack()">◀ PREV</button>
        <button id="playBtn" onclick="togglePlay()">▶ PLAY</button>
        <button onclick="stopMusic()">■ STOP</button>
        <button onclick="nextTrack()">NEXT ▶</button>
        <button onclick="toggleShuffle()" id="shuffleBtn">SHUFFLE OFF</button>
        <button onclick="toggleRepeat()" id="repeatBtn">REPEAT OFF</button>
    </div>

    <div class="progress">
        <div id="progressFill"></div>
    </div>

    <div class="time">
        <span id="currentTime">00:00</span>
        /
        <span id="duration">00:00</span>
    </div>

    <div class="message" id="message">SYSTEM READY</div>
</div>

<button class="fullBtn" onclick="fullscreen()">⛶ FULL SCREEN</button>

</div>

<script>

// =========================================================
// CONFIG
// =========================================================

const MUSIC = __MUSIC__;
const LOGO_DATA = "__LOGO__";

const COLORS = {
    c1: "#00eaff",
    c2: "#bd00ff",
    c3: "#ffffff",
    c4: "#ffd700",
    c5: "#ff1744",
    c6: "#00ff88"
};

function setColor(name, value) {
    COLORS[name] = value;
    document.documentElement.style.setProperty("--" + name, value);
}

// =========================================================
// LOGO
// =========================================================

const logoBox = document.getElementById("logoBox");

if (LOGO_DATA && LOGO_DATA.length > 20) {
    logoBox.innerHTML =
        `<img src="data:image/jpeg;base64,${LOGO_DATA}" alt="SYNAPSE">`;
}

// =========================================================
// COLOR CONTROLS
// =========================================================

[
    ["color1", "c1"],
    ["color2", "c2"],
    ["color3", "c3"],
    ["color4", "c4"],
    ["color5", "c5"],
    ["color6", "c6"]
].forEach(([id, key]) => {
    const el = document.getElementById(id);
    el.addEventListener("input", () => {
        setColor(key, el.value);
    });
});

// =========================================================
// CREATE BARS
// =========================================================

const spectrum = document.getElementById("spectrum");
const miniTop = document.getElementById("miniTop");
const bassMeter = document.getElementById("bassMeter");
const trebleMeter = document.getElementById("trebleMeter");

for (let i = 0; i < 96; i++) {
    const bar = document.createElement("span");
    spectrum.appendChild(bar);
}

for (let i = 0; i < 48; i++) {
    const bar = document.createElement("span");
    miniTop.appendChild(bar);
}

for (let i = 0; i < 24; i++) {
    bassMeter.appendChild(document.createElement("span"));
    trebleMeter.appendChild(document.createElement("span"));
}

// =========================================================
// AUDIO PLAYER
// =========================================================

let audio = new Audio();
audio.preload = "auto";

let audioContext = null;
let analyser = null;
let sourceNode = null;
let freq = null;
let timeData = null;

let currentIndex = 0;
let isShuffle = false;
let isRepeat = false;
let isPlaying = false;

function initAudio() {
    if (!audioContext) {
        audioContext = new (
            window.AudioContext ||
            window.webkitAudioContext
        )();

        analyser = audioContext.createAnalyser();
        analyser.fftSize = 512;
        analyser.smoothingTimeConstant = 0.78;

        sourceNode = audioContext.createMediaElementSource(audio);

        sourceNode.connect(analyser);
        analyser.connect(audioContext.destination);

        freq = new Uint8Array(analyser.frequencyBinCount);
        timeData = new Uint8Array(analyser.fftSize);
    }

    if (audioContext.state === "suspended") {
        audioContext.resume();
    }
}

function fmtTime(sec) {
    if (!Number.isFinite(sec)) return "00:00";

    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);

    return String(m).padStart(2, "0") 
               + ":" +
           String(s).padStart(2, "0");
}

// =========================================================
// AUDIO TRACK CONTROL
// =========================================================

function loadTrack(index, autoPlay = true) {
    if (!MUSIC.length) {
        document.getElementById("message").textContent =
            "NO MUSIC FILE FOUND";
        return;
    }

    currentIndex = (index + MUSIC.length) % MUSIC.length;

    const track = MUSIC[currentIndex];

    audio.src = `data:${track.type};base64,${track.data}`;
    audio.load();

    document.getElementById("trackName").textContent = track.name;
    document.getElementById("message").textContent =
        "TRACK " + (currentIndex + 1) + " / " + MUSIC.length;

    if (autoPlay) {
        playMusic();
    }
}

function playMusic() {
    if (!MUSIC.length) {
        document.getElementById("message").textContent =
            "ADD MUSIC BESIDE Ta_app.py";
        return;
    }

    initAudio();

    if (!audio.src) {
        loadTrack(currentIndex, false);
    }

    audio.play().then(() => {
        isPlaying = true;

        document.getElementById("playBtn").textContent = "❚❚ PAUSE";
        document.getElementById("systemStatus").textContent = "AUDIO PLAYING";
        document.getElementById("bassStatus").textContent = "ACTIVE";
        document.getElementById("trebleStatus").textContent = "ACTIVE";
        document.getElementById("message").textContent = "NEURAL AUDIO ACTIVE";

    }).catch(() => {
        document.getElementById("message").textContent =
            "PRESS PLAY TO START";
    });
}

function togglePlay() {
    if (!MUSIC.length) return;

    initAudio();

    if (audio.paused) {
        playMusic();
    } else {
        audio.pause();
        isPlaying = false;

        document.getElementById("playBtn").textContent = "▶ PLAY";
        document.getElementById("systemStatus").textContent = "PAUSED";
    }
}

function stopMusic() {
    audio.pause();
    audio.currentTime = 0;
    isPlaying = false;

    document.getElementById("playBtn").textContent = "▶ PLAY";
    document.getElementById("systemStatus").textContent = "STOPPED";
}

function nextTrack() {
    if (!MUSIC.length) return;

    if (isShuffle && MUSIC.length > 1) {
        let n;

        do {
            n = Math.floor(Math.random() * MUSIC.length);
        } while (n === currentIndex);

        loadTrack(n);
    } else {
        loadTrack(currentIndex + 1);
    }
}

function prevTrack() {
    if (!MUSIC.length) return;

    if (audio.currentTime > 3) {
        audio.currentTime = 0;
        return;
    }

    loadTrack(currentIndex - 1);
}

function toggleShuffle() {
    isShuffle = !isShuffle;

    document.getElementById("shuffleBtn").textContent =
        isShuffle ? "SHUFFLE ON" : "SHUFFLE OFF";
}

function toggleRepeat() {
    isRepeat = !isRepeat;
    audio.loop = isRepeat;

    document.getElementById("repeatBtn").textContent =
        isRepeat ? "REPEAT ON" : "REPEAT OFF";
}

audio.addEventListener("ended", () => {
    if (!isRepeat) nextTrack();
});

audio.addEventListener("timeupdate", () => {
    document.getElementById("currentTime").textContent =
        fmtTime(audio.currentTime);

    document.getElementById("duration").textContent =
        fmtTime(audio.duration);

    if (audio.duration > 0) {
        document.getElementById("progressFill").style.width =
            (audio.currentTime / audio.duration * 100) + "%";
    }
});

// =========================================================
// FULLSCREEN
// =========================================================

function fullscreen() {
    const el = document.getElementById("screen");

    if (!document.fullscreenElement) {
        if (el.requestFullscreen) {
            el.requestFullscreen();
        }
    } else {
        document.exitFullscreen();
    }
}

// =========================================================
// CANVAS VISUALIZER
// =========================================================

const orbitCanvas = document.getElementById("orbitCanvas");
const orbitCtx = orbitCanvas.getContext("2d");

const waveCanvas = document.getElementById("waveCanvas");
const waveCtx = waveCanvas.getContext("2d");

function fitCanvas(canvas) {
    const rect = canvas.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    canvas.width = Math.max(1, rect.width * dpr);
    canvas.height = Math.max(1, rect.height * dpr);

    const context = canvas.getContext("2d");
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function resizeAll() {
    fitCanvas(orbitCanvas);
    fitCanvas(waveCanvas);
    resizeBackground();
}

window.addEventListener("resize", resizeAll);

let tick = 0;
let bass = 0;
let mid = 0;
let treble = 0;

function average(arr, start, end) {
    let sum = 0;
    let count = 0;

    for (let i = start; i < end; i++) {
        sum += arr[i];
        count++;
    }

    return count ? sum / count : 0;
}

function animate() {
    requestAnimationFrame(animate);

    tick += 0.015;

    if (analyser && isPlaying) {
        analyser.getByteFrequencyData(freq);
        analyser.getByteTimeDomainData(timeData);

        const n = freq.length;

        bass = average(freq, 0, Math.floor(n * 0.15));
        mid = average(freq, Math.floor(n * 0.15), Math.floor(n * 0.55));
        treble = average(freq, Math.floor(n * 0.55), n);

    } else {
        bass = 8 + Math.random() * 10;
        mid = 5 + Math.random() * 8;
        treble = 4 + Math.random() * 8;
    }

    document.getElementById("bassValue").textContent =
        Math.round(bass).toString().padStart(3, "0");

    document.getElementById("trebleValue").textContent =
        Math.round(treble).toString().padStart(3, "0");

    updateBars();
    drawOrbit();
    drawWave();
}

// =========================================================
// SPECTRUM BARS
// =========================================================

function updateBars() {
    const bars = spectrum.children;

    for (let i = 0; i < bars.length; i++) {
        let value;

        if (analyser && isPlaying) {
            const idx = Math.floor(i / bars.length * freq.length);
            value = Math.max(3, freq[idx] / 255 * 100);
        } else {
            value = 4 + Math.random() * 20;
        }

        bars[i].style.height = value + "%";

        const hue = (i / bars.length * 360 + tick * 25) % 360;

        bars[i].style.background = `hsl(${hue},100%,65%)`;
        bars[i].style.boxShadow = `0 0 10px hsl(${hue},100%,60%)`;
    }

    const topBars = miniTop.children;

    for (let i = 0; i < topBars.length; i++) {
        let value;

        if (analyser && isPlaying) {
            const idx = Math.floor(i / topBars.length * freq.length);
            value = Math.max(3, freq[idx] / 255 * 100);
        } else {
            value = 5 + Math.random() * 15;
        }

        topBars[i].style.height = value + "%";
    }

    const bm = bassMeter.children;
    const tm = trebleMeter.children;

    for (let i = 0; i < bm.length; i++) {
        let b, t;

        if (analyser && isPlaying) {
            b = freq[i] / 255 * 100;
            t = freq[freq.length - 1 - i] / 255 * 100;
        } else {
            b = Math.random() * 70;
            t = Math.random() * 70;
        }

        bm[i].style.height = Math.max(4, b) + "%";
        tm[i].style.height = Math.max(4, t) + "%";
    }
}

// =========================================================
// CIRCULAR AUDIO ORBIT
// =========================================================

function drawOrbit() {
    const rect = orbitCanvas.getBoundingClientRect();
    const w = rect.width;
    const h = rect.height;

    orbitCtx.clearRect(0, 0, w, h);
    orbitCtx.save();
    orbitCtx.translate(w / 2, h / 2);

    const base = Math.min(w, h) * 0.36;

    for (let layer = 0; layer < 5; layer++) {
        orbitCtx.beginPath();

        const points = 260;

        for (let i = 0; i <= points; i++) {
            const angle = i / points * Math.PI * 2;

            let data = 0;

            if (analyser && isPlaying) {
                const idx = Math.floor(i / points * freq.length);
                data = freq[idx] / 255;
            } else {
                data = Math.sin(angle * 12 + tick + layer) * 0.1;
            }

            const radius =
                base +
                layer * 10 +
                data * (25 + bass * 0.15);

            const rotation = tick * (layer % 2 ? 1 : -1);

            const x = Math.cos(angle + rotation) * radius;
            const y = Math.sin(angle + rotation) * radius;

            if (i === 0) orbitCtx.moveTo(x, y);
            else orbitCtx.lineTo(x, y);
        }

        orbitCtx.closePath();

        const colors = [
            COLORS.c1,
            COLORS.c2,
            COLORS.c3,
            COLORS.c4,
            COLORS.c5
        ];

        orbitCtx.strokeStyle = colors[layer];
        orbitCtx.lineWidth = layer === 0 ? 2 : 1;
        orbitCtx.globalAlpha = 0.65 - layer * 0.08;
        orbitCtx.shadowBlur = 15;
        orbitCtx.shadowColor = colors[layer];
        orbitCtx.stroke();
    }

    for (let i = 0; i < 28; i++) {
        const angle =
            tick * (i % 2 ? 1 : -1) +
            i * Math.PI * 2 / 28;

        const radius = base + 25 + Math.sin(tick * 3 + i) * 12;

        orbitCtx.beginPath();

        orbitCtx.arc(
            Math.cos(angle) * radius,
            Math.sin(angle) * radius,
            2 + bass / 55,
            0,
            Math.PI * 2
        );

        orbitCtx.fillStyle =
            i % 3 === 0 ? COLORS.c4 :
            i % 3 === 1 ? COLORS.c1 : COLORS.c5;

        orbitCtx.shadowBlur = 20;
        orbitCtx.shadowColor = orbitCtx.fillStyle;
        orbitCtx.fill();
    }

    const sweepAngle = tick * 0.8;

    orbitCtx.beginPath();
    orbitCtx.moveTo(0, 0);
    orbitCtx.arc(0, 0, base * 1.55, sweepAngle, sweepAngle + 0.35);
    orbitCtx.closePath();

    orbitCtx.fillStyle = COLORS.c1;
    orbitCtx.globalAlpha = 0.06;
    orbitCtx.fill();

    orbitCtx.restore();
}

// =========================================================
// SOUND WAVE
// =========================================================

function drawWave() {
    const rect = waveCanvas.getBoundingClientRect();
    const w = rect.width;
    const h = rect.height;

    waveCtx.clearRect(0, 0, w, h);

    const colors = [COLORS.c1, COLORS.c2, COLORS.c3, COLORS.c4];

    for (let layer = 0; layer < 4; layer++) {
        waveCtx.beginPath();

        for (let x = 0; x < w; x++) {
            let v;

            if (analyser && isPlaying) {
                const idx = Math.floor(x / w * timeData.length);
                v = (timeData[idx] - 128) / 128;
            } else {
                v = Math.sin(x * 0.03 + tick + layer) * 0.2;
            }

            const y =
                h / 2 +
                v * h * 0.35 +
                Math.sin(x * 0.015 + tick + layer) * (layer + 1) * 3;

            if (x === 0) waveCtx.moveTo(x, y);
            else waveCtx.lineTo(x, y);
        }

        waveCtx.strokeStyle = colors[layer];
        waveCtx.globalAlpha = 0.75 - layer * 0.12;
        waveCtx.lineWidth = layer === 0 ? 2 : 1;
        waveCtx.shadowBlur = 15;
        waveCtx.shadowColor = colors[layer];
        waveCtx.stroke();
    }
}

// =========================================================
// PARTICLE BACKGROUND
// =========================================================

const particleCanvas = document.getElementById("particleCanvas");
const pctx = particleCanvas.getContext("2d");

let particles = [];

function resizeBackground() {
    const w = window.innerWidth;
    const h = window.innerHeight;

    particleCanvas.width = w;
    particleCanvas.height = h;

    const starCanvas = document.getElementById("starCanvas");
    starCanvas.width = w;
    starCanvas.height = h;

    const gridCanvas = document.getElementById("gridCanvas");
    gridCanvas.width = w;
    gridCanvas.height = h;

    particles = [];

    for (let i = 0; i < 150; i++) {
        particles.push({
            x: Math.random() * w,
            y: Math.random() * h,
            r: Math.random() * 2.5 + 0.5,
            dx: (Math.random() - 0.5) * 0.5,
            dy: (Math.random() - 0.5) * 0.5,
            hue: Math.random() * 360,
            alpha: Math.random()
        });
    }

    drawGrid();
}

function drawGrid() {
    const canvas = document.getElementById("gridCanvas");
    const g = canvas.getContext("2d");

    const w = canvas.width;
    const h = canvas.height;

    g.clearRect(0, 0, w, h);
    g.strokeStyle = COLORS.c1;
    g.lineWidth = 0.5;

    const gap = 35;

    for (let x = 0; x < w; x += gap) {
        g.beginPath();
        g.moveTo(x, 0);
        g.lineTo(x, h);
        g.stroke();
    }

    for (let y = 0; y < h; y += gap) {
        g.beginPath();
        g.moveTo(0, y);
        g.lineTo(w, y);
        g.stroke();
    }
}

function drawParticles() {
    requestAnimationFrame(drawParticles);

    pctx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);

    const starCanvas = document.getElementById("starCanvas");
    const sctx = starCanvas.getContext("2d");

    sctx.clearRect(0, 0, starCanvas.width, starCanvas.height);

    for (const p of particles) {
        p.x += p.dx * (1 + bass / 30);
        p.y += p.dy * (1 + bass / 30);

        if (p.x < 0) p.x = particleCanvas.width;
        if (p.x > particleCanvas.width) p.x = 0;
        if (p.y < 0) p.y = particleCanvas.height;
        if (p.y > particleCanvas.height) p.y = 0;

        p.alpha += (Math.random() - 0.5) * 0.05;
        p.alpha = Math.max(0.15, Math.min(1, p.alpha));

        const color = `hsla(${p.hue},100%,65%,${p.alpha})`;

        pctx.beginPath();
        pctx.arc(p.x, p.y, p.r + bass / 90, 0, Math.PI * 2);
        pctx.fillStyle = color;
        pctx.shadowBlur = 18;
        pctx.shadowColor = color;
        pctx.fill();

        sctx.beginPath();
        sctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        sctx.fillStyle = color;
        sctx.fill();
    }
}

// =========================================================
// START ENGINE
// =========================================================

resizeAll();
drawParticles();
animate();

if (MUSIC.length > 0) {
    document.getElementById("message").textContent =
        MUSIC.length + " MUSIC FILES FOUND";

    document.getElementById("systemStatus").textContent =
        "MUSIC LIBRARY READY";

    loadTrack(0, false);

} else {
    document.getElementById("message").textContent =
        "NO MUSIC / ADD MP3 BESIDE Ta_app.py";

    document.getElementById("systemStatus").textContent =
        "WAITING FOR MUSIC";
}

</script>
</body>
</html>
"""

# =========================================================
# INJECT DATA
# =========================================================

html = html.replace("__MUSIC__", music_json)
html = html.replace("__LOGO__", logo_b64)

# =========================================================
# RENDER
# =========================================================

components.html(
    html,
    height=850,
    scrolling=False
)
