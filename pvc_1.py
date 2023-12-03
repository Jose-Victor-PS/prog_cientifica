import numpy as np

L = 10  # Tamanho da barra
n = 6  # Numero de pontos

dx = L / (n-1)

restr1 = [1, 300]  # 1 eh Dirichlet  (0 seria Neuman)
restr2 = [1, 400]  # 1 eh Dirichlet  (0 seria Neuman)
A = np.zeros(shape=(n, n))
b = np.zeros(shape=(n, 1))
for i in range(n-2):
    A[i + 1, i] = -1
    A[i + 1, i + 1] = 2.2
    A[i + 1, i + 2] = -1
    b[i + 1] = 40

if restr1[0] == 1:
    A[0, 0] = 1
    b[0] = restr1[1]
else:
    A[0, 0] = 2.2
    A[0, 1] = -2
    b[0] = 40 + restr1[1]
if restr2[0] == 1:
    A[n-1, n-1] = 1
    b[n - 1] = restr2[1]

T = np.linalg.solve(A, b)


if __name__ == '__main__':
    print(T)
