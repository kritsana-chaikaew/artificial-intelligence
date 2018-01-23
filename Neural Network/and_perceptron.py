import csv

def threshold(inputs, weights):
    summation = 0

    for i, w in zip(inputs, weights):
            summation += i * w

    if summation > 0:
        return 1
    else:
        return -1

def initialize_weight(weights, lenght):
    for i in range(lenght):
        weights.append(0.1)

def train(inputs, weights, target_output):
    output = threshold(inputs, weights)
    print("%d & %d == %d" % (inputs[1], inputs[2], output))

    error = target_output - output

    for i in range(len(inputs)):
        delta = learning_rate * error * inputs[i]
        weights[i] += delta

    if target_output == output:
        return 1
    else:
        return 0


weights = []
training_data = []
learning_rate = 0.01

with open('and_training_set.csv') as training_file:
    reader = csv.reader(training_file)
    training_data = [row[:] for row in reader]
    del training_data[0]
    training_data = [list(map(int, row)) for row in training_data]

target_outputs = [row[-1] for row in training_data]
target_outputs = [-1 if x==0 else x for x in target_outputs]
inputs = training_data.copy()

for row in inputs:
    row.insert(0, 1)
    del row[-1]

initialize_weight(weights, len(inputs[0]))

accurate = 0

while accurate < 1:
    lenght = len(inputs)
    correct = 0

    for i in range(lenght):
        correct += train(inputs[i], weights, target_outputs[i])
    print()

    accurate = correct / lenght

print(weights)
