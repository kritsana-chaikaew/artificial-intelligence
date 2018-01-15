import csv
import math

class Attribute(object):
    def __init__(self, fields):
        self.name = fields[0]
        self.fields = fields
        self.values = set(fields[1:])
        self.values_count = dict(
                (v,fields.count(v)) for v in self.values)

class Node(object):
    def __init__(self, attribute):
        self.attribute = attribute
        self.links = dict(
                (attr, None) for attr in self.attribute.values)

class Tree(object):
    def __init__(self, root):
        self.root = root

def entropy(positive, negative):
    if positive == 0 or negative == 0:
        return 0.0

    summation = positive + negative
    positive_ratio = positive / summation
    negative_ratio = negative / summation

    return -positive_ratio * math.log(positive_ratio, 2) \
        - negative_ratio * math.log(negative_ratio, 2)

def classify(data, attribute):
    pass

data = []
data_transpose = []
attributes = {}

with open('training_example.csv', newline='') as training_example:
    reader = csv.reader(training_example)
    data = [r for r in reader]
    data_transpose = zip(*data)
    for row in data_transpose:
        attributes[row[0]] = Attribute(row)

s = (attributes['PlayTennis'].fields.count('Yes'),
        attributes['PlayTennis'].fields.count('No'))

overcast = [0, 0]
rain = [0, 0]
sunny = [0, 0]

outlook = [overcast, rain, sunny]

for i in range(1, len(data)):
    if data[i][5] == 'Yes':
        index = 0
    elif data[i][5] == 'No':
        index = 1

    if data[i][1] == 'Overcast':
        overcast[index] += 1
    elif data[i][1] == 'Rain':
        rain[index] += 1
    elif data[i][1] == 'Sunny':
        sunny[index] += 1

overcast_entropy = entropy(overcast[0], overcast[1])
rain_entropy = entropy(rain[0], rain[1])
sunny_entropy = entropy(sunny[0], sunny[1])

entropies = [overcast_entropy, rain_entropy, sunny_entropy]
weight = [(x[0]+x[1])/14 for x in outlook[::]]
weighted_entropies = sum([entropies[i]*weight[i] for i in range(len(entropies))])

print(outlook)
print(entropies)
print(weight)
print(weighted_entropies)
