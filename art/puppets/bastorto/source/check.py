"""Validate Bastorto's complete handoff, including mirrored pixels and planted toes."""
from pathlib import Path
import json, hashlib, math, subprocess, shutil, xml.etree.ElementTree as ET
from PIL import Image
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent;Q=A/'qa'
COUNTS=dict(idle=12,walk=12,attack=9,cast=12,hit=6,defeated=12,spawn=9)
manifest=json.loads((A/'manifest.json').read_text());motion=json.loads((Q/'motion.json').read_text())
issues=[];exports=[];islands=[]
def components(mask):
 seen=mask.copy();sizes=[];h,w=seen.shape
 for y,x in zip(*np.where(seen)):
  if not seen[y,x]:continue
  todo=[(y,x)];seen[y,x]=False;n=0
  while todo:
   yy,xx=todo.pop();n+=1
   for ny,nx in [(yy-1,xx),(yy+1,xx),(yy,xx-1),(yy,xx+1)]:
    if 0<=ny<h and 0<=nx<w and seen[ny,nx]:seen[ny,nx]=False;todo.append((ny,nx))
  sizes.append(n)
 return sorted(sizes,reverse=True)
for state,n in COUNTS.items():
 key=dict(attack='basic',hit='hurt',defeated='ko').get(state,state)
 for face in ['left','right']:
  clip=manifest['clips'][key][face]
  assert len(clip['frames'])==n and clip['canvas']==dict(width=128,height=128)
  assert clip['footOrigin']==dict(x=64,y=125) and clip['loop']==(state in ['idle','walk'])
  assert all(abs(ms-1000/12)<1e-8 for ms in clip['frameHoldMs'])
  root=ET.parse(S/f'{state}-{face}.sif').getroot();assert root.find('bones') is not None
  for i,path in enumerate(clip['frames']):
   fn=A.parent/path;im=Image.open(fn);ar=np.array(im);assert im.mode=='RGBA' and im.size==(128,128)
   assert np.all(ar[ar[:,:,3]==0,:3]==0)
   border=np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])
   if border.max()>16:issues.append(f'Canvas edge {fn.name}: alpha {border.max()}')
   if face=='right':
    left=Image.open(A/'frames'/f'{state}-left-{i:03}.png');assert np.array_equal(ar,np.array(left.transpose(Image.Transpose.FLIP_LEFT_RIGHT)))
   else:
    sizes=components(ar[:,:,3]>=32);islands.append(dict(state=state,frame=i,components=sizes))
    if len([x for x in sizes if x>=6])>1:issues.append(f'Detached paint {fn.name}: {sizes[:6]}')
   exports.append(dict(file=str(fn.relative_to(A)),sha256=hashlib.sha256(fn.read_bytes()).hexdigest()))
 # Every state must make visible changes at phone size; purposeful holds remain listed.
 assert sum(x.get('changedPixels58',0) for x in motion['states'][state])>200
 assert (Q/f'contact-{state}.png').exists()
rig=motion['measuredRigAmplitudes'];k=58/128
assert rig['walkBodyBobCanvas']*k>=4
assert rig['attackTravelCanvas']*k>=6
assert rig['castFrontShellLift58']>=6
# All stationary upright toe pivots remain planted. Swing feet rise on walk.
toe_error=0
for state in ['idle','attack','cast']:
 for row in motion['landmarks'][state]:
  for toe in row['toes'].values():toe_error=max(toe_error,abs(toe[1]-123.5))
assert toe_error<1e-7,toe_error
assert len(exports)==144
receipt=dict(status='PASS' if not issues else 'CONCERNS',frameCount=len(exports),issues=issues,toeYMaxErrorCanvas=toe_error,measurements=rig,alphaEdgeLimit=16,componentThreshold=6,components=islands,exports=exports)
(Q/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['status','frameCount','issues','toeYMaxErrorCanvas','measurements']},indent=2))
if issues:raise SystemExit(1)
# Optional native determinism probe, bounded to the planted neutral frame.
import sys
if '--repeat' in sys.argv:
 scratch=S/'repeat-check';scratch.mkdir(exist_ok=True)
 cmd=['/opt/homebrew/bin/synfig',str(S/'idle-left.sif'),'--begin-time','0f','--end-time','0f','--fps','12','-w','1024','-h','1024','-t','png','-o',str(scratch/'frame.png')]
 result=subprocess.run(cmd,capture_output=True,text=True);assert result.returncode==0,result.stderr
 files=list(scratch.glob('*.png'));assert len(files)==1,files
 im=Image.open(files[0]).convert('RGBA').resize((128,128),Image.Resampling.LANCZOS);ar=np.array(im);ar[ar[:,:,3]<=4]=0;ar[ar[:,:,3]==0,:3]=0
 original=np.array(Image.open(A/'frames/idle-left-000.png'));equal=np.array_equal(ar,original)
 (Q/'repeat-render.json').write_text(json.dumps(dict(pixelIdentical=bool(equal),state='idle',frame=0,authorSize=[1024,1024],exportSize=[128,128],renderer='/opt/homebrew/bin/synfig',changedPixels=int(np.any(ar!=original,axis=2).sum())),indent=2)+'\n')
 shutil.rmtree(scratch);assert equal
 print('Native repeat render: pixel identical')
