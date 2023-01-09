import numpy as np


def min_edit_dist(_src, _tar):

    def sub_cost(_src_i, _tar_j):
        return 0 if _src_i == _tar_j else 2

    n = len(_src)
    m = len(_tar)
    D = np.zeros(shape=(n+1,m+1), dtype=int)

    # Initialization: the zeroth row and column is the distance from the empty string
    D[0, 0] = 0
    for i in range(1, n+1):
        D[i, 0] = D[i-1, 0] + 1

    for j in range(1, m+1):
        D[0, j] = D[0, j-1] + 1

    for i in range(1, n+1):
        for j in range(1, m+1):
            D[i, j] = min(D[i-1, j] + 1,
                          D[i-1, j-1]+sub_cost(_src[i-1], _tar[j-1]),
                          D[i, j-1] + 1)
    print(D)

    return D[n, m]

dist = min_edit_dist("drive", "divers")
print(f"dist = {dist}")