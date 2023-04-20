def matrix2bytes(matrix):
    return "".join([chr(matrix[x][y]) for x in range(4) for y in range(4)])

matrix = [
    [99, 114, 121, 112],
    [116, 111, 123, 105],
    [110, 109, 97, 116],
    [114, 105, 120, 125],
]

print(matrix2bytes(matrix))
