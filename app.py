import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

# =========================================================
# SYNAPSE NEON MUSIC STUDIO
# =========================================================

APP_DIR = Path(__file__).resolve().parent
LOGO_PATH = APP_DIR / "logo1.jpg"

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
[data-testid="stToolbar"] {
    display: none !important;
}

html, body, [data-testid="stAppViewContainer"] {
    margin: 0 !important;
    padding: 0 !important;
    background: #03030a !important;
}

.block-container {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stMainBlockContainer"] {
    padding: 0 !important;
}

.stApp {
    background: #03030a !important;
    overflow-x: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGO
# =========================================================

logo_b64 = ""

if LOGO_PATH.exists():
    logo_b64 = base64.b64encode(
        LOGO_PATH.read_bytes()
    ).decode()

# =========================================================
# MUSIC UPLOAD
# =========================================================

st.markdown("""
<style>
.upload-area {
    color: #00eaff;
}
</style>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "เพิ่มไฟล์เพลง",
    type=["mp3", "wav", "ogg", "m4a", "aac"],
    accept_multiple_files=True,
    key="music_upload"
)

# =========================================================
# THEME SELECT
# =========================================================

themes = {
    "CYBER BLUE": "#00eaff",
    "NEON PURPLE": "#bf00ff",
    "GOLD POWER": "#ffd700",
    "CHROME RED": "#ff1744",
    "SILVER PULSE": "#e8f7ff"
}

theme_name = st.selectbox(
    "NEON COLOR",
    list(themes.keys()),
    index=0
)

accent = themes[theme_name]

# =========================================================
# MUSIC FILE DATA
# =========================================================

tracks = []

if uploaded_files:
    for file in uploaded_files:
        audio_data = base64.b64encode(
            file.getvalue()
        ).decode()

        tracks.append({
            "name": file.name,
            "data": audio_data,
            "type": file.type or "audio/mpeg"
        })

# =========================================================
# PLAYER HTML
# =========================================================

music_json = __import__("json").dumps(tracks)

player_html = r"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    width: 100%;
    height: 100%;
    background: #03030a;
    overflow: hidden;
    font-family: Arial, Helvetica, sans-serif;
}

body {
    color: #ffffff;
}

#main {
    position: relative;
    width: 100%;
    height: 100vh;
    min-height: 720px;
    overflow: hidden;
    background:
        radial-gradient(circle at 50% 45%,
        #10162c 0%,
        #090a17 30%,
        #03030a 75%);
}

#stars {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
}

.scanline {
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: 0.08;
    background: repeating-linear-gradient(
        to bottom,
        transparent 0px,
        transparent 3px,
        #ffffff 4px
    );
}

.header {
    position: absolute;
    top: 25px;
    left: 4%;
    right: 4%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 5;
}

.brand {
    font-size: 24px;
    font-weight: 900;
    letter-spacing: 5px;
    color: var(--accent);
    text-shadow: 0 0 20px var(--accent);
}

.subbrand {
    font-size: 9px;
    letter-spacing: 4px;
    color: #7c8ba8;
    margin-top: 6px;
}

.status {
    font-size: 10px;
    color: var(--accent);
    letter-spacing: 3px;
}

.status::before {
    content: "● ";
    animation: blink 1s infinite;
}

@keyframes blink {
    50% { opacity: 0.15; }
}

.side {
    position: absolute;
    top: 22%;
    width: 19%;
    z-index: 3;
}

.left {
    left: 3%;
}

.right {
    right: 3%;
    text-align: right;
}

.label {
    color: var(--accent);
    letter-spacing: 4px;
    font-size: 11px;
    margin-bottom: 15px;
}

.meter {
    display: flex;
    gap: 5px;
    height: 150px;
    align-items: flex-end;
}

.left .meter {
    justify-content: flex-start;
}

.right .meter {
    justify-content: flex-end;
}

.meter span {
    display: block;
    width: 9px;
    height: 20%;
    border: 1px solid var(--accent);
    background: var(--accent);
    box-shadow: 0 0 12px var(--accent);
    opacity: 0.8;
    border-radius: 2px 2px 0 0;
}

.readout {
    margin-top: 20px;
    color: #a6b6cc;
    font-size: 10px;
    letter-spacing: 2px;
    line-height: 2;
}

.readout b {
    color: var(--accent);
    font-size: 17px;
}

.core {
    position: absolute;
    width: 430px;
    height: 430px;
    left: 50%;
    top: 43%;
    transform: translate(-50%, -50%);
}

.ring {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 1px solid var(--accent);
    box-shadow:
        0 0 15px var(--accent),
        inset 0 0 15px var(--accent);
    opacity: 0.35;
}

.r1 {
    inset: 0;
    border-style: dashed;
    animation: rotate 24s linear infinite;
}

.r2 {
    inset: 20px;
    border-width: 2px;
    animation: rotateback 16s linear infinite;
}

.r3 {
    inset: 38px;
    border-style: dotted;
    animation: rotate 9s linear infinite;
}

.r4 {
    inset: 58px;
    border-color: #ffffff;
    opacity: 0.25;
    animation: rotateback 30s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes rotateback {
    from { transform: rotate(360deg); }
    to { transform: rotate(0deg); }
}

.logo-box {
    position: absolute;
    width: 190px;
    height: 190px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    overflow: hidden;
    background: #05060c;
    border: 2px solid var(--accent);
    box-shadow:
        0 0 30px var(--accent),
        0 0 80px var(--accent),
        inset 0 0 30px var(--accent);
}

.logo-box img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    animation: breathe 3s ease-in-out infinite;
}

.logo-placeholder {
    font-size: 32px;
    font-weight: 900;
    color: var(--accent);
    text-shadow: 0 0 25px var(--accent);
}

@keyframes breathe {
    0%, 100% { transform: scale(0.95); }
    50% { transform: scale(1.04); }
}

#circle {
    position: absolute;
    inset: -20px;
    width: calc(100% + 40px);
    height: calc(100% + 40px);
}

.bottom-spectrum {
    position: absolute;
    left: 4%;
    right: 4%;
    bottom: 220px;
    height: 130px;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 4px;
    z-index: 3;
}

.bottom-spectrum span {
    flex: 1;
    max-width: 12px;
    min-width: 2px;
    height: 5%;
    background: var(--accent);
    box-shadow: 0 0 10px var(--accent);
    border-radius: 3px 3px 0 0;
}

.track-panel {
    position: absolute;
    bottom: 110px;
    width: 100%;
    text-align: center;
    z-index: 4;
}

.track-name {
    font-size: 22px;
    letter-spacing: 3px;
    color: #fff;
    text-shadow: 0 0 20px var(--accent);
    padding: 10px;
}

.track-sub {
    color: var(--accent);
    font-size: 10px;
    letter-spacing: 5px;
}

.controls {
    position: absolute;
    bottom: 30px;
    width: 100%;
    text-align: center;
    z-index: 5;
}

.buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15px;
}

button {
    color: var(--accent);
    background: #090d18;
    border: 1px solid var(--accent);
    padding: 12px 18px;
    border-radius: 6px;
    font-size: 11px;
    letter-spacing: 2px;
    cursor: pointer;
    box-shadow: 0 0 10px #000;
}

button:hover {
    background: var(--accent);
    color: #000;
    box-shadow: 0 0 20px var(--accent);
}

#play {
    font-size: 15px;
    padding: 14px 25px;
}

.progress {
    width: 70%;
    margin: 20px auto 0;
    height: 4px;
    background: #202637;
    border-radius: 5px;
    overflow: hidden;
}

#progressFill {
    width: 0%;
    height: 100%;
    background: var(--accent);
    box-shadow: 0 0 15px var(--accent);
}

.time {
    margin-top: 8px;
    color: #8a9ab4;
    font-size: 10px;
    letter-spacing: 2px;
}

#message {
    color: #ffcf40;
    font-size: 11px;
    margin-top: 12px;
}

@media (max-width: 700px) {
    .core {
        width: 270px;
        height: 270px;
        top: 38%;
    }

    .logo-box {
        width: 130px;
        height: 130px;
    }

    .side {
        top: 14%;
        width: 25%;
    }

    .meter {
        height: 75px;
    }

    .bottom-spectrum {
        bottom: 200px;
        height: 90px;
    }

    .track-panel {
        bottom: 105px;
    }

    .track-name {
        font-size: 14px;
    }

    .buttons {
        gap: 5px;
    }

    button {
        padding: 10px;
        font-size: 9px;
    }

    .progress {
        width: 90%;
    }
}

</style>
</head>

<body>

<div id="main">

<canvas id="stars"></canvas>

<div class="scanline"></div>

<div class="header">
    <div>
        <div class="brand">SYNAPSE</div>
        <div class="subbrand">NEON MUSIC STUDIO / AUDIO SYSTEM</div>
    </div>
    <div class="status" id="status">SYSTEM READY</div>
</div>

<div class="side left">
    <div class="label">LOW FREQUENCY</div>
    <div class="meter" id="bassMeter"></div>
    <div class="readout">
        BASS ENERGY<br>
        <b id="bassValue">000</b>
    </div>
    <div class="readout">
        AUDIO INPUT<br>
        <span id="inputName">STANDBY</span>
    </div>
</div>

<div class="side right">
    <div class="label">HIGH FREQUENCY</div>
    <div class="meter" id="trebleMeter"></div>
    <div class="readout">
        TREBLE ENERGY<br>
        <b id="trebleValue">000</b>
    </div>
    <div class="readout">
        STEREO CHANNEL<br>
        <span>L / R ACTIVE</span>
    </div>
</div>

<div class="core">

    <div class="ring r1"></div>
    <div class="ring r2"></div>
    <div class="ring r3"></div>
    <div class="ring r4"></div>

    <canvas id="circle"></canvas>

    <div class="logo-box" id="logoBox">
        LOGO
    </div>

</div>

<div class="bottom-spectrum" id="spectrum"></div>

<div class="track-panel">
    <div class="track-sub">NOW PLAYING</div>
    <div class="track-name" id="trackName">SYNAPSE NEON MUSIC</div>
</div>

<div class="controls">

    <div class="buttons">
        <button onclick="previousTrack()">◀◀</button>
        <button onclick="togglePlay()" id="play">▶ PLAY</button>
        <button onclick="stopTrack()">■ STOP</button>
        <button onclick="nextTrack()">▶▶</button>
        <button onclick="toggleShuffle()" id="shuffle">SHUFFLE OFF</button>
    </div>

    <div class="progress">
        <div id="progressFill"></div>
    </div>

    <div class="time">
        <span id="currentTime">00:00</span>
        /
        <span id="duration">00:00</span>
    </div>

    <div id="message">
        SELECT MUSIC FROM STREAMLIT
    </div>

</div>

</div>

<script>

const MUSIC = __MUSIC_DATA__;
const ACCENT = "__ACCENT__";
const LOGO = "__LOGO__";

document.documentElement.style.setProperty("--accent", ACCENT);

const logoBox = document.getElementById("logoBox");

if (LOGO && LOGO.length > 20) {
    logoBox.innerHTML = `<img src="data:image/jpeg;base64,${LOGO}">`;
} else {
    logoBox.innerHTML = `<div class="logo-placeholder">SYNAPSE</div>`;
}

// ==================================================
// BUILD METERS
// ==================================================

const spectrum = document.getElementById("spectrum");
const bassMeter = document.getElementById("bassMeter");
const trebleMeter = document.getElementById("trebleMeter");

for (let i = 0; i < 64; i++) {
    const bar = document.createElement("span");
    spectrum.appendChild(bar);
}

for (let i = 0; i < 18; i++) {
    const b = document.createElement("span");
    bassMeter.appendChild(b);

    const t = document.createElement("span");
    trebleMeter.appendChild(t);
}

// ==================================================
// AUDIO
// ==================================================

let audio = new Audio();
audio.crossOrigin = "anonymous";

let audioContext = null;
let analyser = null;
let source = null;
let frequencyData = null;
let shuffle = false;
let currentIndex = 0;
let playing = false;

function initAudio() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();

        analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;
        analyser.smoothingTimeConstant = 0.82;

        source = audioContext.createMediaElementSource(audio);
        source.connect(analyser);
        analyser.connect(audioContext.destination);

        frequencyData = new Uint8Array(analyser.frequencyBinCount);
    }

    if (audioContext.state === "suspended") {
        audioContext.resume();
    }
}

function fmtTime(sec) {
    if (!isFinite(sec)) return "00:00";

    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);

    return String(m).padStart(2, "0") + ":" +
           String(s).padStart(2, "0");
}

function loadTrack(index, autoplay = true) {
    if (!MUSIC.length) {
        document.getElementById("message").textContent =
            "PLEASE UPLOAD MUSIC IN STREAMLIT";
        return;
    }

    currentIndex = (index + MUSIC.length) % MUSIC.length;

    const track = MUSIC[currentIndex];

    audio.src = `data:${track.type};base64,${track.data}`;
    audio.load();

    document.getElementById("trackName").textContent = track.name;
    document.getElementById("inputName").textContent = "ACTIVE";

    if (autoplay) {
        initAudio();

        audio.play().then(() => {
            playing = true;
            document.getElementById("play").textContent = "❚❚ PAUSE";
            document.getElementById("status").textContent = "AUDIO PLAYING";
        }).catch(() => {
            document.getElementById("message").textContent =
                "PRESS PLAY TO START AUDIO";
        });
    }
}

function togglePlay() {
    if (!MUSIC.length) {
        document.getElementById("message").textContent =
            "UPLOAD SONGS FIRST";
        return;
    }

    initAudio();

    if (audio.paused) {
        if (!audio.src) {
            loadTrack(currentIndex, false);
        }

        audio.play().then(() => {
            playing = true;
            document.getElementById("play").textContent = "❚❚ PAUSE";
            document.getElementById("status").textContent = "AUDIO PLAYING";
        }).catch(() => {});
    } else {
        audio.pause();
        playing = false;
        document.getElementById("play").textContent = "▶ PLAY";
        document.getElementById("status").textContent = "AUDIO PAUSED";
    }
}

function stopTrack() {
    audio.pause();
    audio.currentTime = 0;
    playing = false;

    document.getElementById("play").textContent = "▶ PLAY";
    document.getElementById("status").textContent = "SYSTEM READY";
}

function nextTrack() {
    if (!MUSIC.length) return;

    if (shuffle && MUSIC.length > 1) {
        let next;

        do {
            next = Math.floor(Math.random() * MUSIC.length);
        } while (next === currentIndex);

        loadTrack(next);
    } else {
        loadTrack(currentIndex + 1);
    }
}

function previousTrack() {
    if (!MUSIC.length) return;

    loadTrack(currentIndex - 1);
}

function toggleShuffle() {
    shuffle = !shuffle;

    document.getElementById("shuffle").textContent =
        shuffle ? "SHUFFLE ON" : "SHUFFLE OFF";
}

audio.addEventListener("ended", () => {
    nextTrack();
});

audio.addEventListener("timeupdate", () => {
    document.getElementById("currentTime").textContent =
        fmtTime(audio.currentTime);

    document.getElementById("duration").textContent =
        fmtTime(audio.duration);

    if (audio.duration) {
        document.getElementById("progressFill").style.width =
            (audio.currentTime / audio.duration * 100) + "%";
    }
});

// ==================================================
// VISUALIZER
// ==================================================

const canvas = document.getElementById("circle");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;

    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();

let pulse = 0;

function animateVisualizer() {
    requestAnimationFrame(animateVisualizer);

    const w = canvas.clientWidth;
    const h = canvas.clientHeight;

    ctx.clearRect(0, 0, w, h);

    let bass = 0;
    let mid = 0;
    let treble = 0;

    if (analyser && playing) {
        analyser.getByteFrequencyData(frequencyData);

        const third = Math.floor(frequencyData.length / 3);

        bass = frequencyData.slice(0, third)
            .reduce((a, b) => a + b, 0) / third;

        mid = frequencyData.slice(third, third * 2)
            .reduce((a, b) => a + b, 0) / third;

        treble = frequencyData.slice(third * 2)
            .reduce((a, b) => a + b, 0) /
            (frequencyData.length - third * 2);
    }

    pulse += 0.025 + bass / 6000;

    document.getElementById("bassValue").textContent =
        Math.round(bass).toString().padStart(3, "0");

    document.getElementById("trebleValue").textContent =
        Math.round(treble).toString().padStart(3, "0");

    const bars = spectrum.children;

    for (let i = 0; i < bars.length; i++) {
        let value = 5;

        if (analyser && playing) {
            const index = Math.floor(i / bars.length * frequencyData.length);
            value = Math.max(3, frequencyData[index] / 255 * 100);
        } else {
            value = 5 + Math.abs(Math.sin(pulse + i * 0.3)) * 8;
        }

        bars[i].style.height = value + "%";
    }

    const bm = bassMeter.children;
    const tm = trebleMeter.children;

    for (let i = 0; i < bm.length; i++) {
        let bv, tv;

        if (analyser && playing) {
            bv = frequencyData[i] / 255 * 100;
            tv = frequencyData[frequencyData.length - 1 - i] / 255 * 100;
        } else {
            bv = 10 + Math.random() * 20;
            tv = 10 + Math.random() * 20;
        }

        bm[i].style.height = Math.max(5, bv) + "%";
        tm[i].style.height = Math.max(5, tv) + "%";
    }

    // CIRCULAR FREQUENCY WAVE

    const cx = w / 2;
    const cy = h / 2;
    const baseRadius = Math.min(w, h) * 0.39;

    ctx.save();
    ctx.translate(cx, cy);

    for (let layer = 0; layer < 3; layer++) {
        ctx.beginPath();

        const points = 240;

        for (let i = 0; i <= points; i++) {
            const angle = i / points * Math.PI * 2;

            let data = 0;

            if (analyser && playing) {
                const index = Math.floor(i / points * frequencyData.length);
                data = frequencyData[index] / 255;
            } else {
                data = Math.sin(angle * 8 + pulse) * 0.08;
            }

            const radius =
                baseRadius +
                layer * 8 +
                data * (25 + bass * 0.15);

            const x = Math.cos(angle) * radius;
                        const y = Math.sin(angle) * radius;

            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }

        ctx.closePath();

        ctx.strokeStyle = layer === 0 ? ACCENT :
                         layer === 1 ? "#ffffff" : "#a000ff";

        ctx.lineWidth = layer === 0 ? 2 : 1;
        ctx.globalAlpha = 0.7 - layer * 0.15;

        ctx.shadowBlur = 18;
        ctx.shadowColor = ACCENT;

        ctx.stroke();
    }

    // ENERGY ORBIT DOTS

    for (let i = 0; i < 16; i++) {
        const angle = pulse * (i % 2 ? 1 : -1) + i * Math.PI / 8;
        const radius = baseRadius + 30 + Math.sin(pulse * 2 + i) * 8;

        ctx.beginPath();
        ctx.arc(
            Math.cos(angle) * radius,
            Math.sin(angle) * radius,
            2 + bass / 100,
            0,
            Math.PI * 2
        );

        ctx.fillStyle = ACCENT;
        ctx.shadowBlur = 15;
        ctx.shadowColor = ACCENT;
        ctx.fill();
    }

    ctx.restore();
}

animateVisualizer();

// ==================================================
// BACKGROUND STARS
// ==================================================

const starCanvas = document.getElementById("stars");
const starCtx = starCanvas.getContext("2d");

let starList = [];

function resizeStars() {
    starCanvas.width = window.innerWidth;
    starCanvas.height = window.innerHeight;

    starList = [];

    for (let i = 0; i < 160; i++) {
        starList.push({
            x: Math.random() * starCanvas.width,
            y: Math.random() * starCanvas.height,
            size: Math.random() * 2,
            alpha: Math.random(),
            speed: Math.random() * 0.5
        });
    }
}

resizeStars();
window.addEventListener("resize", resizeStars);

function drawStars() {
    requestAnimationFrame(drawStars);

    starCtx.clearRect(
        0, 0, starCanvas.width, starCanvas.height
    );

    for (const s of starList) {
        s.alpha += (Math.random() - 0.5) * 0.04;
        s.alpha = Math.max(0.1, Math.min(1, s.alpha));
        s.y -= s.speed;

        if (s.y < 0) {
            s.y = starCanvas.height;
            s.x = Math.random() * starCanvas.width;
        }

        starCtx.beginPath();
        starCtx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
        starCtx.fillStyle = `rgba(150,210,255,${s.alpha})`;
        starCtx.fill();
    }
}

drawStars();

// ==================================================
// START
// ==================================================

if (MUSIC.length > 0) {
    document.getElementById("message").textContent =
        MUSIC.length + " TRACKS LOADED — PRESS PLAY";

    document.getElementById("status").textContent =
        "MUSIC READY";
} else {
    document.getElementById("message").textContent =
        "UPLOAD MUSIC TO START";
}

</script>

</body>
</html>
"""

# =========================================================
# INJECT DATA
# =========================================================

player_html = (
    player_html
    .replace("__MUSIC_DATA__", music_json)
    .replace("__ACCENT__", accent)
    .replace("__LOGO__", logo_b64)
)

# =========================================================
# RENDER
# =========================================================

components.html(
    player_html,
    height=1000,
    scrolling=False
)

# =========================================================
# FOOTER CSS
# =========================================================

st.markdown("""
<style>
div[data-testid="stFileUploader"] {
    position: relative;
    z-index: 10;
}

div[data-testid="stSelectbox"] {
    position: relative;
    z-index: 10;
}
</style>
""", unsafe_allow_html=True)
