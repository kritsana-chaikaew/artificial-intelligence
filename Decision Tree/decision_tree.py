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

attributes = []

with open('training_example.csv', newline='') as training_example:
    reader = csv.reader(training_example)
    transpose = zip(*reader)
    for row in transpose:
        attributes.append(Attribute(row))

print(entropy(5, 0))
