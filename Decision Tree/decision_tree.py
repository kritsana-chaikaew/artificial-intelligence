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

def entropy(sample):
    summation = sum(sample)
    entropy = 0
    for s in sample:
        if s != 0:
            pob = s / summation
            entropy -= pob * math.log(pob, 2)

    return entropy

def average_entropy(sample, attribute):
    weighted_entropy = 0
    sample_size = sum(sample)

    for value in attribute.keys():
        weighted_entropy += entropy(attribute[value]) \
                * sum(attribute[value]) / sample_size

    return weighted_entropy


def split(data, attribute):
    for i in range(1, len(data)):
        if data[i][5] == 'Yes':
            index = 0
        elif data[i][5] == 'No':
            index = 1

        for value in attribute.keys():
            if data[i][1] == value:     # 1 is outlook attribute
                attribute[value][index] += 1

    return attribute

data = []
data_transpose = []
attributes = {}

with open('training_example.csv', newline='') as training_example:
    reader = csv.reader(training_example)
    data = [r for r in reader]
    data_transpose = zip(*data)
    data_transpose = [list(x) for x in data_transpose]
    for row in data_transpose:
        attributes[row[0]] = Attribute(row)

s = [attributes['PlayTennis'].fields.count('Yes'),
        attributes['PlayTennis'].fields.count('No')]

outlook = {}
for value in set(data_transpose[1][1:]):      # 1 is outlook attribute
    outlook[value] = [0, 0]

outlook = split(data, outlook)

print(average_entropy(s,outlook))
