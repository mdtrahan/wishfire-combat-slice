"""Validate delivered frames, native parent links, loop flags and repeat rendering."""
from pathlib import Path
from PIL import Image
import hashlib, json, subprocess, xml.etree.ElementTree as ET
import numpy as np
from build import COUNTS, pose, SYNFIG
S=Path(__file__).resolve().parent; A=S.parent; Q=A/'qa'; P=A.parent
meta=json.loads((S/'parts.json').read_text());m=json.loads((A/'manifest.json').read_text())
known={'body'}
for name,part in meta['parts'].items():
 assert part['composition']['parent'] in known,(name,'parent ordering');known.add(name)
 im=Image.open(S/part['file']);assert im.mode=='RGBA' and im.getchannel('A').getbbox()
 assert im.size==tuple(part['sourceDimensions'].values())
assert len(meta['parts'])==14
receipt={'actor':'fizzmite','sourceParts':len(meta['parts']),'frames':0,'clips':{},'repeats':[]}
for state,count in COUNTS.items():
 key={'attack':'basic','hit':'hurt','defeated':'ko'}.get(state,state);boxes=[];digests=[]
 for face in ['left','right']:
  clip=m['clips'][key][face];assert len(clip['frames'])==count
  assert clip['loop']==(state in ['idle','walk'])
  assert clip['canvas']=={'width':128,'height':128} and clip['footOrigin']=={'x':64,'y':125}
  assert clip['frameHoldMs']==[1000/12]*count
  assert len(list((A/'frames').glob(f'{state}-{face}-*.png')))==count
  doc=ET.parse(P/clip['source']).getroot();assert len(doc.findall('./bones/bone'))==15
  assert len(doc.findall('.//bone_link'))==14 and len(doc.findall('.//layer[@type="skeleton"]'))==1
  assert len(doc.findall('.//layer[@type="import"]/param[@name="c"]/integer[@value="1"]'))==14
  parents={doc.find('./bones/bone_root').get('guid')}
  for b in doc.findall('./bones/bone'):
   assert b.find('parent/bone_valuenode').get('guid') in parents;parents.add(b.get('guid'))
  for i,fn in enumerate(clip['frames']):
   im=Image.open(P/fn);assert im.mode=='RGBA' and im.size==(128,128)
   a=im.getchannel('A');b=a.point(lambda n:255 if n>=16 else 0).getbbox();assert b and b[0]>0 and b[1]>0 and b[2]<128 and b[3]<128,(fn,b)
   # Any edge paint at all would indicate cropping, including faint alpha.
   ar=np.array(im);assert max(ar[0,:,3].max(),ar[-1,:,3].max(),ar[:,0,3].max(),ar[:,-1,3].max())==0,(fn,'edge alpha')
   assert not ar[ar[:,:,3]==0,:3].any(),(fn,'transparent RGB')
   if face=='right':
    left=Image.open(A/'frames'/f'{state}-left-{i:03}.png');assert im.tobytes()==left.transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()
   else:boxes.append(b);digests.append(hashlib.sha256(im.tobytes()).hexdigest())
   receipt['frames']+=1
 assert len(set(digests))>1,state
 if state in ['idle','attack','cast','hit','spawn']:
  assert len({b[3] for b in boxes})==1,(state,'stationary foot baseline',boxes)
  # Independently verify each planted pivot from rig channels.
  for i in range(count):
   d=pose(state,i,count)
   for name,part in meta['parts'].items():
    if not name.startswith('leg'):continue
    dx,dy,angle=d['parts'][name];c=part['composition'];assert abs(d['body'][1]+160-c['y']+dy-(256-c['y']))<1e-7
    assert angle==0
 receipt['clips'][state]={'framesPerFacing':count,'distinctLeftFrames':len(set(digests)),'alpha16Union':[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)],'leftPixelSHA256':digests}
# Repeat native render for both facings, using the actual SIF sources.
for face in ['left','right']:
 fn=Q/f'repeat-{face}-author.png'; proc=subprocess.run([SYNFIG,str(S/f'neutral-{face}.sif'),'--time','0f','-w','1024','-h','1024','-t','png','-o',str(fn)],capture_output=True,text=True)
 assert proc.returncode==0,proc.stderr
 im=Image.open(fn).convert('RGBA').resize((128,128),Image.Resampling.LANCZOS);ar=np.array(im);ar[ar[:,:,3]<=4]=0;ar[ar[:,:,3]==0,:3]=0
 actual=Image.fromarray(ar);expected=Image.open(S/f'neutral-{face}.png')
 # Native negative-scale sampling differs slightly from mirrored positive-scale sampling.
 # Runtime opposite-facing delivery is an exact semantic pixel mirror.
 delta=np.abs(np.array(expected).astype(int)-ar.astype(int))
 if face=='left':assert delta.max()==0,(face,int(delta.max()))
 else:assert delta.mean()<1.5,(face,float(delta.mean()))
 repeat=Q/f'repeat-{face}-second.png'
 proc=subprocess.run([SYNFIG,str(S/f'neutral-{face}.sif'),'--time','0f','-w','1024','-h','1024','-t','png','-o',str(repeat)],capture_output=True,text=True)
 assert proc.returncode==0,proc.stderr
 assert Image.open(fn).convert('RGBA').tobytes()==Image.open(repeat).convert('RGBA').tobytes(),face
 receipt['repeats'].append({'facing':face,'nativeRepeatPixelsEqual':True,'packagedVsNativeMeanChannelDifference':float(delta.mean()),'packagedVsNativeMaximumChannelDifference':int(delta.max()),'decodedRGBA_SHA256':hashlib.sha256(actual.tobytes()).hexdigest()})
 fn.unlink();repeat.unlink()
assert receipt['frames']==144
(Q/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: 144 straight-alpha frames, 14 parts, 16 native SIFs, bounds, planted pivots, semantic mirrors, loops, native repeats.')
