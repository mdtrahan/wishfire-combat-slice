"""Actor-local schema/frame checks and review contact sheets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json, hashlib
S=Path(__file__).resolve().parent;A=S.parent;Q=A/'qa';Q.mkdir(exist_ok=True)
concept=A.parents[1]/'_work/enemy-identities/new/gloamink-128.png'
counts=dict(idle=12,walk=12,attack=9,cast=12,hit=6,defeated=12,spawn=9)
records=[]
for state,n in counts.items():
 card=Image.new('RGB',(384*min(n,6),416*((n+5)//6)*2),'#d6c09a')
 ImageDraw.Draw(card).rectangle((0,416*((n+5)//6),card.width,card.height),fill='#101116')
 for bgindex,bg in enumerate(['#d6c09a','#101116']):
  for i in range(n):
   im=Image.open(A/'frames'/f'{state}-left-{i:03}.png').convert('RGBA');assert im.size==(128,128) and im.mode=='RGBA'
   other=Image.open(A/'frames'/f'{state}-right-{i:03}.png').convert('RGBA')
   assert ImageChops.difference(im.transpose(Image.Transpose.FLIP_LEFT_RIGHT),other).getchannel('A').getbbox() is None
   assert im.transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()==other.tobytes()
   x=i%6*384;y=(bgindex*((n+5)//6)+i//6)*416
   cell=Image.new('RGB',(384,416),bg);cell.paste(im.resize((384,384),Image.Resampling.NEAREST),(0,25),im.resize((384,384),Image.Resampling.NEAREST))
   ImageDraw.Draw(cell).text((8,5),f'{state} {i:03} | {bg}',fill='black' if bgindex==0 else 'white');card.paste(cell,(x,y))
   if bgindex==0:
    alpha=im.getchannel('A').point(lambda a:255 if a>=24 else 0);bb=alpha.getbbox();assert bb
    records.append(dict(state=state,frame=i,bbox=bb,canvasSafe=bb[0]>0 and bb[1]>0 and bb[2]<128 and bb[3]<128))
 card.save(Q/f'contact-{state}.png')
card=Image.new('RGB',(768,832))
for j,bg in enumerate(['#d6c09a','#101116']):
 for i,path in enumerate([A/'frames/idle-left-000.png',concept]):
  im=Image.open(path).convert('RGBA').resize((384,384),Image.Resampling.NEAREST);cell=Image.new('RGB',(384,416),bg);cell.paste(im,(0,25),im);ImageDraw.Draw(cell).text((8,5),'puppet idle 000' if i==0 else 'approved concept',fill='black' if j==0 else 'white');card.paste(cell,(384*i,416*j))
card.save(Q/'vs-concept.png')
small=Image.new('RGB',(7*174,240))
for j,bg in enumerate(['#d6c09a','#101116']):
 for i,state in enumerate(counts):
  im=Image.open(A/'frames'/f'{state}-left-{counts[state]//2:03}.png').resize((58,58),Image.Resampling.LANCZOS);cell=Image.new('RGB',(174,120),bg);cell.paste(im,(58,30),im);ImageDraw.Draw(cell).text((8,8),state,fill='black' if j==0 else 'white');small.paste(cell,(i*174,j*120))
small.save(Q/'readability-58.png')
m=json.loads((A/'manifest.json').read_text());assert set(m['clips'])=={'idle','walk','basic','cast','hurt','ko','spawn'}
for state,faces in m['clips'].items():
 for face,c in faces.items():
  assert c['loop']==(state in ['idle','walk']);assert c['footOrigin']==dict(x=64,y=125)
  assert len(c['frames'])==len(c['frameHoldMs']);assert all(abs(x-1000/12)<1e-7 for x in c['frameHoldMs'])
  for file in [c['source'],*c['frames']]:assert (A.parent/file).is_file(),file
receipt=dict(frames=len(records)*2,allCanvasSafe=all(r['canvasSafe'] for r in records),bounds=records,mirror='pixel-exact horizontal mirror',rgba=True,sourceHashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in S.glob('*.png')})
(Q/'checks.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['bounds','sourceHashes']}))
for state in counts:
 r=[x['bbox'] for x in records if x['state']==state];print(state,'bottom range',min(x[3] for x in r),max(x[3] for x in r))

# Complete cycles at the runtime size, with no enlargement of the 58px cells.
for state,n in counts.items():
 sheet=Image.new('RGB',(n*76,180),'#d6c09a');d=ImageDraw.Draw(sheet)
 d.rectangle((0,90,sheet.width,180),fill='#101116')
 for row,bg in enumerate(['#d6c09a','#101116']):
  for i in range(n):
   im=Image.open(A/'frames'/f'{state}-left-{i:03}.png').resize((58,58),Image.Resampling.LANCZOS)
   sheet.paste(im,(i*76+9,row*90+24),im);d.text((i*76+8,row*90+5),str(i),fill='black' if row==0 else 'white')
 sheet.save(Q/f'readability-58-{state}.png')
 # Reviewable continuous playback, two backgrounds, both facings.
 cells=[]
 for i in range(n):
  cell=Image.new('RGB',(256,256),'#d6c09a');ImageDraw.Draw(cell).rectangle((0,128,256,256),fill='#101116')
  for row in range(2):
   for col,face in enumerate(['left','right']):
    im=Image.open(A/'frames'/f'{state}-{face}-{i:03}.png');cell.paste(im,(col*128,row*128),im)
  cells.append(cell)
 cells[0].save(Q/f'playback-{state}.gif',save_all=True,append_images=cells[1:],duration=[83,83,84]*(n//3),loop=0 if state in ('walk','idle') else 1,disposal=2)
for state in ['walk','attack']:
 n=counts[state];sheet=Image.new('RGB',(n*256,4*280),'#d6c09a');d=ImageDraw.Draw(sheet)
 for bgrow,bg in enumerate(['#d6c09a','#101116']):
  for revision in range(2):
   row=bgrow*2+revision;d.rectangle((0,row*280,sheet.width,(row+1)*280),fill=bg)
   for i in range(n):
    folder=A/'_r1/frames' if revision==0 else A/'frames'
    im=Image.open(folder/f'{state}-left-{i:03}.png').resize((256,256),Image.Resampling.NEAREST)
    sheet.paste(im,(i*256,row*280+24),im)
    d.text((i*256+6,row*280+6),f'R{revision+1} {state} {i:03}',fill='black' if bgrow==0 else 'white')
 sheet.save(Q/f'r1-vs-r2-{state}.png')
# Same-coordinate overlay, concept in cyan and puppet in magenta.
ref=Image.open(concept).convert('RGBA');cur=Image.open(A/'frames/idle-left-000.png').convert('RGBA')
over=Image.new('RGB',(128,128),'#101116')
for im,col in [(ref,(50,220,255)),(cur,(255,80,180))]:
 tint=Image.new('RGBA',im.size,col+(0,));tint.putalpha(im.getchannel('A').point(lambda a:round(a*.5)));over.paste(tint,(0,0),tint)
over.resize((512,512),Image.Resampling.NEAREST).save(Q/'neutral-overlay.png')
# Archive verification covers every preserved file, including original native rig.
archive=json.loads((A/'_r1/archive-sha256.json').read_text())
assert all(hashlib.sha256((A/'_r1'/f).read_bytes()).hexdigest()==sha for f,sha in archive.items())
assert receipt['allCanvasSafe'], 'Paint clipped: inspect bounds in qa/checks.json'
print('R1 archive verified:',len(archive),'files; comparison sheets and all-frame 58px sheets exported.')
# Connected-paint proof catches detached heads, feet and tail tips after rig changes.
from collections import deque
islands=[]
for state,n in counts.items():
 for i in range(n):
  im=Image.open(A/'frames'/f'{state}-left-{i:03}.png').getchannel('A');pix=im.load();seen=set();areas=[]
  for y in range(128):
   for x in range(128):
    if (x,y) in seen or pix[x,y]<48:continue
    seen.add((x,y));todo=deque([(x,y)]);area=0
    while todo:
     xx,yy=todo.popleft();area+=1
     for q in [(xx-1,yy),(xx+1,yy),(xx,yy-1),(xx,yy+1)]:
      if 0<=q[0]<128 and 0<=q[1]<128 and q not in seen and pix[q[0],q[1]]>=48:seen.add(q);todo.append(q)
    areas.append(area)
  areas.sort(reverse=True)
  if len(areas)>1 and areas[1]>12:islands.append(dict(state=state,frame=i,areas=areas))
poses=json.loads((S/'poses-r2.json').read_text())
metrics={}
for state in ('walk','attack'):
 ps=poses[state];record={}
 for part in ('body','head','front_foot_near','front_foot_far','rear_foot_near','rear_foot_far'):
  xs=[p['world'][part][0] for p in ps];ys=[p['world'][part][1] for p in ps]
  record[part]=dict(xSpan=round(max(xs)-min(xs),3),ySpan=round(max(ys)-min(ys),3))
 metrics[state]=record
metrics['walk']['torsoScaleX']=[min(p['sc']['torso'][0] for p in poses['walk']),max(p['sc']['torso'][0] for p in poses['walk'])]
metrics['detachedIslandsOver12PixelsAtAlpha48']=islands
metrics['r1ArchiveFilesVerified']=len(archive)
(Q/'motion-checks-r2.json').write_text(json.dumps(metrics,indent=2)+'\n')
assert not islands, f'Detached paint: {islands}'
print('Connected-paint proof passed for all 72 left frames; mirrors cover right.')
