import numpy as np

class NeuralNet:
    def __init__(self, n_inputs, n_outputs):
        # weights - 3d array: layer, neuron of layer, neuron pointing to
        self.weights = np.random.uniform(low=-1, high=1, size=(1, n_outputs, n_inputs))
        # biases - 2d array: layer, neuron of layer
        self.biases = np.random.uniform(low=-1, high=1, size=(1, n_outputs))

    def feed_forward(self, inputs):
        layer_output = inputs
        for layer_weights, layer_biases in zip(self.weights, self.biases):
            # multiply inputs by weights and add biases
            layer_output = np.dot(layer_weights, layer_output) + layer_biases
            
            # apply activation function (e.g. sigmoid)
            layer_output = np.tanh(layer_output)
        
        return layer_output
