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
   im=Image.open(A/'frames'/f'{state}-left-{i:03}.png').convert('RGBA');assert im.size==(128,128)
   other=Image.open(A/'frames'/f'{state}-right-{i:03}.png').convert('RGBA')
   assert ImageChops.difference(im.transpose(Image.Transpose.FLIP_LEFT_RIGHT),other).getbbox() is None
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
