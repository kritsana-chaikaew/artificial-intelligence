import csv

class Attribute(object):
    def __init__(self, fields):
        self.name = fields[0]
        self.fields = fields
        self.values = set(fields[1:])
        self.values_count = dict(
                (v,fields.count(v)) for v in self.values)

attributes = []

with open('training_example.csv', newline='') as training_example:
    reader = csv.reader(training_example)
    transpose = zip(*reader)
    for row in transpose:
        attributes.append(Attribute(row))

print(attributes[1].values)
print(attributes[1].values_count[1])
