import csv
import math

class Node:
    def __init__(self):
        self.attribute = None
        self.children = []

def transpose(data):
    data_transpose = [list(x) for x in zip(*data)]

    return data_transpose

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


def split(data, attribute, attribute_number):
    for i in range(1, len(data)):
        if data[i][-1] == 'Yes':
            index = 0
        elif data[i][-1] == 'No':
            index = 1

        for value in attribute.keys():
            if data[i][attribute_number] == value:
                attribute[value][index] += 1

    return attribute

def select_attribute(data):
    attributes = []
    attribute_number = 0
    max_information_gain = 0
    data_transpose = transpose(data)

    sample = [0, 0]
    if len(data_transpose) > 0:
        sample = [data_transpose[-1].count('Yes'),
                data_transpose[-1].count('No')]

    sample_entropy = entropy(sample)

    for number in range(len(data[0])-1):
        attributes.append({})

        for value in set(data_transpose[number][1:]):
            attributes[number][value] = [0, 0]

        attributes[number] = split(data, attributes[number], number)
        information_gain = sample_entropy - average_entropy(sample, attributes[number])

        if information_gain > max_information_gain:
            max_information_gain = information_gain
            attribute_number = number

    return attribute_number, attributes[attribute_number]

def branch(data):
    data_transpose = transpose(data)

    if len(data_transpose) == 1 or len(data) <= 1:
        return Node()

    root = Node()
    number, root.attribute = select_attribute(data)

    for value in root.attribute.keys():
        new_data = []

        for i in range(len(data)):
            if len(data) <= 0 or len(data[i]) <= 0:
                return Node()

            if data[i][number] == value or i == 0:
                new_data.append(data[i])
            del data[i][number]

        root.children.append(branch(new_data))

    return root

with open('training_example.csv', newline='') as training_example:
    reader = csv.reader(training_example)
    data = [r[1:] for r in reader]

root = branch(data)
print([x for x in root.children])
