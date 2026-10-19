"""Renderiza as duas páginas de referência a partir do Markdown."""

from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont


PASTA = Path(__file__).resolve().parent
FONTE = Path(r"C:\Windows\Fonts\consola.ttf")
LARGURA, ALTURA = 2480, 3508  # A4, aproximadamente 300 dpi
MARGEM = 190


def gerar():
    markdown = (PASTA / "O_QUE_ESCREVER_NO_PAPEL.md").read_text(encoding="utf-8")
    paginas = re.findall(r"```text\n(.*?)\n```", markdown, re.DOTALL)
    if len(paginas) != 2:
        raise ValueError("Esperados exatamente dois blocos de texto no Markdown.")

    fonte = ImageFont.truetype(str(FONTE), 49)
    cabecalho = ImageFont.truetype(str(FONTE), 30)
    for numero, conteudo in enumerate(paginas, start=1):
        imagem = Image.new("RGB", (LARGURA, ALTURA), "white")
        desenho = ImageDraw.Draw(imagem)
        desenho.rectangle((0, 0, LARGURA, 22), fill="#1e5875")
        desenho.text((MARGEM, 90), f"MODELO PARA COPIAR NO PAPEL  /  PÁGINA {numero}",
                     font=cabecalho, fill="#63717b")
        desenho.line((MARGEM, 155, LARGURA - MARGEM, 155), fill="#d2dce2", width=3)

        y = 215
        for linha in conteudo.splitlines():
            if linha.startswith(("1. ", "2. ", "3. ", "4. ", "Iteração")):
                cor = "#155473"
            else:
                cor = "#17232c"
            largura_texto = desenho.textbbox((0, 0), linha, font=fonte)[2]
            if largura_texto > LARGURA - 2 * MARGEM:
                raise ValueError(f"Linha longa demais na página {numero}: {linha}")
            desenho.text((MARGEM, y), linha, font=fonte, fill=cor)
            y += 79 if linha else 55
        if y > ALTURA - 120:
            raise ValueError(f"A página {numero} não cabe na imagem.")

        destino = PASTA / f"modelo_pagina_{numero}.png"
        imagem.save(destino, optimize=True)
        print(destino)


if __name__ == "__main__":
    gerar()
