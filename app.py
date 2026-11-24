import base64
import mimetypes
import random
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# SYNAPSE NEON MUSIC STUDIO — single-file Streamlit app
# Put logo1.jpg and your music files in the same folder as app.py
# ============================================================

APP_DIR = Path(__file__).resolve().parent
LOGO_FILE = APP_DIR / "logo1.jpg"
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac"}

st.set_page_config(
    page_title="SYNAPSE NEON MUSIC STUDIO",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit chrome; keep the app as a one-screen music studio.
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] { background:#02020b !important; }
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], footer, #MainMenu { display:none !important; }
.block-container { padding:0 !important; margin:0 !important; max-width:100% !important; }
</style>
""", unsafe_allow_html=True)

tracks = sorted(
    [p for p in APP_DIR.iterdir() if p.is_file() and p.suffix.lower() in AUDIO_EXTS],
    key=lambda p: p.name.lower()
)

def to_data_uri(path: Path):
    mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"

track_payload = [{"name": p.stem, "src": to_data_uri(p)} for p in tracks]
logo_uri = ""
if LOGO_FILE.exists():
    mime = mimetypes.guess_type(LOGO_FILE.name)[0] or "image/jpeg"
    logo_uri = "data:" + mime + ";base64," + base64.b64encode(LOGO_FILE.read_bytes()).decode("ascii")

# Pass data safely into the embedded player.
import json
tracks_json = json.dumps(track_payload, ensure_ascii=False).replace("</", "<\\/")
logo_json = json.dumps(logo_uri)

player_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#02020b;color:#eaf7ff;font-family:Arial,Helvetica,sans-serif}
body{background:
 radial-gradient(ellipse at 50% 45%,rgba(30,15,78,.45),transparent 55%),
 radial-gradient(ellipse at 5% 85%,rgba(0,135,255,.25),transparent 40%),
 radial-gradient(ellipse at 95% 12%,rgba(190,0,255,.23),transparent 38%),
 #02020b}
#stars{position:fixed;inset:0;width:100%;height:100%;pointer-events:none}
.frame{position:relative;height:100dvh;width:100%;max-width:900px;margin:auto;padding:12px 14px 10px;display:flex;flex-direction:column;gap:7px;overflow:hidden}
.panel{border:1px solid rgba(54,196,255,.48);border-radius:17px;box-shadow:0 0 13px rgba(0,180,255,.12),inset 0 0 15px rgba(0,70,180,.08);background:linear-gradient(110deg,rgba(4,12,32,.82),rgba(15,5,35,.72));}
.header{padding:10px 14px;display:flex;align-items:center;justify-content:space-between;min-height:70px;gap:12px}
.brand{font-size:clamp(24px,6vw,48px);font-weight:900;letter-spacing:.1em;font-style:italic;color:#a6eaff;text-shadow:0 0 8px #08baff,0 0 22px #2869ff}
.sub{font-size:clamp(8px,2vw,13px);letter-spacing:.35em;color:#a8c4e6;margin-top:2px}
.status{font-size:clamp(9px,2.3vw,12px);letter-spacing:.12em;line-height:1.8;text-align:right;color:#d7e8a7;white-space:nowrap}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#48ff9b;box-shadow:0 0 10px #48ff9b;margin-right:6px}
#topviz{height:76px;width:100%;display:block;flex-shrink:0}
.centerstage{position:relative;flex:1;min-height:0;display:flex;align-items:center;justify-content:center}
.ringwrap{position:relative;width:min(70vw,48vh,460px);height:min(70vw,48vh,460px);max-width:100%;max-height:100%;display:grid;place-items:center}
#ringcanvas{position:absolute;width:100%;height:100%;inset:0}
.logoBox{position:relative;width:44%;height:44%;border-radius:50%;overflow:hidden;border:2px solid #4deeff;box-shadow:0 0 12px #00bfff,0 0 26px #7d2bff,inset 0 0 15px #00aaff;background:#030712;display:grid;place-items:center}
.logoBox img{width:100%;height:100%;object-fit:contain}
.logoFallback{font-weight:900;font-size:clamp(10px,3vw,20px);letter-spacing:.1em;color:#8ef7ff;text-shadow:0 0 10px #00bfff;text-align:center}
.metrics{position:absolute;top:50%;transform:translateY(-50%);width:24%;padding:10px 7px;text-align:center;border:1px solid rgba(0,210,255,.55);background:rgba(3,8,24,.72);border-radius:12px;box-shadow:0 0 14px rgba(0,180,255,.15)}
.metrics.left{left:1%}.metrics.right{right:1%;border-color:rgba(255,60,210,.55)}
.mlabel{font-size:clamp(8px,2.1vw,12px);letter-spacing:.12em;color:#65eaff}
.right .mlabel{color:#ff83e6}
.mvalue{font-size:clamp(22px,6vw,44px);font-weight:900;font-style:italic;color:#00eaff;text-shadow:0 0 15px #00cfff;margin:4px 0}
.right .mvalue{color:#ff50df;text-shadow:0 0 15px #ff40df}
.bars{height:18px;display:flex;gap:2px;justify-content:center;align-items:end}
.bars i{display:block;width:4px;height:var(--h);background:#08eaff;box-shadow:0 0 5px #08eaff}
.right .bars i{background:#ff42db;box-shadow:0 0 5px #ff42db}
.trackinfo{flex-shrink:0;text-align:center;padding:7px 4px 2px}
.trackname{font-size:clamp(16px,4vw,26px);font-weight:bold;font-style:italic;color:#eff7ff;text-shadow:0 0 12px #25bfff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tracksub{font-size:10px;letter-spacing:.22em;color:#7fdfff;margin-top:2px}
.controls{display:flex;justify-content:center;align-items:center;gap:clamp(7px,3vw,24px);padding:7px 0;flex-shrink:0}
.btn{width:clamp(42px,11vw,68px);height:clamp(42px,11vw,68px);border-radius:50%;border:1.5px solid #21cfff;background:rgba(4,14,34,.82);color:#e8fbff;font-size:clamp(16px,4vw,25px);box-shadow:0 0 12px rgba(0,185,255,.45),inset 0 0 10px rgba(0,130,255,.15);cursor:pointer}
.btn.main{width:clamp(60px,15vw,90px);height:clamp(60px,15vw,90px);border:3px solid transparent;background:linear-gradient(#050914,#050914) padding-box,conic-gradient(#08eaff,#d900ff,#ff3bda,#ffe500,#08eaff) border-box;font-size:clamp(22px,5vw,32px);box-shadow:0 0 23px rgba(170,0,255,.55)}
.btn.active{color:#ffed59;border-color:#ffed59;box-shadow:0 0 13px #ffed59}
.seekarea{flex-shrink:0;padding:0 5px}
input[type=range]{width:100%;accent-color:#22dfff;height:20px}
.times{display:flex;justify-content:space-between;font-size:12px;color:#d7e8ff}
.footerline{display:flex;justify-content:space-between;gap:10px;flex-shrink:0;padding:5px 0 2px}
.smallbtn{border:1px solid #27dfff;border-radius:25px;background:rgba(4,12,32,.7);padding:8px 14px;color:#8eeaff;letter-spacing:.08em;font-size:11px;box-shadow:0 0 10px rgba(0,190,255,.3);cursor:pointer}
.songpanel{position:absolute;z-index:10;top:12%;left:5%;right:5%;max-height:70%;overflow:auto;display:none;padding:10px;border:1px solid #28dcff;border-radius:15px;background:rgba(2,4,17,.97);box-shadow:0 0 25px #146bff}
.songpanel.show{display:block}
.songrow{padding:10px;border-bottom:1px solid rgba(0,190,255,.22);font-size:13px;cursor:pointer;color:#dffaff}
.songrow:hover{color:#fff;background:rgba(0,160,255,.15)}
.songrow.playing{color:#ff65e8;text-shadow:0 0 9px #ff40d0}
.tagline{text-align:center;font-size:clamp(8px,2vw,12px);letter-spacing:.14em;color:#9cc9ef;padding:4px 2px;flex-shrink:0}
@media(max-height:650px){.frame{gap:3px;padding:6px}.header{min-height:54px;padding:5px 10px}#topviz{height:50px}.controls{padding:2px}.trackinfo{padding:2px}.footerline{padding:2px}.tagline{display:none}}
</style>
</head>
<body>
<canvas id="stars"></canvas>
<div class="frame">
  <div class="header panel">
    <div><div class="brand">SYNAPSE</div><div class="sub">NEON MUSIC STUDIO</div></div>
    <div class="status"><span class="dot"></span>AUDIO READY<br><span id="librarycount">LIBRARY: 0 TRACKS</span><br>● SOUND THERAPY</div>
  </div>
  <canvas id="topviz"></canvas>
  <div class="centerstage">
    <div class="metrics left"><div class="mlabel">BASS ENERGY</div><div class="mvalue" id="bass">000</div><div class="bars" id="bassbars"></div></div>
    <div class="ringwrap"><canvas id="ringcanvas"></canvas><div class="logoBox" id="logoBox"></div></div>
    <div class="metrics right"><div class="mlabel">TREBLE ENERGY</div><div class="mvalue" id="treble">000</div><div class="bars" id="treblebars"></div></div>
    <div class="songpanel" id="songpanel"><div id="songlist"></div></div>
  </div>
  <div class="trackinfo panel"><div class="trackname" id="trackname">ยังไม่ตั้งเพลง</div><div class="tracksub">SYNAPSE MUSIC STUDIO</div></div>
  <div class="controls">
    <button class="btn" id="prev" title="Previous">|◀</button>
    <button class="btn" id="back" title="Back 10 seconds">◀</button>
    <button class="btn main" id="play" title="Play/Pause">▶</button>
    <button class="btn" id="next" title="Next">▶|</button>
    <button class="btn" id="shuffle" title="Shuffle">🔀</button>
    <button class="btn" id="repeat" title="Repeat">🔁</button>
  </div>
  <div class="seekarea"><input type="range" id="seek" min="0" max="1000" value="0"><div class="times"><span id="current">00:00</span><span id="duration">00:00</span></div></div>
  <div class="tagline">▮▮▮　FEEL THE MUSIC • HEAL YOUR MIND • LIVE IN HARMONY　▮▮▮</div>
  <div class="footerline"><button class="smallbtn" id="songsbtn">♫ SONG LIST</button><button class="smallbtn" id="fullscreen">⛶ FULL SCREEN</button></div>
</div>
<audio id="audio" crossorigin="anonymous"></audio>
<script>
const tracks = TRACKS_PLACEHOLDER;
const logoData = LOGO_PLACEHOLDER;
const audio = document.getElementById('audio');
const playBtn = document.getElementById('play');
const nameEl = document.getElementById('trackname');
const songPanel = document.getElementById('songpanel');
const listEl = document.getElementById('songlist');
const seek = document.getElementById('seek');
let idx=0, shuffleOn=false, repeatOn=false, audioCtx=null, analyser=null, source=null, freq=null, timeData=null;
document.getElementById('librarycount').textContent=`LIBRARY: ${tracks.length} TRACKS`;
const logoBox=document.getElementById('logoBox');
if(logoData){logoBox.innerHTML=`<img src="${logoData}" alt="SYNAPSE logo">`;}
else{logoBox.innerHTML='<div class="logoFallback">SYNAPSE<br><small>MUSIC • HEALING • ENERGY</small></div>';}
function fmt(s){if(!isFinite(s)||s<0)s=0;return `${String(Math.floor(s/60)).padStart(2,'0')}:${String(Math.floor(s%60)).padStart(2,'0')}`}
function makeBars(target,n,color){target.innerHTML='';for(let i=0;i<n;i++){let b=document.createElement('i');b.style.setProperty('--h',(5+Math.random()*13)+'px');target.appendChild(b)}}
makeBars(document.getElementById('bassbars'),18);
makeBars(document.getElementById('treblebars'),18);
function renderList(){
 listEl.innerHTML='';
 tracks.forEach((t,i)=>{let row=document.createElement('div');row.className='songrow'+(i===idx?' playing':'');row.textContent=`${String(i+1).padStart(2,'0')}  ♫  ${t.name}`;row.onclick=()=>{load(i);play()};listEl.appendChild(row)});
}
function load(i,auto=false){if(!tracks.length)return;idx=(i+tracks.length)%tracks.length;audio.src=tracks[idx].src;nameEl.textContent=tracks[idx].name;renderList();if(auto)play();}
async function initAudio(){
 if(audioCtx)return;
 try{audioCtx=new (window.AudioContext||window.webkitAudioContext)();analyser=audioCtx.createAnalyser();analyser.fftSize=1024;analyser.smoothingTimeConstant=.82;source=audioCtx.createMediaElementSource(audio);source.connect(analyser);analyser.connect(audioCtx.destination);freq=new Uint8Array(analyser.frequencyBinCount);timeData=new Uint8Array(analyser.fftSize);if(audioCtx.state==='suspended')await audioCtx.resume();}catch(e){console.warn('Audio analyzer unavailable',e)}
}
async function play(){if(!tracks.length){nameEl.textContent='ไม่พบไฟล์เพลงในโฟลเดอร์';return}await initAudio();if(audioCtx&&audioCtx.state==='suspended')await audioCtx.resume();if(!audio.src)load(idx);try{await audio.play();playBtn.textContent='Ⅱ'}catch(e){playBtn.textContent='▶';nameEl.textContent='แตะปุ่มเล่นเพื่อเริ่มเพลง'}}
playBtn.onclick=async()=>{if(audio.paused)await play();else{audio.pause();playBtn.textContent='▶'}};
document.getElementById('prev').onclick=()=>load(idx-1,true);
document.getElementById('next').onclick=()=>{if(shuffleOn&&tracks.length>1){let n=idx;while(n===idx)n=Math.floor(Math.random()*tracks.length);load(n,true)}else load(idx+1,true)};
document.getElementById('back').onclick=()=>audio.currentTime=Math.max(0,audio.currentTime-10);
document.getElementById('shuffle').onclick=e=>{shuffleOn=!shuffleOn;e.currentTarget.classList.toggle('active',shuffleOn)};
document.getElementById('repeat').onclick=e=>{repeatOn=!repeatOn;e.currentTarget.classList.toggle('active',repeatOn);audio.loop=repeatOn};
audio.onended=()=>{if(repeatOn)return;if(shuffleOn&&tracks.length>1){let n=idx;while(n===idx)n=Math.floor(Math.random()*tracks.length);load(n,true)}else load(idx+1,true)};
audio.onloadedmetadata=()=>document.getElementById('duration').textContent=fmt(audio.duration);
audio.ontimeupdate=()=>{if(audio.duration){seek.value=Math.floor(audio.currentTime/audio.duration*1000);document.getElementById('current').textContent=fmt(audio.currentTime)}};
seek.oninput=()=>{if(audio.duration)audio.currentTime=Number(seek.value)/1000*audio.duration};
document.getElementById('songsbtn').onclick=()=>songPanel.classList.toggle('show');
document.getElementById('fullscreen').onclick=()=>{if(!document.fullscreenElement)document.documentElement.requestFullscreen?.();else document.exitFullscreen?.()};
document.addEventListener('keydown',e=>{if(e.code==='Space'&&e.target.tagName!=='INPUT'){e.preventDefault();playBtn.click()}});
renderList();if(tracks.length)load(0,false);

// Background stars animation
const stars=document.getElementById('stars'),sctx=stars.getContext('2d');let starDots=[];
function resizeStars(){stars.width=innerWidth;stars.height=innerHeight;starDots=Array.from({length:95},()=>({x:Math.random()*stars.width,y:Math.random()*stars.height,r:Math.random()*1.6+.3,a:Math.random(),v:Math.random()*.018+.004}))}
resizeStars();addEventListener('resize',resizeStars);
function drawStars(){sctx.clearRect(0,0,stars.width,stars.height);starDots.forEach(p=>{p.a+=p.v;if(p.a>1||p.a<.1)p.v*=-1;sctx.fillStyle=`rgba(${Math.random()>.97?'255,70,240':'60,190,255'},${p.a})`;sctx.beginPath();sctx.arc(p.x,p.y,p.r,0,Math.PI*2);sctx.fill()});requestAnimationFrame(drawStars)}drawStars();

// Upper spectrum bars
const top=document.getElementById('topviz'),tctx=top.getContext('2d');
function resizeTop(){top.width=top.clientWidth*devicePixelRatio;top.height=top.clientHeight*devicePixelRatio}
resizeTop();addEventListener('resize',resizeTop);
function drawTop(){
 let w=top.width,h=top.height;tctx.clearRect(0,0,w,h);let n=100;
 for(let i=0;i<n;i++){let v=freq&&analyser?freq[Math.floor(i/n*freq.length)]/255:Math.abs(Math.sin(Date.now()/500+i*.17))*.22;let bh=8+v*(h*.88);let x=i*w/n;let grad=tctx.createLinearGradient(0,h-bh,0,h);grad.addColorStop(0,`hsl(${180+i*2.4},100%,65%)`);grad.addColorStop(1,`hsl(${180+i*2.4},100%,42%)`);tctx.fillStyle=grad;tctx.fillRect(x,h-bh,w/n*.65,bh)}
 requestAnimationFrame(drawTop)
}drawTop();

// Central radial visualizer
const ring=document.getElementById('ringcanvas'),rctx=ring.getContext('2d');
function resizeRing(){let rect=ring.getBoundingClientRect();ring.width=rect.width*devicePixelRatio;ring.height=rect.height*devicePixelRatio}
resizeRing();addEventListener('resize',resizeRing);
function drawRing(){
 let w=ring.width,h=ring.height,cx=w/2,cy=h/2,base=Math.min(w,h)*.29;rctx.clearRect(0,0,w,h);
 let energy=0;if(freq&&analyser){analyser.getByteFrequencyData(freq);analyser.getByteTimeDomainData(timeData);for(let i=0;i<freq.length;i++)energy+=freq[i];energy/=freq.length}
 const now=Date.now()/1000;
 for(let layer=0;layer<6;layer++){let rad=base+layer*base*.14;let hue=(now*45+layer*48)%360;rctx.beginPath();rctx.arc(cx,cy,rad+Math.sin(now*1.5+layer)*4,0,Math.PI*2);rctx.strokeStyle=`hsla(${hue},100%,65%,${.4+energy/500})`;rctx.lineWidth=2+layer%2;rctx.shadowBlur=14;rctx.shadowColor=`hsl(${hue},100%,60%)`;rctx.stroke();rctx.shadowBlur=0}
 let bars=160;for(let i=0;i<bars;i++){let val=freq&&analyser?freq[Math.floor(i/bars*freq.length)]/255:Math.abs(Math.sin(now*2+i*.11))*.16;let angle=i/bars*Math.PI*2;let len=7+val*base*.65;let inner=base*.86;let outer=inner+len;rctx.beginPath();rctx.moveTo(cx+Math.cos(angle)*inner,cy+Math.sin(angle)*inner);rctx.lineTo(cx+Math.cos(angle)*outer,cy+Math.sin(angle)*outer);rctx.strokeStyle=`hsl(${(i/bars*360+now*25)%360},100%,65%)`;rctx.lineWidth=2.2;rctx.shadowBlur=9;rctx.shadowColor=rctx.strokeStyle;rctx.stroke();rctx.shadowBlur=0}
 if(timeData&&analyser){let bass=0,treble=0;for(let i=0;i<24;i++)bass+=freq[i]||0;for(let i=Math.floor(freq.length*.65);i<freq.length;i++)treble+=freq[i]||0;document.getElementById('bass').textContent=String(Math.min(999,Math.round(bass/24*3.9))).padStart(3,'0');document.getElementById('treble').textContent=String(Math.min(999,Math.round(treble/(freq.length*.35)*3.9))).padStart(3,'0')}
 requestAnimationFrame(drawRing)
}drawRing();
</script>
</body>
</html>
"""

player_html = player_html.replace("TRACKS_PLACEHOLDER", tracks_json).replace("LOGO_PLACEHOLDER", logo_json)

if not tracks:
    st.warning("ยังไม่พบเพลง กรุณาวางไฟล์ MP3/WAV/OGG/M4A ไว้ในโฟลเดอร์เดียวกับ app.py")
# Use components.html: it supports inline HTML/JS and is compatible with Streamlit embeds.
components.html(player_html, height=900, scrolling=False)
