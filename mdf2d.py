import numpy as np

n = 16 # quantidade de pontos da malha

cc = [[1,100], [1,75], [1,75], [1,75], [1,100], [0,0], [0,0], [1,0], [1,100], [0,0], [0,0], [1,0], [1,100], [1,25], [1,25], [1,0]]

connect = [[0,2,0,5,1], 
           [1,3,0,6,2], 
           [2,4,0,7,3], 
           [3,0,0,8,4], 
           [0,6,1,9,5], 
           [5,7,2,10,6],
           [6,8,3,11,7], 
           [7,0,4,12,8], 
           [0,10,5,13,9], 
           [9,11,6,14,10], 
           [10,12,7,15,11],
           [11,0,8,16,12], 
           [0,14,9,0,13], 
           [13,15,10,0,14], 
           [14,16,11,0,15], 
           [15,0,12,0,16]]

A = np.zeros(shape=(n,n))
b = np.zeros(shape=(n,1))

for i in range(len(b)):
    if cc[i][0] == 1:
        b[i] = cc[i][1]    


for i in range(len(connect)):
    if cc[i][0] == 0:
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
