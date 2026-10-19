"""Resolução da lista de Gauss-Seidel da Prof.ª Raquel Lobosco.

Compatível com Python 3, Jupyter e Google Colab. Requer matplotlib apenas
para gerar os gráficos. Execute: python gauss_seidel.py
"""

from pathlib import Path

import matplotlib.pyplot as plt


TOLERANCIA = 1e-5
MAX_ITERACOES = 100


def gauss_seidel(tolerancia=TOLERANCIA, max_iteracoes=MAX_ITERACOES):
    """Devolve linhas (k, x, y, z, erro) até a primeira diferença < tolerância."""
    if tolerancia <= 0 or max_iteracoes < 1:
        raise ValueError("Use tolerância positiva e ao menos uma iteração.")

    x = y = z = 0.0
    linhas = [(0, x, y, z, None)]
    for k in range(1, max_iteracoes + 1):
        anterior = (x, y, z)
        x = (6 + y - 2 * z) / 10
        y = (22 + x + z) / 11
        z = (-10 - 2 * x + y) / 10
        erro = max(abs(atual - velho) for atual, velho in zip((x, y, z), anterior))
        linhas.append((k, x, y, z, erro))
        if erro < tolerancia:
            return linhas
    raise RuntimeError(f"Não convergiu em {max_iteracoes} iterações.")


def salvar_graficos(linhas, pasta=Path(".")):
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    ks = [linha[0] for linha in linhas]

    fig, ax = plt.subplots(figsize=(8, 4.8), layout="constrained")
    for indice, nome in ((1, "x"), (2, "y"), (3, "z")):
        ax.plot(ks, [linha[indice] for linha in linhas], marker="o", label=nome)
    ax.set(xlabel="Iteração k", ylabel="Aproximação", title="Gauss–Seidel: evolução das incógnitas")
    ax.set_xticks(ks)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.savefig(pasta / "aproximacoes.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.8), layout="constrained")
    ax.semilogy(ks[1:], [linha[4] for linha in linhas[1:]], marker="o")
    ax.axhline(TOLERANCIA, color="crimson", ls="--", label="tolerância = 10⁻⁵")
    ax.set(xlabel="Iteração k", ylabel="Norma infinito da diferença",
           title="Gauss–Seidel: erro entre iterações")
    ax.set_xticks(ks[1:])
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.savefig(pasta / "erro_log.png", dpi=180)
    plt.close(fig)


def main():
    linhas = gauss_seidel()
    print(f"{'k':>2} {'x':>14} {'y':>14} {'z':>14} {'erro infinito':>16}")
    for k, x, y, z, erro in linhas:
        print(f"{k:2d} {x:14.10f} {y:14.10f} {z:14.10f} "
              + (f"{erro:16.10e}" if erro is not None else f"{'—':>16}"))
    _, x, y, z, erro = linhas[-1]
    print(f"\nSolução aproximada: ({x:.10f}, {y:.10f}, {z:.10f})")
    print(f"Iterações: {len(linhas) - 1}; erro final: {erro:.10e}")
    salvar_graficos(linhas, Path(__file__).resolve().parent)


if __name__ == "__main__":
    main()
