from pathlib import Path
import math,json,hashlib,subprocess
import numpy as np
from PIL import Image
S=Path(__file__).resolve().parent; A=S.parent; F=A/"frames"
SYNFIG="/opt/homebrew/bin/synfig"
v=lambda x,y:f'<vector><x>{x:.7f}</x><y>{y:.7f}</y></vector>'
p=lambda n,x:f'<param name="{n}">{x}</param>'
g=lambda n:hashlib.md5(('bastorto/'+n).encode()).hexdigest().upper()
def value(t,x):
 if t=='vector':return v(*x)
 return f'<{t} value="{x:.8f}"/>'
def anim(t,values):
 return f'<animated type="{t}">'+''.join(f'<waypoint time="{i/12:.8f}s" before="linear" after="linear">{value(t,x)}</waypoint>' for i,x in enumerate(values))+'</animated>'
def bone(name,parent,origins,angles):
 return f'<bone type="bone_object" guid="{g(name)}"><name><string>{name}</string></name><parent><bone_valuenode type="bone_object" guid="{g(parent)}"/></parent><origin>{anim("vector",origins)}</origin><angle>{anim("angle",angles)}</angle><scalelx><real value="1"/></scalelx><scalex><real value="1"/></scalex><width><real value=".1"/></width><tipwidth><real value=".1"/></tipwidth><bone_depth><real value="0"/></bone_depth><length><real value="1"/></length></bone>'

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
 order=['tail','leg_rear_far','leg_front_far','plastron','leg_rear_near','leg_front_near','neck','harness','head','shell']
 for name in list(order):
  if name.startswith('leg_'):order.insert(order.index(name)+1,name.replace('leg_','foot_'))
 layers=''
 for name in order:
  c=parts[name]['composition'];scale=anim('vector',[d['scales'].get(name,(1,1)) for d in poses]); opacity=anim('real',[d['alpha'].get(name,1) for d in poses])
  base=f'<composite type="transformation"><offset>{v(0,0)}</offset><angle><angle value="0"/></angle><skew_angle><angle value="0"/></skew_angle><scale>{scale}</scale></composite>'
  tr=f'<bone_link type="transformation"><bone><bone_valuenode type="bone_object" guid="{g(name)}"/></bone><base_value>{base}</base_value><translate><bool value="true"/></translate><rotate><bool value="true"/></rotate><skew><bool value="true"/></skew><scale_x><bool value="true"/></scale_x><scale_y><bool value="true"/></scale_y></bone_link>'
  imp=p('amount','<real value="1"/>')+p('blend_method','<integer value="0"/>')+p('tl',v(-c['w']*c['pivotX'],c['h']*c['pivot']))+p('br',v(c['w']*(1-c['pivotX']),-c['h']*(1-c['pivot'])))+p('c','<integer value="1"/>')+p('filename',f'<string>{name}.png</string>')
  layers+=f'<layer type="group" version="0.2" desc="{name}">'+p('amount',opacity)+p('blend_method','<integer value="0"/>')+p('origin',v(0,0))+p('transformation',tr)+p('canvas',f'<canvas><layer type="import" version="0.1">{imp}</layer></canvas>')+'</layer>'
 skeleton='<layer type="skeleton" active="true" exclude_from_rendering="true" version="0.1" desc="editable parented Bastorto rig">'+p('name','<string>Bastorto</string>')+p('bones','<static_list type="bone_object">'+''.join(f'<entry><bone type="bone_object" guid="{g(name)}"/></entry>' for name in ['body',*parts])+'</static_list>')+'</layer>'
 tr=f'<composite type="transformation"><offset>{v(256 if face=="right" else 0,0)}</offset><angle><angle value="0"/></angle><skew_angle><angle value="0"/></skew_angle><scale>{v(-1 if face=="right" else 1,1)}</scale></composite>'
 sif=f'<?xml version="1.0"?><canvas version="1.0" width="256" height="256" view-box="0 256 256 0" fps="12" begin-time="0f" end-time="{count/12}s" bgcolor="0 0 0 0"><name>Bastorto {state} {face}</name><bones><bone_root type="bone_object" guid="{g("root")}"/>{bones}</bones>{skeleton}<layer type="group" version="0.2">'+p('amount','<real value="1"/>')+p('origin',v(0,0))+p('transformation',tr)+p('canvas',f'<canvas>{layers}</canvas>')+'</layer></canvas>'
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

