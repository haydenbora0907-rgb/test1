import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Pocket Football 3D",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {
    background:#07131a !important;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
header, footer, [data-testid="stToolbar"] {
    display:none !important;
}
iframe {
    width:100% !important;
    border:0 !important;
}
</style>
""", unsafe_allow_html=True)

game = r"""
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#07131a;font-family:Arial,sans-serif;touch-action:none}
#game{position:fixed;inset:0}
canvas{display:block}
#hud{position:fixed;inset:0;pointer-events:none;color:white}
.top{
 position:absolute;top:max(10px,env(safe-area-inset-top));left:0;right:0;
 display:flex;justify-content:center;align-items:center;gap:12px
}
.score{
 background:rgba(3,12,17,.72);backdrop-filter:blur(8px);
 padding:8px 15px;border-radius:14px;font-weight:800;font-size:18px
}
.clock{font-size:13px;opacity:.9}
#help{
 position:absolute;left:50%;top:18%;transform:translateX(-50%);
 background:rgba(0,0,0,.55);padding:9px 14px;border-radius:18px;
 font-size:12px;white-space:nowrap;opacity:1;transition:opacity .4s
}
#help.hide{opacity:0}
#passLine{
 position:absolute;left:50%;bottom:148px;transform:translateX(-50%);
 padding:8px 13px;border-radius:18px;background:rgba(0,0,0,.48);
 font-size:12px;opacity:0;transition:.15s
}
#passLine.show{opacity:1}
.controls{
 position:absolute;left:0;right:0;bottom:max(15px,env(safe-area-inset-bottom));
 display:flex;justify-content:space-between;align-items:flex-end;padding:0 18px
}
.pad{
 width:132px;height:132px;border-radius:50%;
 background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);
 position:relative;pointer-events:auto
}
.stick{
 position:absolute;width:55px;height:55px;border-radius:50%;left:38px;top:38px;
 background:rgba(255,255,255,.25);border:1px solid rgba(255,255,255,.25)
}
.actions{display:flex;gap:12px;align-items:flex-end;pointer-events:auto}
.btn{
 width:70px;height:70px;border-radius:50%;border:0;color:white;font-weight:900;
 background:rgba(255,255,255,.14);box-shadow:0 6px 18px #0006;
 font-size:13px
}
.btn.big{width:82px;height:82px;background:rgba(15,145,90,.8)}
.btn:active{transform:scale(.94)}
#toast{
 position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);
 font-size:32px;font-weight:900;text-shadow:0 3px 10px #000;
 opacity:0;transition:.2s
}
#toast.show{opacity:1}
#start{
 position:fixed;inset:0;background:linear-gradient(#06151de8,#06151df2);
 display:flex;align-items:center;justify-content:center;z-index:5;color:white;text-align:center
}
.card{width:min(88vw,420px);padding:28px;border-radius:26px;background:#10252e;border:1px solid #ffffff18;box-shadow:0 20px 70px #0009}
.card h1{margin:0 0 8px;font-size:30px}
.card p{font-size:14px;line-height:1.55;color:#c5d2d7}
.startBtn{margin-top:14px;width:100%;padding:15px;border:0;border-radius:15px;background:#12a36d;color:#fff;font-weight:900;font-size:17px}
.badge{display:inline-block;padding:6px 10px;border-radius:20px;background:#ffffff12;font-size:11px;margin-bottom:14px}
@media(min-width:800px){
 .controls{padding:0 50px}
 .pad{width:145px;height:145px}
 .stick{left:45px;top:45px}
}
</style>
</head>
<body>
<div id="game"></div>
<div id="hud">
  <div class="top">
    <div class="score"><span id="home">0</span> : <span id="away">0</span></div>
    <div class="score clock" id="clock">00:00</div>
  </div>
  <div id="help">선수를 탭하면 그 방향으로 패스합니다 · 드래그하면 이동</div>
  <div id="passLine">PASS</div>
  <div id="toast"></div>
  <div class="controls">
    <div class="pad" id="pad"><div class="stick" id="stick"></div></div>
    <div class="actions">
      <button class="btn" id="switch">SWITCH</button>
      <button class="btn big" id="shoot">SHOOT</button>
    </div>
  </div>
</div>

<div id="start">
 <div class="card">
   <div class="badge">3D MOBILE FOOTBALL</div>
   <h1>Pocket Football</h1>
   <p>가상의 3D 경기장에서 빠르게 플레이하세요.<br>
   왼쪽 스틱으로 이동 · 상대/팀 선수를 탭해서 패스 · SHOOT으로 슈팅</p>
   <button class="startBtn" id="startBtn">경기 시작</button>
 </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const root=document.getElementById('game');
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x071a21);
scene.fog=new THREE.Fog(0x071a21,55,110);

const camera=new THREE.PerspectiveCamera(48,innerWidth/innerHeight,.1,200);
camera.position.set(0,24,25);

const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.8));
renderer.setSize(innerWidth,innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
root.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xbdefff,0x16331d,2.2));
const sun=new THREE.DirectionalLight(0xffffff,2.4);
sun.position.set(-25,45,18); sun.castShadow=true; scene.add(sun);

