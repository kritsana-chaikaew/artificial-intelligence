import csv

inputs = [1, ]
weights = []

def threshold(inputs, weights):

    for i, w in inputs[:], weights[:]:
        summation += i * w

    if w > 0:
        return 1
    else:
        return 0

def initialize_weight(weights, lenght):
    for i in range(lenght):
        weights.append(0.1)

training_data = []

with open('and_training_set.csv') as training_file:
    reader = csv.reader(training_file)
    training_data = [row[:] for row in reader]
    del training_data[0]

print(training_data)
