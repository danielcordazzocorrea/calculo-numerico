"""Animação didática vetorial renderizada em GIF com Pillow.

Execute: python gauss_visual.py (requer Pillow).
O exemplo e a ordem das operações seguem a seção 3 da atividade.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import math
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
W, H = 1200, 820
NAVY = '#14273d'
BG = '#eff3f8'
INK = '#172c45'
MUTED = '#63758c'
BLUE = '#2463eb'
TEAL = '#008774'
AMBER = '#ffc655'
WHITE = '#ffffff'
X = [184, 320, 456, 604]
Y = [287, 389, 491]

@lru_cache(None)
def font(size, bold=False):
    root = Path('C:/Windows/Fonts')
    return ImageFont.truetype(str(root / ('arialbd.ttf' if bold else 'arial.ttf')), size)

def fmt(v):
    return str(v).replace('-', '−')

def ease(t):
    t = max(0, min(1, t))
    return t*t*(3-2*t)

def mix(a, b, t):
    return a+(b-a)*ease(t)

A = [[F(v) for v in row] for row in [[2,1,-1,8],[-3,-1,2,-11],[-2,1,2,-3]]]
M = [[r[:] for r in A]]
OPS = [(0,1,F(3,2)), (0,2,F(1)), (1,2,F(-4))]
for src, dst, multiplier in OPS:
    updated = [r[:] for r in M[-1]]
    updated[dst] = [v+multiplier*u for v,u in zip(updated[dst],updated[src])]
    M.append(updated)
assert M[-1] == [[2,1,-1,8],[0,F(1,2),F(1,2),1],[0,0,-1,1]]
sol = [F(0)]*3
for i in [2,1,0]:
    sol[i] = (M[-1][i][3]-sum(M[-1][i][j]*sol[j] for j in range(i+1,3)))/M[-1][i][i]
assert sol == [2,3,-1]
assert all(sum(row[j]*sol[j] for j in range(3)) == row[3] for row in A)

class Canvas:
    def __init__(self, phase, title, sub, progress):
        self.im = Image.new('RGB',(W,H),BG)
        self.d = ImageDraw.Draw(self.im)
        self.d.rectangle((0,0,W,158),fill=NAVY)
        self.text(36,23,'ELIMINAÇÃO DE GAUSS',17,AMBER,True)
        self.text(36,52,title,34,WHITE,True)
        self.text(36,105,sub,20,'#c7d6e9')
        for i,label in enumerate(['01  ORGANIZAR','02  ELIMINAR','03  RESOLVER']):
            x=731+i*149
            self.box((x,26,x+137,58),BLUE if i==phase else '#253a51',10)
            self.text(x+68,42,label,12,WHITE,True,'mm')
        self.box((30,179,692,555),WHITE,20)
        self.box((715,179,1170,555),WHITE,20)
        self.box((30,575,1170,745),WHITE,20)
        self.text(36,766,'Mesmo sistema • operações equivalentes • solução preservada',17,MUTED)
        self.d.rectangle((36,798,1164,804),fill='#d4deeb')
        self.d.rectangle((36,798,36+1128*progress,804),fill=BLUE)

    def box(self, rect, color, radius=12, outline=None, width=1):
        self.d.rounded_rectangle(tuple(map(int,rect)),radius,fill=color,outline=outline,width=width)

    def text(self,x,y,s,size=25,color=INK,bold=False,anchor=None):
        self.d.text((int(x),int(y)),s,font=font(size,bold),fill=color,anchor=anchor)

    def arrow(self, start, end, color=BLUE, width=4):
        self.d.line((*start,*end),fill=color,width=width)
        angle=math.atan2(end[1]-start[1],end[0]-start[0])
        pts=[end]+[(end[0]-15*math.cos(angle+a),end[1]-15*math.sin(angle+a)) for a in [-.45,.45]]
        self.d.polygon(pts,fill=color)

    def chip(self,x,y,s,color=BLUE,scale=1):
        w,h=104*scale,58*scale
        self.box((x-w/2,y-h/2,x+w/2,y+h/2),color,12)
        self.text(x,y,s,int(28*scale),WHITE,True,'mm')

    def matrix(self, mat, pivot=None, focus=None, pulse=0, revealed=3):
        self.text(52,198,'MATRIZ AUMENTADA',14,MUTED,True)
        for c,label in enumerate(['x','y','z','b']):
            self.text(X[c],236,label,20,MUTED,True,'mm')
        if focus is not None:
            self.box((124,Y[focus]-38,661,Y[focus]+38),'#eaf1ff')
        if pivot is not None:
            r,c=pivot
            pad=3+3*math.sin(pulse*math.pi*2)
            self.box((X[c]-47-pad,Y[r]-36-pad,X[c]+47+pad,Y[r]+36+pad),AMBER,14)
        self.d.line([(121,257),(106,257),(106,531),(121,531)],fill=INK,width=3)
        self.d.line([(652,257),(667,257),(667,531),(652,531)],fill=INK,width=3)
        self.d.line((530,257,530,531),fill='#bdc9d9',width=2)
        for r,row in enumerate(mat):
            self.text(68,Y[r],f'R{r+1}',18,MUTED,True,'mm')
            if r>=revealed:
                continue
            for c,v in enumerate(row):
                self.text(X[c],Y[r],fmt(v),34,TEAL if v==0 else INK,True,'mm')


def intro(t,p):
    c=Canvas(0,'Das equações para a matriz','Cada linha guarda os coeficientes de uma equação.',p)
    row=min(2,int(t//1.7))
    local=(t-row*1.7)/1.7
    c.matrix(A,revealed=row if local<.85 else row+1)
    c.text(741,202,'O SISTEMA DA ATIVIDADE',15,BLUE,True)
    eqs=['2x + y − z = 8','−3x − y + 2z = −11','−2x + y + 2z = −3']
    for r,eq in enumerate(eqs):
        if r==row:
            c.box((735,Y[r]-36,1150,Y[r]+36),'#eaf1ff')
        c.text(752,Y[r],eq,27,INK,True,'lm')
    if local<.85:
        u=ease(local/.85)
        for j,v in enumerate(A[row]):
            c.chip(mix(790+j*93,X[j],u),Y[row]-math.sin(u*math.pi)*47,fmt(v))
    c.text(58,598,'COMO LER',15,BLUE,True)
    c.text(58,633,'x, y, z → coeficientes',28,INK,True)
    c.text(58,681,'b → termo independente',25,MUTED)
    c.arrow((595,660),(712,660))
    c.text(752,624,'Objetivo: criar zeros',28,TEAL,True)
    c.text(752,667,'abaixo da diagonal.',28,TEAL,True)
    return c.im


def operation(k,t,p):
    src,dst,mult=OPS[k]
    ready=t>=6.3
    labels=['R2 ← R2 + (3/2) R1','R3 ← R3 + R1','R3 ← R3 − 4R2']
    c=Canvas(1,['Zerando o −3','Zerando o −2','Zerando o 2'][k],
             'Copie a linha do pivô, multiplique e combine com a linha em foco.',p)
    c.matrix(M[k+1] if ready else M[k],(src,src),dst,t/1.5)
    c.text(742,204,f'OPERAÇÃO {k+1} DE 3',15,BLUE,True)
    c.text(742,243,labels[k],30,INK,True)
    c.box((739,301,1146,343),'#fff3d3')
    c.text(757,322,['Pivô: 2      multiplicador: −3/2','Pivô: 2      multiplicador: −1','Pivô: 1/2      multiplicador: 4'][k],19,INK,True,'lm')
    arithmetic=[['−3 + 3 = 0','−1 + 3/2 = 1/2','2 − 3/2 = 1/2','−11 + 12 = 1'],
                ['−2 + 2 = 0','1 + 1 = 2','2 − 1 = 1','−3 + 8 = 5'],
                ['0 − 0 = 0','2 − 2 = 0','1 − 2 = −1','5 − 4 = 1']][k]
    for j,line in enumerate(arithmetic):
        if t>2.7+j*.55:
            c.text(749,362+j*43,['x','y','z','b'][j],17,MUTED,True)
            c.text(789,358+j*43,line,25,TEAL if j==src else INK,True)
    c.text(51,591,['1  COPIAR A LINHA DO PIVÔ','1  COPIAR A LINHA DO PIVÔ','1  COPIAR A LINHA DO PIVÔ'][k]
           if t<1.7 else ('2  MULTIPLICAR E SOMAR' if t<5.1 else '3  DEVOLVER A NOVA LINHA À MATRIZ'),15,BLUE,True)
    if t<1.7:
        u=ease(t/1.3)
        for j,v in enumerate(M[k][src]):
            c.chip(X[j],mix(Y[src],661,u),fmt(v))
        c.text(751,642,'A linha original permanece.',23,INK,True)
        c.text(751,681,'Usamos uma cópia dela.',22,MUTED)
    elif t<5.1:
        c.text(68,651,'+',28,BLUE,True,'mm')
        for j,v in enumerate(M[k][src]):
            c.chip(X[j],650,fmt(v*mult))
            c.text(X[j],706,fmt(M[k][dst][j]),29,INK,True,'mm')
        c.text(752,627,['Cópia × (3/2)','Cópia × 1','Cópia × (−4)'][k],26,BLUE,True)
        c.text(752,674,f'+ valores atuais de R{dst+1}',23,MUTED)
    elif t<6.3:
        u=ease((t-5.1)/1.2)
        for j,v in enumerate(M[k+1][dst]):
            c.chip(X[j],mix(671,Y[dst],u),fmt(v),TEAL)
        c.text(751,644,'Nova linha calculada!',27,TEAL,True)
    else:
        # A ring expands from the coefficient that has just become zero.
        r=39+18*ease((t-6.3)/1.1)
        x,y=X[src],Y[dst]
        c.d.ellipse((x-r,y-r,x+r,y+r),outline=TEAL,width=3)
        c.text(64,635,'0',60,TEAL,True)
        c.text(135,638,'Coeficiente eliminado.',30,TEAL,True)
        c.text(135,686,'Todas as quatro entradas da linha foram atualizadas.',23,MUTED)
    return c.im


def triangular(t,p):
    c=Canvas(1,'Agora temos uma matriz triangular','Os três zeros abaixo da diagonal preparam a substituição regressiva.',p)
    c.matrix(M[3])
    for r,col in [(1,0),(2,0),(2,1)]:
        radius=39+4*math.sin(t*3)
        x,y=X[col],Y[r]
        c.d.ellipse((x-radius,y-radius,x+radius,y+radius),outline=TEAL,width=3)
    c.text(741,207,'SISTEMA EQUIVALENTE',15,BLUE,True)
    for i,s in enumerate(['2x + y − z = 8','(1/2)y + (1/2)z = 1','−z = 1']):
        c.text(749,Y[i],s,27,INK,True,'lm')
    c.arrow((1131,494),(1131,mix(470,273,t/3)),TEAL)
    c.text(60,610,'A próxima etapa começa aqui:  −z = 1',31,INK,True)
    c.text(60,666,'Resolva de baixo para cima: primeiro z, depois y e, por fim, x.',26,MUTED)
    return c.im


def back(k,t,p):
    row=2-k
    name=['z','y','x'][k]
    c=Canvas(2,f'Encontrando {name}', 'Substituição regressiva: cada resultado ajuda a resolver a linha acima.',p)
    c.matrix(M[3],focus=row)
    c.arrow((79,513),(79,mix(507,Y[row]-33,t/1.2)),TEAL)
    c.text(742,207,f'USANDO A LINHA R{row+1}',15,BLUE,True)
    steps=[['−z = 1','z = 1 / (−1)','z = −1'],
           ['(1/2)y + (1/2)z = 1','(1/2)y − 1/2 = 1','y = 3'],
           ['2x + y − z = 8','2x + 3 − (−1) = 8','x = (8 − 4) / 2 = 2']][k]
    for j,s in enumerate(steps):
        if t>=j*.85:
            c.text(746,277+j*85,s,27,TEAL if j==2 else INK,True)
    c.text(56,595,'SOLUÇÃO EM CONSTRUÇÃO',15,BLUE,True)
    for j in range(3):
        x=222+378*j
        c.box((x-160,636,x+160,720),'#e6f5f0' if j>row or (j==row and t>2.5) else '#f1f4f8',16)
        s=f'{"xyz"[j]} = {fmt(sol[j])}' if j>row or (j==row and t>2.5) else f'{"xyz"[j]} = ?'
        c.text(x,678,s,34,TEAL if '?' not in s else MUTED,True,'mm')
    if 1.9<t<2.9:
        u=(t-1.9)
        c.chip(mix(950,222+row*378,u),mix(466,678,u),f'{name}={fmt(sol[row])}',TEAL)
    if k>0 and t<1.5:
        c.chip(mix(222+(row+1)*378,1011,t/1.5),mix(678,298,t/1.5),['','z=−1','y=3'][k],TEAL)
    return c.im


def finish(t,p):
    c=Canvas(2,'Sistema resolvido!', 'Conferindo os valores nas três equações originais.',p)
    c.text(59,210,'A SOLUÇÃO',16,TEAL,True)
    for j in range(3):
        y=292+j*96
        c.box((57,y-36,663,y+36),'#e6f5f0',14)
        c.text(360,y,f'{"xyz"[j]} = {fmt(sol[j])}',42,TEAL,True,'mm')
    c.text(742,210,'CONFERÊNCIA',16,BLUE,True)
    for j,s in enumerate(['2(2) + 3 − (−1) = 8','−3(2) − 3 + 2(−1) = −11','−2(2) + 3 + 2(−1) = −3']):
        c.text(741,285+j*95,s,25,INK,True)
        if t>.4+j*.6:
            c.text(1110,321+j*95,'OK',16,TEAL,True)
    c.text(60,612,'Pivô → eliminação → matriz triangular → solução',31,INK,True)
    c.text(60,671,'Exemplo da seção 3 da atividade • Gauss sem troca de linhas',23,MUTED)
    return c.im


def main():
    segments=[(intro,5.5)]
    segments += [(lambda t,p,k=k: operation(k,t,p),8) for k in range(3)]
    segments += [(triangular,4)]
    segments += [(lambda t,p,k=k: back(k,t,p),5) for k in range(3)]
    segments += [(finish,5)]
    total=sum(duration for _,duration in segments)
    frames=[]
    elapsed=0
    previews=[]
    for render,duration in segments:
        for step in range(round(duration*10)):
            t=step/10
            frame=render(t,(elapsed+t)/total)
            frames.append(frame.quantize(colors=96,method=Image.Quantize.MEDIANCUT))
        previews.append(render(duration*.65,(elapsed+duration*.65)/total))
        elapsed+=duration
    path=OUT/'gauss_visual_animado.gif'
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False,disposal=1)
    finish(4,1).save(OUT/'gauss_visual_previa.png')
    sheet=Image.new('RGB',(1200,820),'white')
    for i,frame in enumerate(previews):
        thumb=frame.resize((400,273),Image.Resampling.LANCZOS)
        sheet.paste(thumb,((i%3)*400,(i//3)*273))
    sheet.save(OUT/'gauss_visual_storyboard.jpg')
    with Image.open(path) as gif:
        actual_duration=0
        for i in range(gif.n_frames):
            gif.seek(i)
            actual_duration+=gif.info['duration']
        assert actual_duration==round(total*1000)
        assert gif.size==(W,H)
        print(f'Validado: {gif.n_frames} quadros, {actual_duration/1000}s, {path.stat().st_size/1024/1024:.1f} MB. Contas exatas verificadas.')

if __name__=='__main__':
    main()
