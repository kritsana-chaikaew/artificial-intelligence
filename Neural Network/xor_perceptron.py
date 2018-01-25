import csv

class Node():
    def __init__(self, weight=0):
        self.initial_weight = weight
        self.weight = initial_weight

        self.inputs = []
        self.links = []
        self.back_links = []

        self.summation = 0
        self.output = 0
        self.error = 0

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
        self.weight = initial_weight
        self.inputs.clear()

        self.output = 0
        self.summation = 0
        self.error = 0

        for link in self.links:
            link.reset()

    def update(self, weight):
        self.weight += weight * self.source.output

        for link in back_links:
            link.update(weight*link.source.output)


class Link():
    def __init__(self, source, destination, weight=0, back_update=True):
        self.source = source
        self.destination = destination
        self.initial_weight = weight
        self.weight = initial_weight
        self.back_update = back_update

        self.source.links.append(self)
        self.destination.back_links.append(self)

    def reset(self):
        self.weight = self.initial_weight
        self.destination.reset()        # bad idea

    def update(self, weight):
        self.weight += weight

        if back_update:
            self.source.update(self.weight)

def error(target_output, output):
    return target_output - output


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
            node.error = learning_rate * error(target_outputs[i], node.output)

        print("%d ^ %d == %d" % (inputs[i][0], inputs[i][1], output_nodes[0].output))
    print()
