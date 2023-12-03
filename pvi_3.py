import json
import numpy as np
import matplotlib.pyplot as plt

# Leap Frog Method
# Condicoes Iniciais
def main():
    with open("input.json", "r") as file:
        model = json.load(file)
    x = np.array([i[0] for i in model["coords"]])
    y = np.array([i[1] for i in model["coords"]])
    Np = x.shape[0]
    k = model["k"]
    m = model["m"]
    r = model["r"]
    forces = np.array([i for i in model["forces"]])
    forces = np.reshape(forces, (2*Np))
    restrs = np.array([i for i in model["restrs"]])
    restrs = np.reshape(restrs, (2 * Np))
    connect = np.array([i for i in model["connect"]])

    fi = np.zeros(2*Np)
    u = np.zeros(2*Np)
    v = np.zeros(2*Np)
    a = (1/m)*forces

    N = 100
    h = 0.00004
    d = np.zeros(N)
    for i in range(N):
        v += a * (0.5 * h)
        u += v * h
        # Contato
        for j in range(Np):
            if restrs[2 * j] == 1:
                u[2 * j] = 0
            if restrs[2 * j + 1] == 1:
                u[2 * j + 1] = 0
            xj = x[j] + u[2 * j]
            yj = y[j] + u[2 * j + 1]
            for ki in range(connect[j, 0] - 1):
                pk = connect[j, ki + 1] - 1
                xk = x[pk] + u[pk * 2]
                yk = y[pk] + u[pk * 2 + 1]
                dx = xj - xk
                dy = yj - yk
                di = (dx**2 + dy**2)**0.5
                d2 = di - 2*r
                dx = d2 * dx/di
                dy = d2 * dy/di
                fi[2 * j] += k * dx
                fi[2 * j + 1] += k * dy
        a = (1. / m) * (forces - fi)
        v += a * (0.5 * h)
        fi *= 0
        d[i] = u[17 * 2]

    plt.plot(d)
    plt.show()


if __name__ == '__main__':
    main()