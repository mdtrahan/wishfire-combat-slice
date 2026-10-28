"""Gloamink generated paint cleanup, native parented Synfig rig and seven clips.
Run from any cwd: python3 source/prepare.py [--render]. No writes outside actor folder.
"""
from pathlib import Path
import json, math, hashlib, subprocess, sys, shutil
from PIL import Image, ImageFilter
S=Path(__file__).resolve().parent; A=S.parent
# name, atlas rectangle, world joint x/y, displayed w/h, local pivot x/y, parent
rows=[
 ('head',(0,0,452,474),(45,99,56,54),(.70,.84),'body'),
 ('neck',(82,472,334,728),(47,101,17,20),(.5,.3),'body'),
 ('torso',(410,130,805,466),(63,104,48,29),(.45,.45),'body'),
 ('tail_base',(740,95,1125,457),(78,95,32,24),(.12,.22),'body'),
 ('tail_tip',(1120,250,1448,461),(89,110,39,21),(.12,.45),'tail_base'),
 ('front_upper_near',(82,472,334,728),(41,107,13,17),(.50,.2),'body'),
 ('front_paw_near',(425,490,709,734),(36,117,17,15),(.7,.25),'front_upper_near'),
 ('front_upper_far',(800,470,1013,732),(45,106,13,20),(.5,.2),'body'),
 ('front_paw_far',(1150,485,1398,737),(35,119,19,17),(.7,.25),'front_upper_far'),
 ('rear_upper_near',(85,731,354,1057),(83,108,17,18),(.5,.2),'body'),
 ('rear_paw_near',(426,743,705,1068),(93,119,15,15),(.5,.25),'rear_upper_near'),
 ('rear_upper_far',(800,733,1048,1058),(70,106,15,17),(.5,.2),'body'),
 ('rear_paw_far',(1160,741,1407,1070),(68,116,14,15),(.5,.25),'rear_upper_far'),
]
parts={};atlas=Image.open(S/'parts-left-v1.png').convert('RGBA')
for name,box,comp,pivot,parent in rows:
 im=atlas.crop(box); alpha=im.getchannel('A'); alpha=alpha.point(lambda x:0 if x<12 else x);im.putalpha(alpha)
 # Keep the dominant connected paint island, preserving its antialiased edge.
 from collections import deque
 ww,hh=im.size;data=im.getchannel('A').tobytes();seen=bytearray(a>=24 for a in data);best=[]
 for first in range(ww*hh):
  if not seen[first]:continue
  seen[first]=0;todo=deque([first]);component=[]
  while todo:
   k=todo.popleft();yy,xx=divmod(k,ww);component.append(k)
   for j in ([k-1] if xx else [])+([k+1] if xx<ww-1 else [])+([k-ww] if yy else [])+([k+ww] if yy<hh-1 else []):
    if seen[j]:seen[j]=0;todo.append(j)
  if len(component)>len(best):best=component
 mb=bytearray(ww*hh)
 for k in best:mb[k]=255
 mask=Image.frombytes('L',im.size,bytes(mb)).filter(ImageFilter.MaxFilter(3))
 from PIL import ImageChops
 im.putalpha(ImageChops.multiply(im.getchannel('A'),mask))
 bb=im.getbbox();im=im.crop(bb);im.save(S/f'{name}.png')
 x,y,w,h=comp;px,py=pivot
 parts[name]={'file':name+'.png','crop':dict(zip(['x','y','width','height'],[box[0],box[1],box[2]-box[0],box[3]-box[1]])), 'sourceDimensions':dict(width=im.width,height=im.height),'pivot':dict(x=px*im.width,y=py*im.height),'composition':dict(x=x,y=y,w=w,h=h,pivotX=px,pivot=py,parent=parent)}
