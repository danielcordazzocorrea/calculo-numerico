from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

base = Path(__file__).resolve().parent / 'resultados'
df = pd.read_csv(base / 'tabela_resultados.csv')
rows = []
for _, r in df.iterrows():
    initial = str(r['Valores iniciais']).replace('.0', '')
    if r['Método'] == 'Bisseção':
        initial = initial.replace('(', '[').replace(')', ']')
    rows.append([r['Função'], r['Método'], initial,
                 f"{r['Raiz aproximada']:.9f}", f"{r['|f(x)| final']:.2e}",
                 r['Iterações/resultado']])
fig, ax = plt.subplots(figsize=(13, 7.2), facecolor='white')
ax.axis('off')
fig.text(.035, .945, 'Resultados dos métodos numéricos', fontsize=21, weight='bold', color='#18364e')
fig.text(.035, .9, 'Tolerância: 10⁻⁶  •  Limite: 100 iterações  •  Critério: |f(x)| < tolerância', fontsize=12, color='#526579')
table = ax.table(cellText=rows,
    colLabels=['Função', 'Método', 'Valores iniciais', 'Raiz aproximada', '|f(x)| final', 'Iterações / resultado'],
    colWidths=[.20, .115, .135, .18, .13, .24], cellLoc='left', colLoc='left', bbox=[0, 0, 1, 1])
table.auto_set_font_size(False)
table.set_fontsize(11)
for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor('white')
    cell.set_linewidth(1.5)
    cell.PAD = .09
    if row == 0:
        cell.set_facecolor('#18364e')
        cell.set_text_props(color='white', weight='bold')
    else:
        cell.set_facecolor('#edf3f8' if ((row-1)//3)%2 == 0 else '#f8fafc')
        cell.set_text_props(color='#18364e')
fig.subplots_adjust(left=.03, right=.97, bottom=.08, top=.855)
fig.text(.035, .035, 'Valores arredondados para apresentação; resíduos calculados com as aproximações completas.', fontsize=10, color='#526579')
fig.savefig(base / 'tabela_mathcha.png', dpi=200)
plt.close(fig)
print(base / 'tabela_mathcha.png')
