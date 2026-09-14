"""Render the illustrative monochrome build sequence; no live CI data."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
import math

W,H,S = 1200,320,2
MONO=['/System/Library/Fonts/Monaco.ttf', 'DejaVuSansMono.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf']
SANS=['/System/Library/Fonts/Helvetica.ttc', 'DejaVuSans.ttf']
FONTS={}
def font(size, sans=False):
    key=(size,sans)
    if key not in FONTS:
        for candidate in (SANS if sans else MONO):
            try:
                FONTS[key]=ImageFont.truetype(candidate, round(size*S))
                break
            except OSError:
                pass
        else:
            FONTS[key]=ImageFont.load_default(size=round(size*S))
    return FONTS[key]

def make_frame(i, n=100):
    im=Image.new('L',(W*S,H*S),10)
    d=ImageDraw.Draw(im)
    t=i/n
    # Cycles assemble, hold, then quietly dissolve into the next pass.
    p=min(t/.76,1)
    fade=1 if t < .88 else max(0,(1-t)/.12)
    def line(points,fill=48,width=1): d.line([(round(x*S),round(y*S)) for x,y in points],fill=fill,width=round(width*S))
    def rect(box,fill=None,outline=None,width=1,radius=0):
        b=tuple(round(v*S) for v in box)
        if radius: d.rounded_rectangle(b,radius=round(radius*S),fill=fill,outline=outline,width=round(width*S))
        else: d.rectangle(b,fill=fill,outline=outline,width=round(width*S))
    def txt(x,y,text,size=13,fill=148,sans=False): d.text((round(x*S),round(y*S)),text,font=font(size,sans),fill=fill)
    def dot(x,y,r,fill): d.ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S),fill=fill)
    def activity(x): return round(45+(x-45)*fade)
    rect((0,0,W-1,H-1),outline=72,radius=0)
    line([(24,49),(1176,49)],42)
    txt(28,19,'BUILD SEQUENCE',13,230)
    txt(183,19,'/ VISUAL DEMO',12,100)
    txt(992,19,'LOCAL / SIMULATED',11,100)
    line([(683,71),(683,284)],38)
    txt(28,72,'$ ./build --target native --release',15,222)
    txt(28,103,'STAGE',10,87)
    txt(250,103,'OUTPUT',10,87)
    txt(496,103,'PROGRESS',10,87)
    stages=[('resolve','12 dependencies'),('compile','.asm -> .o / x86_64'),('link','symbols + relocation'),('package','binary + checksum')]
    for k,(name,desc) in enumerate(stages):
        y=129+k*31
        stage=min(max(p*4-k,0),1)
        active=stage>0
        shade=activity(214 if stage>=1 else 235) if active else 78
        txt(28,y,f'{k+1:02}',12,activity(130) if active else 62)
        txt(62,y,name,14,shade)
        txt(250,y+1,desc,11,activity(160) if active else 69)
        rect((496,y+6,587,y+10),fill=33)
        if stage>0: rect((496,y+6,496+91*stage,y+10),fill=activity(214))
        txt(607,y+1,f'{round(stage*100):03}%',11,activity(180) if active else 69)
    line([(28,258),(654,258)],35)
    txt(28,277,'BUILD',11,120)
    rect((82,281,492,285),fill=32)
    if p: rect((82,281,82+410*p,285),fill=activity(215))
    txt(517,277,f'{round(p*12):02} / 12 OBJECTS',11,activity(174))

    txt(710,74,'ASSEMBLY GRAPH',12,220)
    txt(710,94,'dependency lattice / 12 modules',10,94)
    # Grid supports the floating geometry, without visual noise.
    for gx in range(716,1161,24):
        for gy in range(126,270,24): dot(gx,gy,.7,26)
    # Isometric modules form a stepped native build artifact.
    cubes=[]
    for z in range(2):
        for a in range(3):
            for b in range(2):
                cx=932+(a-b)*48
                cy=149+(a+b)*24-z*39
                cubes.append((z,a,b,cx,cy))
    # Draw from rear to foreground, lower layer before upper layer.
    cubes.sort(key=lambda c:(c[0],c[1]+c[2],c[1]))
    def poly(points,fill,outline):
        pts=[(round(x*S),round(y*S)) for x,y in points]
        d.polygon(pts,fill=fill)
        d.line(pts+[pts[0]],fill=outline,width=S)
    for idx,(z,a,b,cx,cy) in enumerate(cubes):
        # Three modules lock into place per build stage.
        build=min(max(p*12-idx,0),1)
        local=build*fade
        lift=(1-build)*15
        cy-=lift if build>0 else 0
        top=[(cx,cy-22),(cx+41,cy-1),(cx,cy+20),(cx-41,cy-1)]
        left=[(cx-41,cy-1),(cx,cy+20),(cx,cy+51),(cx-41,cy+30)]
        right=[(cx,cy+20),(cx+41,cy-1),(cx+41,cy+30),(cx,cy+51)]
        edge=round(40+145*local)
        poly(left,round(12+11*local),edge)
        poly(right,round(12+20*local),edge)
        poly(top,round(14+36*local),edge)
        if build:
            txt(cx-10,cy-8,f'{idx:02X}',9,round(62+164*local))
        else:
            dot(cx,cy-2,1.5,48)
    # Flow indicator follows a dedicated trace, separate from the modules.
    trace=[(716,246),(749,246),(749,224),(799,224),(822,201),(862,201)]
    line(trace,52)
    travel=(t*3)%1
    seglen=[math.dist(a,b) for a,b in zip(trace,trace[1:])]
    pos=travel*sum(seglen)
    for (a,b),length in zip(zip(trace,trace[1:]),seglen):
        if pos <= length:
            q=pos/length
            x=a[0]+(b[0]-a[0])*q; y=a[1]+(b[1]-a[1])*q
            dot(x,y,2.5,activity(225)); break
        pos-=length
    txt(710,279,'SOURCE',10,110)
    txt(792,279,'>',10,59)
    txt(825,279,'OBJECTS',10,110)
    txt(918,279,'>',10,59)
    txt(951,279,'EXECUTABLE',10,110)
    # Slow, tiny status indicator avoids blinking or strobes.
    dot(1156,284,3,round(80+45*(.5+.5*math.sin(t*2*math.pi))))
    im=im.resize((W,H),Image.Resampling.LANCZOS)
    # One fixed grayscale palette is deterministic and cannot introduce color.
    pal=Image.new('P',(1,1))
    pal.putpalette([v for i in range(256) for v in (i,i,i)])
    return im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE)

def build(out):
    global OUT
    OUT = Path(out)
    OUT.mkdir(parents=True, exist_ok=True)
    frames=[make_frame(i) for i in range(100)]
    frames[0].save(OUT/'build-loop.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=1)
    frames[72].convert('RGB').save(OUT/'build-loop-static.png')
    g=Image.open(OUT/'build-loop.gif')
    assert g.n_frames==100
    assert sum(g.seek(i) or g.info.get('duration',0) for i in range(g.n_frames))==10000
    for frame in frames:
        rgb=frame.convert('RGB')
        r,gg,b=rgb.split()
        assert ImageChops.difference(r,gg).getbbox() is None
        assert ImageChops.difference(r,b).getbbox() is None
    assert ImageChops.difference(frames[0].convert('RGB'),frames[50].convert('RGB')).getbbox()
    print({'gif':str(OUT/'build-loop.gif'),'size_bytes':(OUT/'build-loop.gif').stat().st_size,'frames':g.n_frames,'duration_seconds':10,'strict_grayscale':True,'static':str(OUT/'build-loop-static.png')})

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('assets'))
    build(parser.parse_args().out)