# Lower-leg paint is split with a generous shared overlap for articulated paws.
for name in list(parts):
 if '_paw_' not in name:continue
 part=parts[name];c=part['composition'];raw=Image.open(S/part['file']).convert('RGBA');w,h=raw.size
 shin=raw.crop((0,0,w,round(h*.68)));foot=raw.crop((0,round(h*.44),w,h))
 shin.save(S/part['file']);footname=name.replace('_paw_','_foot_');foot.save(S/f'{footname}.png')
 oldh=c['h'];oldpivot=c['pivot'];left=c['x']-c['w']*c['pivotX'];top=c['y']-oldh*oldpivot
 py=top+oldh*.70;px=c['x']-2
 fc=dict(x=px,y=py,w=c['w'],h=oldh*(h-round(h*.44))/h,pivotX=(px-left)/c['w'],pivot=(.70*h-round(h*.44))/(h-round(h*.44)),parent=name)
 parts[footname]=dict(file=footname+'.png',derivedFrom=name,sourceDimensions=dict(width=foot.width,height=foot.height),pivot=dict(x=foot.width*fc['pivotX'],y=foot.height*fc['pivot']),composition=fc)
 c['h']=oldh*shin.height/h;c['pivot']=oldh*oldpivot/c['h'];part['sourceDimensions']=dict(width=shin.width,height=shin.height);part['pivot']['y']=shin.height*c['pivot']
(S/'parts.json').write_text(json.dumps(dict(actor='gloamink',atlas='parts-left-v1.png',facing='left',sourceFacing='left',oppositeFacing='semantic horizontal mirror; costume reverses',parts=parts),indent=2)+'\n')
COUNTS=dict(idle=12,walk=12,attack=9,cast=12,hit=6,defeated=12,spawn=9)
v=lambda x,y:f'<vector><x>{x:.7f}</x><y>{y:.7f}</y></vector>'
p=lambda name,val:f'<param name="{name}">{val}</param>'
g=lambda name:hashlib.md5(('gloamink/'+name).encode()).hexdigest().upper()
def anim(kind,values):
 return f'<animated type="{kind}">'+''.join(f'<waypoint time="{i/12:.8f}s" before="linear" after="linear">'+(v(*val) if kind=='vector' else f'<angle value="{val:.7f}"/>')+'</waypoint>' for i,val in enumerate(values))+'</animated>'
