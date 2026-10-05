# Conteúdo para o dashboard no Mathcha

## Identificação

Atividade prática III — Cálculo Numérico  
Prof.ª Raquel J. Lobosco  
Daniel Cordazzo e Rodrigo Valle

## Objetivo e configuração

Encontrar raízes de x² − 2, x³ − x − 2, exp(−x) − x e x³ − 2x + 2 com bisseção, Newton e secante. Tolerância: 10⁻⁶. Limite: 100 iterações. Sucesso quando |f(x)| < 10⁻⁶.

## Resultados e ilustrações

A tabela completa est? dispon?vel em `resultados/tabela_resultados.html` e `resultados/tabela_resultados.csv`.

Anima??es e gr?fico:

- `resultados/bissecao_f1.gif`: intervalo e redução pela metade.
- `resultados/newton_f2.gif`: tangentes e interseção com o eixo x.
- `resultados/secante_f3.gif`: retas pelos dois pontos anteriores.
- `resultados/comparacao_convergencia.png`: comparação de resíduos.


## Análise para acompanhar a tabela

Os três métodos convergem nos quatro casos com os valores iniciais sugeridos. As raízes são aproximadamente 1,414214; 1,521380; 0,567143 e −1,769292. A bisseção mantém uma raiz em um intervalo com troca de sinal para funções contínuas. Newton converge rapidamente perto de raízes simples, mas depende da derivada e do valor inicial. A secante dispensa a derivada, porém pode apresentar denominador quase nulo. Em f4, Newton iniciado em zero entra no ciclo 0 → 1 → 0 e falha por atingir 100 iterações; iniciado em −2 converge.
