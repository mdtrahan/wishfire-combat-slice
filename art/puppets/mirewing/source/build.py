"""Approved-pixel cutouts with generated hidden underpaint; native Synfig bone animation."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFilter
import json, math, hashlib, subprocess, shutil, concurrent.futures
S=Path(__file__).resolve().parent; A=S.parent; Q=A/'qa'; F=A/'frames'
REF=A.parents[1]/'_work/enemy-identities/new'
GEN=Path('/Users/Mace/.codex/generated_images/01a18108-c7ae-7b41-ab3f-fd44b2260837/exec-74db0ea8-da78-42ab-a808-35fdea6de7c4.png')
COUNTS=dict(idle=12,walk=12,attack=9,cast=12,hit=6,defeated=12,spawn=9)
v=lambda x,y:f'<vector><x>{x:.6f}</x><y>{y:.6f}</y></vector>'
p=lambda n,x:f'<param name="{n}">{x}</param>'
g=lambda n:hashlib.md5(('mirewing/'+n).encode()).hexdigest().upper()
def anim(kind,values):
 def value(a): return v(*a) if kind=='vector' else f'<{kind} value="{a:.6f}"/>'
 return f'<animated type="{kind}">'+''.join(f'<waypoint time="{i/12:.8f}s" before="linear" after="linear">{value(a)}</waypoint>' for i,a in enumerate(values))+'</animated>'
def prepare():
 shutil.copy2(GEN,S/'generated-parts-atlas.png'); shutil.copy2(REF/'mirewing-source.png',S/'approved-source.png');shutil.copy2(REF/'mirewing-128.png',S/'approved-128.png')
 im=Image.open(S/'approved-source.png').convert('RGBA'); im.putalpha(im.getchannel('A').point(lambda a:0 if a<12 else a)); size=im.size
 def poly(points):
  m=Image.new('L',size);ImageDraw.Draw(m).polygon(points,fill=255);return m
 masks={}
 # Trace the visible body contour first; wings own every remaining source pixel.
 bodymask=poly([(318,426),(360,408),(421,398),(474,399),(528,412),(573,417),(607,437),(612,448),(685,466),(669,490),(641,500),(681,519),(729,540),(713,562),(696,578),(724,608),(701,626),(686,642),(718,661),(756,686),(720,701),(733,721),(696,734),(673,724),(668,747),(707,760),(746,800),(775,852),(766,904),(752,941),(761,984),(723,1003),(704,1021),(675,1034),(679,1064),(671,1090),(663,1114),(646,1168),(613,1156),(597,1130),(594,1093),(611,1041),(563,1033),(552,1061),(545,1109),(566,1147),(544,1151),(511,1136),(487,1105),(478,1076),(500,1030),(456,1017),(414,1012),(394,995),(390,949),(413,916),(388,898),(355,886),(315,868),(320,847),(245,851),(217,817),(202,795),(123,798),(118,725),(132,696),(170,687),(189,681),(201,646),(196,602),(189,569),(201,529),(221,491),(248,471),(276,450)])
 antenna_far=poly([(302,466),(280,422),(276,365),(282,317),(305,285),(343,254),(350,289),(414,244),(471,208),(475,224),(451,268),(422,297),(416,327),(388,350),(349,371),(329,409),(323,447)])
 antenna_near=poly([(428,491),(451,426),(471,386),(495,350),(540,313),(539,343),(615,296),(649,279),(660,282),(661,311),(670,325),(654,349),(658,367),(637,388),(609,410),(574,428),(537,436),(498,465),(477,489)])
 bodymask=ImageChops.lighter(bodymask,ImageChops.lighter(antenna_far,antenna_near))
 wings=ImageChops.invert(bodymask)
 farzone=poly([(400,160),(700,155),(787,377),(711,548),(491,500)])
 masks['wing_far']=ImageChops.multiply(wings,farzone)
 masks['wing_near']=ImageChops.subtract(wings,masks['wing_far'])
 masks['gland_near']=poly([(318,752),(328,707),(365,669),(417,649),(474,648),(526,676),(562,719),(576,770),(563,814),(525,847),(471,864),(415,861),(365,837),(333,799)])
 masks['gland_far']=poly([(214,733),(246,726),(285,737),(315,763),(336,811),(314,839),(280,849),(243,837),(223,811)])
 masks['mouth']=poly([(124,730),(133,699),(168,686),(199,693),(229,682),(254,677),(270,689),(280,707),(265,724),(229,742),(207,762),(190,789),(164,796),(140,781),(125,755)])
 # Ownership masks partition approved visible pixels. Original palette/face retained exactly.
 whole=Image.new('L',size,255);ImageDraw.Draw(whole).rectangle((0,1165,1254,1254),fill=0)
 occupied=Image.new('L',size)
 for n in masks:
  masks[n]=ImageChops.multiply(ImageChops.subtract(masks[n],occupied),whole);occupied=ImageChops.lighter(occupied,masks[n])
 # Tiny contour fragments belong to the body, never to a flapping wing.
 from collections import deque
 for name in ['wing_far','wing_near']:
  occupied_alpha=ImageChops.multiply(masks[name],im.getchannel('A'))
  bw=occupied_alpha.point(lambda a:255 if a>8 else 0); pix=bw.load();visited=set();components=[]
  for yy in range(size[1]):
   for xx in range(size[0]):
    if not pix[xx,yy] or (xx,yy) in visited:continue
    queue=deque([(xx,yy)]);visited.add((xx,yy));comp=[]
    while queue:
     x,y=queue.popleft();comp.append((x,y))
     for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
      if 0<=nx<size[0] and 0<=ny<size[1] and pix[nx,ny] and (nx,ny) not in visited:visited.add((nx,ny));queue.append((nx,ny))
    components.append(comp)
  keep=Image.new('L',size);kp=keep.load()
  for x,y in max(components,key=len):kp[x,y]=255
  keep=keep.filter(ImageFilter.MaxFilter(3));masks[name]=ImageChops.multiply(masks[name],keep)
 occupied=Image.new('L',size)
 for mask in masks.values():occupied=ImageChops.lighter(occupied,mask)
 masks['body_paint']=ImageChops.subtract(whole,occupied)
 spec={
 'shadow':(128,250,0.5,0.5,'root'),
 'body_paint':(115,145,None,None,'body'),
 'wing_far':(124,104,None,None,'body'),
 'wing_near':(134,144,None,None,'body'),
 'gland_far':(59,154,None,None,'body'),
 'gland_near':(89,149,None,None,'body'),
 'mouth':(55,141,None,None,'body')}
 parts={}
 for n in ['body_paint','wing_far','wing_near','gland_far','gland_near','mouth']:
  cut=im.copy();cut.putalpha(ImageChops.multiply(im.getchannel('A'),masks[n]));box=cut.getbbox();cut=cut.crop(box)
  # Tiny overlapped underpaint closes mouth/gland attachment exposure during pulse.
  cut.save(S/f'{n}.png');x,y,_,_,parent=spec[n];w=(box[2]-box[0])*.176;h=(box[3]-box[1])*.176
  px=(x-(10+box[0]*.176))/w;py=(y-(16+box[1]*.176))/h
  parts[n]=dict(file=f'{n}.png',crop=dict(x=box[0],y=box[1],width=cut.width,height=cut.height),sourceDimensions=dict(width=cut.width,height=cut.height),pivot=dict(x=px*cut.width,y=py*cut.height),composition=dict(x=x,y=y,w=w,h=h,pivotX=px,pivot=py,parent=parent),paint='approved source pixels; generated atlas retained for hidden attachment underpaint')
 # Generated head underpaint fills attachment holes only and is covered in the rest pose.
 gen=Image.open(S/'generated-parts-atlas.png').convert('RGBA')
 patch=gen.crop((165,390,290,480)).resize((180,130),Image.Resampling.LANCZOS)
 # Elliptical interior patch avoids generated background and never changes face/outline.
 alpha=Image.new('L',patch.size);ImageDraw.Draw(alpha).ellipse((10,10,170,120),fill=255);patch.putalpha(alpha);patch.save(S/'attachment_underpaint.png')
 parts['attachment_underpaint']=dict(file='attachment_underpaint.png',sourceDimensions=dict(width=180,height=130),pivot=dict(x=90,y=65),composition=dict(x=79,y=150,w=33,h=24,pivotX=.5,pivot=.5,parent='body'),paint='generated matching teal hidden tissue; Pillow alpha cleanup')
 sh=im.crop((450,1171,785,1224));sh.save(S/'shadow.png');parts['shadow']=dict(file='shadow.png',sourceDimensions=dict(width=sh.width,height=sh.height),pivot=dict(x=sh.width/2,y=sh.height/2),composition=dict(x=128,y=250,w=62,h=8,pivotX=.5,pivot=.5,parent='root'))
 meta=dict(actor='mirewing',atlas='approved-source.png',facing='left',sourceFacing='left',oppositeFacing='semantic horizontal mirror; asymmetry reverses',nativeCanvas=dict(width=256,height=256),footOrigin=dict(x=128,y=250),parts=parts)
 (S/'parts.json').write_text(json.dumps(meta,indent=2)+'\n');return parts

def poses(state,n):
 result=[]
 for i in range(n+1):
  t=i/n;wave=math.sin(2*math.pi*t);flap=math.sin(2*math.pi*(3 if state=='walk' else 2)*t)
  pose=dict(x=115,y=111+2.8*wave,angle=0,wing=flap*6,wingScale=.83+.17*math.cos(2*math.pi*(3 if state=='walk' else 2)*t),pulse=1,mouth=0,shadow=1)
  if state=='idle':pose['wingScale']=.84+.16*math.cos(4*math.pi*t)
  if state=='walk':pose.update(x=113+1.7*wave,angle=5,wing=flap*9)
  if state=='attack':
   swell=math.sin(math.pi*min(t/.55,1)) if t<.55 else 0
   thrust=max(0,1-abs(t-.55)/.22)
   pose.update(pulse=1+.12*swell,mouth=thrust*8,x=115+2*swell-3*thrust,angle=-3*thrust)
  if state=='cast':pose.update(pulse=1+.23*math.sin(math.pi*t)**2,mouth=3*math.sin(math.pi*t)**2,angle=-2*math.sin(math.pi*t))
  if state=='hit':
   recoil=math.sin(math.pi*min(t/.65,1)) if t<.65 else 0
   pose.update(x=115+12*recoil,angle=-10*recoil)
  if state=='spawn':pose['y']+=8*(1-t)**2;pose['wing']=flap*6
  if state=='defeated':
   fall=min(1,max(0,(t-.15)/.65));ease=fall*fall*(3-2*fall)
   pose.update(y=111-26*ease+2.8*wave*(1-ease),angle=-3*ease,wing=flap*6*(1-ease)+25*ease,wingScale=(.83+.17*math.cos(4*math.pi*t))*(1-ease)+.22*ease)
  result.append(pose)
 return result

def build_sif(state,n,face,parts):
 poseset=poses(state,n);root=g('root');body=g('body');bones=''
 def bone(name,parent,origins,angles):
  return f'<bone type="bone_object" guid="{g(name)}"><name><string>{name}</string></name><parent><bone_valuenode type="bone_object" guid="{g(parent)}"/></parent><origin>{anim("vector",origins)}</origin><angle>{anim("angle",angles)}</angle><scalelx><real value="1"/></scalelx><scalex><real value="1"/></scalex><width><real value=".1"/></width><tipwidth><real value=".1"/></tipwidth><bone_depth><real value="0"/></bone_depth><length><real value="1"/></length></bone>'
 bones+=bone('body','root',[(a['x'],a['y']) for a in poseset],[a['angle'] for a in poseset])
 for name,part in parts.items():
  c=part['composition'];parent=c['parent'];ox=115 if parent=='body' else 0;oy=145 if parent=='body' else 256
  angles=[a['wing']*(.7 if name=='wing_far' else 1) if name.startswith('wing') else 0 for a in poseset]
  origins=[(c['x']-ox,oy-c['y']) for a in poseset]
  bones+=bone(name,parent,origins,angles)
 order=['shadow','wing_far','wing_near','attachment_underpaint','body_paint','gland_far','gland_near','mouth'];layers=''
 for name in order:
  c=parts[name]['composition'];scales=[]
  for a in poseset:
   if name.startswith('wing'):scales.append((a['wingScale'],1))
   elif name.startswith('gland'):scales.append((a['pulse'],a['pulse']))
   elif name=='mouth':scales.append((1+a['mouth']*.08,1))
   else:scales.append((1,1))
  base=f'<composite type="transformation"><offset>{v(0,0)}</offset><angle><angle value="0"/></angle><skew_angle><angle value="0"/></skew_angle><scale>{anim("vector",scales)}</scale></composite>'
  tr=f'<bone_link type="transformation"><bone><bone_valuenode type="bone_object" guid="{g(name)}"/></bone><base_value>{base}</base_value>'+''.join(f'<{x}><bool value="true"/></{x}>' for x in ['translate','rotate','skew','scale_x','scale_y'])+'</bone_link>'
  imp=p('amount','<real value="1"/>')+p('blend_method','<integer value="0"/>')+p('tl',v(-c['w']*c['pivotX'],c['h']*c['pivot']))+p('br',v(c['w']*(1-c['pivotX']),-c['h']*(1-c['pivot'])))+p('c','<integer value="1"/>')+p('filename',f'<string>{parts[name]["file"]}</string>')
  layers+=f'<layer type="group" version="0.2" desc="{name}">'+p('amount','<real value="1"/>')+p('blend_method','<integer value="0"/>')+p('origin',v(0,0))+p('transformation',tr)+p('canvas',f'<canvas><layer type="import" version="0.1">{imp}</layer></canvas>')+'</layer>'
 skeleton='<layer type="skeleton" active="true" exclude_from_rendering="true" version="0.1" desc="editable parented bones">'+p('name','<string>Mirewing flight skeleton</string>')+p('bones','<static_list type="bone_object">'+''.join(f'<entry><bone type="bone_object" guid="{g(x)}"/></entry>' for x in ['body',*parts])+'</static_list>')+'</layer>'
 tr=f'<composite type="transformation"><offset>{v(256 if face=="right" else 0,0)}</offset><angle><angle value="0"/></angle><skew_angle><angle value="0"/></skew_angle><scale>{v(-1 if face=="right" else 1,1)}</scale></composite>'
 return f'<?xml version="1.0"?><canvas version="1.0" width="256" height="256" view-box="0 256 256 0" fps="12" begin-time="0f" end-time="{n/12}s" bgcolor="0 0 0 0"><name>Mirewing {state} {face}</name><bones><bone_root type="bone_object" guid="{root}"/>{bones}</bones>{skeleton}<layer type="group" version="0.2" desc="semantic facing">'+p('amount','<real value="1"/>')+p('origin',v(0,0))+p('transformation',tr)+p('canvas',f'<canvas>{layers}</canvas>')+'</layer></canvas>'
def render(job):
 state,i=job;out=S/'renders'/f'{state}-{i:03}.png';out.parent.mkdir(exist_ok=True)
 cmd=['/opt/homebrew/bin/synfig',str(S/f'{state}-left.sif'),'-t','png','-w','1024','-h','1024','--time',f'{i}f','-o',str(out)]
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if r.returncode:raise RuntimeError(r.stderr.decode()[-2500:])
 im=Image.open(out).convert('RGBA');im=im.resize((128,128),Image.Resampling.LANCZOS);im.save(F/f'{state}-left-{i:03}.png');im.transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(F/f'{state}-right-{i:03}.png')
 return state,i
if __name__=='__main__':
 import sys
 parts=prepare();manifest=dict(sourceFacing='left',oppositeFacing='semantic horizontal mirror; asymmetric markings reverse sides',clips={})
 for state,n in COUNTS.items():
  for face in ['left','right']:
   (S/f'{state}-{face}.sif').write_text(build_sif(state,n,face,parts).replace('><','>\n<')+'\n')
   key=dict(attack='basic',hit='hurt',defeated='ko').get(state,state);manifest['clips'].setdefault(key,{})[face]=dict(source=f'mirewing/source/{state}-{face}.sif',frames=[f'mirewing/frames/{state}-{face}-{i:03}.png' for i in range(n)],frameHoldMs=[1000/12]*n,loop=state in ['idle','walk'],canvas=dict(width=128,height=128),footOrigin=dict(x=64,y=125))
 for face in ['left','right']:(S/f'neutral-{face}.sif').write_text(build_sif('idle',12,face,parts).replace('><','>\n<')+'\n')
 (A/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 if '--sources-only' not in sys.argv:
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
   for state,i in pool.map(render,[(s,i) for s,n in COUNTS.items() for i in range(n)]):print(state,i,flush=True)
