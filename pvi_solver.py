import numpy as np
import json
import matplotlib.pyplot as plt


def solve_pvi(file_name):
    with open(file_name, "r") as f:
        model = json.load(f)

    x = np.array([e[0] for e in model["coords"]])
    y=np.array([e[1] for e in model["coords"]])

    connect = model["connect"]
    forces = model["forces"]
    restrs = model["restrs"]

    k = model["k"]
    m = model["m"]
    r = 5
    Np = x.shape[0]

    f = np.array([e for e in forces])
    f = np.reshape(f,(2*Np))

    fi = np.zeros(2*Np)
    u = np.zeros(2*Np)
    v = np.zeros(2*Np)
    a = (1/m)*f
    N = 3_000  # Quantos passos
    h = 0.00001  # Tamanho do passo
    d = np.zeros(N)
    for i in range(N):
        v += a*h/2  # Velocidade
        u += v*h  # Deslocamento
        # contato
        for j in range(Np):  # Particula J
            if (restrs[j][0]==1):  # Se ta presa, ignora
                u[2*j]=0
            if (restrs[j][1] == 1):  # Se ta presa, ignora
                u[2*j+1]=0
            xj = x[j] + u[2*j]  # A posicao dela + ultimo deslocamento
            yj = y[j] + u[2*j+1]  # A posicao dela + ultimo deslocamento
            for ki in range(4):
                if (connect[j][ki]):  # Olhar para as particular adjacentes
                    pk = connect[j][ki]-1  # particula K proxima de P
                    xk = x[pk]+u[pk*2]  # Verifica o X da particula K
                    yk = y[pk]+u[pk*2+1]  # Verifica o Y da particula K
                    dx = xj-xk  # distancia do X da particula J para a particula K
                    dy = yj-yk  # distancia do Y da particula J para a particula K
                    di = (dx**2+dy**2)**0.5  # Pitagora da distancia no X e Y
                    d2 = di-2*r  # Verifica se elas estao tangenciando, se estao dentro uma da outra, ou distanciadas
                    dx = d2*dx/di
                    dy = d2*dy/di
                    fi[2*j] += k*dx  # Forca na particula J no eixo X, causado por K
                    fi[2*j+1] += k*dy  # Forca na particula J no eixo Y, causado por K

        a = (1. / m) * (f-fi)  # Aceleracao
        v += a*h/2.  # Velocidade
        fi *= 0.  # Forca
        d[i] = u[-2]  # X da ultima particula

    plt.plot(d)
    plt.show()


if __name__ == '__main__':
    solve_pvi("teste2_pvi.json")
