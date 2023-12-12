grid_i = [[11, 32, 13, 4], [55, 62, 7, 28], [19, 10, 1, 52], [23, 44, 5, 16]]


def setUpGridIds(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = (i * len(grid[i])) + (j + 1)
    return grid


def setUpConnect(grid):
    lines = len(grid)
    columns = len(grid[0])
    connect = [[0 for _ in range(5)] for _ in range(lines * columns)]
    for i in range(len(connect)):
        connect[i][-1] = i + 1
        connect[i][0] = 0 if i % columns == 0 else i
        connect[i][1] = 0 if i + 1 % columns == 0 else i + 2
        connect[i][2] = 0 if i - columns + 1 <= 0 else i - columns + 1
        connect[i][3] = 0 if i + columns + 1 > lines * columns else i + columns + 1
    return connect


grid_f = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

if __name__ == '__main__':
    c = setUpGridIds(grid_i)
    c = setUpConnect(c)
    print(c)