const field=new THREE.Mesh(
 new THREE.PlaneGeometry(48,82),
 new THREE.MeshStandardMaterial({color:0x18723d,roughness:.92})
);
field.rotation.x=-Math.PI/2; field.receiveShadow=true; scene.add(field);

function line(points,w=.12){
 const g=new THREE.BufferGeometry().setFromPoints(points.map(p=>new THREE.Vector3(p[0],.045,p[1])));
 const m=new THREE.LineBasicMaterial({color:0xeaf7e9});
 const l=new THREE.Line(g,m); scene.add(l); return l;
}
line([[-24,-41],[24,-41],[24,41],[-24,41],[-24,-41]]);
line([[-24,0],[24,0]]);
const circle=new THREE.LineLoop(
 new THREE.BufferGeometry().setFromPoints([...Array(65)].map((_,i)=>{
   const a=i/64*Math.PI*2; return new THREE.Vector3(Math.cos(a)*6,.05,Math.sin(a)*6)
 })),
 new THREE.LineBasicMaterial({color:0xeaf7e9})
); scene.add(circle);

line([[-10,-41],[10,-41],[10,-31],[-10,-31],[-10,-41]]);
line([[-10,41],[10,41],[10,31],[-10,31],[-10,41]]);
line([[-3.2,-41],[3.2,-41]]); line([[-3.2,41],[3.2,41]]);

function box(w,h,d,c,x,y,z){
 const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),new THREE.MeshStandardMaterial({color:c}));
 m.position.set(x,y,z);m.castShadow=true;scene.add(m);return m;
}
box(10,.7,.7,0xffffff,0,2,-41);
box(10,.7,.7,0xffffff,0,2,41);

const ball=new THREE.Mesh(new THREE.SphereGeometry(.65,20,14),new THREE.MeshStandardMaterial({color:0xf5f5f5,roughness:.35}));
ball.position.set(0,.65,8);ball.castShadow=true;scene.add(ball);

function player(team,x,z,num){
 const group=new THREE.Group();
 const c=team===0?0x16a5ff:0xf04b4b;
 const body=new THREE.Mesh(new THREE.CapsuleGeometry(.55,1.1,6,12),new THREE.MeshStandardMaterial({color:c}));
 body.position.y=1.05;body.castShadow=true;group.add(body);
 const head=new THREE.Mesh(new THREE.SphereGeometry(.42,14,10),new THREE.MeshStandardMaterial({color:0xf0c39a}));
 head.position.y=2.05;head.castShadow=true;group.add(head);
 group.position.set(x,0,z);group.userData={team,num,vel:new THREE.Vector3(),target:null};
 scene.add(group);return group;
}
const home=[
 player(0,-11,25,7),player(0,11,25,11),player(0,-10,12,8),
 player(0,10,12,10),player(0,-7,-2,6),player(0,7,-2,9),player(0,0,8,10)
];
const away=[
 player(1,-10,-25,7),player(1,10,-25,11),player(1,-12,-12,8),
 player(1,12,-12,10),player(1,-7,2,6),player(1,7,2,9),player(1,0,-8,10)
];
let controlled=home[6];
let score=[0,0], running=false, elapsed=0, last=performance.now();
let joystick={x:0,y:0,active:false}, dragging=false, dragStart={x:0,y:0};

function dist(a,b){return a.position.distanceTo(b.position)}
function nearestOpponent(p){
 let best=null,bd=999;
 away.forEach(o=>{let d=dist(p,o);if(d<bd){bd=d;best=o}});
 return best;
}
function passTo(target){
 if(!running)return;
 const dir=new THREE.Vector3().subVectors(target.position,controlled.position).normalize();
 ball.position.copy(controlled.position).add(new THREE.Vector3(0,.7,0));
 ball.userData={moving:true,start:ball.position.clone(),end:target.position.clone().add(new THREE.Vector3(0,.7,0)),t:0};
 document.getElementById('passLine').classList.add('show');
 setTimeout(()=>document.getElementById('passLine').classList.remove('show'),350);
}
function kick(){
 if(!running)return;
 const dir=new THREE.Vector3(0,0,-1);
 const towardGoal=controlled.position.z<0? -1:1;
 dir.set((ball.position.x-controlled.position.x)*.18,towardGoal*-1,(towardGoal*-1)).normalize();
 ball.userData={moving:true,start:ball.position.clone(),end:ball.position.clone().add(dir.multiplyScalar(22)),t:0};
}
function toast(t){
 const e=document.getElementById('toast');e.textContent=t;e.classList.add('show');
 setTimeout(()=>e.classList.remove('show'),700);
}

