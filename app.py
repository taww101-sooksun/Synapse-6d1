# -*- coding: utf-8 -*-
"""
SYNAPSE NEON MUSIC STUDIO
Fresh standalone Streamlit music player.
Place app.py, logo1.jpg, and your music files in the same folder.
Supported: mp3, wav, ogg, m4a, aac, flac

Run locally: streamlit run app.py
"""

from __future__ import annotations

import base64
import json
import mimetypes
import random
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ------------------------------------------------------------
# APP SETTINGS
# ------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
LOGO_PATH = APP_DIR / "logo1.jpg"
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac"}

st.set_page_config(
    page_title="SYNAPSE NEON MUSIC STUDIO",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit's own header/footer/sidebar so only the studio remains.
st.markdown(
    """
    <style>
      html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"],
      [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
        background:#02040b !important;
      }
      [data-testid="stHeader"], [data-testid="stToolbar"],
      [data-testid="stDecoration"], [data-testid="stStatusWidget"],
      [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
      footer, #MainMenu { display:none !important; }
      [data-testid="stMainBlockContainer"] {
        padding:0 !important; margin:0 auto !important; max-width:100% !important;
      }
      .block-container { padding:0 !important; max-width:100% !important; }
      iframe { border:0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# LOAD LOCAL MUSIC AND LOGO
# ------------------------------------------------------------
music_files = sorted(
    [p for p in APP_DIR.iterdir()
     if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS],
    key=lambda p: p.name.casefold(),
)

def encode_file(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"

tracks = []
for path in music_files:
    try:
        tracks.append({"name": path.stem, "src": encode_file(path)})
    except OSError:
        pass

logo_data = ""
if LOGO_PATH.exists():
    try:
        logo_data = encode_file(LOGO_PATH)
    except OSError:
        logo_data = ""

tracks_json = json.dumps(tracks, ensure_ascii=False).replace("</", "<\\/")
logo_json = json.dumps(logo_data)

# ------------------------------------------------------------
# PLAYER PAGE (HTML/CSS/JS runs inside its own interactive iframe)
# ------------------------------------------------------------
HTML = r"""
<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
:root{--cyan:#00eaff;--blue:#168bff;--pink:#ff24d6;--purple:#a52cff;--gold:#ffe34d;--green:#28ff91}
*{box-sizing:border-box}
html,body{margin:0;width:100%;min-height:100%;background:#02040b;color:#eafaff;font-family:Arial,"Noto Sans Thai",sans-serif;overflow-x:hidden}
body{
 background:
  radial-gradient(ellipse at 50% 52%,rgba(0,94,150,.20),transparent 38%),
  radial-gradient(ellipse at 50% 100%,rgba(77,0,120,.13),transparent 50%),
  repeating-linear-gradient(0deg,rgba(45,175,220,.055) 0px,rgba(45,175,220,.055) 1px,transparent 1px,transparent 28px),
  repeating-linear-gradient(90deg,rgba(45,175,220,.045) 0px,rgba(45,175,220,.045) 1px,transparent 1px,transparent 68px),
  #02040b;
}
#stars{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:0}
.shell{position:relative;z-index:1;width:100%;max-width:850px;min-height:850px;margin:auto;padding:15px 18px 18px;display:flex;flex-direction:column;gap:10px}
.top{display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:100px}
.brand{font-size:clamp(30px,7vw,54px);font-weight:900;letter-spacing:.20em;color:#a6f5ff;text-shadow:0 0 8px #00dfff,0 0 23px #007bff,0 0 42px #00bfff;line-height:1.1}
.subtitle{font-size:clamp(9px,2vw,14px);letter-spacing:.42em;color:#aabbd8;margin-top:8px}
.righttop{display:flex;flex-direction:column;align-items:flex-end;gap:8px}
.songsTop{border:2px solid var(--cyan);border-radius:15px;padding:12px 20px;background:rgba(3,18,36,.75);color:var(--cyan);font-size:18px;box-shadow:0 0 16px #008bff55;cursor:pointer}
.state{font-size:12px;letter-spacing:.2em;color:#f7e88a}
.state span{color:#43ffb1}
#spectrum{width:100%;height:70px;display:block;flex-shrink:0}
.palette{display:flex;justify-content:center;gap:12px;border:2px solid #33495e;border-radius:40px;padding:9px 15px;width:max-content;max-width:100%;margin:0 auto}
.palette button{width:40px;height:40px;border-radius:50%;border:2px solid #657386;background:#101b31;box-shadow:inset 0 0 8px #fff3,0 0 10px #00bfff22;cursor:pointer;font-size:22px}
.palette button:nth-child(1){color:#ff5aee}.palette button:nth-child(2){color:#168cff}.palette button:nth-child(3){color:#d64cff}.palette button:nth-child(4){color:#ffd52e}.palette button:nth-child(5){color:#8de34b}
.visual{position:relative;width:100%;height:min(100vw,620px);min-height:390px;max-height:620px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
#rings{position:absolute;width:100%;height:100%;inset:0}
.logo{position:relative;width:min(34vw,230px);height:min(34vw,230px);min-width:145px;min-height:145px;max-width:230px;max-height:230px;border-radius:50%;overflow:hidden;border:4px solid #b7faff;background:#030a18;box-shadow:0 0 12px #00eaff,0 0 28px #008cff,0 0 55px #a52cff,inset 0 0 22px #00aaff;display:flex;align-items:center;justify-content:center}
.logo img{width:100%;height:100%;object-fit:contain}
.fallback{font-size:23px;font-weight:900;color:#9af8ff;text-align:center;text-shadow:0 0 12px #00eaff}
.metric{position:absolute;top:50%;transform:translateY(-50%);width:23%;max-width:160px;text-align:left;color:#a9c9e8}
.metric.left{left:0}.metric.right{right:0;text-align:right}
.metricTitle{font-size:clamp(9px,2vw,14px);letter-spacing:.16em}
.metricValue{font-size:clamp(28px,6vw,42px);font-weight:800;color:#fff;text-shadow:0 0 12px #00dfff;margin:5px 0}
.metric.right .metricValue{color:#fff;text-shadow:0 0 12px #ff22d6}
.metricSub{font-size:10px;letter-spacing:.16em;color:#9fb5d1}
.meter{height:5px;background:#14243a;border-radius:5px;overflow:hidden;margin-top:8px}
.meter i{display:block;width:0%;height:100%;background:linear-gradient(90deg,#00eaff,#a52cff,#ff24d6);box-shadow:0 0 10px #00eaff}
.trackline{text-align:center;min-height:50px;padding:5px 0}
.trackname{font-size:clamp(17px,4vw,25px);font-weight:700;color:#fff;text-shadow:0 0 12px #00bfff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.trackcaption{font-size:11px;letter-spacing:.30em;color:#a7bad6;margin-top:5px}
.controls{display:flex;align-items:center;justify-content:center;gap:clamp(8px,2.5vw,22px);padding:6px 0}
.control{width:clamp(48px,10vw,70px);height:clamp(48px,10vw,70px);border-radius:50%;border:2px solid #00dfff;background:rgba(3,14,32,.88);color:#eaffff;font-size:clamp(17px,4vw,25px);box-shadow:0 0 14px #008bff77,inset 0 0 12px #008bff22;cursor:pointer;touch-action:manipulation}
.control.main{width:clamp(66px,14vw,92px);height:clamp(66px,14vw,92px);font-size:31px;border:3px solid #fff;background:linear-gradient(135deg,#00aaff,#8b00ff,#ff00a8);box-shadow:0 0 22px #a000ff,0 0 35px #00cfff66}
.control.on{border-color:#ffe34d;color:#ffe34d;box-shadow:0 0 15px #ffe34d}
.seekbox{padding:0 8px}
#seek{width:100%;accent-color:#00eaff;height:20px;cursor:pointer;touch-action:pan-x}
.times{display:flex;justify-content:space-between;color:#a9bdd8;font-size:13px}
.bottom{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:3px}
.bottom button{border:1.5px solid #00dfff;border-radius:24px;background:rgba(4,13,32,.8);color:#a5f4ff;padding:11px 17px;font-size:12px;letter-spacing:.12em;box-shadow:0 0 13px #007bff66;cursor:pointer;touch-action:manipulation}
.tag{text-align:center;color:#839bbd;font-size:10px;letter-spacing:.22em;padding:5px}
#playlist{display:none;position:absolute;z-index:10;top:10px;left:5%;right:5%;max-height:80%;overflow:auto;border:1px solid #00eaff;border-radius:15px;background:rgba(2,6,20,.97);box-shadow:0 0 25px #007bff;padding:12px}
#playlist.show{display:block}
.listhead{display:flex;justify-content:space-between;align-items:center;color:#8ef8ff;font-weight:bold;margin-bottom:8px}
.listhead button{background:#18223b;color:white;border:1px solid #00dfff;border-radius:8px;padding:6px 10px}
.song{padding:12px 8px;border-bottom:1px solid #1c4360;color:#d9f5ff;cursor:pointer;touch-action:manipulation}
.song.active{color:#ff7be7;text-shadow:0 0 9px #ff24d6}
.song:active{background:#102949}
.empty{color:#ffdb83;text-align:center;padding:12px;font-size:12px}
@media(max-width:520px){
 .shell{padding:12px 12px 16px;gap:7px;min-height:100vh}
 .top{min-height:78px}.subtitle{letter-spacing:.25em}
 .songsTop{padding:10px 12px;font-size:14px}
 .state{font-size:9px}
 #spectrum{height:55px}
 .palette{gap:8px;padding:7px 10px}.palette button{width:34px;height:34px}
 .visual{height:112vw;min-height:350px;max-height:490px}
 .metric{width:22%}.metricTitle{font-size:8px;letter-spacing:.08em}.metricValue{font-size:27px}.metricSub{font-size:8px}
 .logo{width:36vw;height:36vw;min-width:130px;min-height:130px}
 .bottom button{padding:10px 12px;font-size:10px}
}
@media(max-height:760px) and (min-width:521px){
 .shell{min-height:100vh;gap:5px;padding-top:7px}.top{min-height:65px}#spectrum{height:45px}.visual{height:45vh;min-height:300px}.trackline{min-height:40px}
}
</style>
</head>
<body>
<canvas id="stars"></canvas>
<div class="shell">
 <header class="top">
  <div><div class="brand">SYNAPSE</div><div class="subtitle">NEON MUSIC STUDIO / SOUND SYSTEM</div></div>
  <div class="righttop"><button class="songsTop" id="songsTop">♫ SONGS</button><div class="state"><span>●</span> SYSTEM READY<br><span id="trackcount">●</span> LIBRARY: 0 TRACKS</div></div>
 </header>
 <canvas id="spectrum"></canvas>
 <div class="palette">
  <button title="Rainbow">🌈</button><button title="Blue">●</button><button title="Purple">●</button><button title="Gold">●</button><button title="Green">●</button>
 </div>
 <section class="visual">
  <canvas id="rings"></canvas>
  <div class="metric left"><div class="metricTitle">BASS ENERGY</div><div class="metricValue" id="bass">000</div><div class="metricSub">AUDIO INPUT</div><div class="meter"><i id="bassbar"></i></div></div>
  <div class="logo" id="logo"></div>
  <div class="metric right"><div class="metricTitle">TREBLE ENERGY</div><div class="metricValue" id="treble">000</div><div class="metricSub">STEREO CHANNEL</div><div class="meter"><i id="treblebar"></i></div></div>
  <div id="playlist"><div class="listhead"><span>♫ SONG LIBRARY</span><button id="closeList">CLOSE ✕</button></div><div id="songrows"></div></div>
 </section>
 <section class="trackline"><div class="trackname" id="trackname">ยังไม่มีเพลงในรายการ</div><div class="trackcaption">SOUND FREQUENCY / VISUAL EXPERIENCE</div></section>
 <nav class="controls">
  <button class="control" id="previous" aria-label="Previous">|◀</button>
  <button class="control" id="rewind" aria-label="Back 10 seconds">◀</button>
  <button class="control main" id="play" aria-label="Play">▶</button>
  <button class="control" id="next" aria-label="Next">▶|</button>
  <button class="control" id="shuffle" aria-label="Shuffle">🔀</button>
  <button class="control" id="repeat" aria-label="Repeat">🔁</button>
 </nav>
 <div class="seekbox"><input id="seek" type="range" min="0" max="1000" value="0"><div class="times"><span id="elapsed">00:00</span><span id="total">00:00</span></div></div>
 <div class="tag">✦ FEEL THE MUSIC • HEAL YOUR MIND • LIVE IN HARMONY ✦</div>
 <footer class="bottom"><button id="songlistBtn">♫ SONG LIST</button><button id="full">⛶ FULL SCREEN</button></footer>
</div>
<audio id="audio" preload="metadata" playsinline></audio>
<script>
"use strict";
const TRACKS = TRACKS_JSON;
const LOGO = LOGO_JSON;
const $ = id => document.getElementById(id);
const audio = $("audio");
let current = 0, shuffleMode = false, repeatMode = false;
let audioContext = null, analyser = null, sourceNode = null, freqData = null;
let lastTap = 0;

if (LOGO) {
  const img = document.createElement("img");
  img.src = LOGO; img.alt = "SYNAPSE logo"; $("logo").appendChild(img);
} else {
  $("logo").innerHTML = '<div class="fallback">SYNAPSE<br><small>SOUND & VISUAL THERAPY</small></div>';
}
$("trackcount").textContent = `● LIBRARY: ${TRACKS.length} TRACKS`;

function timeText(value) {
  if (!Number.isFinite(value) || value < 0) value = 0;
  return `${String(Math.floor(value/60)).padStart(2,"0")}:${String(Math.floor(value%60)).padStart(2,"0")}`;
}
function showTrack() {
  $("trackname").textContent = TRACKS[current]?.name || "ยังไม่มีเพลงในรายการ";
  document.querySelectorAll(".song").forEach((el,i)=>el.classList.toggle("active",i===current));
}
function buildPlaylist() {
  const box = $("songrows"); box.innerHTML = "";
  if (!TRACKS.length) { box.innerHTML='<div class="empty">ไม่พบไฟล์เพลง กรุณาวางไฟล์เพลงไว้ในโฟลเดอร์เดียวกับ app.py</div>'; return; }
  TRACKS.forEach((track,i)=>{
    const row=document.createElement("div"); row.className="song"; row.textContent=`${String(i+1).padStart(2,"0")}  ♫  ${track.name}`;
    row.addEventListener("click",()=>{loadTrack(i);startPlayback();$("playlist").classList.remove("show");});
    box.appendChild(row);
  });
  showTrack();
}
function loadTrack(index) {
  if (!TRACKS.length) return;
  current=(index+TRACKS.length)%TRACKS.length;
  audio.src=TRACKS[current].src; audio.load(); showTrack();
  $("elapsed").textContent="00:00"; $("total").textContent="00:00"; $("seek").value=0;
}
async function prepareAnalyzer() {
  if (audioContext) { if(audioContext.state==="suspended") await audioContext.resume(); return; }
  try {
    const AudioCtx=window.AudioContext||window.webkitAudioContext;
    if(!AudioCtx) return;
    audioContext=new AudioCtx();
    analyser=audioContext.createAnalyser(); analyser.fftSize=1024; analyser.smoothingTimeConstant=.82;
    sourceNode=audioContext.createMediaElementSource(audio);
    sourceNode.connect(analyser); analyser.connect(audioContext.destination);
    freqData=new Uint8Array(analyser.frequencyBinCount);
    if(audioContext.state==="suspended") await audioContext.resume();
  } catch(err) { console.warn("Analyzer unavailable:",err); }
}
async function startPlayback() {
  if(!TRACKS.length){$("trackname").textContent="ยังไม่พบไฟล์เพลง";return;}
  if(!audio.src) loadTrack(current);
  await prepareAnalyzer();
  try { await audio.play(); $("play").textContent="Ⅱ"; }
  catch(err) { $("play").textContent="▶"; $("trackname").textContent="แตะปุ่มเล่นอีกครั้งเพื่อเริ่มเพลง"; console.warn(err); }
}
$("play").addEventListener("click",async()=>{
  if(audio.paused) await startPlayback();
  else {audio.pause();$("play").textContent="▶";}
});
$("previous").addEventListener("click",()=>{loadTrack(current-1);startPlayback();});
$("next").addEventListener("click",()=>{nextTrack();});
$("rewind").addEventListener("click",()=>{audio.currentTime=Math.max(0,(audio.currentTime||0)-10);});
$("shuffle").addEventListener("click",()=>{shuffleMode=!shuffleMode;$("shuffle").classList.toggle("on",shuffleMode);});
$("repeat").addEventListener("click",()=>{repeatMode=!repeatMode;audio.loop=repeatMode;$("repeat").classList.toggle("on",repeatMode);});
function nextTrack(){
  if(!TRACKS.length)return;
  if(shuffleMode&&TRACKS.length>1){let n=current;while(n===current)n=Math.floor(Math.random()*TRACKS.length);loadTrack(n);}
  else loadTrack(current+1);
  startPlayback();
}
audio.addEventListener("ended",()=>{if(!repeatMode)nextTrack();});
audio.addEventListener("loadedmetadata",()=>{$("total").textContent=timeText(audio.duration);});
audio.addEventListener("timeupdate",()=>{
  if(Number.isFinite(audio.duration)&&audio.duration>0){
    $("seek").value=Math.round(audio.currentTime/audio.duration*1000);
    $("elapsed").textContent=timeText(audio.currentTime);
  }
});
$("seek").addEventListener("input",()=>{
  if(Number.isFinite(audio.duration)&&audio.duration>0) audio.currentTime=(Number($("seek").value)/1000)*audio.duration;
});
function togglePlaylist(){$("playlist").classList.toggle("show");}
$("songsTop").addEventListener("click",togglePlaylist);
$("songlistBtn").addEventListener("click",togglePlaylist);
$("closeList").addEventListener("click",()=>$("playlist").classList.remove("show"));
$("full").addEventListener("click",async()=>{
  try {
    if(!document.fullscreenElement){await document.documentElement.requestFullscreen();}
    else await document.exitFullscreen();
  } catch(e) { $("full").textContent="FULL SCREEN NOT AVAILABLE"; }
});
document.addEventListener("fullscreenchange",()=>{$("full").textContent=document.fullscreenElement?"✕ EXIT FULL SCREEN":"⛶ FULL SCREEN";});
buildPlaylist();
if(TRACKS.length)loadTrack(0);

// Twinkling particles
const stars=$("stars"),sc=stars.getContext("2d");let particles=[];
function resizeStars(){
  stars.width=window.innerWidth*(window.devicePixelRatio||1);
  stars.height=window.innerHeight*(window.devicePixelRatio||1);
  particles=Array.from({length:85},()=>({x:Math.random()*stars.width,y:Math.random()*stars.height,r:Math.random()*2+0.4,a:Math.random(),v:Math.random()*.018+.004,h:Math.random()*360}));
}
window.addEventListener("resize",resizeStars);resizeStars();
function drawStars(){
  sc.clearRect(0,0,stars.width,stars.height);
  particles.forEach(p=>{p.a+=p.v;if(p.a>1||p.a<.12)p.v*=-1;sc.beginPath();sc.arc(p.x,p.y,p.r,0,Math.PI*2);sc.fillStyle=`hsla(${p.h},100%,70%,${p.a})`;sc.shadowBlur=12;sc.shadowColor=sc.fillStyle;sc.fill();sc.shadowBlur=0;});
  requestAnimationFrame(drawStars);
}
drawStars();
</script>
</body>
</html>
"""

page = HTML.replace("TRACKS_JSON", tracks_json).replace("LOGO_JSON", logo_json)

if not music_files:
    st.warning(
        "ยังไม่พบไฟล์เพลง กรุณาวางไฟล์เพลง MP3/WAV/OGG/M4A ไว้ในโฟลเดอร์เดียวกับ app.py "
        "แล้วรีเฟรชแอป"
    )

# components.html creates an isolated interactive frame. All controls and audio
# playback live together inside that frame; tap Play once to satisfy mobile autoplay rules.
components.html(page, height=1120, scrolling=False)
