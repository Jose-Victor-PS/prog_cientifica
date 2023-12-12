import numpy as np
import json


def solve_mdf(json_filename):
    with open(json_filename, "r") as file:
        model = json.load(file)
    temperatures = model["temperatures"]
    connect = model["coonect"]

    n = sum(1 for el in connect if el[-1] != -1)  # Buraco tem ID -1

    A = np.zeros(shape=(n, n))
    b = np.zeros(shape=(n, 1))

    for i in range(1, len(b) + 1):
        if temperatures[str(i)][0] == 1:
            b[i - 1] = temperatures[str(i)][1]

    for i in range(len(connect)):
        if connect[i][-1] == -1:  # Buraco tem ID -1
            continue
        if temperatures[str(i + 1)][0] == 0:
            if connect[i][0] != 0:
                A[i][connect[i][0]-1] = 1
            if connect[i][1] != 0:
                A[i][connect[i][1]-1] = 1
            if connect[i][2] != 0:
                A[i][connect[i][2]-1] = 1
            if connect[i][3] != 0:
                A[i][connect[i][3]-1] = 1
            if connect[i][4] != 0:
                A[i][connect[i][4]-1] = -4
        else:
            A[i][i] = 1

    T = np.linalg.solve(A,b)

    print(T)


if __name__ == '__main__':
    solve_mdf("example_pvc.json")
