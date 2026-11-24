from pathlib import Path
import base64, mimetypes, json
import streamlit as st
import streamlit.components.v1 as components

APP_DIR=Path(__file__).resolve().parent
LOGO_FILE=APP_DIR/'logo1.jpg'
AUDIO_EXTS={'.mp3','.wav','.ogg','.m4a','.aac','.flac'}
st.set_page_config(page_title='SYNAPSE NEON MUSIC STUDIO', page_icon='🎧', layout='wide')
st.markdown('''<style>
html,body,[data-testid="stAppViewContainer"]{background:#02020b!important;color:#eaf7ff!important}
[data-testid="stHeader"],footer,#MainMenu{visibility:hidden;height:0}
.block-container{padding:0.15rem 0.4rem!important;max-width:100%!important}
[data-testid="stSidebar"]{background:#06091a!important}
</style>''',unsafe_allow_html=True)

# Tracks are loaded from the app folder, plus optional files uploaded through the sidebar.
local_files=sorted([p for p in APP_DIR.iterdir() if p.is_file() and p.suffix.lower() in AUDIO_EXTS],key=lambda p:p.name.lower())
with st.sidebar:
    st.markdown('### 🎵 SONG LIBRARY')
    uploaded=st.file_uploader('เพิ่มเพลงจากโทรศัพท์/อุปกรณ์',type=[x[1:] for x in AUDIO_EXTS],accept_multiple_files=True)
    st.caption('หรือวางไฟล์เพลงไว้ในโฟลเดอร์เดียวกับ app.py แล้วรีเฟรชแอป')

def data_uri_bytes(name, data):
    mime=mimetypes.guess_type(name)[0] or 'audio/mpeg'
    return f'data:{mime};base64,'+base64.b64encode(data).decode('ascii')
tracks=[]
for p in local_files:
    try: tracks.append({'name':p.stem,'src':data_uri_bytes(p.name,p.read_bytes())})
    except Exception: pass
if uploaded:
    for f in uploaded:
        tracks.append({'name':Path(f.name).stem,'src':data_uri_bytes(f.name,f.getvalue())})
logo=''
if LOGO_FILE.exists():
    logo=data_uri_bytes(LOGO_FILE.name,LOGO_FILE.read_bytes())
tracks_json=json.dumps(tracks,ensure_ascii=False).replace('</','<\\/')
logo_json=json.dumps(logo)