def pose(state,i,n):
 t=i/(n-1) if n>1 else 0; phase=2*math.pi*i/12
 # Native bone-local deltas and paint scales. All distances are final canvas pixels.
 a={k:0. for k in parts};off={k:[0.,0.] for k in parts};sc={k:(1.,1.) for k in parts}
 dx=dy=rot=0
 # Lift near forepaw, plant far forepaw and separate the hind feet.
 a.update(front_upper_near=-20,front_paw_near=-40,front_upper_far=12,
          front_paw_far=0,rear_upper_near=-20,rear_paw_near=0,
          rear_upper_far=10,rear_paw_far=-10,tail_base=-4,tail_tip=4)
 if state=='idle':
  a['head']=math.sin(phase)*1.1;a['tail_base']+=math.sin(phase)*2;a['tail_tip']+=math.sin(phase-.6)*2
 elif state=='walk':
  # One twelve-frame transverse gallop. Contact -> drive -> flight -> gather -> reach.
  front=[-48,-32,-8,24,48,62,66,50,20,-20,-55,-65]
  rear =[38,60,64,42,2,-35,-62,-68,-46,-10,18,30]
  fk=[8,10,5,-12,-48,-76,-88,-82,-48,-8,12,10]
  rk=[-28,-38,-28,0,38,66,88,80,44,5,-20,-28]
  dy=[0,1,0,-3,-7,-10,-11,-9,-6,-3,-1,0][i]
  rot=[0,2,3,1,-2,-4,-3,0,3,4,2,0][i]
  for side,lag in [('near',0),('far',2)]:
   j=(i+lag)%12
   a['front_upper_'+side]=front[j];a['front_paw_'+side]=fk[j]
   a['rear_upper_'+side]=rear[j];a['rear_paw_'+side]=rk[j]
  a['head']=-8+3*math.sin(phase-.4)
  off['head']=[-1,3];a['tail_base']=-12+5*math.sin(phase-.8);a['tail_tip']=5*math.sin(phase-1.3)
  # Stretch only the torso; joint spacing follows the same 12% stride pulse.
  stretch=[1.08,1.10,1.08,1.02,.94,.89,.88,.91,.99,1.08,1.14,1.12][i]
  sc['torso']=(stretch,2-stretch)
  for name in parts:
   if name.startswith(('front_','rear_')) and '_upper_' in name:off[name][0]=(parts[name]['composition']['x']-63)*(stretch-1)
 elif state in ('attack','cast'):
  drive=([0,-.45,-1,.4,1,.92,.56,.15,0] if state=='attack' else [0,-.2,-.5,-1,-.7,.35,1,.92,.7,.4,.1,0])[i]
  l=max(0,drive);c=max(0,-drive);dx=-15*l+12*c;dy=-7*l+5*c;rot=-5*l+5*c
  off['head']=[-3*l+8*c, 5*l+3*c];a['head']=-14*l+10*c
  sc['torso']=(1+.12*l-.12*c,1-.08*l+.1*c)
  for side,factor in [('near',1),('far',.78)]:
   a['front_upper_'+side]=a['front_upper_'+side]*(1-max(l,c))-64*l*factor+32*c
   a['front_paw_'+side]=a['front_paw_'+side]*(1-max(l,c))+8*l-66*c
   a['rear_upper_'+side]=a['rear_upper_'+side]*(1-max(l,c))+52*l-38*c
   a['rear_paw_'+side]=a['rear_paw_'+side]*(1-max(l,c))-20*l+46*c
  a['tail_base']=-16*l+45*c;a['tail_tip']=5*l+50*c
 elif state=='hit':
  k=[0,1,.55,.15,-.1,0][i];dx=5*k;rot=9*k;a['head']=17*k;a['tail_base']=-12*k
  for side in ('near','far'):a['front_upper_'+side]+=16*k;a['front_paw_'+side]-=12*k
 elif state=='defeated':
  k=min(1,t/.7);k=k*k*(3-2*k);rot=12*k;dx=-2*k;dy=8*k
  # Roll rigid torso onto its side; splay the four limbs independently.
  off['front_paw_far']=[20*k*(1-k),-20*k*(1-k)]
  a['head']=-30*k;off['head']=[-2*k,9*k];a['tail_base']=-12*k;a['tail_tip']=12*k
  a['front_upper_near']=a['front_upper_near']*(1-k)+(-85)*k;a['front_paw_near']=a['front_paw_near']*(1-k)+(15)*k
  a['front_upper_far']=a['front_upper_far']*(1-k)+(65)*k;a['front_paw_far']=a['front_paw_far']*(1-k)+(25)*k
  a['rear_upper_near']=a['rear_upper_near']*(1-k)+(85)*k;a['rear_paw_near']=a['rear_paw_near']*(1-k)+(-10)*k
  a['rear_upper_far']=a['rear_upper_far']*(1-k)+(-55)*k;a['rear_paw_far']=a['rear_paw_far']*(1-k)+(-35)*k
 elif state=='spawn':
  k=[1,.8,.4,.05,-.2,-.1,0,0,0][i];dx=10*max(k,0);dy=-13*max(k,0)+3*min(k,0);rot=-9*k
  a['head']=7*k;a['tail_base']=14*k
  for side in ('near','far'):
   a['front_upper_'+side]+=-40*k;a['front_paw_'+side]+=30*k
   a['rear_upper_'+side]+=40*k;a['rear_paw_'+side]+=-30*k
 for name in parts:
  if '_foot_' in name:
   shin=name.replace('_foot_','_paw_');upper=name.replace('_foot_','_upper_')
   a[name]=-(a[upper]+a[shin])*(1.1 if state in ('idle','hit') else .8) if state!='defeated' else 0
 return dict(a=a,off=off,sc=sc,dx=dx,dy=dy,rot=rot)
# Painted order back to front: distant limbs behind torso, near limbs beneath pale mane.
order=['tail_tip','tail_base','rear_paw_far','rear_upper_far','front_paw_far','front_upper_far','neck','torso','rear_paw_near','rear_upper_near','front_paw_near','front_upper_near','head']
for name in list(order):
 if '_paw_' in name:order.insert(order.index(name),name.replace('_paw_','_foot_'))
def bone(name,parent,origins,angles):
 return f'<bone type="bone_object" guid="{g(name)}"><name><string>{name}</string></name><parent><bone_valuenode type="bone_object" guid="{g(parent)}"/></parent><origin>{anim("vector",origins)}</origin><angle>{anim("angle",angles)}</angle><scalelx><real value="1"/></scalelx><scalex><real value="1"/></scalex><width><real value=".1"/></width><tipwidth><real value=".1"/></tipwidth><bone_depth><real value="0"/></bone_depth><length><real value="1"/></length></bone>'
