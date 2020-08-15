import numpy as np

x = np.ndarray(shape=(3, 2), dtype=int)
for i in range(3):
    for j in range(2):
        x[i, j] = i*j + 1

print(x)
b = np.ndarray(shape=(2))
b[0] = 1
b[1] = 1
print(b)

c = np.linalg.norm(x, axis=1, keepdims=True)
print('-'*10)
print(c)

