import matplotlib.pyplot as plt
import numpy as np

SIZE = 100
AXIS_LEN = 10
K = 10

positive = [[x, y, 1] for x, y in zip(
        np.random.uniform(0, 0.6*AXIS_LEN, SIZE//2),
        np.random.uniform(0, AXIS_LEN, SIZE//2))]
negative = [[x, y, -1] for x, y in zip(
        np.random.uniform(0.4*AXIS_LEN, AXIS_LEN, SIZE//2),
        np.random.uniform(0, AXIS_LEN, SIZE//2))]

positive = np.asarray(positive)
negative = np.asarray(negative)
sample = np.concatenate((positive, negative), axis=0)
query = np.random.uniform(0, AXIS_LEN, 2)

distances = []
for neighbor in sample:
    distance = np.linalg.norm(query-neighbor[:2])
    distances.append(distance)

arg = np.argsort(distances)
k_nearest = arg[:K]

radius = distances[k_nearest[-1]]

pos = 0
neg = 0
for idx in k_nearest:
    if sample[idx, 2] == 1:
        pos += 1
    if sample[idx, 2] == -1:
        neg += 1

output = ''
if pos > neg:
    output = '+'
elif neg > pos:
    output = '_'
else:
    output = '*'

circle1 = plt.Circle(query, radius, color='g', fill=False, linestyle='--')
fig, ax = plt.subplots(figsize=(7, 7))
ax.add_artist(circle1)

plt.plot(positive[:, 0],positive[:, 1], 'b+')
plt.plot(negative[:, 0],negative[:, 1], 'r_')
plt.plot(query[0], query[1], 'g'+output, markersize=10)
plt.axis([0, AXIS_LEN, 0, AXIS_LEN])
plt.title("Class "+str(output)+" "+str(pos)+" positive, "+str(neg)+" negative")
plt.show()
