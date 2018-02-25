import numpy as np
import math

def gaussian(x, u, sd):
    return math.e ** (-(1 / (sd ** 2)) * ((x - u) ** 2))

def expected_z(x, u, sd, j):
    frac = gaussian(x, u[j], sd)
    div = sum([gaussian(x, un, sd) for un in u])

    return frac / div


u1 = np.random.uniform(1, 10)
u2 = np.random.uniform(1, 10)

x1 = np.random.normal(size=(100, 1))
x2 = np.random.normal(size=(100, 1))

x1 = x1 + u1
x2 = x2 + u2

sd = 1
x = np.concatenate((x1, x2), axis=0)
z = np.empty(shape=(200, 2))

u = [2, 3]

while True:
    for i in range(200):
        for j in range(2):
            z[i, j] = expected_z(x[i], u[:], sd, j)
            print(z[i, j],)

    u[0] = 0
    u[1] = 0
    for i in range(200):
        for j in range(2):
            u[j] += z[i, j] * x[i] / 200
    print(u[0], u[1], u1, u2)

    if abs(u[0]-u1) < 0.1 and abs(u[1]-u2) < 0.1:
        break
