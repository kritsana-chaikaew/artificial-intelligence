import csv
import collections

class Node():
    def __init__(self, weight=0):
        self.inputs = []
        self.output = 0
        self.initial_weight = weight
        self.weight = initial_weight
        self.summation = 0
        self.links = []

    def threshold(self, _input):
        if _input > 0:
            return 1
        else:
            return -1

    def feed(self, _input):       # not efficient
        self.inputs.append(_input)

        self.summation = sum(self.inputs)
        self.output = self.threshold(self.summation*self.weight)

        for link in self.links:
            link.destination.feed(self.output*link.weight)

    def reset(self):        # duplicate call, not efficient
        self.inputs.clear()
        self.output = 0
        self.weight = initial_weight
        self.summation = 0

        for link in self.links:
            link.reset()


class Link():
    def __init__(self, source, destination, weight=0):
        self.initial_weight = weight
        self.weight = initial_weight
        self.source = source
        self.destination = destination
        self.source.links.append(self)

    def reset(self):
        self.weight = self.initial_weight
        self.destination.reset()        # bad idea


with open('xor_training_set.csv') as training_file:
    reader = csv.reader(training_file)
    training_data = [row for row in reader]

del training_data[0]
training_data = [list(map(int, row)) for row in training_data]
inputs = []
target_outputs = []

for row in training_data:
    inputs.append(row[:-1])
    target_outputs.append(row[-1])

initial_weight = 0.1

input_node1 = Node(1)
input_node2 = Node(1)

hidden_node1 = Node(initial_weight)
hidden_node2 = Node(initial_weight)

output_node = Node(1)

link11 = Link(input_node1, hidden_node1, initial_weight)
link12 = Link(input_node1, hidden_node2, initial_weight)
link21 = Link(input_node2, hidden_node1, initial_weight)
link22 = Link(input_node2, hidden_node2, initial_weight)
link1O = Link(hidden_node1, output_node, initial_weight)
link2O = Link(hidden_node2, output_node, initial_weight)

input_node1.feed(1)
input_node2.feed(-1)
print(output_node.output)
