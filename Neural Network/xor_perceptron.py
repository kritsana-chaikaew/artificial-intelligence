import csv
import math
import random
import math

class Node():
    def __init__(self, weight=0):
        self.weight = weight

        self.inputs = []
        self.links = []
        self.back_links = []

        self.output = 0
        self.delta = 0

    def sigmoid(self, summation):
        self.output = 1 / (1 + (math.e ** -summation))

    def activate(self):
        for link in self.links:
            link.destination.feed(self.output*link.weight)

    def feed(self, _input):

        if len(self.back_links) == 0:       # is input node
            self.output = _input
            self.activate()
        else:
            self.inputs.append(_input)
            if len(self.inputs) == len(self.back_links):        # all inputs are fed
                self.sigmoid(sum(self.inputs)+self.weight)
                self.inputs.clear()
                self.activate()


    def calculate_delta(self, term):
        return self.output * (1 - self.output) * term

    def update(self, learning_rate):
        self.weight +=  learning_rate * self.delta * 1


class Link():
    def __init__(self, source, destination, weight=0):
        self.source = source
        self.destination = destination
        self.weight = weight

        self.source.links.append(self)
        self.destination.back_links.append(self)

    def update(self, learning_rate):
        self.weight += learning_rate * self.destination.delta * self.source.output

def initial_weight():
    return random.random() / 1000     #small weight


inputs = [
        [1, 1],
        [1, 0],
        [0, 1],
        [0, 0]]
target_outputs = [0, 1, 1, 0]
learning_rate = 0.01


input_nodes = []
input_nodes.append(Node())
input_nodes.append(Node())

hidden_nodes = []
hidden_nodes.append(Node(initial_weight()))
hidden_nodes.append(Node(initial_weight()))

output_nodes = []
output_nodes.append(Node(random.random()))

links = []
links.append(Link(input_nodes[0], hidden_nodes[0], initial_weight()))
links.append(Link(input_nodes[0], hidden_nodes[1], initial_weight()))

links.append(Link(input_nodes[1], hidden_nodes[0], initial_weight()))
links.append(Link(input_nodes[1], hidden_nodes[1], initial_weight()))

links.append(Link(hidden_nodes[0], output_nodes[0], initial_weight()))
links.append(Link(hidden_nodes[1], output_nodes[0], initial_weight()))
iteration = 50000

for it in range(iteration):
    for i in range(len(inputs)):
        for j in range(len(input_nodes)):
            input_nodes[j].feed(inputs[i][j])

        for node in output_nodes:
            term = target_outputs[i]-node.output
            node.delta = node.calculate_delta(term)

        for node in hidden_nodes:
            term = 0
            for link in node.links:
                term += link.weight*link.destination.delta
            node.delta = node.calculate_delta(term)

        for node in output_nodes:
            node.update(learning_rate)

        for node in hidden_nodes:
            node.update(learning_rate)

        for link in links:
            link.update(learning_rate)
        print("% d ^ % d == % d % f % f" % (inputs[i][0], inputs[i][1], target_outputs[i], output_nodes[0].output, output_nodes[0].delta))
