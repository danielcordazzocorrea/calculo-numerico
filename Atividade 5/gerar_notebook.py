"""Gera e executa a entrega em formato Jupyter."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

def formatar_markdown(texto):
    """Usa delimitadores matemáticos compatíveis com o Markdown do Jupyter."""
    barra = chr(92)
    return (texto.replace(barra + "[", "$$")
            .replace(barra + "]", "$$")
            .replace(barra + "(", "$")
            .replace(barra + ")", "$"))

pasta = Path(__file__).resolve().parent
texto = (pasta / "RESOLUCAO.md").read_text(encoding="utf-8")
codigo = (pasta / "atividade_5.py").read_text(encoding="utf-8")
inicio, resto = texto.split("## 4. Implementação de Gauss sem pivoteamento")
parte4, parte5 = resto.split("## 5. Modelo de balanço térmico")
nb = nbformat.v4.new_notebook()
nb.cells = [
    nbformat.v4.new_markdown_cell(inicio),
    nbformat.v4.new_markdown_cell("## 4. Implementação de Gauss sem pivoteamento" + parte4),
    nbformat.v4.new_code_cell(codigo.split('if __name__ ==')[0]),
    nbformat.v4.new_code_cell('''solucao_2 = comparar("Exercício 4 — sistema do exercício 2",
    [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
    np.array([8, -11, -3]), [2, 3, -1])'''),
    nbformat.v4.new_markdown_cell("## 5. Modelo de balanço térmico" + parte5),
    nbformat.v4.new_code_cell('''temperaturas = comparar("Exercício 5 — balanço térmico",
    [[4, -1, 0], [-1, 4, -1], [0, -1, 3]],
    np.array([15, 10, 10]), [5, 5, 5])'''),
]
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
}
# Cada exercício manual fica em uma célula própria para facilitar a leitura.
celulas = []
for celula in nb.cells:
    if celula.cell_type == "markdown":
        secoes = formatar_markdown(celula.source).split("\n## ")
        for indice, secao in enumerate(secoes):
            celulas.append(nbformat.v4.new_markdown_cell(
                secao if indice == 0 else "## " + secao))
    else:
        celulas.append(celula)
nb.cells = celulas
NotebookClient(nb, timeout=120, kernel_name="python3").execute()
nbformat.write(nb, pasta / "Atividade_5_Sistemas_Lineares.ipynb")
print("Notebook executado e salvo com os resultados e verificações.")
