import csv

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

        self.summation = sum(self.inputs) + self.weight
        self.output = self.threshold(self.summation)

        for link in self.links:
            link.destination.feed(self.output*link.weight)

    def reset(self):        # duplicate call, not efficient
        self.inputs.clear()
        self.output = 0
        self.weight = initial_weight
        self.summation = 0

        for link in self.links:
            link.reset()

    def update(self, weight):
        self.weight += weight


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

    def update(self, weight):
        self.weight += weight


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

input_node = []
input_node.append(Node(1))
input_node.append(Node(1))

hidden_node = []
hidden_node.append(Node(initial_weight))
hidden_node.append(Node(initial_weight))

output_node = Node(initial_weight)

links = []
links.append(Link(input_node[0], hidden_node[0], initial_weight))
links.append(Link(input_node[0], hidden_node[1], initial_weight))

links.append(Link(input_node[1], hidden_node[0], initial_weight))
links.append(Link(input_node[1], hidden_node[1], initial_weight))

links.append(Link(hidden_node[0], output_node, initial_weight))
links.append(Link(hidden_node[1], output_node, initial_weight))

error = 0
iteration = 10
for it in range(iteration):
    for i in range(len(inputs)):
        input_node[0].feed(inputs[i][0])
        input_node[1].feed(inputs[i][1])

        error = target_outputs[i] - output_node.output
        delta = learning_rate * error

        for link in links:
            link.update(delta*link.source.output)

        print("%d ^ %d == %d" % (inputs[i][0], inputs[i][1], output_node.output))
    print()
