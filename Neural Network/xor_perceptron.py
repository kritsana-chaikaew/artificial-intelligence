import csv
import math

class Node():
    def __init__(self, weight=0):
        self.weight = weight

        self.inputs = []
        self.links = []
        self.back_links = []

        self.summation = 0
        self.output = 0
        self.sigma = 0

    def threshold(self):
        if self.summation > 0:
            self.output = 1
        else:
            self.output -1

    def sigmoid(self):
        self.output = 1 / (1 + (math.e ** -self.summation))

    def feed(self, _input):       # not efficient
        self.inputs.append(_input)

        if len(self.back_links) == 0 or len(self.inputs) == len(self.back_links):
            self.summation = sum(self.inputs) + self.weight
            self.threshold()
            self.inputs.clear()

            for link in self.links:
                link.destination.feed(self.output*link.weight)

    def calculate_error(self, term):
        return term #self.output * (1 - self.output) * term

    def update(self, learning_rate):
        self.weight +=  learning_rate * self.sigma

        for link in self.back_links:
            link.update(learning_rate, self.sigma)


class Link():
    def __init__(self, source, destination, weight=0):
        self.source = source
        self.destination = destination
        self.weight = weight

        self.source.links.append(self)
        self.destination.back_links.append(self)

    def update(self, learning_rate, sigma):
        self.weight += learning_rate * sigma * self.source.output


with open('xor_training_set.csv') as training_file:
    reader = csv.reader(training_file)
    training_data = [row for row in reader]

del training_data[0]
training_data = [list(map(int, row)) for row in training_data]
inputs = []
target_outputs = []
learning_rate = 0.01

for row in training_data:
    inputs.append([-1 if x==0 else x for x in row[:-1]])
    if row[-1] == 0:
        target_outputs.append(-1)
    else:
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
links.append(Link(input_nodes[0], hidden_nodes[0], initial_weight))
links.append(Link(input_nodes[0], hidden_nodes[1], initial_weight))

links.append(Link(input_nodes[1], hidden_nodes[0], initial_weight))
links.append(Link(input_nodes[1], hidden_nodes[1], initial_weight))

links.append(Link(hidden_nodes[0], output_nodes[0], initial_weight))
links.append(Link(hidden_nodes[1], output_nodes[0], initial_weight))
iteration = 200

for it in range(iteration):
    for i in range(len(inputs)):
        for j in range(len(input_nodes)):
            input_nodes[j].feed(inputs[i][j])

        for node in output_nodes:
            node.sigma = node.calculate_error(target_outputs[i]-node.output)
            node.update(learning_rate)

        for node in hidden_nodes:
            node.sigma = 0
            for link in node.links:
                node.sigma += node.calculate_error(link.weight*link.destination.sigma)
            node.update(learning_rate)
        print("% d ^ % d == % d % f % f " % (inputs[i][0], inputs[i][1], target_outputs[i], output_nodes[0].output, output_nodes[0].sigma), end="")
        for link in links:
            print('\t', link.weight, end='')
        print()
    #print()
