"""Gera a animação do exemplo da seção 3 do notebook. Requer Pillow."""
from pathlib import Path
from fractions import Fraction as F
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
W, H = 1200, 760
BG, INK, MUTED = '#f3f5fa', '#172842', '#58677d'
BLUE, GREEN, GOLD = '#245bd6', '#087c66', '#fff0bc'
FONT = Path('C:/Windows/Fonts')

def font(size, bold=False):
    return ImageFont.truetype(str(FONT / ('arialbd.ttf' if bold else 'arial.ttf')), size)

original = [[F(v) for v in r] for r in [[2,1,-1,8],[-3,-1,2,-11],[-2,1,2,-3]]]
matrices = [[r[:] for r in original]]
for dest, src, mult in [(1,0,F(3,2)), (2,0,F(1)), (2,1,F(-4))]:
    m = [r[:] for r in matrices[-1]]
    m[dest] = [a + mult*b for a,b in zip(m[dest], m[src])]
    matrices.append(m)
solution = [F(0)] * 3
for i in range(2,-1,-1):
    solution[i] = (matrices[-1][i][3] - sum(matrices[-1][i][j]*solution[j] for j in range(i+1,3)))/matrices[-1][i][i]
assert solution == [2,3,-1]
assert all(sum(r[j]*solution[j] for j in range(3)) == r[3] for r in original)

# title, matrix, pivot, active row, explanation lines, duration
scenes = [
 ('O sistema original',0,None,None,['2x + y − z = 8','−3x − y + 2z = −11','−2x + y + 2z = −3','Cada equação vira uma linha','da matriz aumentada [A | b].'],6500),
 ('Escolha o primeiro pivô',0,(0,0),None,['Pivô: 2','Vamos zerar os valores −3 e −2','abaixo dele, na coluna de x.','Regra: Rᵢ ← Rᵢ − m Rₖ','m = elemento / pivô'],6500),
 ('Elimine x da segunda linha',0,(0,0),1,['m = −3/2','R₂ ← R₂ + (3/2) R₁','−3 + (3/2) × 2 = 0','A operação vale para toda a linha,','incluindo o termo independente.'],6500),
 ('Segunda linha transformada',1,(0,0),1,['R₂ = [0, 1/2, 1/2 | 1]','O primeiro zero foi criado.','A segunda equação agora é:','(1/2)y + (1/2)z = 1'],4500),
 ('Elimine x da terceira linha',1,(0,0),2,['m = −2/2 = −1','R₃ ← R₃ + R₁','−2 + 2 = 0','1 + 1 = 2     e     2 − 1 = 1','−3 + 8 = 5'],6000),
 ('Primeira coluna eliminada',2,(1,1),2,['R₃ = [0, 2, 1 | 5]','O próximo pivô é 1/2.','Vamos zerar o 2 abaixo dele.','m = 2 / (1/2) = 4','R₃ ← R₃ − 4R₂'],6500),
 ('A matriz ficou triangular',3,(1,1),2,['R₃ = [0, 0, −1 | 1]','2 − 4 × (1/2) = 0','1 − 4 × (1/2) = −1','5 − 4 × 1 = 1','Todos os termos abaixo da','diagonal principal são zero.'],6500),
 ('Substituição regressiva: encontre z',3,None,2,['Resolvemos de baixo para cima.','Terceira linha: −z = 1','z = −1'],5500),
 ('Substituição regressiva: encontre y',3,None,1,['Segunda linha:','(1/2)y + (1/2)z = 1','Substitua z = −1:','(1/2)y − 1/2 = 1','y = 3'],6000),
 ('Substituição regressiva: encontre x',3,None,0,['Primeira linha: 2x + y − z = 8','Substitua y = 3 e z = −1:','2x + 3 − (−1) = 8','2x + 4 = 8','x = 2'],6000),
 ('Solução e conferência',3,None,None,['x = 2       y = 3       z = −1','Nas equações originais:','2(2) + 3 − (−1) = 8','−3(2) − 3 + 2(−1) = −11','−2(2) + 3 + 2(−1) = −3','As três igualdades são satisfeitas.'],8500),
]

def render(index, progress=1):
    title, mid, pivot, active, lines, duration = scenes[index]
    im = Image.new('RGB',(W,H), BG)
    d = ImageDraw.Draw(im)
    def text(x,y,s,size=26,color=INK,bold=False):
        d.text((x,y),s,font=font(size,bold),fill=color)
    text(44,27,'CÁLCULO NUMÉRICO  /  SISTEMAS LINEARES',18,BLUE,True)
    text(44,64,'Eliminação de Gauss',40,INK,True)
    text(44,123,title,28)
    d.rounded_rectangle((40,184,650,594),20,fill='white')
    d.rounded_rectangle((670,184,1160,594),20,fill='white')
    text(696,206,'PASSO A PASSO',17,BLUE,True)
    for j,line in enumerate(lines):
        text(696,251+j*48,line,23,GREEN if index==10 and j==0 else INK,j==0)
    xs = [185,310,435,575]
    ys = [310,409,508]
    for x,label in zip(xs,['x','y','z','b']):
        d.text((x,223),label,font=font(22,True),fill=MUTED,anchor='mm')
    if active is not None:
        y = ys[active]
        d.rounded_rectangle((123,y-37,619,y+37),12,fill='#e9f0ff')
    if pivot:
        r,c = pivot
        x,y = xs[c],ys[r]
        d.rounded_rectangle((x-43,y-36,x+43,y+36),12,fill=GOLD)
    for r,row in enumerate(matrices[mid]):
        d.text((82,ys[r]),f'R{r+1}',font=font(20),fill=MUTED,anchor='mm')
        for c,v in enumerate(row):
            s = str(v).replace('-','−')
            d.text((xs[c],ys[r]),s,font=font(36,True),fill=GREEN if v==0 else INK,anchor='mm')
    d.line([(137,267),(119,267),(119,553),(137,553)],fill=INK,width=3)
    d.line([(607,267),(625,267),(625,553),(607,553)],fill=INK,width=3)
    d.line((501,269,501,551),fill='#b3bfd0',width=2)
    d.rounded_rectangle((44,619,66,641),5,fill=GOLD)
    text(78,617,'Pivô',19,MUTED)
    d.rounded_rectangle((183,619,205,641),5,fill='#e9f0ff')
    text(218,617,'Linha em foco',19,MUTED)
    text(428,617,'0',20,GREEN,True)
    text(455,617,'Coeficiente eliminado',19,MUTED)
    text(44,674,'Operações equivalentes → forma triangular → substituição regressiva',21,INK)
    text(1040,675,f'{index+1:02d} / {len(scenes)}',20,BLUE,True)
    d.rounded_rectangle((44,718,1156,725),3,fill='#dce3ef')
    d.rounded_rectangle((44,718,44+int(1112*(index+progress)/len(scenes)),725),3,fill=BLUE)
    return im

frames, durations = [], []
for i,scene in enumerate(scenes):
    # A moving progress bar makes each long, readable step visibly animated.
    for tick in range(10):
        frames.append(render(i,(tick+1)/10))
        durations.append(scene[-1]//10)
frames[0].save(OUT/'eliminacao_gauss.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
render(10).save(OUT/'previa_gauss.png')
with Image.open(OUT/'eliminacao_gauss.gif') as gif:
    assert gif.n_frames == len(frames)
    assert gif.size == (W,H)
print(f'GIF validado: {len(frames)} quadros; {sum(durations)/1000:.1f} s; solução verificada.')
