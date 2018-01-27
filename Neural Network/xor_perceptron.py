import csv
import math

class Node():
    def __init__(self, weight=0):
        self.initial_weight = weight
        self.weight = initial_weight

        self.inputs = []
        self.links = []
        self.back_links = []

        self.summation = 0
        self.output = 0
        self.sigma = 0

    def sigmoid(summation):
        return 1 / (1 + (math.e ** -summation))

    def feed(self, _input):       # not efficient
        self.inputs.append(_input)

        if len(self.inputs) == len(self.back_links):
            self.summation = sum(self.inputs) + self.weight
            calculate_output()
            calculate_error()
            self.inputs.clear()

            for link in self.links:
                link.destination.feed(self.output*link.weight)

    def calculate_output():
        self.output = sigmoid(self.summation)

    def calculate_error(target_output):
        self.sigma = self.output \
                * (1 - self.output) \
                * (target_output - self.output)

    def update(self, learning_rate, sigma):
        self.weight +=  learning_rate * sigma

        for link in self.back_links:
            link.update(learning_rate, self.sigma)


class Link():
    def __init__(self, source, destination, weight=0, back_update=True):
        self.source = source
        self.destination = destination
        self.initial_weight = weight
        self.weight = initial_weight
        self.back_update = back_update

        self.source.links.append(self)
        self.destination.back_links.append(self)

    def update(self, learning_rate, sigma):
        self.weight += learning_rate * sigma * self.source.output

        if self.back_update:
            self.source.update(learning_rate, sigma*self.weight)


with open('xor_training_set.csv') as training_file:
    reader = csv.reader(training_file)
    training_data = [row for row in reader]

del training_data[0]
training_data = [list(map(int, row)) for row in training_data]
inputs = []
target_outputs = []
learning_rate = 0.01

for row in training_data:
    inputs.append(row[:-1])
    target_outputs.append(row[-1])

initial_weight = 0.1

input_nodes = []
input_nodes.append(Node(1))
input_nodes.append(Node(1))

hidden_nodes = []
hidden_nodes.append(Node(initial_weight))
hidden_nodes.append(Node(initial_weight))

output_nodes = []
output_nodes.append(Node(initial_weight))

links = []
links.append(Link(input_nodes[0], hidden_nodes[0], initial_weight, False))
links.append(Link(input_nodes[0], hidden_nodes[1], initial_weight, False))

links.append(Link(input_nodes[1], hidden_nodes[0], initial_weight))
links.append(Link(input_nodes[1], hidden_nodes[1], initial_weight))

links.append(Link(hidden_nodes[0], output_nodes[0], initial_weight))
links.append(Link(hidden_nodes[1], output_nodes[0], initial_weight))

iteration = 10

for it in range(iteration):
    for i in range(len(inputs)):
        input_nodes[0].feed(inputs[i][0])
        input_nodes[1].feed(inputs[i][1])

        for node in output_nodes:
            node.update(learning_rate, node.sigma)

        print("%d ^ %d == %d" % (inputs[i][0], inputs[i][1], output_nodes[0].output))
    print()
