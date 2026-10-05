"""Novo exemplo de Gauss, em estilo escuro com animação de blocos.

Requer Pillow. Execute: python gauss_neon.py
Use --preview para gerar apenas o storyboard.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import math
import sys
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).resolve().parent
W,H=1200,820
BG='#0e1020'
PANEL='#191d34'
TEXT='#f2f4ff'
MUTED='#a2abc5'
CYAN='#61e5ef'
PURPLE='#b394ff'
GOLD='#ffc778'
GREEN='#8df0bb'
X=[330,520,710,940]
Y=[302,394,486]
A=[[F(v) for v in row] for row in [[1,1,1,6],[2,3,1,11],[1,2,3,14]]]
OPS=[(0,1,F(-2)),(0,2,F(-1)),(1,2,F(-1))]
M=[[r[:] for r in A]]
for src,dst,m in OPS:
    mat=[r[:] for r in M[-1]]
    mat[dst]=[a+m*b for a,b in zip(mat[dst],mat[src])]
    M.append(mat)
assert M[-1]==[[1,1,1,6],[0,1,-1,-1],[0,0,3,9]]
SOL=[F(0)]*3
for i in [2,1,0]:
    SOL[i]=(M[-1][i][3]-sum(M[-1][i][j]*SOL[j] for j in range(i+1,3)))/M[-1][i][i]
assert SOL==[1,2,3]
assert all(sum(row[j]*SOL[j] for j in range(3))==row[3] for row in A)

@lru_cache(None)
def font(size,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)

def fmt(v):
    return str(v).replace('-','−')

def smooth(t):
    t=max(0,min(1,t))
    return t*t*(3-2*t)

def lerp(a,b,t):
    return a+(b-a)*smooth(t)

class Board:
    def __init__(self,title,tag,progress):
        self.im=Image.new('RGB',(W,H),BG)
        self.d=ImageDraw.Draw(self.im)
        for x in range(30,W,30):
            for y in range(150,H-40,30):
                self.d.point((x,y),fill='#24283e')
        self.text(42,24,'GAUSS / EM MOVIMENTO',16,CYAN,True)
        self.text(42,60,title,37,TEXT,True)
        self.box((976,30,1158,75),PANEL,14)
        self.text(1067,52,tag,16,PURPLE,True,'mm')
        self.d.line((42,116,1158,116),fill='#30354f',width=1)
        self.d.line((42,790,1158,790),fill='#30354f',width=4)
        self.d.line((42,790,42+1116*max(.002,progress),790),fill=CYAN,width=4)
        for i,label in enumerate(['SISTEMA','ELIMINAÇÃO','SUBSTITUIÇÃO','SOLUÇÃO']):
            self.text(42+i*300,800,label,10,MUTED)

    def text(self,x,y,s,size=24,color=TEXT,bold=False,anchor=None):
        self.d.text((int(x),int(y)),s,font=font(size,bold),fill=color,anchor=anchor)

    def box(self,r,fill=PANEL,radius=16,outline=None,width=1):
        self.d.rounded_rectangle(tuple(map(int,r)),radius,fill=fill,outline=outline,width=width)

    def chip(self,x,y,value,color=CYAN,scale=1):
        self.box((x-61*scale,y-30*scale,x+61*scale,y+30*scale),color,12)
        self.text(x,y,value,int(30*scale),BG,True,'mm')

    def matrix(self,mat,pivot=None,focus=None,t=0,hide=False):
        self.box((162,211,1090,551),PANEL,22)
        for j,label in enumerate(['x','y','z','b']):
            self.text(X[j],240,label,20,MUTED,True,'mm')
        if focus is not None:
            self.box((250,Y[focus]-35,1025,Y[focus]+35),'#272c48',12)
        self.d.line((830,264,830,523),fill='#515974',width=2)
        self.d.line([(253,270),(237,270),(237,519),(253,519)],fill=MUTED,width=2)
        self.d.line([(1009,270),(1029,270),(1029,519),(1009,519)],fill=MUTED,width=2)
        for r,row in enumerate(mat):
            self.text(195,Y[r],f'R{r+1}',18,PURPLE,True,'mm')
            if hide:
                continue
            for j,v in enumerate(row):
                if pivot==(r,j):
                    self.box((X[j]-55,Y[r]-34,X[j]+55,Y[r]+34),'#443526',12,outline=GOLD,width=2)
                    radius=39+4*math.sin(t*4)
                    self.d.arc((X[j]-radius,Y[r]-radius,X[j]+radius,Y[r]+radius),20,160,fill=GOLD,width=2)
                self.text(X[j],Y[r],fmt(v),38,GREEN if v==0 else TEXT,True,'mm')

def intro(t,p):
    b=Board('Outro sistema. A mesma ideia.','01 / COMEÇO',p)
    b.text(42,145,'Transforme três equações em uma matriz aumentada.',25,MUTED)
    eqs=['x + y + z = 6','2x + 3y + z = 11','x + 2y + 3z = 14']
    if t<2.4:
        for r,s in enumerate(eqs):
            offset=60*(1-smooth((t-r*.25)/.7))
            b.box((200+offset,253+r*99,1000+offset,333+r*99),PANEL,18)
            b.text(600+offset,293+r*99,s,34,[CYAN,PURPLE,GOLD][r],True,'mm')
    else:
        b.matrix(A,hide=t<4.1)
        if t<4.1:
            u=(t-2.4)/1.7
            for r,row in enumerate(A):
                for j,v in enumerate(row):
                    b.chip(lerp(440+j*107,X[j],u),lerp(293+r*99,Y[r],u),fmt(v),[CYAN,PURPLE,GOLD][r],.9)
    b.text(62,618,'META',16,CYAN,True)
    b.text(62,654,'Criar zeros abaixo da diagonal.',34,TEXT,True)
    b.text(62,711,'Depois, resolver de baixo para cima.',25,MUTED)
    return b.im

def operation(k,t,p):
    src,dst,m=OPS[k]
    b=Board(['Primeiro zero.','Segundo zero.','Terceiro zero.'][k],f'02 / PASSO {k+1}',p)
    label=['R2 ← R2 − 2R1','R3 ← R3 − R1','R3 ← R3 − R2'][k]
    b.text(48,146,label,31,CYAN,True)
    b.text(610,153,['Pivô = 1     •     multiplicador = 2','Pivô = 1     •     multiplicador = 1','Pivô = 1     •     multiplicador = 1'][k],21,MUTED)
    completed=t>=6.8
    b.matrix(M[k+1] if completed else M[k],(src,src),dst,t)
    b.text(46,242,'PIVÔ',13,GOLD,True)
    b.text(46,273,'1',46,GOLD,True)
    b.text(45,399,'ZEROS',13,GREEN,True)
    b.text(46,430,f'{k+int(completed)} / 3',25,GREEN,True)
    b.text(47,570,'CALCULANDO A NOVA LINHA, COLUNA POR COLUNA',15,PURPLE,True)
    centers=[185,462,739,1016]
    for j,cx in enumerate(centers):
        b.box((cx-128,600,cx+128,735),PANEL,16)
        b.text(cx,618,['x','y','z','b'][j],16,MUTED,True,'mm')
        a,v,new=M[k][dst][j],M[k][src][j],M[k+1][dst][j]
        operand=f'({fmt(v)})' if v<0 else fmt(v)
        expression=f'{fmt(a)} − '+(f'{fmt(-m)} × ' if m!=-1 else '')+operand
        b.text(cx,655,expression,23,TEXT,True,'mm')
        local=t-(1+j*1.1)
        if local>=.65:
            b.text(cx,703,f'= {fmt(new)}',29,GREEN if new==0 else CYAN,True,'mm')
        if 0<local<.65:
            u=local/.65
            b.chip(lerp(X[j],cx,u),lerp(Y[src],646,u),fmt(v),GOLD,.8)
    if 5.7<t<6.8:
        u=(t-5.7)/1.1
        for j,v in enumerate(M[k+1][dst]):
            b.chip(lerp(centers[j],X[j],u),lerp(703,Y[dst],u),fmt(v),GREEN,.95)
    if completed:
        radius=39+16*smooth((t-6.8)/.8)
        b.d.ellipse((X[src]-radius,Y[dst]-radius,X[src]+radius,Y[dst]+radius),outline=GREEN,width=3)
        b.text(48,753,'Linha inteira atualizada. O sistema continua equivalente.',18,GREEN)
    else:
        b.text(48,753,'A operação também é aplicada ao termo independente b.',18,MUTED)
    return b.im

def triangle(t,p):
    b=Board('A escada está pronta.','02 / TRIANGULAR',p)
    b.text(47,149,'Todos os coeficientes abaixo da diagonal agora são zero.',25,MUTED)
    b.matrix(M[3])
    for r,col in [(1,0),(2,0),(2,1)]:
        radius=36+6*math.sin(t*2)
        b.d.ellipse((X[col]-radius,Y[r]-radius,X[col]+radius,Y[r]+radius),outline=GREEN,width=3)
    points=[(260,344),(615,344),(615,437),(808,437)]
    end=min(3,int(t/.6)+1)
    b.d.line(points[:end+1],fill=CYAN,width=3)
    b.text(62,617,'3z = 9',38,GOLD,True)
    b.text(330,628,'→  z = 3',29,TEXT,True)
    b.text(62,686,'Começamos pela última linha e subimos: z → y → x.',27,MUTED)
    return b.im

def back(k,t,p):
    b=Board(['Encontre z.','Use z para encontrar y.','Use y e z para encontrar x.'][k],'03 / SUBSTITUIR',p)
    b.text(48,148,'Uma incógnita por vez, da última equação até a primeira.',25,MUTED)
    equations=['x + y + z = 6','y − z = −1','3z = 9']
    substitutions=['x + 2 + 3 = 6','y − 3 = −1','z = 9 / 3']
    row=2-k
    for r in range(3):
        y=270+r*133
        b.box((65,y-44,837,y+49),PANEL,18,outline=CYAN if r==row else None,width=2)
        b.text(98,y,f'R{r+1}',19,PURPLE,True,'lm')
        shown=substitutions[r] if (r>row or (r==row and t>1.25)) else equations[r]
        b.text(460,y,shown,35,TEXT if r==row else MUTED,True,'mm')
        b.box((872,y-44,1137,y+49),'#18312f' if r>row or (r==row and t>2.7) else PANEL,18)
        result=f'{"xyz"[r]} = {fmt(SOL[r])}' if r>row or (r==row and t>2.7) else f'{"xyz"[r]} = ?'
        b.text(1004,y,result,35,GREEN if '?' not in result else MUTED,True,'mm')
    if k>0 and t<1.3:
        u=t/1.3
        b.chip(lerp(1004,520,u),lerp(270+(row+1)*133,270+row*133,u),f'{"xyz"[row+1]}={fmt(SOL[row+1])}',GOLD)
    if 2<t<2.9:
        u=(t-2)/.9
        b.chip(lerp(610,1004,u),270+row*133,fmt(SOL[row]),GREEN)
    messages=['Divida os dois lados por 3.','Some 3 aos dois lados: y = −1 + 3.','Subtraia 2 e 3: x = 6 − 2 − 3.']
    b.text(65,639,messages[k],29,GOLD,True)
    b.text(65,701,'Substituição regressiva: usamos os valores que já conhecemos.',23,MUTED)
    return b.im

def finish(t,p):
    b=Board('Solução encontrada.','04 / CONFERIR',p)
    b.text(48,149,'Agora substitua os valores nas equações originais.',25,MUTED)
    for j,(name,v) in enumerate(zip('xyz',SOL)):
        cx=220+j*380
        scale=1+.05*math.sin(min(t,1)*math.pi) if t<1 else 1
        b.box((cx-161*scale,227,cx+161*scale,365),PANEL,23,outline=[CYAN,PURPLE,GOLD][j],width=2)
        b.text(cx,295,f'{name} = {fmt(v)}',49,[CYAN,PURPLE,GOLD][j],True,'mm')
    checks=['1 + 2 + 3 = 6','2(1) + 3(2) + 3 = 11','1 + 2(2) + 3(3) = 14']
    for j,s in enumerate(checks):
        y=431+j*87
        b.box((62,y-15,1138,y+51),PANEL,13)
        b.text(90,y,s,29,TEXT,True)
        if t>.6+j*.5:
            b.text(1024,y+3,'OK',25,GREEN,True)
    b.text(65,701,'Três equações satisfeitas. Uma única solução: (1, 2, 3).',28,GREEN,True)
    return b.im

SEGMENTS=[(intro,6)]+[(lambda t,p,k=k:operation(k,t,p),8) for k in range(3)]+[(triangle,4)]+[(lambda t,p,k=k:back(k,t,p),5) for k in range(3)]+[(finish,6)]
TOTAL=sum(d for _,d in SEGMENTS)

def main():
    preview='--preview' in sys.argv
    elapsed=0
    frames=[]
    sheet=Image.new('RGB',(1200,820),BG)
    for i,(fn,duration) in enumerate(SEGMENTS):
        shot=fn(duration*.73,(elapsed+duration*.73)/TOTAL)
        sheet.paste(shot.resize((400,273),Image.Resampling.LANCZOS),((i%3)*400,(i//3)*273))
        if not preview:
            for step in range(duration*10):
                frame=fn(step/10,(elapsed+step/10)/TOTAL)
                frames.append(frame.quantize(colors=96,method=Image.Quantize.MEDIANCUT))
            print(f'Etapa {i+1}/9 renderizada.',flush=True)
        elapsed+=duration
    sheet.save(OUT/'gauss_neon_storyboard.jpg')
    if preview:
        return
    path=OUT/'gauss_visual_neon.gif'
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=100,loop=0,disposal=1,optimize=False)
    with Image.open(path) as gif:
        ms=0
        for i in range(gif.n_frames):
            gif.seek(i)
            ms+=gif.info['duration']
        assert ms==TOTAL*1000
        print(f'Validado: {gif.n_frames} quadros; {ms/1000}s; {path.stat().st_size/1024/1024:.1f} MB. Solução exata (1,2,3).')

if __name__=='__main__':
    main()
