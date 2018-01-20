import csv
import math

class Node:
    def __init__(self):
        self.attribute_name = ''
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

def select_attribute(data):
    attributes = []
    attribute_number = 0
    attribute_name = ''
    max_information_gain = 0
    data_transpose = transpose(data.copy())

    sample = [0, 0]
    if len(data_transpose) > 1:
        sample = [data_transpose[-1].count('Yes'),
                data_transpose[-1].count('No')]

    sample_entropy = entropy(sample)

    for number in range(len(data[0])-1):        # headers exclude PlayTennis
        attributes.append({})
        name = data[0][number]

        for value in set(data_transpose[number][1:]):
            attributes[number][value] = [0, 0]

        split(data.copy(), attributes[number], number)
        information_gain = sample_entropy - average_entropy(sample, attributes[number].copy())

        if information_gain > max_information_gain:
            max_information_gain = information_gain
            attribute_number = number
            attribute_name = name

    return attribute_name, \
            attribute_number, \
            attributes[attribute_number].copy()

def branch(data, depth):
    data_transpose = transpose(data.copy())

    if len(data_transpose) <= 1 or len(data) <= 2:
        return None

    root = Node()
    root.attribute_name, number, root.attribute = select_attribute(data.copy())

    print(" "*(25-5*depth), '-------')
    print(" "*(25-5*depth), data_transpose[number][0])

    for value in root.attribute.keys():
        print(" "*(25-5*depth), "\"", value,"\"")
        data_copy = [x.copy() for x in data.copy()]
        new_data = list([])

        for i in range(len(data)):
            found = False
            if data_copy[i][number] == value or i == 0:
                found = True

            print(" "*(25-5*depth), id(data_copy), value, data_copy[i][number], data[i])
            del data_copy[i][number]
            if found == True:
                new_data.append(data_copy[i].copy())
                found = False
        child = branch(new_data.copy(), depth+1)
        if child is not None:
            root.children.append(child)

    return root

def print_tree(root, depth=0):
    if depth > 0:
        print(" "*depth, end="")

    print("|_%s" % root.attribute_name)
    for child in root.children:
        if child is not None:
            print(" "*depth, end="")
            print_tree(child, depth+1)


with open('training_example.csv', newline='') as training_example:
    reader = csv.reader(training_example)
    data = [r[1:] for r in reader]

root = branch(data.copy(), 0)
#print([x for x in root.children])
print_tree(root)