def transforms(pose):
 a=pose['a'];off=pose['off'];out={'body':(64+pose['dx'],103+pose['dy'],-pose['rot'])}
 def at(name):
  if name in out:return out[name]
  c=parts[name]['composition'];parent=c['parent'];px,py,pa=at(parent);q=parts[parent]['composition'] if parent!='body' else dict(x=64,y=103)
  r=math.radians(pa);lx=c['x']-q['x']+off[name][0];ly=c['y']-q['y']+off[name][1]
  out[name]=(px+lx*math.cos(r)-ly*math.sin(r),py+lx*math.sin(r)+ly*math.cos(r),pa-a[name]);return out[name]
 for name in parts:at(name)
 return out
# Cache sampled paint hulls; no per-frame disk reads.
hulls={}
for name,part in parts.items():
 c=part['composition'];im=Image.open(S/part['file']).getchannel('A').resize((max(1,round(c['w']*3)),max(1,round(c['h']*3))))
 hulls[name]=[((xx+.5)/im.width*c['w']-c['w']*c['pivotX'],(yy+.5)/im.height*c['h']-c['h']*c['pivot']) for yy in range(im.height) for xx in range(im.width) if im.getpixel((xx,yy))>=32]
def lowest(pose):
 tr=transforms(pose);bottom=-1e9;left=1e9;right=-1e9
 for name in parts:
  x,y,a=tr[name];r=math.radians(a);cs=math.cos(r);sn=math.sin(r);sx,sy=pose['sc'][name]
  for lx,ly in hulls[name]:
   lx*=sx;ly*=sy;bottom=max(bottom,y+lx*sn+ly*cs);xp=x+lx*cs-ly*sn;left=min(left,xp);right=max(right,xp)
 return bottom,left,right
