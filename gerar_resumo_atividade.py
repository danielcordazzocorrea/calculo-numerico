"""Gera um PNG único com o resumo da Atividade Prática I.

Personalização: altere somente as dataclasses na seção CONFIGURAÇÃO.
Dependências: numpy e matplotlib.
Execução: python gerar_resumo_atividade.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import PercentFormatter


# ============================== CONFIGURAÇÃO ==============================
@dataclass(frozen=True)
class Dados:
    valores_parte_a: dict[str, float] = field(default_factory=lambda: {
        "x₁ = 3,14159265": 3.14159265,
        "x₂ = 98,76543": 98.76543,
        "x₃ = 0,00498765": 0.00498765,
    })
    pressao_mmhg: tuple[float, ...] = (
        121.7, 120.4, 122.1, 119.8, 121.2,
        120.9, 122.4, 121.0, 120.2, 121.5,
    )
    raio_tubo_mm: float = 0.80
    comprimento_tubo_m: float = 0.20
    viscosidade_pa_s: float = 3.5e-3
    delta_p_tubo_pa: float = 1200.0
    raio_nano_nm: float = 50.0
    comprimento_nano_um: float = 10.0
    delta_p_nano_pa: float = 5000.0


@dataclass(frozen=True)
class Visual:
    titulo: str = "Cálculo Numérico • Atividade Prática I"
    subtitulo: str = "Erros numéricos, pressão arterial e sensibilidade da vazão"
    arquivo_saida: str = "resumo_atividade_pratica_I.png"
    github: str = "https://github.com/danielcordazzocorrea/calculo-numerico"
    largura_px: int = 2400
    altura_px: int = 1500
    dpi: int = 150
    fundo: str = "#F4F7FB"
    painel: str = "#FFFFFF"
    texto: str = "#172033"
    texto_secundario: str = "#5B6475"
    azul: str = "#246BCE"
    ciano: str = "#00A6A6"
    laranja: str = "#F28E2B"
    vermelho: str = "#E15759"
    verde: str = "#2A9D66"


DADOS = Dados()
VISUAL = Visual()


# ================================ CÁLCULOS ================================
def truncar(valor: float, casas: int) -> float:
    fator = 10**casas
    return math.trunc(valor * fator) / fator


def arredondar(valor: float, casas: int) -> float:
    """Arredondamento decimal usual (metade para cima) para valores positivos."""
    fator = 10**casas
    return math.floor(valor * fator + 0.5) / fator


def vazao(raio_m: np.ndarray | float, mu: float, dp: float, comprimento: float):
    return np.pi * np.asarray(raio_m) ** 4 * dp / (8 * mu * comprimento)


def erro_percentual(exato: np.ndarray | float, aproximado: np.ndarray | float):
    return np.abs(np.asarray(exato) - np.asarray(aproximado)) / np.abs(exato) * 100


def preparar_resultados(d: Dados) -> dict[str, object]:
    pressao = np.asarray(d.pressao_mmhg)
    pressao_arred = np.floor(pressao + 0.5)
    pressao_trunc = np.trunc(pressao)

    raio_tubo_m = d.raio_tubo_mm * 1e-3
    q_tubo = float(vazao(raio_tubo_m, d.viscosidade_pa_s,
                         d.delta_p_tubo_pa, d.comprimento_tubo_m))
    raios_tubo_mm = np.linspace(0.70, 0.90, 101)
    q_tubo_curva = vazao(raios_tubo_mm * 1e-3, d.viscosidade_pa_s,
                         d.delta_p_tubo_pa, d.comprimento_tubo_m)

    raio_nano_m = d.raio_nano_nm * 1e-9
    comprimento_nano_m = d.comprimento_nano_um * 1e-6
    q_nano = float(vazao(raio_nano_m, d.viscosidade_pa_s,
                         d.delta_p_nano_pa, comprimento_nano_m))
    delta_nm = np.linspace(0.1, 5.0, 50)
    q_mais = vazao((d.raio_nano_nm + delta_nm) * 1e-9,
                   d.viscosidade_pa_s, d.delta_p_nano_pa, comprimento_nano_m)
    q_menos = vazao((d.raio_nano_nm - delta_nm) * 1e-9,
                    d.viscosidade_pa_s, d.delta_p_nano_pa, comprimento_nano_m)
    erro_exato = np.maximum(erro_percentual(q_nano, q_mais),
                            erro_percentual(q_nano, q_menos))
    erro_linear = 4 * delta_nm / d.raio_nano_nm * 100

    return locals()


# ================================ DESENHO =================================
def estilizar_eixo(ax, v: Visual, titulo: str) -> None:
    ax.set_facecolor(v.painel)
    ax.set_title(titulo, loc="left", fontsize=13, fontweight="bold",
                 color=v.texto, pad=12)
    ax.grid(axis="y", color="#DCE3ED", linewidth=0.8, alpha=0.85)
    ax.set_axisbelow(True)
    ax.tick_params(colors=v.texto_secundario, labelsize=9)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#CBD4E1")


def cartao(fig, posicao, rotulo, valor, detalhe, cor, v: Visual) -> None:
    ax = fig.add_axes(posicao)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch(
        (0, 0), 1, 1, boxstyle="round,pad=0.018,rounding_size=0.04",
        transform=ax.transAxes, facecolor=v.painel, edgecolor="#DFE5EE",
        linewidth=1.2,
    ))
    ax.add_patch(FancyBboxPatch(
        (0.035, 0.18), 0.018, 0.64, boxstyle="round,pad=0.002",
        transform=ax.transAxes, facecolor=cor, edgecolor="none",
    ))
    ax.text(0.085, 0.73, rotulo.upper(), color=v.texto_secundario,
            fontsize=9, fontweight="bold", transform=ax.transAxes)
    ax.text(0.085, 0.43, valor, color=v.texto, fontsize=18,
            fontweight="bold", transform=ax.transAxes)
    ax.text(0.085, 0.18, detalhe, color=v.texto_secundario, fontsize=9,
            transform=ax.transAxes)


def gerar_resumo(d: Dados = DADOS, v: Visual = VISUAL) -> Path:
    r = preparar_resultados(d)
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.unicode_minus": False})
    fig = plt.figure(figsize=(v.largura_px / v.dpi, v.altura_px / v.dpi),
                     dpi=v.dpi, facecolor=v.fundo)

    fig.text(0.045, 0.955, v.titulo, fontsize=25, fontweight="bold",
             color=v.texto, va="top")
    fig.text(0.045, 0.918, v.subtitulo, fontsize=12,
             color=v.texto_secundario, va="top")
    fig.text(0.955, 0.947, "SÍNTESE VISUAL", fontsize=9, fontweight="bold",
             color=v.azul, ha="right", va="top")

    media = float(r["pressao"].mean())
    media_arred = float(r["pressao_arred"].mean())
    media_trunc = float(r["pressao_trunc"].mean())
    cartao(fig, [0.045, 0.795, 0.285, 0.095], "Pressão média",
           f"{media:.2f} mmHg", f"10 medições • amplitude {np.ptp(r['pressao']):.1f} mmHg",
           v.azul, v)
    cartao(fig, [0.357, 0.795, 0.285, 0.095], "Vazão no tubo",
           f"{r['q_tubo']:.3e} m³/s", f"r = {d.raio_tubo_mm:.2f} mm • Q ∝ r⁴",
           v.ciano, v)
    cartao(fig, [0.670, 0.795, 0.285, 0.095], "Vazão no nanocateter",
           f"{r['q_nano']:.3e} m³/s", f"r = {d.raio_nano_nm:.0f} nm • escala nanométrica",
           v.laranja, v)

    gs = fig.add_gridspec(2, 2, left=0.055, right=0.955, bottom=0.205,
                          top=0.745, hspace=0.48, wspace=0.22)

    # Parte A: reúne os três valores, mostrando a tendência global.
    ax = fig.add_subplot(gs[0, 0])
    estilizar_eixo(ax, v, "A • Erro absoluto médio × casas decimais")
    casas = np.arange(5)
    erros_t, erros_a = [], []
    for n in casas:
        erros_t.append(np.mean([abs(x - truncar(x, int(n))) for x in d.valores_parte_a.values()]))
        erros_a.append(np.mean([abs(x - arredondar(x, int(n))) for x in d.valores_parte_a.values()]))
    ax.semilogy(casas, erros_t, "o-", color=v.vermelho, linewidth=2.2,
                label="Truncamento")
    ax.semilogy(casas, erros_a, "s--", color=v.azul, linewidth=2.2,
                label="Arredondamento")
    ax.set(xlabel="Casas decimais (n)", ylabel="Erro absoluto médio")
    ax.set_xticks(casas)
    ax.legend(frameon=False, fontsize=9)

    # Parte B: as três séries preservam a sequência das medições.
    ax = fig.add_subplot(gs[0, 1])
    estilizar_eixo(ax, v, "B • Pressão: original × aproximações inteiras")
    medicao = np.arange(1, len(r["pressao"]) + 1)
    ax.plot(medicao, r["pressao"], "o-", color=v.texto, linewidth=2,
            label=f"Original ({media:.2f})")
    ax.plot(medicao, r["pressao_arred"], "s--", color=v.azul, linewidth=1.8,
            label=f"Arred. ({media_arred:.2f})")
    ax.plot(medicao, r["pressao_trunc"], "^:", color=v.laranja, linewidth=2,
            label=f"Trunc. ({media_trunc:.2f})")
    ax.set(xlabel="Medição", ylabel="Pressão (mmHg)")
    ax.set_xticks(medicao)
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="lower center")

    # Parte C: curva normalizada evidencia a quarta potência sem notação minúscula.
    ax = fig.add_subplot(gs[1, 0])
    estilizar_eixo(ax, v, "C • Sensibilidade da vazão ao raio (Q ∝ r⁴)")
    q_rel = r["q_tubo_curva"] / r["q_tubo"] * 100
    ax.plot(r["raios_tubo_mm"], q_rel, color=v.ciano, linewidth=2.8)
    ax.axvline(d.raio_tubo_mm, color=v.texto_secundario, linestyle="--", linewidth=1)
    ax.scatter([d.raio_tubo_mm], [100], s=55, color=v.ciano, edgecolor="white", zorder=3)
    ax.fill_between(r["raios_tubo_mm"], q_rel, 0, color=v.ciano, alpha=0.08)
    ax.set(xlabel="Raio (mm)", ylabel="Vazão relativa à referência")
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.annotate("referência", (d.raio_tubo_mm, 100), xytext=(8, -18),
                textcoords="offset points", fontsize=8, color=v.texto_secundario)

    # Parte D: comparação solicitada entre erro exato e aproximação 4Δr/r.
    ax = fig.add_subplot(gs[1, 1])
    estilizar_eixo(ax, v, "D • Nanocateter: erro geométrico máximo")
    ax.plot(r["delta_nm"], r["erro_exato"], color=v.laranja, linewidth=2.8,
            label="Modelo exato")
    ax.plot(r["delta_nm"], r["erro_linear"], color=v.azul, linewidth=2,
            linestyle="--", label="Aprox. linear 4Δr/r")
    ax.fill_between(r["delta_nm"], r["erro_linear"], r["erro_exato"],
                    color=v.laranja, alpha=0.12)
    ax.set(xlabel="Incerteza no raio Δr (nm)", ylabel="Erro máximo em Q")
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.legend(frameon=False, fontsize=9)

    # Conclusão dentro do PNG.
    conclusao = (
        "CONCLUSÃO  •  Mais casas decimais reduzem os erros, e o arredondamento mantém a média da pressão "
        f"mais próxima da original (Ea = {abs(media-media_arred):.2f} contra {abs(media-media_trunc):.2f} mmHg).  "
        "Como Q depende de r⁴, pequenas incertezas no raio são amplificadas, um efeito crítico no nanocateter. "
        "A aproximação 4Δr/r é adequada apenas para perturbações pequenas."
    )
    ax_footer = fig.add_axes([0.045, 0.055, 0.91, 0.095])
    ax_footer.axis("off")
    ax_footer.add_patch(FancyBboxPatch(
        (0, 0), 1, 1, boxstyle="round,pad=0.018,rounding_size=0.035",
        transform=ax_footer.transAxes, facecolor="#E9F1FD", edgecolor="#C9DAF5",
    ))
    ax_footer.text(0.025, 0.5, conclusao, transform=ax_footer.transAxes,
                   va="center", color=v.texto, fontsize=10.5, wrap=True)
    fig.text(0.5, 0.022, v.github, ha="center", va="center",
             color=v.azul, fontsize=9.5, fontweight="bold")

    destino = Path(v.arquivo_saida).resolve()
    fig.savefig(destino, dpi=v.dpi, facecolor=fig.get_facecolor(),
                metadata={"Title": v.titulo, "Author": "Resumo gerado em Python"})
    plt.close(fig)
    return destino


if __name__ == "__main__":
    saida = gerar_resumo()
    print(f"PNG gerado: {saida}")
