import csv
import math

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

data = []
data_transpose = []
attributes = []
max_information_gain = 0
root_attribute_number = 0

with open('training_example.csv', newline='') as training_example:
    reader = csv.reader(training_example)
    data = [r[1:] for r in reader]
    data_transpose = zip(*data)
    data_transpose = [list(x) for x in data_transpose]

s = [data_transpose[-1].count('Yes'),
        data_transpose[-1].count('No')]

sample_entropy = entropy(s)

for number in range(len(data[0])-1):
    attributes.append({})
    for value in set(data_transpose[number][1:]):
        attributes[number][value] = [0, 0]

    attributes[number] = split(data, attributes[number], number)
    information_gain = sample_entropy - average_entropy(s, attributes[number])

    if information_gain > max_information_gain:
        max_information_gain = information_gain
        root_attribute_number = number

print(data[0][root_attribute_number])
