"""Exercícios 4 e 5: eliminação de Gauss sem pivoteamento."""

import numpy as np


def gauss_sem_pivoteamento(A, b, exibir_etapas=False):
    """Resolve Ax=b sem trocar linhas e sem modificar os dados de entrada."""
    A = np.array(A, dtype=float, copy=True)
    b = np.array(b, dtype=float, copy=True)
    if A.ndim != 2 or A.shape[0] != A.shape[1] or A.shape[0] == 0:
        raise ValueError("A deve ser uma matriz quadrada não vazia.")
    n = A.shape[0]
    if b.shape != (n,):
        raise ValueError("b deve ser um vetor com n elementos.")
    if not np.isfinite(A).all() or not np.isfinite(b).all():
        raise ValueError("A e b devem conter somente valores finitos.")

    # Une os coeficientes e o termo independente na matriz [A | b].
    aumentada = np.column_stack((A, b))
    limite = np.finfo(float).eps * n * np.max(np.abs(A))

    def verificar_pivo(k):
        if abs(aumentada[k, k]) <= limite:
            raise ValueError(
                f"Pivô zero ou numericamente pequeno na linha {k + 1}; "
                "este algoritmo sem pivoteamento não pode prosseguir."
            )

    if exibir_etapas:
        print("Matriz aumentada inicial:\n", aumentada)
    for k in range(n - 1):
        verificar_pivo(k)
        for i in range(k + 1, n):
            # Li <- Li - multiplicador * Lk, incluindo o termo independente.
            multiplicador = aumentada[i, k] / aumentada[k, k]
            aumentada[i, k:] -= multiplicador * aumentada[k, k:]
            aumentada[i, k] = 0.0
            if exibir_etapas:
                print(f"L{i + 1} <- L{i + 1} - ({multiplicador:g}) L{k + 1}")
                print(aumentada)

    # Resolve da última equação para a primeira.
    solucao = np.zeros(n)
    for i in range(n - 1, -1, -1):
        verificar_pivo(i)
        soma = np.dot(aumentada[i, i + 1:n], solucao[i + 1:])
        solucao[i] = (aumentada[i, n] - soma) / aumentada[i, i]
    return solucao


def comparar(titulo, A, b, esperado):
    print(f"\n{titulo}")
    solucao = gauss_sem_pivoteamento(A, b, exibir_etapas=True)
    referencia = np.linalg.solve(A, b)
    print("Solução por Gauss:", solucao)
    print("Solução por numpy.linalg.solve:", referencia)
    print("Resíduo A @ solução - b:", np.asarray(A) @ solucao - b)
    print("Maior diferença entre os métodos:", np.max(np.abs(solucao - referencia)))
    # Confere tanto a referência numérica quanto a resposta obtida manualmente.
    assert np.allclose(solucao, referencia, rtol=1e-12, atol=1e-12)
    assert np.allclose(solucao, esperado, rtol=1e-12, atol=1e-12)
    assert np.allclose(np.asarray(A) @ solucao, b, rtol=1e-12, atol=1e-12)
    return solucao


if __name__ == "__main__":
    comparar("Exercício 4 — sistema do exercício 2",
             [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
             np.array([8, -11, -3]), [2, 3, -1])
    comparar("Exercício 5 — balanço térmico",
             [[4, -1, 0], [-1, 4, -1], [0, -1, 3]],
             np.array([15, 10, 10]), [5, 5, 5])
