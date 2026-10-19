"""Gera notebook executável e PDF de estudo a partir da solução verificada."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import nbformat as nbf

from gauss_seidel import gauss_seidel


PASTA = Path(__file__).resolve().parent
LINK_CODIGO = (
    "https://colab.research.google.com/github/danielcordazzocorrea/"
    "calculo-numerico/blob/main/tarefa%20gauss/Gauss_Seidel_Lista.ipynb"
)
LINK_GITHUB = (
    "https://github.com/danielcordazzocorrea/calculo-numerico/"
    "blob/main/tarefa%20gauss/Gauss_Seidel_Lista.ipynb"
)


def notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
        "colab": {"name": "Gauss_Seidel_Lista.ipynb", "provenance": []},
    }
    fonte = (PASTA / "gauss_seidel.py").read_text(encoding="utf-8")
    funcoes = fonte.split("def main():")[0]
    nb.cells = [
        nbf.v4.new_markdown_cell(
            "# Lista de exercícios — Gauss–Seidel\n"
            "**Cálculo Numérico — Prof.ª Raquel Lobosco**\n\n"
            "Sistema: $10x-y+2z=6$, $-x+11y-z=22$, $2x-y+10z=-10$. "
            "Aproximação inicial $(0,0,0)$; parada quando "
            "$\\|\\mathbf{x}^{(k)}-\\mathbf{x}^{(k-1)}\\|_\\infty<10^{-5}$."
        ),
        nbf.v4.new_markdown_cell(
            "## 1. Forma matricial\n"
            "$$A=\\begin{bmatrix}10&-1&2\\\\-1&11&-1\\\\2&-1&10\\end{bmatrix},"
            "\\quad \\mathbf{x}=\\begin{bmatrix}x\\\\y\\\\z\\end{bmatrix},"
            "\\quad \\mathbf{b}=\\begin{bmatrix}6\\\\22\\\\-10\\end{bmatrix}. $$\n"
            "## 2. Dominância diagonal\n"
            "Linha 1: $|10|=10>|-1|+|2|=3$; "
            "linha 2: $|11|=11>|-1|+|-1|=2$; "
            "linha 3: $|10|=10>|2|+|-1|=3$. "
            "Logo, $A$ é estritamente diagonalmente dominante por linhas, "
            "o que garante a convergência do método para qualquer chute inicial.\n"
            "## 3. Fórmulas iterativas\n"
            "$$x^{(k)}=\\frac{6+y^{(k-1)}-2z^{(k-1)}}{10},\\quad"
            "y^{(k)}=\\frac{22+x^{(k)}+z^{(k-1)}}{11},\\quad"
            "z^{(k)}=\\frac{-10-2x^{(k)}+y^{(k)}}{10}. $$\n"
            "Cada equação usa imediatamente as componentes já atualizadas."
        ),
        nbf.v4.new_markdown_cell(
            "## 4. Três primeiras iterações\n"
            "Com $\\mathbf{x}^{(0)}=(0,0,0)$:\n\n"
            "**$k=1$:** $x^{(1)}=(6+0-2\\cdot0)/10=0,6$; "
            "$y^{(1)}=(22+0,6+0)/11=2,0545454545$; "
            "$z^{(1)}=(-10-2\\cdot0,6+2,0545454545)/10=-0,9145454545$.\n\n"
            "**$k=2$:** $x^{(2)}=(6+2,0545454545-2(-0,9145454545))/10=0,9883636364$; "
            "$y^{(2)}=(22+0,9883636364-0,9145454545)/11=2,0067107438$; "
            "$z^{(2)}=(-10-2(0,9883636364)+2,0067107438)/10=-0,9970016529$.\n\n"
            "**$k=3$:** $x^{(3)}=(6+2,0067107438-2(-0,9970016529))/10=1,0000714050$; "
            "$y^{(3)}=(22+1,0000714050-0,9970016529)/11=2,0002790684$; "
            "$z^{(3)}=(-10-2(1,0000714050)+2,0002790684)/10=-0,9999863742$. "
            "Os valores exibidos são arredondados; os cálculos usam precisão completa."
        ),
        nbf.v4.new_markdown_cell("## 5. Código Python"),
        nbf.v4.new_code_cell(funcoes),
        nbf.v4.new_markdown_cell("## 6. Tabela de iterações"),
        nbf.v4.new_code_cell(
            "linhas = gauss_seidel()\n"
            "print(f\"{'k':>2} {'x':>14} {'y':>14} {'z':>14} {'erro infinito':>16}\")\n"
            "for k, x, y, z, erro in linhas:\n"
            "    e = f'{erro:.10e}' if erro is not None else '—'\n"
            "    print(f'{k:2d} {x:14.10f} {y:14.10f} {z:14.10f} {e:>16}')\n"
            "print(f'\\nIterações: {len(linhas)-1}')\n"
            "print(f'Solução aproximada: {linhas[-1][1:4]}')"
        ),
        nbf.v4.new_markdown_cell("## 7. Gráficos"),
        nbf.v4.new_code_cell(
            "# Funciona no Colab e salva dois PNGs na pasta da sessão.\n"
            "salvar_graficos(linhas)\n"
            "from IPython.display import display, Image\n"
            "display(Image(filename='aproximacoes.png'))\n"
            "display(Image(filename='erro_log.png'))"
        ),
        nbf.v4.new_markdown_cell(
            "## Conclusão\n"
            "O critério estrito de parada é satisfeito em $k=6$, "
            "com solução aproximada $(1,0000000269; 1,9999999762; -1,0000000078)$. "
            "A solução exata $(1,2,-1)$ confirma o resultado."
        ),
    ]
    (PASTA / "Gauss_Seidel_Lista.ipynb").write_text(nbf.writes(nb), encoding="utf-8")


def pagina_texto(pdf, titulo, linhas, rodape=None, tamanho=11):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    fig.text(0.08, 0.955, "CÁLCULO NUMÉRICO  /  LISTA DE EXERCÍCIOS", color="#536879", fontsize=9)
    fig.text(0.08, 0.915, titulo, color="#172f44", fontsize=19, weight="bold")
    y = 0.865
    for linha in linhas:
        if linha.startswith("## "):
            y -= 0.027
            fig.text(0.08, y, linha[3:], fontsize=tamanho + 2, weight="bold", color="#165d79")
            y -= 0.039
        elif linha == "":
            y -= 0.020
        elif linha.startswith("https://"):
            fig.text(0.08, y, linha, fontsize=7.3, color="#135e9c",
                     family="DejaVu Sans", url=linha)
            y -= 0.031
        else:
            fig.text(0.08, y, linha, fontsize=tamanho, color="#1c2833", family="DejaVu Sans")
            y -= 0.031
    if rodape:
        fig.text(0.08, 0.047, rodape, fontsize=8, color="#536879")
    pdf.savefig(fig)
    plt.close(fig)


def pagina_grafico(pdf, titulo, imagem):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    fig.text(0.08, 0.95, titulo, fontsize=18, weight="bold", color="#172f44")
    ax = fig.add_axes([0.07, 0.31, 0.86, 0.49])
    ax.imshow(plt.imread(PASTA / imagem))
    ax.axis("off")
    fig.text(0.08, 0.24, "Fonte: execução do código Python da atividade.", fontsize=10)
    pdf.savefig(fig)
    plt.close(fig)


def pagina_foto(pdf, titulo, imagem, observacao=None):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    fig.text(0.08, 0.955, titulo, fontsize=16, weight="bold", color="#172f44")
    ax = fig.add_axes([0.07, 0.115, 0.86, 0.80])
    ax.imshow(plt.imread(PASTA / imagem))
    ax.axis("off")
    if observacao:
        fig.text(0.08, 0.075, observacao, fontsize=8.5, color="#9b2f2f")
    pdf.savefig(fig)
    plt.close(fig)


def pdf():
    linhas = gauss_seidel()
    destino = PASTA / "Entrega_Gauss_Seidel.pdf"
    with PdfPages(destino, metadata={"Title": "Lista de exercícios — Gauss-Seidel"}) as doc:
        if (PASTA / "foto1.jpeg").exists():
            pagina_foto(doc, "Resolução manuscrita · questões 1 a 3", "foto1.jpeg")
        if (PASTA / "foto2.jpeg").exists():
            pagina_foto(
                doc, "Resolução manuscrita · questão 4", "foto2.jpeg",
                "Correção: na iteração 3, y = 2,000279 e z = -0,999986 (ver cálculo digitado).",
            )
        pagina_texto(doc, "Método de Gauss–Seidel", [
            "Prof.ª Raquel Lobosco  |  Sistemas lineares",
            "",
            "## 1. Forma matricial A x = b",
            "A = [[10, -1, 2], [-1, 11, -1], [2, -1, 10]]",
            "x = [x, y, z]^T                 b = [6, 22, -10]^T",
            "",
            "## 2. Dominância diagonal por linhas",
            "Linha 1: |10| = 10 > |-1| + |2| = 3",
            "Linha 2: |11| = 11 > |-1| + |-1| = 2",
            "Linha 3: |10| = 10 > |2| + |-1| = 3",
            "A dominância estrita garante convergência para qualquer ponto inicial.",
            "",
            "## 3. Fórmulas de atualização",
            "x(k) = [6 + y(k-1) - 2 z(k-1)] / 10",
            "y(k) = [22 + x(k) + z(k-1)] / 11",
            "z(k) = [-10 - 2 x(k) + y(k)] / 10",
            "Usamos x(k) e y(k) assim que são calculados.",
            "",
            "## 4. Ponto inicial",
            "(x(0), y(0), z(0)) = (0, 0, 0).",
        ], "A seção seguinte detalha as três primeiras iterações.")

        pagina_texto(doc, "Três primeiras iterações", [
            "## Iteração 1",
            "x(1) = (6 + 0 - 2·0)/10 = 0,6000000000",
            "y(1) = (22 + 0,6 + 0)/11 = 2,0545454545",
            "z(1) = (-10 - 2·0,6 + 2,0545454545)/10 = -0,9145454545",
            "",
            "## Iteração 2",
            "x(2) = [6 + 2,0545454545 - 2·(-0,9145454545)]/10",
            "       = 0,9883636364",
            "y(2) = [22 + 0,9883636364 - 0,9145454545]/11",
            "       = 2,0067107438",
            "z(2) = [-10 - 2·0,9883636364 + 2,0067107438]/10",
            "       = -0,9970016529",
            "",
            "## Iteração 3",
            "x(3) = [6 + 2,0067107438 - 2·(-0,9970016529)]/10",
            "       = 1,0000714050",
            "y(3) = [22 + 1,0000714050 - 0,9970016529]/11",
            "       = 2,0002790684",
            "z(3) = [-10 - 2·1,0000714050 + 2,0002790684]/10",
            "       = -0,9999863742",
        ], "Valores exibidos arredondados; as iterações usam precisão completa.", tamanho=10)

        pagina_texto(doc, "Código Python · método e critério", [
            "## Implementação essencial",
            "def gauss_seidel(tol=1e-5, max_iter=100):",
            "    x = y = z = 0.0",
            "    linhas = [(0, x, y, z, None)]",
            "    for k in range(1, max_iter + 1):",
            "        anterior = (x, y, z)",
            "        x = (6 + y - 2*z) / 10",
            "        y = (22 + x + z) / 11",
            "        z = (-10 - 2*x + y) / 10",
            "        erro = max(abs(a-b) for a, b in",
            "                   zip((x, y, z), anterior))",
            "        linhas.append((k, x, y, z, erro))",
            "        if erro < tol:",
            "            return linhas",
            "    raise RuntimeError('Sem convergência')",
            "",
            "## Resultado",
            "Critério: ||x(k) - x(k-1)|| infinito < 10^-5",
            "Iterações realizadas: 6",
            "Solução: (1,0000000269; 1,9999999762; -1,0000000078)",
            "Erro da sexta iteração: 1,2626069386 × 10^-6",
            "Solução exata para comparação: (1, 2, -1).",
            "",
            "## Link para o código no Colab",
            LINK_CODIGO,
            "## Link direto para o código no GitHub",
            LINK_GITHUB,
        ], "O arquivo Gauss_Seidel_Lista.ipynb contém a versão completa para Colab.", tamanho=10)

        pagina_texto(doc, "Tabela de iterações", [
            "Critério de parada: erro entre iterações estritamente menor que 10^-5.",
            "",
            " k       x(k)              y(k)              z(k)           erro infinito",
            *[
                f" {k:<2}  {x:>13.10f}   {y:>13.10f}   {z:>13.10f}    "
                + (f"{erro:.5e}" if erro is not None else "—")
                for k, x, y, z, erro in linhas
            ],
            "",
            "Em k=5, o erro ainda é maior que a tolerância.",
            "Em k=6, o critério é atendido e o processo para.",
        ], tamanho=9)
        pagina_grafico(doc, "Evolução das aproximações", "aproximacoes.png")
        pagina_grafico(doc, "Erro entre iterações em escala logarítmica", "erro_log.png")


if __name__ == "__main__":
    notebook()
    pdf()
    print("Gerados: Gauss_Seidel_Lista.ipynb e Entrega_Gauss_Seidel.pdf")
