# Atividade 5 — Sistemas lineares e implementação numérica realizado por Daniel Cordazzo e Rodrigo Valle

Resolução baseada em `calculo_numerico-atividade-5-10.pdf`.

## 1. Sistemas na forma matricial

### a)

$$
A=\begin{bmatrix}2&1\\1&-3\end{bmatrix},\qquad
\mathbf{x}=\begin{bmatrix}x\\y\end{bmatrix},\qquad
b=\begin{bmatrix}7\\-5\end{bmatrix}.
$$

Logo, o sistema é $A\mathbf{x}=b$. A matriz A contém os coeficientes das incógnitas; o vetor de incógnitas contém x e y; b contém os termos independentes.

### b)

$$
A=\begin{bmatrix}1&2&-1\\3&-1&2\\2&1&1\end{bmatrix},\qquad
\mathbf{x}=\begin{bmatrix}x\\y\\z\end{bmatrix},\qquad
b=\begin{bmatrix}2\\9\\7\end{bmatrix}.
$$

Cada linha de A corresponde a uma equação, mantendo a ordem x, y, z.

## 2. Eliminação de Gauss manual

A matriz aumentada inicial é:

$$
\left[\begin{array}{rrr|r}2&1&-1&8\\-3&-1&2&-11\\-2&1&2&-3\end{array}\right].
$$

Aplicando $L_2\leftarrow L_2+\frac32L_1$:

$$
\left[\begin{array}{rrr|r}2&1&-1&8\\0&\frac12&\frac12&1\\-2&1&2&-3\end{array}\right].
$$

Aplicando $L_3\leftarrow L_3+L_1$:

$$
\left[\begin{array}{rrr|r}2&1&-1&8\\0&\frac12&\frac12&1\\0&2&1&5\end{array}\right].
$$

Aplicando $L_3\leftarrow L_3-4L_2$:

$$
\left[\begin{array}{rrr|r}2&1&-1&8\\0&\frac12&\frac12&1\\0&0&-1&1\end{array}\right].
$$

Substituição regressiva:

$$
-z=1\Rightarrow z=-1,
\qquad \frac12y+\frac12(-1)=1\Rightarrow y=3,
\qquad 2x+3-(-1)=8\Rightarrow x=2.
$$

**Solução:** $(x,y,z)=(2,3,-1)$.

Conferência: $4+3+1=8$, $-6-3-2=-11$ e $-4+3-2=-3$.

## 3. Número de soluções

### a) Infinitas soluções

$$
\left[\begin{array}{rr|r}1&1&3\\2&2&6\end{array}\right]
\xrightarrow{L_2\leftarrow L_2-2L_1}
\left[\begin{array}{rr|r}1&1&3\\0&0&0\end{array}\right].
$$

A segunda linha expressa 0 = 0. Há uma variável livre: tomando $y=t$, obtemos $(x,y)=(3-t,t)$, para todo $t\in\mathbb R$. Os postos de A e da matriz aumentada são 1, menores que o número de incógnitas (2).

### b) Nenhuma solução

$$
\left[\begin{array}{rr|r}1&1&3\\2&2&7\end{array}\right]
\xrightarrow{L_2\leftarrow L_2-2L_1}
\left[\begin{array}{rr|r}1&1&3\\0&0&1\end{array}\right].
$$

A segunda linha exige 0 = 1, uma contradição. O posto de A é 1 e o da matriz aumentada é 2: o sistema é incompatível.

### c) Solução única

$$
\left[\begin{array}{rr|r}1&1&3\\2&-1&0\end{array}\right]
\xrightarrow{L_2\leftarrow L_2-2L_1}
\left[\begin{array}{rr|r}1&1&3\\0&-3&-6\end{array}\right]
\xrightarrow{L_2\leftarrow -L_2/3}
\left[\begin{array}{rr|r}1&1&3\\0&1&2\end{array}\right]
\xrightarrow{L_1\leftarrow L_1-L_2}
\left[\begin{array}{rr|r}1&0&1\\0&1&2\end{array}\right].
$$

Assim, $(x,y)=(1,2)$. Há pivô para cada incógnita; ambos os postos são 2.

## 4. Implementação de Gauss sem pivoteamento

O código comentado está em `atividade_5.py` e no notebook `Atividade_5_Sistemas_Lineares.ipynb`. Ele forma uma cópia da matriz aumentada, elimina os elementos abaixo de cada pivô e aplica substituição regressiva. Não troca linhas.

Para o exercício 2, tanto o algoritmo quanto `numpy.linalg.solve` fornecem **[2, 3, -1]**, com diferenças apenas de arredondamento de ponto flutuante. O resíduo $A\mathbf{x}-b$ é numericamente nulo.

Sem pivoteamento, um pivô zero impede a divisão, mesmo em alguns sistemas com solução única. Pivôs muito pequenos podem amplificar erros de arredondamento. O código detecta pivôs numericamente pequenos e informa a limitação; ele não classifica o sistema como singular só por esse motivo.

## 5. Modelo de balanço térmico

### a) Resolução manual

As equações são $4T_1-T_2=15$, $-T_1+4T_2-T_3=10$ e $-T_2+3T_3=10$.

$$
\left[\begin{array}{rrr|r}4&-1&0&15\\-1&4&-1&10\\0&-1&3&10\end{array}\right]
\xrightarrow{L_2\leftarrow L_2+\frac14L_1}
\left[\begin{array}{rrr|r}4&-1&0&15\\0&\frac{15}{4}&-1&\frac{55}{4}\\0&-1&3&10\end{array}\right].
$$

Aplicando $L_3\leftarrow L_3+\frac4{15}L_2$:

$$
\left[\begin{array}{rrr|r}4&-1&0&15\\0&\frac{15}{4}&-1&\frac{55}{4}\\0&0&\frac{41}{15}&\frac{41}{3}\end{array}\right].
$$

Substituição regressiva:

$$
T_3=\frac{41/3}{41/15}=5,
\qquad T_2=\frac{55/4+5}{15/4}=5,
\qquad T_1=\frac{15+5}{4}=5.
$$

**Resultado:** $T_1=T_2=T_3=5$, nas unidades de temperatura adotadas pelo modelo; o PDF não especifica a unidade.

### b) Solução em Python e interpretação

O mesmo algoritmo de Gauss e `numpy.linalg.solve` retornam **[5, 5, 5]**. Substituindo: $4(5)-5=15$, $-5+4(5)-5=10$ e $-5+3(5)=10$.

As três temperaturas desconhecidas são iguais e satisfazem o balanço imposto. Os termos independentes representam as contribuições térmicas prescritas no modelo; temperaturas iguais não implicam ausência de todas as trocas com o exterior. Os pivôs 4, 15/4 e 41/15 são não nulos, garantindo solução única.
