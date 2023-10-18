import numpy as np


def strassen(x, y):

    def prepare_matrix(matrix):
        root = np.ceil(np.sqrt(matrix.shape[0]))
        times = int(np.power(2, root) - matrix.shape[0])

        for _ in range(times):
            matrix = np.vstack([matrix, [0 for _ in range(matrix.shape[1])]])
            matrix = np.hstack([matrix, [[0] for _ in range(matrix.shape[0])]])

        return matrix, times

    def multiply_matrixes(x, y):
        if len(x) == 1:
            return x * y

        def split(matrix):
            row, col = matrix.shape
            row2, col2 = row//2, col//2
            return matrix[:row2, :col2], matrix[:row2, col2:], matrix[row2:, :col2], matrix[row2:, col2:]

        a, b, c, d = split(x)
        e, f, g, h = split(y)

        p1 = multiply_matrixes(a, f - h)
        p2 = multiply_matrixes(a + b, h)
        p3 = multiply_matrixes(c + d, e)
        p4 = multiply_matrixes(d, g - e)
        p5 = multiply_matrixes(a + d, e + h)
        p6 = multiply_matrixes(b - d, g + h)
        p7 = multiply_matrixes(a - c, e + f)

        c11 = p5 + p4 - p2 + p6
        c12 = p1 + p2
        c21 = p3 + p4
        c22 = p1 + p5 - p3 - p7

        c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))

        return c

    x, times = prepare_matrix(x)
    y, times = prepare_matrix(y)

    result = multiply_matrixes(x, y)

    for _ in range(times):
        result = np.delete(result, -1, 0)
        result = np.delete(result, -1, 1)

    return result