html=r'''<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1"><style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#03030c;color:#e9f8ff;font-family:Arial,sans-serif}
body{background:radial-gradient(ellipse at center,rgba(24,8,72,.7),transparent 60%),radial-gradient(ellipse at 8% 90%,rgba(0,110,255,.3),transparent 40%),#03030c}
#stars{position:fixed;inset:0;width:100%;height:100%;pointer-events:none}
.shell{height:100dvh;width:100%;max-width:980px;margin:auto;padding:8px 10px;display:flex;flex-direction:column;gap:5px;overflow:hidden;position:relative}
:fullscreen{background:#03030c;width:100vw;height:100vh}.panel{border:1px solid #258bdb88;border-radius:14px;background:linear-gradient(100deg,#041024e8,#120626df);box-shadow:0 0 12px #008dff22,inset 0 0 12px #3a00ff12}
.header{display:flex;justify-content:space-between;align-items:center;padding:7px 12px;flex-shrink:0}.brand{font-size:clamp(25px,7vw,48px);font-weight:900;letter-spacing:.12em;font-style:italic;color:#9deeff;text-shadow:0 0 8px #00cfff,0 0 24px #285bff}.sub{letter-spacing:.3em;font-size:clamp(8px,2vw,12px);color:#aac9ef}.status{text-align:right;font-size:clamp(9px,2vw,12px);letter-spacing:.12em;line-height:1.6;color:#d8eea0}.led{color:#56ff99;text-shadow:0 0 8px #56ff99}
#top{width:100%;height:clamp(42px,9vh,78px);flex-shrink:0}
.stage{position:relative;flex:1;min-height:0;display:grid;place-items:center}.ring{height:min(58vh,78vw);width:min(58vh,78vw);position:relative;max-height:100%;max-width:100%}#radial{width:100%;height:100%;position:absolute;inset:0}.logo{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);height:42%;width:42%;border-radius:50%;border:2px solid #7cf8ff;overflow:hidden;display:grid;place-items:center;background:#030816;box-shadow:0 0 12px #00bfff,0 0 28px #ae20ff}.logo img{width:100%;height:100%;object-fit:contain}.fallback{font-size:14px;text-align:center;color:#b3f7ff;text-shadow:0 0 10px #00cfff;font-weight:bold}
.metric{position:absolute;top:50%;transform:translateY(-50%);width:22%;padding:7px 3px;text-align:center;border:1px solid #12d6ff88;border-radius:10px;background:#030a20dd}.metric.l{left:0}.metric.r{right:0;border-color:#ff3cce88}.label{font-size:clamp(7px,2vw,11px);letter-spacing:.1em;color:#5feaff}.r .label{color:#ff80e7}.val{font-size:clamp(20px,6vw,42px);font-weight:bold;color:#00eaff;text-shadow:0 0 12px #00cfff}.r .val{color:#ff4cdb;text-shadow:0 0 12px #ff38da}.meter{display:flex;height:14px;gap:2px;align-items:end;justify-content:center}.meter b{width:3px;height:var(--h);background:#00dfff;box-shadow:0 0 4px #00dfff}.r .meter b{background:#ff35d4;box-shadow:0 0 4px #ff35d4}
.song{flex-shrink:0;text-align:center;padding:5px}.songname{font-size:clamp(14px,4vw,23px);font-weight:bold;font-style:italic;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-shadow:0 0 10px #00bfff}.songcaption{font-size:9px;letter-spacing:.2em;color:#83dfff}
.controls{display:flex;align-items:center;justify-content:center;gap:clamp(5px,2.2vw,17px);flex-shrink:0;padding:3px}.btn{height:clamp(40px,10vw,64px);width:clamp(40px,10vw,64px);border-radius:50%;background:#051025;border:1px solid #00cfff;color:#e8fbff;font-size:clamp(14px,4vw,24px);box-shadow:0 0 10px #00aaff55;cursor:pointer}.btn.main{height:clamp(55px,14vw,82px);width:clamp(55px,14vw,82px);border:3px solid #c74aff;background:#080a20;font-size:27px;box-shadow:0 0 19px #ad20ff77}.btn.on{border-color:#ffe84b;color:#ffe84b;box-shadow:0 0 12px #ffe84b}
.seek{flex-shrink:0;padding:0 5px}input[type=range]{width:100%;height:18px;accent-color:#28e4ff}.times{display:flex;justify-content:space-between;font-size:11px;color:#cfe8ff}
.tag{text-align:center;font-size:clamp(8px,1.8vw,11px);letter-spacing:.12em;color:#9fcdf2;flex-shrink:0;padding:2px}.foot{display:flex;justify-content:space-between;flex-shrink:0}.mini{border:1px solid #23dfff;border-radius:24px;padding:7px 12px;background:#04102a;color:#8ceeff;font-size:11px;cursor:pointer;box-shadow:0 0 9px #00baff33}
.list{display:none;position:absolute;z-index:5;left:4%;right:4%;top:10%;max-height:75%;overflow:auto;background:#030716f5;border:1px solid #18dfff;border-radius:13px;padding:9px;box-shadow:0 0 20px #006aff88}.list.open{display:block}.entry{padding:10px;border-bottom:1px solid #1c8aff44;cursor:pointer;font-size:12px}.entry.sel{color:#ff72e7}
@media(max-height:600px){.shell{padding:4px;gap:3px}.header{padding:4px 8px}.stage{min-height:0}.tag{display:none}.song{padding:2px}.controls{padding:0}}
</style></head><body><canvas id="stars"></canvas><main class="shell" id="shell">
<header class="header panel"><div><div class="brand">SYNAPSE</div><div class="sub">NEON MUSIC STUDIO</div></div><div class="status"><span class="led">● AUDIO READY</span><br><span id="count">LIBRARY: 0 TRACKS</span><br>● SOUND THERAPY</div></header>
<canvas id="top"></canvas><section class="stage"><div class="metric l"><div class="label">BASS ENERGY</div><div class="val" id="bass">000</div><div class="meter" id="bm"></div></div><div class="ring"><canvas id="radial"></canvas><div class="logo" id="logo"></div></div><div class="metric r"><div class="label">TREBLE ENERGY</div><div class="val" id="treble">000</div><div class="meter" id="tm"></div></div><div class="list" id="list"><div style="display:flex;justify-content:space-between;padding:4px 5px;color:#8beeff"><b>♫ SONG LIST</b><button class="mini" id="close">CLOSE ×</button></div><div id="entries"></div></div></section>
<div class="song panel"><div class="songname" id="songname">Choose a song</div><div class="songcaption">SYNAPSE MUSIC STUDIO</div></div>
<div class="controls"><button class="btn" id="prev">|◀</button><button class="btn" id="rew">◀</button><button class="btn main" id="play">▶</button><button class="btn" id="next">▶|</button><button class="btn" id="shuffle">🔀</button><button class="btn" id="repeat">🔁</button></div>
<div class="seek"><input id="seek" type="range" min="0" max="1000" value="0"><div class="times"><span id="elapsed">00:00</span><span id="total">00:00</span></div></div><div class="tag">FEEL THE MUSIC • HEAL YOUR MIND • LIVE IN HARMONY</div><div class="foot"><button class="mini" id="songtoggle">♫ SONG LIST</button><button class="mini" id="fs">⛶ FULL SCREEN</button></div></main><audio id="audio"></audio>
<script>
const tracks=TRACKS_PLACEHOLDER,logoData=LOGO_PLACEHOLDER;const audio=document.getElementById('audio'),playBtn=document.getElementById('play'),nameEl=document.getElementById('songname'),seek=document.getElementById('seek');let idx=0,shuffle=false,repeat=false,ctx=null,an=null,srcNode=null,fd=null,td=null;
document.getElementById('count').textContent='LIBRARY: '+tracks.length+' TRACKS';const logo=document.getElementById('logo');logo.innerHTML=logoData?'<img src="'+logoData+'">':'<div class="fallback">SYNAPSE<br>MUSIC • HEALING • ENERGY</div>';
const fmt=n=>{n=Math.max(0,Number(n)||0);return String(Math.floor(n/60)).padStart(2,'0')+':'+String(Math.floor(n%60)).padStart(2,'0')};
function bars(id){let e=document.getElementById(id);e.innerHTML='';for(let j=0;j<18;j++){let b=document.createElement('b');b.style.setProperty('--h',(4+Math.random()*10)+'px');e.appendChild(b)}}bars('bm');bars('tm');
function listRender(){let e=document.getElementById('entries');e.innerHTML='';if(!tracks.length){e.innerHTML='<div class="entry">No music files loaded. Add songs in the sidebar or app folder.</div>';return;}tracks.forEach((t,i)=>{let row=document.createElement('div');row.className='entry'+(i===idx?' sel':'');row.textContent=(i+1)+'. ♫ '+t.name;row.onclick=()=>{load(i);startPlay();document.getElementById('list').classList.remove('open')};e.appendChild(row)})}
function load(i){if(!tracks.length){nameEl.textContent='No tracks loaded';listRender();return;}idx=(i+tracks.length)%tracks.length;audio.src=tracks[idx].src;nameEl.textContent=tracks[idx].name;seek.value=0;listRender()}
async function analyzerInit(){if(ctx)return;try{ctx=new (window.AudioContext||window.webkitAudioContext)();an=ctx.createAnalyser();an.fftSize=1024;an.smoothingTimeConstant=.8;srcNode=ctx.createMediaElementSource(audio);srcNode.connect(an);an.connect(ctx.destination);fd=new Uint8Array(an.frequencyBinCount);td=new Uint8Array(an.fftSize);if(ctx.state==='suspended')await ctx.resume()}catch(err){console.warn('Analyzer initialization:',err)}}
async function startPlay(){if(!tracks.length){nameEl.textContent='Upload songs using the sidebar or add audio files beside app.py';return;}await analyzerInit();if(ctx&&ctx.state==='suspended')await ctx.resume();if(!audio.src)load(idx);try{await audio.play();playBtn.textContent='Ⅱ'}catch(e){playBtn.textContent='▶';nameEl.textContent='Tap Play to start audio'}}
playBtn.onclick=()=>audio.paused?startPlay():(audio.pause(),playBtn.textContent='▶');document.getElementById('prev').onclick=()=>load(idx-1),document.getElementById('next').onclick=()=>shuffle&&tracks.length>1?load(Math.floor(Math.random()*tracks.length)):load(idx+1);document.getElementById('rew').onclick=()=>{audio.currentTime=Math.max(0,(audio.currentTime||0)-10)};
document.getElementById('shuffle').onclick=e=>{shuffle=!shuffle;e.currentTarget.classList.toggle('on',shuffle)};document.getElementById('repeat').onclick=e=>{repeat=!repeat;e.currentTarget.classList.toggle('on',repeat);audio.loop=repeat};audio.onended=()=>{if(repeat)return;if(tracks.length>1)load(shuffle?Math.floor(Math.random()*tracks.length):idx+1);else playBtn.textContent='▶'};audio.onerror=()=>{if(audio.src)nameEl.textContent='Audio file error';};audio.onloadedmetadata=()=>document.getElementById('total').textContent=fmt(audio.duration);audio.ontimeupdate=()=>{if(audio.duration){seek.value=audio.currentTime/audio.duration*1000;document.getElementById('elapsed').textContent=fmt(audio.currentTime)}};seek.oninput=()=>{if(audio.duration)audio.currentTime=seek.value/1000*audio.duration};
const list=document.getElementById('list');document.getElementById('songtoggle').onclick=()=>list.classList.toggle('open');document.getElementById('close').onclick=()=>list.classList.remove('open');document.getElementById('fs').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await (document.getElementById('shell').requestFullscreen?document.getElementById('shell').requestFullscreen():document.documentElement.requestFullscreen())}catch(err){nameEl.textContent='Fullscreen blocked by browser; use browser full-screen option'}};document.addEventListener('fullscreenchange',()=>document.getElementById('fs').textContent=document.fullscreenElement?'⛶ EXIT FULL SCREEN':'⛶ FULL SCREEN');
listRender();if(tracks.length)load(0);
// star field
const sc=document.getElementById('stars'),s=sc.getContext('2d');let pts=[];function rs(){sc.width=innerWidth;sc.height=innerHeight;pts=Array.from({length:80},()=>({x:Math.random()*sc.width,y:Math.random()*sc.height,r:Math.random()*1.5+.3,a:Math.random(),v:.01+Math.random()*.015}))}rs();addEventListener('resize',rs);function starLoop(){s.clearRect(0,0,sc.width,sc.height);pts.forEach(p=>{p.a+=p.v;if(p.a>1||p.a<.15)p.v=-p.v;s.fillStyle='rgba(65,190,255,'+p.a+')';s.beginPath();s.arc(p.x,p.y,p.r,0,6.283);s.fill()});requestAnimationFrame(starLoop)}starLoop();
const top=document.getElementById('top'),tc=top.getContext('2d');function rt(){top.width=top.clientWidth*devicePixelRatio;top.height=top.clientHeight*devicePixelRatio}rt();addEventListener('resize',rt);function topLoop(){let w=top.width,h=top.height;tc.clearRect(0,0,w,h);for(let i=0;i<90;i++){let v=fd?fd[Math.floor(i/90*fd.length)]/255:Math.abs(Math.sin(Date.now()/420+i*.13))*.28;let bh=5+v*h*.85,x=i*w/90;tc.fillStyle='hsl('+(180+i*2.2)+',100%,60%)';tc.fillRect(x,h-bh,w/90*.7,bh)}requestAnimationFrame(topLoop)}topLoop();
const rad=document.getElementById('radial'),rc=rad.getContext('2d');function rr(){let b=rad.getBoundingClientRect();rad.width=b.width*devicePixelRatio;rad.height=b.height*devicePixelRatio}rr();addEventListener('resize',rr);function ringLoop(){let w=rad.width,h=rad.height,cx=w/2,cy=h/2,R=Math.min(w,h)*.28;rc.clearRect(0,0,w,h);let bass=0,high=0;if(an&&fd){an.getByteFrequencyData(fd);for(let i=0;i<Math.min(28,fd.length);i++)bass+=fd[i];for(let i=Math.floor(fd.length*.68);i<fd.length;i++)high+=fd[i];document.getElementById('bass').textContent=String(Math.min(999,Math.round(bass/28*3.9))).padStart(3,'0');document.getElementById('treble').textContent=String(Math.min(999,Math.round(high/(fd.length*.32)*3.9))).padStart(3,'0')}
let t=Date.now()/1000;for(let l=0;l<6;l++){let rr0=R+l*R*.14;rc.beginPath();rc.arc(cx,cy,rr0+Math.sin(t*1.4+l)*3,0,Math.PI*2);rc.strokeStyle='hsla('+((t*40+l*50)%360)+',100%,65%,.7)';rc.lineWidth=2;rc.shadowBlur=12;rc.shadowColor=rc.strokeStyle;rc.stroke();rc.shadowBlur=0}for(let k=0;k<150;k++){let a=k/150*Math.PI*2,v=fd&&an?fd[Math.floor(k/150*fd.length)]/255:Math.abs(Math.sin(t*2+k*.1))*.2,len=5+v*R*.65;rc.beginPath();rc.moveTo(cx+Math.cos(a)*R*.82,cy+Math.sin(a)*R*.82);rc.lineTo(cx+Math.cos(a)*(R*.82+len),cy+Math.sin(a)*(R*.82+len));rc.strokeStyle='hsl('+((k*2.4+t*22)%360)+',100%,65%)';rc.lineWidth=2;rc.shadowBlur=7;rc.shadowColor=rc.strokeStyle;rc.stroke();rc.shadowBlur=0}requestAnimationFrame(ringLoop)}ringLoop();
</script></body></html>'''
html=html.replace('TRACKS_PLACEHOLDER',tracks_json).replace('LOGO_PLACEHOLDER',logo_json)
if not tracks: st.info('เพิ่มเพลงผ่านแถบเมนูด้านซ้าย (SONG LIBRARY) หรือวางไฟล์เพลงไว้ในโฟลเดอร์เดียวกับ app.py')
components.html(html,height=900,scrolling=False)
