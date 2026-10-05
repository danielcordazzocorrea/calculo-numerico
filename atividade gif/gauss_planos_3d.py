"""Cada equação é um plano: interpretação geométrica do exemplo de Gauss.

Requer numpy, matplotlib e Pillow. Execute este arquivo para gerar o GIF.
As transformações intermediárias também são operações de linha equivalentes.
No encerramento, os recortes dos planos se contraem até a interseção comum.
Essa contração é visual: os planos matemáticos permanecem infinitos.
"""
from pathlib import Path
from itertools import product
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).resolve().parent
COLORS=['#ed8140','#387bed','#009c87']
BG='#f1f5fa'
INK='#172c45'
MUTED='#61758e'
PURPLE='#8b38ba'
POINT=np.array([2.,3.,-1.])
START=np.array([[2.,1.,-1.,8.],[-3.,-1.,2.,-11.],[-2.,1.,2.,-3.]])
OPS=[(0,1,1.5),(0,2,1.),(1,2,-4.)]
M=[START.copy()]
for src,dst,m in OPS:
    mat=M[-1].copy()
    mat[dst]+=m*mat[src]
    M.append(mat)
EQS=[['2x + y − z = 8','−3x − y + 2z = −11','−2x + y + 2z = −3'],
     ['2x + y − z = 8','(1/2)y + (1/2)z = 1','−2x + y + 2z = −3'],
     ['2x + y − z = 8','(1/2)y + (1/2)z = 1','2y + z = 5'],
     ['2x + y − z = 8','(1/2)y + (1/2)z = 1','−z = 1']]
LO=POINT-5
HI=POINT+5
CORNERS=np.array(list(product(*zip(LO,HI))))
EDGES=[(a,b) for a in range(8) for b in range(a+1,8) if np.count_nonzero(CORNERS[a]!=CORNERS[b])==1]

def polygon(row):
    """Clip the infinite plane against the displayed cube (no singular divisions)."""
    n,d=row[:3],row[3]
    points=[]
    for a,b in EDGES:
        p,q=CORNERS[a],CORNERS[b]
        fp,fq=n@p-d,n@q-d
        if abs(fp)<1e-9:
            points.append(p)
        if fp*fq<0:
            points.append(p+(q-p)*fp/(fp-fq))
    pts=np.unique(np.round(points,10),axis=0)
    assert len(pts)>=3
    center=pts.mean(axis=0)
    normal=n/np.linalg.norm(n)
    u=pts[0]-center
    u/=np.linalg.norm(u)
    v=np.cross(normal,u)
    order=np.argsort(np.arctan2((pts-center)@v,(pts-center)@u))
    return pts[order]

def intersection_line(mat):
    direction=np.cross(mat[0,:3],mat[1,:3])
    direction/=np.linalg.norm(direction)
    bound=5/max(abs(direction))
    return np.array([POINT-bound*direction,POINT+bound*direction])

def ease(t):
    t=np.clip(t,0,1)
    return t*t*(3-2*t)

SEGMENTS=[('intro',5),('op0',8),('op1',8),('op2',8),('solve',8),('converge',7),('final',6)]
TOTAL=sum(d for _,d in SEGMENTS)

def reveal_state(kind,t):
    """Only reveal the solution marker after the patches have met."""
    if kind=='converge':
        return 1-ease(t/5),t>=5
    if kind=='final':
        return ease(t/2.5),True
    return 1.,False

def state(kind,t):
    if kind.startswith('op'):
        k=int(kind[-1]); src,dst,m=OPS[k]
        s=ease((t-1.4)/4.8)
        mat=M[k].copy(); mat[dst]+=s*m*mat[src]
        return mat,k+(s>=1),dst,s
    return (M[0],0,None,0) if kind=='intro' else (M[3],3,None,1)

