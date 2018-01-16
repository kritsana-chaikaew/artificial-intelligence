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
        if data[i][5] == 'Yes':
            index = 0
        elif data[i][5] == 'No':
            index = 1

        for value in attribute.keys():
            if data[i][attribute_number] == value:     # 1 is outlook attribute
                attribute[value][index] += 1

    return attribute

data = []
data_transpose = []
attributes = []

with open('training_example.csv', newline='') as training_example:
    reader = csv.reader(training_example)
    data = [r for r in reader]
    data_transpose = zip(*data)
    data_transpose = [list(x) for x in data_transpose]

s = [data_transpose[5].count('Yes'),
        data_transpose[5].count('No')]

outlook = {}
for number in range(1, len(data[0])-1):
    attributes.append({})
    for value in set(data_transpose[number][1:]):      # 1 is outlook attribute
        attributes[number-1][value] = [0, 0]

    attributes[number-1] = split(data, attributes[number-1], number)
    print(average_entropy(s,attributes[number-1]))
