import numpy as np
from matplotlib import pyplot as plt

# metodo numerico
def euler(f, h, n, w0, t0=0):
    w = np.zeros(( len(f), n+1 ), dtype='float64' )
    w[:,0] = w0[:,0]
    for ii in range(1,n+1):
        for jj in range(len(f)):
            w[jj,ii] = w[jj,ii-1] + h*f[jj]( (ii-1)*h+t0, w[:,ii-1] )
    return w

# eqs
def f1(t,w):
    return w[1]
def f2(t,w):
    return -(9.81/0.6)*w[0]

f = [f1,f2]

# parametros do pvi
w0 = np.array( [ [ np.pi*0.125 ], [ 0 ] ], dtype='float64')

h = 0.1
n = 2
t0 = 0.0

# resolve numericamente
w = euler(f,h,n,w0,t0)

# plota resultados
t = np.linspace(t0,t0+n*h,n+1)
#plt.figure(0)
plt.plot(t,w[0,:])
plt.plot(t,w[1,:])
plt.legend(['w1','w2'])
# plt.figure(1)
# plt.plot(w[0,:],w[1,:])
plt.show()