function selectAt(nx,ny){
 const ray=new THREE.Raycaster();
 ray.setFromCamera(new THREE.Vector2(nx,ny),camera);
 const hits=ray.intersectObjects([...home,...away],true);
 if(!hits.length)return;
 let g=hits[0].object;while(g.parent && !g.userData.team===undefined)g=g.parent;
 while(g.parent && g.userData.team===undefined)g=g.parent;
 if(g.userData.team===0){controlled=g;toast("PLAYER "+g.userData.num)}
 else {passTo(g);toast("PASS")}
}
renderer.domElement.addEventListener('pointerdown',e=>{
 dragging=true;dragStart={x:e.clientX,y:e.clientY};
});
renderer.domElement.addEventListener('pointerup',e=>{
 if(!dragging)return;dragging=false;
 if(Math.hypot(e.clientX-dragStart.x,e.clientY-dragStart.y)<14){
   const r=renderer.domElement.getBoundingClientRect();
   selectAt(((e.clientX-r.left)/r.width)*2-1,-((e.clientY-r.top)/r.height)*2+1);
 }
});

function movePad(e){
 const r=document.getElementById('pad').getBoundingClientRect();
 let x=e.clientX-(r.left+r.width/2), y=e.clientY-(r.top+r.height/2);
 const max=r.width*.34, d=Math.hypot(x,y);
 if(d>max){x=x/d*max;y=y/d*max}
 joystick.x=x/max;joystick.y=y/max;
 const s=document.getElementById('stick');s.style.transform=`translate(${x}px,${y}px)`;
}
const pad=document.getElementById('pad');
pad.addEventListener('pointerdown',e=>{joystick.active=true;pad.setPointerCapture(e.pointerId);movePad(e)});
pad.addEventListener('pointermove',e=>{if(joystick.active)movePad(e)});
pad.addEventListener('pointerup',()=>{joystick.active=false;joystick.x=joystick.y=0;document.getElementById('stick').style.transform='translate(0,0)'});
document.getElementById('shoot').onclick=kick;
document.getElementById('switch').onclick=()=>{
 let idx=home.indexOf(controlled);controlled=home[(idx+1)%home.length];toast("SWITCH");
};

function updatePlayers(dt){
 const speed=7;
 const mv=new THREE.Vector3(joystick.x,0,joystick.y);
 controlled.position.x+=mv.x*speed*dt;
 controlled.position.z+=mv.z*speed*dt;
 controlled.position.x=THREE.MathUtils.clamp(controlled.position.x,-22,22);
 controlled.position.z=THREE.MathUtils.clamp(controlled.position.z,-39,39);

 home.forEach(p=>{
   if(p===controlled)return;
   const base=p.userData.base||p.position.clone();p.userData.base=base;
   p.position.lerp(base,.018);
 });
 away.forEach(p=>{
   const target=ball.position.clone();target.y=0;
   if(p.position.distanceTo(target)<15){
     const d=new THREE.Vector3().subVectors(target,p.position).normalize();
     p.position.add(d.multiplyScalar(1.8*dt));
   }
   p.position.x=THREE.MathUtils.clamp(p.position.x,-22,22);
   p.position.z=THREE.MathUtils.clamp(p.position.z,-39,39);
 });
 if(controlled.position.distanceTo(ball.position)<2.0 && !ball.userData.moving){
   ball.position.x=controlled.position.x;
   ball.position.z=controlled.position.z-1.0;
 }
}

function updateBall(dt){
 if(!ball.userData.moving)return;
 ball.userData.t+=dt*2.2;
 const t=Math.min(ball.userData.t,1);
 ball.position.lerpVectors(ball.userData.start,ball.userData.end,t);
 ball.position.y=.65+Math.sin(t*Math.PI)*2.0;
 if(t>=1){
   ball.userData.moving=false; ball.position.y=.65;
   const near=[...home,...away].sort((a,b)=>dist(a,ball)-dist(b,ball))[0];
   if(near && dist(near,ball)<3) ball.position.copy(near.position).add(new THREE.Vector3(0,.65,0));
 }
 if(Math.abs(ball.position.z)>40.5){
   const side=ball.position.z>0?1:0;
   score[side]++;document.getElementById('home').textContent=score[0];document.getElementById('away').textContent=score[1];
   toast(side===0?"GOAL! ⚽":"GOAL!");
   ball.position.set(0,.65,0);ball.userData.moving=false;
 }
}

function cameraFollow(dt){
 const target=new THREE.Vector3(controlled.position.x*.35,0,controlled.position.z+9);
 camera.position.lerp(new THREE.Vector3(target.x,24,target.z+20),Math.min(1,dt*3));
 camera.lookAt(controlled.position.x,0,controlled.position.z-7);
}
function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min((now-last)/1000,.04);last=now;
 if(running){
   elapsed+=dt;
   const mm=String(Math.floor(elapsed/60)).padStart(2,'0'),ss=String(Math.floor(elapsed%60)).padStart(2,'0');
   document.getElementById('clock').textContent=mm+":"+ss;
   updatePlayers(dt);updateBall(dt);cameraFollow(dt);
 }
 renderer.render(scene,camera);
}
animate(performance.now());

document.getElementById('startBtn').onclick=()=>{
 document.getElementById('start').style.display='none';
 running=true;
 setTimeout(()=>document.getElementById('help').classList.add('hide'),3200);
};

addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
</script>
</body>
</html>
"""

components.html(game, height=window_height if False else 900, scrolling=False)
