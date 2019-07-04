import numpy as np
import random

class Neural:
    def __init__(self, sizes, input):
        self.inputs = input
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]
        self.output = self.feedforward(self.inputs)

    def feedforward(self, a):
        an = a
        for b, w in zip(self.biases, self.weights):
            an = sigmoid(np.dot(w, an) + b)
        return an


#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z) * (1 - sigmoid(z))


def mutate(network):
    random_value = np.random.uniform(-1.0, 1.0, 1)



board = [ 0,1,0, 0,0,0, 0,0,0]
a = Neural([9, 9, 9, 9], board)
out = a.feedforward(np.asarray(board))
print(out)

population = [Neural([9,9,9,9], board) for i in range(20)]




