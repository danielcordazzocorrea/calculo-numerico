# O que escrever no papel — Gauss–Seidel

Os dois quadros abaixo registram o conteúdo de referência das páginas manuscritas. Para a entrega, use as fotos das páginas que você escreveu à mão.

## Página 1 — questões 1, 2 e 3

```text
Cálculo Numérico — Prof.ª Raquel Lobosco
Lista de exercícios: método de Gauss–Seidel

1. Forma matricial

O sistema é A u = b, com:

    [ 10  -1   2 ]        [ x ]        [   6 ]
A = [ -1  11  -1 ],   u = [ y ],   b = [  22 ].
    [  2  -1  10 ]        [ z ]        [ -10 ]

2. Dominância diagonal por linhas

Linha 1: |10| = 10 > |-1| + |2| = 3.
Linha 2: |11| = 11 > |-1| + |-1| = 2.
Linha 3: |10| = 10 > |2| + |-1| = 3.

Logo, A é estritamente diagonalmente dominante por linhas.
Essa propriedade garante a convergência do método de
Gauss–Seidel para qualquer aproximação inicial.

3. Fórmulas iterativas

x^(k) = [6 + y^(k-1) - 2z^(k-1)] / 10
y^(k) = [22 + x^(k) + z^(k-1)] / 11
z^(k) = [-10 - 2x^(k) + y^(k)] / 10

Em cada iteração, primeiro calculo o novo x; depois o novo y
usando esse x; por fim calculo o novo z usando os novos x e y.
```

## Página 2 — questão 4

```text
4. Três primeiras iterações

Aproximação inicial: (x^(0), y^(0), z^(0)) = (0, 0, 0).
O número entre parênteses indica a iteração, não uma potência.

Iteração 1

x^(1) = [6 + 0 - 2(0)] / 10 = 0,6
y^(1) = [22 + 0,6 + 0] / 11 ≈ 2,0545454545
z^(1) = [-10 - 2(0,6) + 2,0545454545] / 10
      ≈ -0,9145454545

Iteração 2

x^(2) = [6 + 2,0545454545 - 2(-0,9145454545)] / 10
      ≈ 0,9883636364
y^(2) = [22 + 0,9883636364 - 0,9145454545] / 11
      ≈ 2,0067107438
z^(2) = [-10 - 2(0,9883636364) + 2,0067107438] / 10
      ≈ -0,9970016529

Iteração 3

x^(3) = [6 + 2,0067107438 - 2(-0,9970016529)] / 10
      ≈ 1,0000714050
y^(3) = [22 + 1,0000714050 - 0,9970016529] / 11
      ≈ 2,0002790684
z^(3) = [-10 - 2(1,0000714050) + 2,0002790684] / 10
      ≈ -0,9999863742

Os valores mostrados são aproximações decimais.
```