pose_log={}
manifest=dict(sourceFacing='left',oppositeFacing='mirrored-source; asymmetric costume reverses sides',clips={})
for state,n in [('neutral',1),*COUNTS.items()]:
 poses=[pose('idle' if state=='neutral' else state,i,n) for i in range(n)]
 # Preserve designed flight arcs. Ground only planted/contact poses, never flatten the gallop.
 corrected=[]
 for i,ps in enumerate(poses):
  bottom,left,right=lowest(ps)
  if state not in ('walk','attack','cast','spawn'):ps['dy']+=124.2-bottom
  elif state=='walk':
   flight=[0,0,0,2,5,8,9,7,4,1,0,0][i];ps['dy']+=124.2-flight-bottom
  elif state in ('attack','cast'):
   ps['dy']+=min(0,124.2-bottom)
  elif state=='spawn':ps['dy']+=min(0,124.2-bottom) if i<5 else 124.2-bottom
  ps['dx']+=max(0,2-left)-max(0,right-126)
  corrected.append(ps)
 poses=corrected
 pose_log[state]=[dict(frame=i,**ps,world=transforms(ps)) for i,ps in enumerate(poses)]
 bones=bone('body','root',[(64+ps['dx'],128-(103+ps['dy'])) for ps in poses],[ps['rot'] for ps in poses])
 for name,part in parts.items():
  c=part['composition'];q=parts[c['parent']]['composition'] if c['parent']!='body' else dict(x=64,y=103)
  bones+=bone(name,c['parent'],[(c['x']-q['x']+ps['off'][name][0],q['y']-c['y']-ps['off'][name][1]) for ps in poses],[ps['a'][name] for ps in poses])
 layers=''
 for name in order:
  c=parts[name]['composition'];tr=f'<bone_link type="transformation"><bone><bone_valuenode type="bone_object" guid="{g(name)}"/></bone><base_value><composite type="transformation"><offset>{v(0,0)}</offset><angle><angle value="0"/></angle><skew_angle><angle value="0"/></skew_angle><scale>{anim("vector",[ps["sc"][name] for ps in poses])}</scale></composite></base_value><translate><bool value="true"/></translate><rotate><bool value="true"/></rotate><skew><bool value="true"/></skew><scale_x><bool value="true"/></scale_x><scale_y><bool value="true"/></scale_y></bone_link>'
  imp=p('amount','<real value="1"/>')+p('blend_method','<integer value="0"/>')+p('tl',v(-c['w']*c['pivotX'],c['h']*c['pivot']))+p('br',v(c['w']*(1-c['pivotX']),-c['h']*(1-c['pivot'])))+p('c','<integer value="1"/>')+p('filename',f'<string>{name}.png</string>')
  layers+=f'<layer type="group" version="0.2" desc="{name}">'+p('amount','<real value="1"/>')+p('blend_method','<integer value="0"/>')+p('origin',v(0,0))+p('transformation',tr)+p('canvas',f'<canvas><layer type="import" version="0.1">{imp}</layer></canvas>')+'</layer>'
 skeleton='<layer type="skeleton" active="true" exclude_from_rendering="true" version="0.1" desc="editable parented Gloamink bones">'+p('name','<string>Gloamink</string>')+p('bones','<static_list type="bone_object">'+''.join(f'<entry><bone type="bone_object" guid="{g(name)}"/></entry>' for name in ['body',*parts])+'</static_list>')+'</layer>'
 for face in ['left','right']:
  tr=f'<composite type="transformation"><offset>{v(128 if face=="right" else 0,0)}</offset><angle><angle value="0"/></angle><skew_angle><angle value="0"/></skew_angle><scale>{v(-1 if face=="right" else 1,1)}</scale></composite>'
  sif=f'<?xml version="1.0"?><canvas version="1.0" width="128" height="128" view-box="0 128 128 0" fps="12" begin-time="0f" end-time="{max(1,n)/12}s" bgcolor="0 0 0 0"><name>Gloamink {state} {face}</name><bones><bone_root type="bone_object" guid="{g("root")}"/>{bones}</bones>{skeleton}<layer type="group" version="0.2">'+p('amount','<real value="1"/>')+p('origin',v(0,0))+p('transformation',tr)+p('canvas',f'<canvas>{layers}</canvas>')+'</layer></canvas>'
  (S/f'{state}-{face}.sif').write_text(sif.replace('><','>\n<')+'\n')
  if state!='neutral':
   key=dict(attack='basic',hit='hurt',defeated='ko').get(state,state);manifest['clips'].setdefault(key,{})[face]=dict(source=f'gloamink/source/{state}-{face}.sif',frames=[f'gloamink/frames/{state}-{face}-{i:03}.png' for i in range(n)],frameHoldMs=[1000/12]*n,loop=state in ('idle','walk'),canvas=dict(width=128,height=128),footOrigin=dict(x=64,y=125))
 if '--render' in sys.argv and (not any(x.startswith('--only=') for x in sys.argv) or '--only='+state in sys.argv):
  raw=S/'render-work';raw.mkdir(exist_ok=True)
  cmd=['/opt/homebrew/bin/synfig',str(S/f'{state}-left.sif'),'-t','png','-w','1024','-h','1024','--begin-time','0f','--end-time',f'{(n-1)/12:.8f}s','--fps','12','-o',str(raw/'frame.png')]
  result=subprocess.run(cmd,capture_output=True,text=True)
  (S/'render.log').open('a').write(state+'\n'+result.stderr+'\n')
  if result.returncode:raise RuntimeError(result.stderr[-4000:])
  imgs=sorted(raw.glob('*.png'))
  if len(imgs)!=n:raise RuntimeError(f'{state}: expected {n}, found {imgs}')
  for i,file in enumerate(imgs):
   im=Image.open(file).convert('RGBA').resize((128,128),Image.Resampling.LANCZOS)
   # Clear invisible RGB for straight alpha consumers.
   pixels=list(im.getdata());im.putdata([(r,g,b,a) if a else (0,0,0,0) for r,g,b,a in pixels])
   target=S if state=='neutral' else A/'frames'
   suffix='' if state=='neutral' else f'-{i:03}'
   im.save(target/f'{state}-left{suffix}.png');im.transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(target/f'{state}-right{suffix}.png')
  shutil.rmtree(raw);print('rendered',state,n,flush=True)
(A/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

(S/'poses-r2.json').write_text(json.dumps(pose_log,indent=2)+'\n')