def render(kind,t,elapsed):
    mat,index,active,s=state(kind,t)
    patch_scale,show_point=reveal_state(kind,t)
    # Verify the common solution throughout every animated transformation.
    assert np.allclose(mat[:,:3]@POINT,mat[:,3])
    assert abs(np.linalg.det(mat[:,:3]))>1e-8
    fig=plt.figure(figsize=(12,8),dpi=100,facecolor=BG)
    ax=fig.add_axes([.025,.19,.64,.65],projection='3d',computed_zorder=False)
    ax.set_facecolor(BG)
    ax.set(xlim=(LO[0],HI[0]),ylim=(LO[1],HI[1]),zlim=(LO[2],HI[2]))
    ax.set_box_aspect((1,1,1))
    # Hold the camera during row operations to make the plane rotation clear.
    az=-57+12*ease(t/5) if kind=='intro' else -45
    if kind=='final':
        az=-45+55*ease(t/6)
    ax.view_init(elev=22,azim=az)
    ax.set_xlabel('x',labelpad=5,color=INK,fontweight='bold',fontsize=13)
    ax.set_ylabel('y',labelpad=5,color=INK,fontweight='bold',fontsize=13)
    ax.set_zlabel('z',labelpad=5,color=INK,fontweight='bold',fontsize=13)
    for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
        axis.set_pane_color((.94,.96,.99,1))
        axis._axinfo['grid']['color']=(.65,.72,.81,.3)
    ax.tick_params(labelsize=9,colors=MUTED)
    for r in range(3):
        if patch_scale<=0:
            continue
        pts=POINT+patch_scale*(polygon(mat[r])-POINT)
        assert np.allclose(pts@mat[r,:3],mat[r,3])
        # All planes are finite display patches of mathematically infinite planes.
        poly=Poly3DCollection([pts],facecolors=COLORS[r],edgecolors=COLORS[r],
                              alpha=.31 if r==active else .19,linewidths=2,zorder=2+r*.01)
        ax.add_collection3d(poly)
        # Subtle parallel rulings help perceive orientation and rotation.
        n=mat[r,:3]; unit=n/np.linalg.norm(n)
        basis=np.cross(unit,[1.,0.,0.])
        if np.linalg.norm(basis)<.1:
            basis=np.cross(unit,[0.,1.,0.])
        basis/=np.linalg.norm(basis)
        second=np.cross(unit,basis)
        for offset in [-3,-1.5,0,1.5,3]:
            origin=POINT+offset*second
            ts=np.linspace(-9,9,110)
            line=origin+ts[:,None]*basis
            line=line[np.all((line>=LO)&(line<=HI),axis=1)]
            line=POINT+patch_scale*(line-POINT)
            if len(line)>1:
                ax.plot(*line.T,color=COLORS[r],alpha=.25,lw=.6,zorder=3)
    line=intersection_line(mat)
    line=POINT+patch_scale*(line-POINT)
    if patch_scale>0:
        ax.plot(*line.T,color='#435672',lw=1.7,ls='--',alpha=.8,zorder=7)
    if show_point:
        pulse=110+45*np.sin(np.pi*min(max(t-5,0),1)) if kind=='converge' else 110
        ax.scatter(*POINT,s=pulse,color=PURPLE,edgecolors='white',linewidths=2,depthshade=False,zorder=20)
        ax.text(POINT[0]+.3,POINT[1]+.35,POINT[2]+.65,'S = (2, 3, −1)',fontsize=11,
                color=PURPLE,fontweight='bold',zorder=21,
                bbox=dict(facecolor='white',alpha=.9,edgecolor='none',pad=3))
    fig.canvas.draw()
    im=Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:,:,:3].copy())
    plt.close(fig)
    d=ImageDraw.Draw(im)
    def txt(x,y,label,size=22,color=INK,bold=False):
        ft=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)
        d.text((x,y),label,font=ft,fill=color)
    def box(rect,color,r=15):
        d.rounded_rectangle(rect,radius=r,fill=color)
    d.rectangle((0,0,1200,137),fill=INK)
    txt(35,19,'GAUSS EM 3D  /  O MESMO EXEMPLO DA ATIVIDADE',16,'#ffc655',True)
    titles={'intro':'Cada equação representa um plano',
            'op0':'1. Transforme o plano azul',
            'op1':'2. Transforme o plano verde',
            'op2':'3. Elimine y do plano verde',
            'solve':'Leia a solução de baixo para cima',
            'converge':'Os recortes se encontram na solução',
            'final':'Três planos. Um único ponto em comum.'}
    txt(35,49,titles[kind],34,'white',True)
    subtitle='Os recortes se fecham sobre a interseção; os planos continuam infinitos.' if kind=='converge' else 'As operações mudam os planos, mas preservam a interseção comum.'
    txt(35,98,subtitle,21,'#d0dbea')
    if kind.startswith('op'):
        k=int(kind[-1])
        text=['R2 ← R2 + (3/2) R1','R3 ← R3 + R1','R3 ← R3 − 4R2'][k]
    else:
        text={'intro':'Sistema original','solve':'Sistema triangular','converge':'Encontro dos três planos','final':'Solução: x = 2, y = 3, z = −1'}[kind]
    txt(760,160,text,24,INK,True)
    for r in range(3):
        top=209+r*126
        box((755,top,1168,top+111),'white')
        d.rounded_rectangle((755,top,762,top+111),radius=3,fill=COLORS[r])
        txt(779,top+12,f'PLANO {r+1}  •  EQUAÇÃO {r+1}',14,COLORS[r],True)
        if active==r and 0<s<1:
            operation=['R2(s) = R2 + s · (3/2)R1','R3(s) = R3 + s · R1','R3(s) = R3 − s · 4R2'][int(kind[-1])]
            txt(779,top+41,operation,22,INK,True)
            txt(779,top+78,f'Em transformação: {round(s*100)}%',17,MUTED)
        else:
            txt(779,top+43,EQS[int(index)][r],25,INK,True)
            if kind in ['solve','final']:
                show=kind=='final' or t>=(2-r)*2
                if show:
                    txt(779,top+78,['y = 3 e z = −1  →  x = 2','z = −1  →  y = 3','z = −1'][r],19,COLORS[r],True)
    box((755,599,1168,652),'#eae2f3')
    status='●  S = (2, 3, −1)' if show_point else ('Aproximando os recortes...' if kind=='converge' else 'O ponto será revelado ao final.')
    txt(776,615,status,21,PURPLE,True)
    txt(47,645,'Tracejado: interseção dos planos 1 e 2.',17,MUTED)
    box((30,682,1170,771),'white')
    descriptions={
        'intro':('Uma equação em x, y e z define um plano.',
                 'Acompanhe as transformações. O ponto comum aparecerá depois do encontro visual.'),
        'op0':('O plano azul gira até a sua equação não depender de x.',
               'O plano laranja fica fixo; a reta comum entre esses dois planos é preservada.'),
        'op1':('O plano verde também passa a ter coeficiente de x igual a zero.',
               'Ao final: plano azul → (1/2)y + (1/2)z = 1; plano verde → 2y + z = 5.'),
        'op2':('O plano verde termina horizontal: −z = 1, ou seja, z = −1.',
               'Depois encontramos y no plano azul e x no plano laranja.'),
        'solve':('Plano verde → z = −1     |     Plano azul → y = 3     |     Plano laranja → x = 2',
                  'Essa é a substituição regressiva: resolver a última equação e subir.'),
        'converge':('Os três recortes diminuem até se encontrarem no mesmo lugar.',
                     'Destaque visual da interseção: Gauss é um método direto, não uma aproximação iterativa.'),
        'final':('Conferência: 2(2) + 3 − (−1) = 8;  −3(2) − 3 + 2(−1) = −11;  −2(2) + 3 + 2(−1) = −3.',
                  'Seções 3 e 3.1 do notebook • Os planos são infinitos; a figura exibe apenas recortes.')}
    a,b=descriptions[kind]
    txt(49,698,a,20,INK,True)
    txt(49,734,b,18,MUTED)
    d.rectangle((31,793,1169,799),fill='#d8e1ec')
    d.rectangle((31,793,31+1138*(elapsed+t)/TOTAL,799),fill=PURPLE)
    return im

