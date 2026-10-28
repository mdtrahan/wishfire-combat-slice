"""Fizzmite: generated painted cutouts -> parented native Synfig -> Lanczos RGBA."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, math, hashlib, subprocess, argparse, shutil
import numpy as np
S=Path(__file__).resolve().parent; A=S.parent; Q=A/'qa'; F=A/'frames'
COUNTS=dict(idle=12,walk=12,attack=9,cast=12,hit=6,defeated=12,spawn=9)
SYNFIG='/opt/homebrew/bin/synfig'
# name, atlas crop, native (pivot x,y,width,height,normalized pivot x,y), parent
ROWS=[
 ('underbody',(1044,146,1536,487),(117,207,110,56,.5,.5),'body'),
 ('shell',(542,5,1031,490),(172,155,128,146,.5,.5),'body'),
 ('head',(10,14,538,474),(82,160,118,110,.5,.5),'body'),
 ('fuse',(156,746,477,1008),(179,81,36,37,.22,.92),'shell'),
 ('flame',(615,743,959,997),(204,50,29,27,.17,.86),'fuse'),
 ('leg_front_far',(141,487,350,711),(91,238,23,28,.5,.95),'body'),
 ('leg_mid_far',(1190,744,1453,995),(141,235,24,29,.5,.95),'body'),
 ('leg_rear_far',(1190,499,1449,723),(201,233,25,28,.5,.95),'body'),
 ('leg_front_near',(141,487,350,711),(80,242,28,32,.5,.95),'body'),
 ('leg_mid_near',(677,496,865,725),(153,248,30,38,.5,.95),'body'),
 ('leg_rear_near',(1190,499,1449,723),(218,243,31,32,.5,.95),'body')]

def prepare():
 atlas=Image.open(S/'parts-left-v1.png').convert('RGBA'); parts={}
 for name,box,c,parent in ROWS:
  im=atlas.crop(box); ar=np.array(im); alpha=ar[:,:,3]; alpha[alpha<22]=0; alpha[alpha>215]=255; ar[:,:,3]=alpha; im=Image.fromarray(ar); im=im.crop(im.getchannel('A').getbbox())
  # Flame atlas includes detached sparks. Split these below; main flame remains a separate cutout.
  if name=='flame':
   # Painted flame occupies left two thirds of the cropped cell.
   im=im.crop((0,0,int(im.width*.69),im.height))
  if name=='head':
   # Preserve approved face pixels verbatim; generated atlas supplies occluded shell/body paint.
   src=Image.open(A.parent.parent/'_work/enemy-identities/new/fizzmite-source.png').convert('RGBA')
   mask=Image.new('L',src.size); ImageDraw.Draw(mask).polygon([(146,820),(169,753),(215,590),(240,626),(295,514),(521,441),(511,492),(571,488),(656,516),(694,564),(705,610),(736,665),(723,721),(700,745),(724,791),(706,839),(677,860),(643,882),(608,899),(587,884),(577,844),(576,875),(550,913),(503,941),(453,950),(402,943),(373,936),(331,963),(313,991),(280,981),(260,951),(258,929),(234,937),(213,959),(180,950),(158,929),(146,902)],fill=255)
   ar=np.array(src); ar[:,:,3]=np.minimum(ar[:,:,3],np.array(mask)); im=Image.fromarray(ar); im=im.crop(im.getchannel('A').getbbox())
  im.save(S/f'{name}.png'); x,y,w,h,px,py=c
  parts[name]=dict(file=f'{name}.png',crop=dict(x=box[0],y=box[1],width=box[2]-box[0],height=box[3]-box[1]),sourceDimensions=dict(width=im.width,height=im.height),pivot=dict(x=im.width*px,y=im.height*py),composition=dict(x=x,y=y,w=w,h=h,pivotX=px,pivot=py,parent=parent))
 # Three independent sparks lifted from original approved source, keeping the source flame colour.
 concept=Image.open(A.parent.parent/'_work/enemy-identities/new/fizzmite-source.png').convert('RGBA')
 for i,box in enumerate([(1096,76,1145,128),(1098,137,1162,188),(1097,209,1142,247)]):
  im=concept.crop(box); im=im.crop(im.getchannel('A').getbbox()); name=f'spark_{i}'; im.save(S/f'{name}.png')
  x,y=[(237,22),(241,38),(237,54)][i]
  parts[name]=dict(file=f'{name}.png',sourceDimensions=dict(width=im.width,height=im.height),pivot=dict(x=im.width/2,y=im.height/2),composition=dict(x=x,y=y,w=5,h=6,pivotX=.5,pivot=.5,parent='flame'))
 (S/'parts.json').write_text(json.dumps(dict(actor='fizzmite',atlas='parts-left-v1.png',facing='left',sourceFacing='left',oppositeFacing='mirrored-source; asymmetric shell and buckle reverse sides',nativeCanvas=[256,256],nativeFootOrigin=[128,250],parts=parts),indent=2)+'\n')
 return parts

v=lambda x,y:f'<vector><x>{x:.7f}</x><y>{y:.7f}</y></vector>'
p=lambda n,x:f'<param name="{n}">{x}</param>'
g=lambda n:hashlib.md5(('fizzmite/'+n).encode()).hexdigest().upper()
def value(t,x):
 if t=='vector':return v(*x)
 return f'<{t} value="{x:.8f}"/>'
def anim(t,values):
 return f'<animated type="{t}">'+''.join(f'<waypoint time="{i/12:.8f}s" before="linear" after="linear">{value(t,x)}</waypoint>' for i,x in enumerate(values))+'</animated>'
def bone(name,parent,origins,angles):
 return f'<bone type="bone_object" guid="{g(name)}"><name><string>{name}</string></name><parent><bone_valuenode type="bone_object" guid="{g(parent)}"/></parent><origin>{anim("vector",origins)}</origin><angle>{anim("angle",angles)}</angle><scalelx><real value="1"/></scalelx><scalex><real value="1"/></scalex><width><real value=".1"/></width><tipwidth><real value=".1"/></tipwidth><bone_depth><real value="0"/></bone_depth><length><real value="1"/></length></bone>'

def pose(state,i,count):
 t=i/12; u=i/max(1,count-1); cyc=2*math.pi*t
 d=dict(body=(128,96,0),parts={},scales={},alpha={})
 bob=0
 if state=='idle':bob=.8*math.sin(cyc)
 if state=='walk':bob=2.4*abs(math.sin(cyc*2)); d['body']=(128,96+bob,0)
 if state in ('attack','cast'):
  pressure=u*u; shake=math.sin(i*2.7)*(0.4+2.3*u)
  d['body']=(128+shake,96,0)
  d['scales']['shell']=(1+.095*pressure,1+.11*pressure)
  d['parts']['head']=(-2*u,-1.5*u,3*u+shake*.6)
  d['scales']['flame']=(1.10+.38*u,1.12+.7*u)
 if state=='hit':
  pulse=[0,1,.6,-.25,.1,0][i]; d['body']=(128+5*pulse,96+2*pulse,0);d['parts']['head']=(2*pulse,1*pulse,-7*pulse)
 if state=='spawn':
  # Uncurl at a fixed ground point, no opacity pop or underground clipping.
  lift=[-5,0,8,12,9,5,2,0,0][i];d['body']=(128,96+lift,0);d['scales']['underbody']=(1, .75+.25*min(1,u*2));d['parts']['head']=(4*(1-u),-7*(1-u),-18*(1-u))
 if state=='defeated':
  # Flip the intact body, fold the fuse and settle the shell on the ground.
  a=[0,-10,-35,-75,-125,-165,-188,-178,-180,-180,-180,-180][i]
  y=[96,110,138,132,117,102,90,91,92,92,92,92][i]
  # Authored roll arc keeps the full silhouette inside the canvas.
  d['body']=([128,128,128,128,146,128,128,128,128,128,128,128][i],y,a)
  d['parts']['fuse']=(0,0,155*min(1,u*2.75))
  d['alpha']['flame']=max(0,1-i/2)
  for k in range(3):d['alpha'][f'spark_{k}']=max(0,1-i)
 if state=='idle':d['body']=(128,96+bob,0);d['parts']['head']=(0,0,.65*math.sin(cyc))
 for name,_,c,parent in ROWS:
  if not name.startswith('leg'):continue
  j=['front','mid','rear'].index(name.split('_')[1]); far=name.endswith('far');phase=cyc*2+j*2.094+(math.pi if far else 0)
  if state=='walk':
   lift=max(0,math.sin(phase))*7; dx=math.cos(phase)*4
   d['parts'][name]=(dx,lift-bob,math.sin(phase)*11)
  elif state=='defeated':d['parts'][name]=(0,0,0)
  else:
   # Exact native y counter-motion holds foot pivots in stationary states.
   d['parts'][name]=(128-d['body'][0],96-d['body'][1],0)
 if state!='defeated':
  flicker=[1,.86,1.13,.93,1.18,.88,1.05,.82,1.15,.96,1.1,.9][i%12]
  base=d['scales'].get('flame',(1,1));d['scales']['flame']=(base[0]*(2-flicker),base[1]*flicker)
  d['parts']['fuse']=(0,0,1.8*math.sin(cyc*3))
  d['parts']['flame']=(0,0,4*math.sin(cyc*4))
  for k in range(3):
   age=((i+k*3)%6)/6; d['parts'][f'spark_{k}']=(age*2,age*5,age*50);d['alpha'][f'spark_{k}']=1-age*.8
 return d

def make_sif(parts,state,face,count):
 poses=[pose(state,i,count) for i in range(count+1)] if state in ('idle','walk') else [pose(state,i,count) for i in range(count)]
 if state in ('idle','walk'):poses[-1]=poses[0]
 n=len(poses)
 bones=bone('body','root',[(d['body'][0],d['body'][1]) for d in poses],[d['body'][2] for d in poses])
 for name,a in parts.items():
  c=a['composition'];par=c['parent'];q=parts[par]['composition'] if par!='body' else dict(x=128,y=160)
  vals=[d['parts'].get(name,(0,0,0)) for d in poses]
  bones+=bone(name,par,[(c['x']-q['x']+z[0],q['y']-c['y']+z[1]) for z in vals],[z[2] for z in vals])
 # Synfig last layer is foremost. Six legs have separate pivots and parent links.
 order=['leg_rear_far','leg_mid_far','leg_front_far','shell','underbody','leg_rear_near','leg_mid_near','leg_front_near','head','fuse','flame','spark_0','spark_1','spark_2']
 layers=''
 for name in order:
  c=parts[name]['composition'];scale=anim('vector',[d['scales'].get(name,(1,1)) for d in poses]); opacity=anim('real',[d['alpha'].get(name,1) for d in poses])
  base=f'<composite type="transformation"><offset>{v(0,0)}</offset><angle><angle value="0"/></angle><skew_angle><angle value="0"/></skew_angle><scale>{scale}</scale></composite>'
  tr=f'<bone_link type="transformation"><bone><bone_valuenode type="bone_object" guid="{g(name)}"/></bone><base_value>{base}</base_value><translate><bool value="true"/></translate><rotate><bool value="true"/></rotate><skew><bool value="true"/></skew><scale_x><bool value="true"/></scale_x><scale_y><bool value="true"/></scale_y></bone_link>'
  imp=p('amount','<real value="1"/>')+p('blend_method','<integer value="0"/>')+p('tl',v(-c['w']*c['pivotX'],c['h']*c['pivot']))+p('br',v(c['w']*(1-c['pivotX']),-c['h']*(1-c['pivot'])))+p('c','<integer value="1"/>')+p('filename',f'<string>{name}.png</string>')
  layers+=f'<layer type="group" version="0.2" desc="{name}">'+p('amount',opacity)+p('blend_method','<integer value="0"/>')+p('origin',v(0,0))+p('transformation',tr)+p('canvas',f'<canvas><layer type="import" version="0.1">{imp}</layer></canvas>')+'</layer>'
 skeleton='<layer type="skeleton" active="true" exclude_from_rendering="true" version="0.1" desc="editable parented Fizzmite rig">'+p('name','<string>Fizzmite</string>')+p('bones','<static_list type="bone_object">'+''.join(f'<entry><bone type="bone_object" guid="{g(name)}"/></entry>' for name in ['body',*parts])+'</static_list>')+'</layer>'
 tr=f'<composite type="transformation"><offset>{v(256 if face=="right" else 0,0)}</offset><angle><angle value="0"/></angle><skew_angle><angle value="0"/></skew_angle><scale>{v(-1 if face=="right" else 1,1)}</scale></composite>'
 sif=f'<?xml version="1.0"?><canvas version="1.0" width="256" height="256" view-box="0 256 256 0" fps="12" begin-time="0f" end-time="{count/12}s" bgcolor="0 0 0 0"><name>Fizzmite {state} {face}</name><bones><bone_root type="bone_object" guid="{g("root")}"/>{bones}</bones>{skeleton}<layer type="group" version="0.2">'+p('amount','<real value="1"/>')+p('origin',v(0,0))+p('transformation',tr)+p('canvas',f'<canvas>{layers}</canvas>')+'</layer></canvas>'
 (S/f'{state}-{face}.sif').write_text(sif.replace('><','>\n<')+'\n')

def render(state,count):
 scratch=S/'renders';scratch.mkdir(exist_ok=True)
 cmd=[SYNFIG,str(S/f'{state}-left.sif'),'--begin-time','0f','--end-time',f'{(count-1)/12:.8f}s','--fps','12','-w','1024','-h','1024','-t','png','-o',str(scratch/'frame.png')]
 proc=subprocess.run(cmd,capture_output=True,text=True)
 if proc.returncode:raise RuntimeError(proc.stdout+'\n'+proc.stderr)
 files=sorted(scratch.glob('frame.*.png'));assert len(files)==count,(state,len(files),proc.stderr[-800:])
 for i,fn in enumerate(files):
  im=Image.open(fn).convert('RGBA').resize((128,128),Image.Resampling.LANCZOS)
  # Straight-alpha PNG, zero transparent RGB avoids downstream bleed.
  ar=np.array(im);ar[ar[:,:,3]<=4]=0;ar[ar[:,:,3]==0,:3]=0;im=Image.fromarray(ar)
  im.save(F/f'{state}-left-{i:03}.png');im.transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(F/f'{state}-right-{i:03}.png');fn.unlink()
  if state=='idle' and i==0:
   im.save(S/'neutral-left.png');im.transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(S/'neutral-right.png')
 print(state,'rendered',count,flush=True)

def qa():
 for state,count in COUNTS.items():
  # 6 columns; every frame repeated on each required background.
  rows=math.ceil(count/6); sheet=Image.new('RGB',(6*384,2*rows*410))
  draw=ImageDraw.Draw(sheet)
  for bgidx,bg in enumerate(['#d6c09a','#101116']):
   draw.rectangle((0,bgidx*rows*410,sheet.width,(bgidx+1)*rows*410),fill=bg)
   for i in range(count):
    im=Image.open(F/f'{state}-left-{i:03}.png').resize((384,384),Image.Resampling.NEAREST);x=i%6*384;y=(bgidx*rows+i//6)*410
    sheet.paste(im,(x,y),im);draw.text((x+8,y+387),f'{state} left {i:03}',fill='white' if bgidx else '#101116')
  sheet.save(Q/f'contact-{state}.png')
 concept=Image.open(A.parent.parent/'_work/enemy-identities/new/fizzmite-128.png').convert('RGBA')
 comp=Image.new('RGB',(768,820));draw=ImageDraw.Draw(comp)
 for j,bg in enumerate(['#d6c09a','#101116']):
  draw.rectangle((0,j*410,768,(j+1)*410),fill=bg)
  for i,im in enumerate([Image.open(F/'idle-left-000.png'),concept]):
   im=im.resize((384,384),Image.Resampling.NEAREST);comp.paste(im,(i*384,j*410),im);draw.text((i*384+8,j*410+388),'Puppet idle 0' if i==0 else 'Approved concept',fill='white' if j else '#101116')
 comp.save(Q/'vs-concept.png')
 small=Image.new('RGB',(7*92,2*100));draw=ImageDraw.Draw(small)
 for j,bg in enumerate(['#d6c09a','#101116']):
  draw.rectangle((0,j*100,small.width,(j+1)*100),fill=bg)
  for i,(state,n) in enumerate(COUNTS.items()):
   im=Image.open(F/f'{state}-left-{(n-1 if state=="defeated" else n//2):03}.png').resize((58,58),Image.Resampling.LANCZOS);small.paste(im,(i*92+17,j*100+8),im);draw.text((i*92+5,j*100+75),state,fill='white' if j else '#101116')
 small.save(Q/'readability-58.png')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--state');parser.add_argument('--prepare-only',action='store_true');args=parser.parse_args()
 parts=prepare()
 manifest=dict(sourceFacing='left',oppositeFacing='mirrored-source; asymmetric shell and buckle reverse sides',clips={})
 for state,count in COUNTS.items():
  semantic=dict(attack='basic',hit='hurt',defeated='ko').get(state,state);manifest['clips'][semantic]={}
  for face in ['left','right']:
   make_sif(parts,state,face,count)
   manifest['clips'][semantic][face]=dict(source=f'fizzmite/source/{state}-{face}.sif',frames=[f'fizzmite/frames/{state}-{face}-{i:03}.png' for i in range(count)],frameHoldMs=[1000/12]*count,loop=state in ['idle','walk'],canvas=dict(width=128,height=128),footOrigin=dict(x=64,y=125))
 # Neutral sources share actual idle frame-0 rig.
 for face in ['left','right']:shutil.copyfile(S/f'idle-{face}.sif',S/f'neutral-{face}.sif')
 (A/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 if not args.prepare_only:
  for state,count in COUNTS.items():
   if not args.state or args.state==state:render(state,count)
  if all((F/f'{s}-left-{n-1:03}.png').exists() for s,n in COUNTS.items()):qa()
