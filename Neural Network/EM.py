import numpy as np
import math

def gaussian(x, u, sd):
    return math.e ** (-(0.5 * (sd ** 2)) * ((x - u) ** 2))

def expected_z(x, u, sd, j):
    fraction = gaussian(x, u[j], sd)
    denominator = sum([gaussian(x, un, sd) for un in u])
    return fraction / denominator


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
old_u = [0, 0]

unchange_couter = 0

while unchange_couter < 5:
    old_u[0] = u[0]
    old_u[1] = u[1]

    print(u[0], u[1], u1, u2)
    for i in range(200):
        for j in range(2):
            z[i, j] = expected_z(x[i], u[:], sd, j)
    for j in range(2):
        u[j] = sum(np.multiply(z[:, j], x[:, 0]))
        u[j] /= sum(z[:, j])

    if (old_u[0] - u[0] == 0) and (old_u[1] - u[1] == 0):
        unchange_couter +=1
