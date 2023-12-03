import numpy as np
from matplotlib import pyplot as plt

def euler(f, h, n, w0, t0=0):
    w = np.zeros(( len(f), n+1), dtype='float64')
    w[:,0] = w0[:,0]  # Todas as linhas da coluna 0
    for ii in range(1, n+1):  # Coluna da matriz
        for jj in range(len(f)):  # Linha da matriz
            w[jj,ii] = w[jj, ii - 1] + h * f[jj]( (ii-1)*h+t0, w[:,ii-1] )
    return w

def f1(t, w):
    return 1.2*w[0] - 0.6*w[0]*w[1]

def f2(t, w):
    return -0.8*w[1] + 0.3*w[0]*w[1]

f = [f1, f2]

w0 = np.array( [ [2], [1] ], dtype='float64')
h = 0.001  # Menor passo, mais preciso(Prefira reduzir o passo)
n = int(30/h)  # Maior numero de passos, mais preciso
t0 = 0.0
w = euler(f, h, n, w0)

t = np.linspace(t0, t0+n*h, n+1)
plt.plot(t, w[0,:])
plt.plot(t, w[1,:])
plt.legend(["w1", "w2"])
plt.show()