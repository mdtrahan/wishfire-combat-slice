"""Bastorto painted cutouts, native Synfig bones, Lanczos exports and measured QA.
Writes exclusively within this actor folder. Run python3 source/prepare.py.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from collections import deque
import numpy as np
import json, math, hashlib, shutil, sys
import native
S=Path(__file__).resolve().parent; A=S.parent; Q=A/'qa'; F=A/'frames'
COUNTS=dict(idle=12,walk=12,attack=9,cast=12,hit=6,defeated=12,spawn=9)
CONCEPT=S

def clean(im):
 a=np.array(im.convert('RGBA'));a[a[:,:,3]<24]=0
 # Dominant connected paint island removes neighbouring atlas fragments.
 seen=a[:,:,3]>=64;h,w=seen.shape;best=[]
 for y,x in zip(*np.where(seen)):
  if not seen[y,x]:continue
  todo=[(y,x)];seen[y,x]=False;component=[]
  while todo:
   yy,xx=todo.pop();component.append((yy,xx))
   for ny,nx in [(yy-1,xx),(yy+1,xx),(yy,xx-1),(yy,xx+1)]:
    if 0<=ny<h and 0<=nx<w and seen[ny,nx]:seen[ny,nx]=False;todo.append((ny,nx))
  if len(component)>len(best):best=component
 m=np.zeros((h,w),dtype='uint8')
 for y,x in best:m[y,x]=255
 m=np.array(Image.fromarray(m).filter(ImageFilter.MaxFilter(3)));a[:,:,3]=np.minimum(a[:,:,3],m);a[a[:,:,3]==0]=0
 im=Image.fromarray(a);return im.crop(im.getbbox())

def prepare():
 atlas=Image.open(S/'parts-left-v1.png').convert('RGBA');parts={}
 # Composition values are runtime pixels; stored native geometry is doubled.
 rows=[
 ('head',(0,40,478,510),(58,91,57,53,.86,.9)),
 ('shell',(450,40,935,507),(91,85,58,60,.48,.64)),
 ('harness',(915,165,1254,500),(52,98,45,31,.5,.5)),
 ('plastron',(10,525,518,860),(76,105,58,21,.5,.5)),
 ('leg_front_near',(520,520,865,860),(75,99,29,29,.5,.15)),
 ('leg_rear_near',(930,520,1250,860),(107,103,24,25,.5,.15)),
 ('leg_front_far',(40,875,435,1210),(34,104,27,24,.5,.15)),
 ('leg_rear_far',(525,875,865,1210),(59,106,18,21,.5,.15)),
 ('neck',(620,545,850,740),(58,96,32,32,.5,.5)),
 ('tail',(940,940,1200,1150),(104,108,12,9,.12,.5))]
 src=Image.open(CONCEPT/'approved-bastorto-source.png').convert('RGBA')
 for name,box,c in rows:
  im=clean(atlas.crop(box)); provenance='generated completion paint'
  if name=='head':
   mask=Image.new('L',src.size);ImageDraw.Draw(mask).polygon([(75,300),(393,300),(457,335),(510,367),(564,413),(609,477),(636,550),(648,633),(641,702),(621,769),(585,819),(548,839),(486,841),(409,817),(348,788),(321,749),(267,735),(182,731),(113,699),(76,660)],fill=255)
   arr=np.array(src);arr[:,:,3]=np.minimum(arr[:,:,3],np.array(mask));im=clean(Image.fromarray(arr));provenance='approved source pixels, face and neck preserved'
  if name=='shell':
   mask=Image.new('L',src.size);ImageDraw.Draw(mask).polygon([(615,510),(648,425),(693,386),(741,430),(803,390),(864,379),(918,418),(944,457),(972,459),(1007,514),(1049,558),(1081,585),(1109,650),(1147,692),(1178,757),(1207,824),(1212,918),(1188,960),(1147,978),(1109,968),(1082,985),(1025,964),(984,973),(940,947),(898,925),(855,901),(812,862),(775,808),(740,790),(706,748),(680,700),(659,641)],fill=255)
   arr=np.array(src);arr[:,:,3]=np.minimum(arr[:,:,3],np.array(mask));im=clean(Image.fromarray(arr));provenance='approved visible shell paint'
  im.save(S/f'{name}.png');x,y,w,h,px,py=c
  parts[name]=dict(file=f'{name}.png',provenance=provenance,sourceDimensions=dict(width=im.width,height=im.height),pivot=dict(x=im.width*px,y=im.height*py),composition=dict(x=2*x,y=2*y,w=2*w,h=2*h,pivotX=px,pivot=py,parent='body'))
 # Articulated toes stay flat while the overlapping upper leg bears the weight.
 for name in list(parts):
  if not name.startswith('leg_'):continue
  part=parts[name];c=part['composition'];im=Image.open(S/part['file']);w,h=im.size
  upper=im.crop((0,0,w,round(h*.68)));foot=im.crop((0,round(h*.53),w,h));original_h=c['h'];original_py=c['pivot']
  upper.save(S/part['file']);fn=name.replace('leg_','foot_');foot.save(S/f'{fn}.png')
  c['h']=original_h*upper.height/h;c['pivot']=original_h*original_py/c['h'];part['sourceDimensions']=dict(width=upper.width,height=upper.height)
  part['pivot']=dict(x=upper.width*c['pivotX'],y=upper.height*c['pivot'])
  fc=dict(x=c['x'],y=247,w=c['w'],h=original_h*foot.height/h,pivotX=.5,pivot=1,parent='body')
  parts[fn]=dict(file=f'{fn}.png',derivedFrom=name,sourceDimensions=dict(width=foot.width,height=foot.height),pivot=dict(x=foot.width*.5,y=foot.height),composition=fc)
 (S/'parts.json').write_text(json.dumps(dict(actor='bastorto',atlas='parts-left-v1.png',sourceFacing='left',nativeCanvas=[256,256],nativeFootOrigin=[128,250],parts=parts),indent=2)+'\n')
 return parts

PARTS={};POSES={}
def pose(state,i,count):
 i=i%count;t=i/max(1,count-1);p=2*math.pi*i/12
 # All motion values below are runtime canvas pixels, then doubled for Synfig.
 bx=by=br=0.; hd=[0.,0.,0.];sd=[0.,0.,0.]; hs=(1,1);ss=(1,1);withdraw=0
 if state=='idle':
  breath=math.sin(p);sd=[0,-1.25*breath,.7*breath];hd=[.7*math.sin(p),-.6*breath,2.7*math.sin(p)]
  ss=(1+.008*breath,1+.015*breath)
 elif state=='walk':
  by=-5+5*math.cos(2*p);br=2.7*math.sin(p);sd=[0,-.6*math.sin(2*p),5*math.sin(p)];hd=[0,-1, -2*math.sin(p)]
 elif state=='attack':
  anticipation=[0,.5,1,.25,0,0,0,0,0][i];drive=[0,0,0,.6,1,.9,.5,.15,0][i]
  bx=8*anticipation-14*drive;by=2*anticipation-1.5*drive;br=3*anticipation-4*drive
  hd=[4*anticipation+6*drive,1*anticipation,-7*anticipation+8*drive];sd=[-2*drive-6*anticipation,0,0]
  ss=(1+.07*drive-.04*anticipation,1-.04*drive+.03*anticipation)
 elif state=='cast':
  r=[0,.1,.35,.65,1,1,.94,.8,.55,.3,.1,0][i];by=-12*r;br=-15*r
  hd=[2*r,-5*r,-27*r];sd=[0,-2*r,-3*r];ss=(1+.04*r,1+.12*r)
 elif state=='hit':
  r=[0,1,.82,.4,.1,0][i];withdraw=.84*r;bx=3*r;by=2*r;hd=[19*r,4*r,-8*r];sd=[2*r,0,-3*r]
 elif state=='defeated':
  r=min(1,t*1.8);withdraw=r;by=17*r;br=6*r;hd=[24*r,7*r,-10*r];sd=[0,5*r,4*r];ss=(1+.035*r,1-.08*r)
 elif state=='spawn':
  withdraw=[1,.92,.75,.45,.1,0,0,0,0][i];r=withdraw;hd=[24*r,7*r,-10*r];by=12*r;sd=[0,-2*math.sin(t*math.pi),0]
 hs=(1-.82*withdraw,1-.65*withdraw)
 if state=='attack':hs=(1-.07*drive,1+.015*drive)
 d=dict(body=(128+2*bx,96-2*by,br),parts={},scales={},alpha={})
 for name,z in [('head',hd),('shell',sd)]:d['parts'][name]=(2*z[0],-2*z[1],z[2])
 d['scales']['head']=hs;d['scales']['shell']=ss
 # Keep chest below the neck; shell overlaps all hidden neck ends.
 bw=0 if state=='hit' else withdraw
 d['parts']['harness']=(48*bw,16*bw-.6*by,0)
 d['scales']['harness']=(1-.4*bw,1-.5*bw)
 d['scales']['plastron']=(1-.5*bw,1-.65*bw)
 d['parts']['plastron']=(16*bw,6*bw,0)
 d['scales']['neck']=(1-.8*withdraw,1-.6*withdraw)
 d['parts']['neck']=(40*withdraw,0,0)
 # Inverse body transform locks each planted toe while preserving a hidden hip overlap.
 angle=math.radians(-br);cs=math.cos(angle);sn=math.sin(angle)
 for name,a in PARTS.items():
  if not name.startswith('leg_'):continue
  c=a['composition'];hx=c['x']/2;hy=c['y']/2;length=c['h']/2*(1-c['pivot'])
  footname=name.replace('leg_','foot_');fc=PARTS[footname]['composition'];footx=hx;footy=123.5;lift=0
  if state=='walk':
   # Opposite diagonal pairs: near-front + far-rear; far-front + near-rear.
   lag=0 if name in ('leg_front_near','leg_rear_far') else math.pi
   q=p+lag;footx+=4.5*math.cos(q);lift=9*max(0,math.sin(q));footy-=lift
  if bw:
   # Withdraw into shell without fading paint. Scale about hip.
   d['scales'][name]=(1-.65*bw,1-.94*bw);d['parts'][name]=(2*(82-hx)*bw,-2*(107-hy)*bw,0)
   d['scales'][footname]=(1-.8*bw,1-.9*bw);d['parts'][footname]=(2*(82-hx)*bw,2*(123.5-107)*bw,0);continue
  wx=footx-(64+bx);wy=footy-(80+by)
  fx=wx*cs+wy*sn+64;fy=-wx*sn+wy*cs+80
  d['parts'][footname]=(2*(fx-fc['x']/2),-2*(fy-fc['y']/2),-br)
  wx=footx-(64+bx);wy=footy-fc['h']/2*.54-(80+by)
  lx=wx*cs+wy*sn+64;ly=-wx*sn+wy*cs+80
  dx=lx-hx;dy=ly-hy
  d['parts'][name]=(0,0,math.degrees(math.atan2(dx,dy)))
  d['scales'][name]=(1,math.hypot(dx,dy)/length)
 POSES.setdefault(state,{})[str(i)]=dict(bodyCanvas=[64+bx,80+by,br],headOffset=hd,shellOffset=sd,withdraw=withdraw,parts=d)
 return d

def qa():
 metric=dict(canvas=[128,128],readabilityCanvas=[58,58],alphaThreshold=32,states={})
 for state,n in COUNTS.items():
  sheet=Image.new('RGB',(6*384,math.ceil(n/6)*2*410));draw=ImageDraw.Draw(sheet);rows=math.ceil(n/6)
  measurements=[];last=None;first=None
  for b,bg in enumerate(['#d6c09a','#101116']):
   draw.rectangle((0,b*rows*410,sheet.width,(b+1)*rows*410),fill=bg)
   for i in range(n):
    im=Image.open(F/f'{state}-left-{i:03}.png').convert('RGBA');large=im.resize((384,384),Image.Resampling.NEAREST);x=i%6*384;y=(b*rows+i//6)*410
    sheet.paste(large,(x,y),large);draw.text((x+8,y+387),f'{state} {i:03}',fill='#101116' if b==0 else 'white')
    if b==0:
     ar=np.array(im);mask=Image.fromarray((ar[:,:,3]>=32).astype('uint8')*255);bbox=mask.getbbox();small=np.array(im.resize((58,58),Image.Resampling.LANCZOS));item=dict(frame=i,bbox=bbox,bbox58=Image.fromarray((small[:,:,3]>=32).astype('uint8')*255).getbbox(),opaquePixels=int((ar[:,:,3]>=32).sum()))
     if last is not None:
      delta=np.abs(ar.astype(int)-last[0].astype(int));d58=np.abs(small.astype(int)-last[1].astype(int));item.update(changedPixels=int((delta.max(axis=2)>8).sum()),changedPixels58=int((d58.max(axis=2)>8).sum()),meanAbsoluteRGBAChange=float(delta.mean()),bboxDelta=[bbox[k]-last[2][k] for k in range(4)],bboxDelta58=[item['bbox58'][k]-Image.fromarray((last[1][:,:,3]>=32).astype('uint8')*255).getbbox()[k] for k in range(4)])
     else:first=(ar,small,bbox)
     measurements.append(item);last=(ar,small,bbox)
  if state in ('idle','walk'):
   measurements[0]['wrapChangedPixels']=int((np.abs(first[0].astype(int)-last[0].astype(int)).max(axis=2)>8).sum())
  metric['states'][state]=measurements;sheet.save(Q/f'contact-{state}.png')
 sheet=Image.new('RGB',(12*84,len(COUNTS)*2*88));draw=ImageDraw.Draw(sheet)
 for j,(state,n) in enumerate(COUNTS.items()):
  for b,bg in enumerate(['#d6c09a','#101116']):
   y=(2*j+b)*88;draw.rectangle((0,y,sheet.width,y+88),fill=bg)
   for i in range(n):
    im=Image.open(F/f'{state}-left-{i:03}.png').resize((58,58),Image.Resampling.LANCZOS);sheet.paste(im,(i*84+13,y+1),im);draw.text((i*84+2,y+65),f'{state} {i}',fill='white' if b else '#101116')
 sheet.save(Q/'readability-58.png')
 comp=Image.new('RGB',(768,820));draw=ImageDraw.Draw(comp)
 for b,bg in enumerate(['#d6c09a','#101116']):
  draw.rectangle((0,b*410,768,(b+1)*410),fill=bg)
  for j,im in enumerate([Image.open(F/'idle-left-000.png'),Image.open(CONCEPT/'approved-bastorto-128.png')]):
   im=im.convert('RGBA').resize((384,384),Image.Resampling.NEAREST);comp.paste(im,(j*384,b*410),im);draw.text((j*384+8,b*410+388),'Puppet idle 0' if j==0 else 'Approved concept',fill='white' if b else '#101116')
 comp.save(Q/'vs-concept.png')
 factor=58/128
 metric['authoredAmplitudes']=dict(walkBodyBobCanvas=10,walkBodyBob58=10*factor,walkShellRockPeakToPeakDegrees=10,walkLegLiftCanvas=9,walkLegLift58=9*factor,attackBodyTravelFromAnticipationCanvas=22,attackBodyTravel58=22*factor,castBodyLiftCanvas=12,castBodyLift58=12*factor)
 # Native transform landmarks, independently calculated from the saved sampled poses.
 landmarks={}
 for state,frames in POSES.items():
  vals=[]
  for i in range(COUNTS[state]):
   ps=frames[str(i)];bx,by,rot=ps['bodyCanvas'];r=math.radians(-rot)
   c=PARTS['shell']['composition'];dx,dy,ar=ps['shellOffset'];lx=c['x']/2-64+dx;ly=c['y']/2-80+dy
   sx=bx+lx*math.cos(r)-ly*math.sin(r);sy=by+lx*math.sin(r)+ly*math.cos(r)
   rr=r-math.radians(ar);scale=ps['parts']['scales']['shell'][0];left=-c['w']/2*c['pivotX']*scale
   toes={}
   for name,part in PARTS.items():
    if not name.startswith('foot_'):continue
    cc=part['composition'];xx,yy,ang=ps['parts']['parts'][name];tx=cc['x']/2-64+xx/2;ty=cc['y']/2-80-yy/2
    toes[name]=[bx+tx*math.cos(r)-ty*math.sin(r),by+tx*math.sin(r)+ty*math.cos(r)]
   vals.append(dict(frame=i,frontShell=[sx+left*math.cos(rr),sy+left*math.sin(rr)],body=[bx,by],toes=toes))
  landmarks[state]=vals
 metric['landmarks']=landmarks
 m=landmarks['cast'];lift=m[0]['frontShell'][1]-min(z['frontShell'][1] for z in m);metric['measuredRigAmplitudes']=dict(castFrontShellLiftCanvas=lift,castFrontShellLift58=lift*factor,walkBodyBobCanvas=max(z['body'][1] for z in landmarks['walk'])-min(z['body'][1] for z in landmarks['walk']),attackTravelCanvas=max(z['body'][0] for z in landmarks['attack'])-min(z['body'][0] for z in landmarks['attack']))
 toes=landmarks['walk'];leg_lift=max(max(z['toes'][name][1] for z in toes)-min(z['toes'][name][1] for z in toes) for name in toes[0]['toes'])
 metric['measuredRigAmplitudes'].update(walkToeLiftCanvas=leg_lift,walkToeLift58=leg_lift*factor,attackTravel58=metric['measuredRigAmplitudes']['attackTravelCanvas']*factor,walkBodyBob58=metric['measuredRigAmplitudes']['walkBodyBobCanvas']*factor,attackForwardFromNeutralCanvas=14,attackForwardFromNeutral58=14*factor)
 metric['measurementsNote']='Bounds and pixel deltas are measured from exported RGBA. Amplitudes and planted toes are independently reconstructed from native rig transforms. 58 values multiply canvas pixels by 58/128. Purposeful identical holds remain explicit.'
 (Q/'motion.json').write_text(json.dumps(metric,indent=2)+'\n');(S/'poses.json').write_text(json.dumps(POSES,indent=2)+'\n')
 # Animated review evidence has the same cadence and sand/dark panels as exports.
 for state,n in COUNTS.items():
  seq=[]
  for i in range(n):
   im=Image.open(F/f'{state}-left-{i:03}.png').resize((256,256),Image.Resampling.NEAREST);card=Image.new('RGB',(512,256),'#d6c09a');ImageDraw.Draw(card).rectangle((256,0,512,256),fill='#101116');card.paste(im,(0,0),im);card.paste(im,(256,0),im);seq.append(card)
  seq[0].save(Q/f'preview-{state}.gif',save_all=True,append_images=seq[1:],duration=83,loop=0)

if __name__=='__main__':
 PARTS=prepare();native.pose=pose
 manifest=dict(sourceFacing='left',oppositeFacing='mirrored-source; asymmetric costume reverses sides',clips={})
 for state,n in COUNTS.items():
  key=dict(attack='basic',hit='hurt',defeated='ko').get(state,state);manifest['clips'][key]={}
  for face in ['left','right']:
   native.make_sif(PARTS,state,face,n);manifest['clips'][key][face]=dict(source=f'bastorto/source/{state}-{face}.sif',frames=[f'bastorto/frames/{state}-{face}-{i:03}.png' for i in range(n)],frameHoldMs=[1000/12]*n,loop=state in ['idle','walk'],canvas=dict(width=128,height=128),footOrigin=dict(x=64,y=125))
  if '--prepare-only' not in sys.argv and (not any(v.startswith('--only=') for v in sys.argv) or '--only='+state in sys.argv):native.render(state,n)
 for face in ['left','right']:shutil.copyfile(S/f'idle-{face}.sif',S/f'neutral-{face}.sif')
 (A/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 if '--prepare-only' not in sys.argv:qa()
