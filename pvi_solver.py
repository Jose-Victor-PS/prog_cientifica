import numpy as np
import json
import matplotlib.pyplot as plt
def main():
    print("main")
    with open(r"C:\Users\fefea\OneDrive\Documentos\UFF\prog científica\códigos\v2\sample.json") as f:
        model = json.load(f)
    # print(model["coords"])

    x = np.array([e[1] for e in model["coords"]])
    print(x)
    y=np.array([e[2] for e in model["coords"]])
    print(y)

    connect = model["connect"]
    forces = model["forces"]
    restrs = model["restrs_pos"]

    k = 210000000000
    m = 7850
    r = 1
    Np = x.shape[0]

    # forces = [
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [0,0],
    #     [-1000,0],
    #     [-1000,0],
    #     [-1000,0],
    # ]
    f = np.array([e for e in forces])
    f = np.reshape(f,(2*Np))
    print(f)

    # restrs = [
    #     [1, 1],
    #     [1, 1],
    #     [1, 1],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    #     [0, 0],
    # ]

    # connect = [
    #     [2,2,4,0, 0],
    #     [3,1,3,5,0],
    #     [2,2,6,0,0],
    #     [3,1,5,7,0],
    #     [4,2,4,6,8],
    #     [3,3,5,9,0],
    #     [3,4,8,10,0],
    #     [4,5,7,9,11],
    #     [3,6,8,12,0],
    #     [3,7,11,13,0],
    #     [4,8,10,12,14],
    #     [3,9,11,15,0],
    #     [3,10,14,16,0],
    #     [4,11,13,15,17],
    #     [3,12,14,18,0],
    #     [2,13,17,0,0],
    #     [3,14,16,18,0],
    #     [2,15,17,0,0],
    # ]

    fi = np.zeros(2*Np)
    u = np.zeros(2*Np)
    v = np.zeros(2*Np)
    a = (1/m)*f

    N = 200
    h = 0.00001
    d = np.zeros(N)

    for i in range(N):
        v += a*h/2
        u += v*h
        #contato
        for j in range(Np):
            if (restrs[j][0]==1):
                u[2*j]=0
            if (restrs[j][1] == 1):
                u[2*j+1]=0
            xj = x[j] + u[2*j]
            yj = y[j] + u[2*j+1]
            for ki in range(4):
                if (connect[j][ki]):
                    pk = connect[j][ki]-1
                    xk = x[pk]+u[pk*2]
                    yk = y[pk]+u[pk*2+1]
                    dx = xj-xk
                    dy = yj-yk
                    di = (dx**2+dy**2)**0.5
                    d2 = di-2*r
                    dx = d2*dx/di
                    dy = d2*dy/di
                    fi[2*j] += k*dx
                    fi[2*j+1] += k*dy

        a = (1. / m) * (f-fi)
        v += a*h/2.
        fi *= 0.
        d[i] = u[56]

    plt.plot(d)
    plt.show()

if __name__ == '__main__':
    main()