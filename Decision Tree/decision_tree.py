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


def split(data, attribute, number):
    for i in range(len(data)):
        if data[i][-1] == 'Yes':
            index = 0
        elif data[i][-1] == 'No':
            index = 1

        for value in attribute.keys():
            if data[i][number] == value:
                attribute[value][index] += 1

    return attribute

def select_attribute(data):
    attributes = []
    attribute_number = 0
    max_information_gain = 0
    data_transpose = transpose(data[:])

    sample = [0, 0]
    if len(data_transpose) > 1:
        sample = [data_transpose[-1].count('Yes'),
                data_transpose[-1].count('No')]

    sample_entropy = entropy(sample)

    for number in range(len(data[0])-1):        # headers exclude PlayTennis
        attributes.append({})

        for value in set(data_transpose[number][1:]):
            attributes[number][value] = [0, 0]

        split(data[:], attributes[number], number)
        information_gain = sample_entropy - average_entropy(sample, attributes[number])

        if information_gain > max_information_gain:
            max_information_gain = information_gain
            attribute_number = number

    return attribute_number, attributes[attribute_number]

def branch(data, depth):
    data_transpose = transpose(data[:])

    if len(data_transpose) <= 1 or len(data) <= 2:
        return None

    root = Node()
    number, root.attribute = select_attribute(data[:])

    print(" "*depth*5, '-------')
    print(" "*depth*5, data_transpose[number][0])

    for value in root.attribute.keys():
        print(" "*depth*5, "\"", value,"\"")
        data_copy = data[:]
        new_data = list([])

        for i in range(len(data)):
            found = False
            if data_copy[i][number] == value or i == 0:
                found = True

            print(" "*depth*5, id(data_copy), value, data_copy[i][number], data[i])
            del data_copy[i][number]
            if found == True:
                new_data.append(data_copy[i][:])
                found = False
        root.children.append(branch(new_data[:], depth+1))

    return root

with open('training_example.csv', newline='') as training_example:
    reader = csv.reader(training_example)
    data = [r[1:] for r in reader]

root = branch(data[:], 0)
print([x for x in root.children])
