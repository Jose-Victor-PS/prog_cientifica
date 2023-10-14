def fun(x):
    return x*x + 2

def Fun(x):
    return 2*x

a = 0
b = 4
n = 64  # Maior n, menor h, maior custo computacional
h = (b-a)/n  # Maior h, maior o erro

x = []
y = []

alfa = fun(a)  # 2
yc = [alfa]

for i in range(n+1):
    xi = i*h
    x.append(xi)
    y.append(fun(xi))
for j in range(n):
    yc.append(yc[j] + h*Fun(x[j]))

import matplotlib.pyplot as plt
plt.plot(x,y,x,yc)
plt.show()
