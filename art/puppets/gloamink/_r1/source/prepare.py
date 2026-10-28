"""Gloamink generated paint cleanup, native parented Synfig rig and seven clips.
Run from any cwd: python3 source/prepare.py [--render]. No writes outside actor folder.
"""
from pathlib import Path
import json, math, hashlib, subprocess, sys, shutil
from PIL import Image, ImageFilter
S=Path(__file__).resolve().parent; A=S.parent
# name, atlas rectangle, world joint x/y, displayed w/h, local pivot x/y, parent
rows=[
 ('head',(0,0,452,474),(45,91.5,56,54),(.70,.84),'body'),
 ('torso',(410,130,805,466),(63,98,48,29),(.45,.45),'body'),
 ('tail_base',(740,95,1125,457),(83,89,27,29),(.15,.2),'body'),
 ('tail_tip',(1120,250,1448,461),(101,108,24,13),(.12,.45),'tail_base'),
 ('front_upper_near',(82,472,334,728),(44,104,13,18),(.50,.2),'body'),
 ('front_paw_near',(425,490,709,734),(41,110,18,20),(.7,.25),'front_upper_near'),
 ('front_upper_far',(800,470,1013,732),(40,102,13,18),(.5,.2),'body'),
 ('front_paw_far',(1150,485,1398,737),(34,106,16,14),(.7,.25),'front_upper_far'),
 ('rear_upper_near',(85,731,354,1057),(79,105,18,17),(.5,.2),'body'),
 ('rear_paw_near',(426,743,705,1068),(84,113,15,17),(.5,.25),'rear_upper_near'),
 ('rear_upper_far',(800,733,1048,1058),(73,103,17,18),(.5,.2),'body'),
 ('rear_paw_far',(1160,741,1407,1070),(70,111,15,14),(.5,.25),'rear_upper_far'),
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
 angle={k:0. for k in parts}; dx=dy=rot=0
 if state=='idle':
  angle['head']=math.sin(phase)*1.1;angle['tail_base']=math.sin(phase)*2;angle['tail_tip']=math.sin(phase-.6)*3
 elif state=='walk':
  # Two low gallop strides per second. Rear limbs drive before front catch.
  q=phase*2;dy=-1.5*(1-math.cos(q*2))/2
  for side,offset in [('near',0),('far',1.1)]:
   angle['front_upper_'+side]=23*math.sin(q+offset)
   angle['front_paw_'+side]=-15*math.sin(q+offset)-8*max(0,math.cos(q+offset))
   angle['rear_upper_'+side]=-25*math.sin(q+offset+.8)
   angle['rear_paw_'+side]=18*math.sin(q+offset+.8)
  angle['head']=-2+2*math.sin(q-.3);angle['tail_base']=7*math.sin(q-.7);angle['tail_tip']=9*math.sin(q-1.4)
 elif state in ('attack','cast'):
  # Anticipate -> stretched bite/claw -> recoil. Cast is an alternate stalking pounce.
  drive=([0,-.18,-.3,.35,1,.85,.40,.12,0] if state=='attack' else [0,-.1,-.2,-.28,-.3,.2,.85,1,.8,.4,.12,0])[i]
  l=max(0,drive);dx=-5*drive;dy=-4*l;rot=-5*l
  angle['head']=-9*drive;angle['front_upper_near']=-42*drive;angle['front_paw_near']=21*drive
  angle['front_upper_far']=-26*drive;angle['front_paw_far']=12*drive
  angle['rear_upper_near']=24*drive;angle['rear_paw_near']=-20*drive
  angle['rear_upper_far']=18*drive;angle['rear_paw_far']=-15*drive
  angle['tail_base']=12*drive;angle['tail_tip']=-10*drive
 elif state=='hit':
  k=[0,1,.55,.15,-.1,0][i];dx=4*k;rot=7*k;angle['head']=13*k;angle['tail_base']=-9*k
  for side in ('near','far'):angle['front_upper_'+side]=9*k;angle['front_paw_'+side]=-8*k
 elif state=='defeated':
  k=min(1,t/.64);k=k*k*(3-2*k);rot=18*k;dx=-4*k;dy=12*k
  angle['head']=50*k;angle['tail_base']=-10*k;angle['tail_tip']=-8*k
  for side in ('near','far'):
   angle['front_upper_'+side]=-35*k;angle['front_paw_'+side]=48*k
   angle['rear_upper_'+side]=35*k;angle['rear_paw_'+side]=-35*k
 elif state=='spawn':
  k=[1,.8,.4,.05,-.2,-.1,0,0,0][i];dx=12*max(k,0);dy=-11*max(k,0)+2*min(k,0);rot=-7*k
  angle['head']=7*k;angle['tail_base']=18*k
  for side in ('near','far'):
   angle['front_upper_'+side]=-25*k;angle['front_paw_'+side]=20*k
   angle['rear_upper_'+side]=25*k;angle['rear_paw_'+side]=-20*k
 for name in parts:
  if '_foot_' in name:
   shin=name.replace('_foot_','_paw_');upper=name.replace('_foot_','_upper_')
   angle[name]=-(angle[upper]+angle[shin])*.65 if state in ('walk','attack','cast','spawn') else 0
 return angle,dx,dy,rot
# Painted order back to front: distant limbs behind torso, near limbs beneath pale mane.
order=['tail_tip','tail_base','rear_paw_far','rear_upper_far','front_paw_far','front_upper_far','torso','rear_paw_near','rear_upper_near','front_paw_near','front_upper_near','head']
for name in list(order):
 if '_paw_' in name:order.insert(order.index(name),name.replace('_paw_','_foot_'))
def bone(name,parent,origins,angles):
 return f'<bone type="bone_object" guid="{g(name)}"><name><string>{name}</string></name><parent><bone_valuenode type="bone_object" guid="{g(parent)}"/></parent><origin>{anim("vector",origins)}</origin><angle>{anim("angle",angles)}</angle><scalelx><real value="1"/></scalelx><scalex><real value="1"/></scalex><width><real value=".1"/></width><tipwidth><real value=".1"/></tipwidth><bone_depth><real value="0"/></bone_depth><length><real value="1"/></length></bone>'
def lowest(angles,dx,dy,rot):
 # Use painted alpha hulls, transformed through the same native hierarchy, to anchor ground.
 transforms={'body':(64+dx,103+dy,-rot)}
 def at(name):
  if name in transforms:return transforms[name]
  c=parts[name]['composition'];parent=c['parent'];px,py,pa=at(parent);q=parts[parent]['composition'] if parent!='body' else dict(x=64,y=103)
  r=math.radians(pa);lx=c['x']-q['x'];ly=c['y']-q['y'];out=(px+lx*math.cos(r)-ly*math.sin(r),py+lx*math.sin(r)+ly*math.cos(r),pa-angles[name]);transforms[name]=out;return out
 bottom=-1e9;left=1e9;right=-1e9
 for name in parts:
  c=parts[name]['composition'];im=Image.open(S/parts[name]['file']).getchannel('A');im=im.resize((max(1,round(c['w']*4)),max(1,round(c['h']*4))))
  x,y,a=at(name);r=math.radians(a);pix=im.load()
  for yy in range(im.height):
   for xx in range(im.width):
    if pix[xx,yy]<48:continue
    lx=(xx+.5)/im.width*c['w']-c['w']*c['pivotX'];ly=(yy+.5)/im.height*c['h']-c['h']*c['pivot']
    bottom=max(bottom,y+lx*math.sin(r)+ly*math.cos(r));xp=x+lx*math.cos(r)-ly*math.sin(r);left=min(left,xp);right=max(right,xp)
 return bottom,left,right
manifest=dict(sourceFacing='left',oppositeFacing='mirrored-source; asymmetric costume reverses sides',clips={})
for state,n in [('neutral',1),*COUNTS.items()]:
 poses=[pose('idle' if state=='neutral' else state,i,n) for i in range(n)]
 # Keep ground at 124.5 while allowing explicit airborne pounce/spawn frames.
 corrected=[]
 for i,(angles,dx,dy,rot) in enumerate(poses):
  if state not in ('attack','cast','spawn'):dy+=124.5-lowest(angles,dx,dy,rot)[0]
  elif state=='spawn' and i>=5:dy+=124.5-lowest(angles,dx,dy,rot)[0]
  _,left,right=lowest(angles,dx,dy,rot)
  dx+=max(0,2-left)-max(0,right-126)
  corrected.append((angles,dx,dy,rot))
 poses=corrected
 bones=bone('body','root',[(64+dx,128-(103+dy)) for a,dx,dy,r in poses],[r for a,x,y,r in poses])
 for name,part in parts.items():
  c=part['composition'];q=parts[c['parent']]['composition'] if c['parent']!='body' else dict(x=64,y=103)
  bones+=bone(name,c['parent'],[(c['x']-q['x'],q['y']-c['y'])]*n,[a[name] for a,x,y,r in poses])
 layers=''
 for name in order:
  c=parts[name]['composition'];tr=f'<bone_link type="transformation"><bone><bone_valuenode type="bone_object" guid="{g(name)}"/></bone><base_value><composite type="transformation"><offset>{v(0,0)}</offset><angle><angle value="0"/></angle><skew_angle><angle value="0"/></skew_angle><scale>{v(1,1)}</scale></composite></base_value><translate><bool value="true"/></translate><rotate><bool value="true"/></rotate><skew><bool value="true"/></skew><scale_x><bool value="true"/></scale_x><scale_y><bool value="true"/></scale_y></bone_link>'
  imp=p('amount','<real value="1"/>')+p('blend_method','<integer value="0"/>')+p('tl',v(-c['w']*c['pivotX'],c['h']*c['pivot']))+p('br',v(c['w']*(1-c['pivotX']),-c['h']*(1-c['pivot'])))+p('c','<integer value="1"/>')+p('filename',f'<string>{name}.png</string>')
  layers+=f'<layer type="group" version="0.2" desc="{name}">'+p('amount','<real value="1"/>')+p('blend_method','<integer value="0"/>')+p('origin',v(0,0))+p('transformation',tr)+p('canvas',f'<canvas><layer type="import" version="0.1">{imp}</layer></canvas>')+'</layer>'
 skeleton='<layer type="skeleton" active="true" exclude_from_rendering="true" version="0.1" desc="editable parented Gloamink bones">'+p('name','<string>Gloamink</string>')+p('bones','<static_list type="bone_object">'+''.join(f'<entry><bone type="bone_object" guid="{g(name)}"/></entry>' for name in ['body',*parts])+'</static_list>')+'</layer>'
 for face in ['left','right']:
  squash=[1-.52*min(1,(i/(n-1))/.64)**2*(3-2*min(1,(i/(n-1))/.64)) for i in range(n)] if state=='defeated' else [1]*n
  tr=f'<composite type="transformation"><offset>{anim("vector",[(128 if face=="right" else 0,3*(1-k)) for k in squash])}</offset><angle><angle value="0"/></angle><skew_angle><angle value="0"/></skew_angle><scale>{anim("vector",[(-1 if face=="right" else 1,k) for k in squash])}</scale></composite>'
  sif=f'<?xml version="1.0"?><canvas version="1.0" width="128" height="128" view-box="0 128 128 0" fps="12" begin-time="0f" end-time="{max(1,n)/12}s" bgcolor="0 0 0 0"><name>Gloamink {state} {face}</name><bones><bone_root type="bone_object" guid="{g("root")}"/>{bones}</bones>{skeleton}<layer type="group" version="0.2">'+p('amount','<real value="1"/>')+p('origin',v(0,0))+p('transformation',tr)+p('canvas',f'<canvas>{layers}</canvas>')+'</layer></canvas>'
  (S/f'{state}-{face}.sif').write_text(sif.replace('><','>\n<')+'\n')
  if state!='neutral':
   key=dict(attack='basic',hit='hurt',defeated='ko').get(state,state);manifest['clips'].setdefault(key,{})[face]=dict(source=f'gloamink/source/{state}-{face}.sif',frames=[f'gloamink/frames/{state}-{face}-{i:03}.png' for i in range(n)],frameHoldMs=[1000/12]*n,loop=state in ('idle','walk'),canvas=dict(width=128,height=128),footOrigin=dict(x=64,y=125))
 if '--render' in sys.argv:
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