def main():
    if '--preview' in sys.argv:
        sheet=Image.new('RGB',(1200,1064),'white')
        elapsed=0
        for i,(kind,duration) in enumerate(SEGMENTS):
            frame=render(kind,3 if kind=='converge' else duration*.7,elapsed)
            frame.resize((600,266)).save(OUT/f'planos_quadro_{i}.png')
            sheet.paste(frame.resize((600,266)),((i%2)*600,(i//2)*266))
            elapsed+=duration
        sheet.save(OUT/'planos_storyboard.jpg')
        return
    frames=[]
    assert all(not reveal_state(kind,0)[1] for kind,_ in SEGMENTS if kind!='final')
    assert reveal_state('converge',4.99)[1] is False
    assert reveal_state('converge',5)==(0.,True)
    elapsed=0
    for kind,duration in SEGMENTS:
        for i in range(duration*8):
            frame=render(kind,i/8,elapsed)
            frames.append(frame.quantize(colors=128,method=Image.Quantize.MEDIANCUT))
        elapsed+=duration
        print(f'Etapa concluída: {kind}',flush=True)
    path=OUT/'gauss_planos_3d.gif'
    # GIF stores time in 10ms units: alternate 120/130ms for exactly 8 fps.
    durations=[120 if i%2==0 else 130 for i in range(len(frames))]
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=False,disposal=1)
    with Image.open(path) as gif:
        ms=0
        for i in range(gif.n_frames):
            gif.seek(i); ms+=gif.info['duration']
        assert ms==TOTAL*1000
        print(f'GIF validado: {gif.n_frames} quadros, {ms/1000}s, {path.stat().st_size/1024/1024:.1f} MB.')

if __name__=='__main__':
    main()
