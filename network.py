from numpy import *
import _pickle as p

class neuralnetwork:
    def __init__(self, structure, fun, funPrime):
        # stucture = [first, second, third ...]
        self.layers = len(structure)
        self.structure = structure
        self.fun = vectorize(fun)
        self.funPrime = vectorize(funPrime)
        # Initialising bases and weights to random values
        self.biases = []
        self.weights = []
        for l in range(self.layers-1):
            self.biases.append(random.randn(structure[l+1], 1))
            self.weights.append(random.randn(structure[l+1], structure[l]))

    # Simply run input through network
    def run(self, inputs):
        # Running values through the network
        for l in range(self.layers-1):
            z = add(dot(self.weights[l], inputs), self.biases[l])
            inputs = sigmoid(z)

        return inputs

    # Run input through network, recording values for later training
    def run_values(self, inputs):
        acts = [inputs]
        zs = []
        # Running values through the network, recording activations at each layer
        for l in range(self.layers-1):
            z = dot(self.weights[l], inputs) + self.biases[l]
            inputs = self.fun(z)
            zs.append(z)
            acts.append(inputs)
        # Return lists by reference
        return (acts, zs)

    # Updates a batch of inputs
    def batch(self, acts_list, zs_list, output_list, learning_rate):

        nabla_b = [zeros(b.shape) for b in self.biases]
        nabla_w = [zeros(w.shape) for w in self.weights]

        for i in range(len(output_list)):
            w, b = self.backprop(acts_list[i], zs_list[i], output_list[i])
            for i in range(self.layers-1):
                nabla_w[i] = nabla_w[i] + w[-i-1]
                nabla_b[i] = nabla_b[i] + b[-i-1]

        learning_batch = learning_rate/len(output_list)

        for i in range(self.layers - 1):
            self.weights[i] = self.weights[i] - learning_batch * nabla_w[i]
            self.biases[i] = self.biases[i] - learning_batch * nabla_b[i]

    # Implimenting the backpropergation algorithim
    def backprop(self, acts, zs, optimal):

        # For storing the gradients of the weights and biases with respect to the cost
        weight_grads = []
        biases_grads = []

        # Finding the output error
        output_error = self.cost_function(acts[-1], optimal) * self.funPrime(zs[-1])

        weight_grads.append(dot(output_error, acts[-2].transpose()))
        biases_grads.append(output_error)

        # Backpropergate the error
        for l in range(self.layers-2, 0, -1):
            output_error = dot(self.weights[l].transpose(), output_error) * self.funPrime(zs[l-1])
            weight_grads.append(output_error * acts[l-1].transpose())
            biases_grads.append(output_error)

        return (weight_grads, biases_grads)

    def cost_function(self, output, correct):
        return output - correct

    def save(self, filename):
        with open(filename, 'wb') as output:
            p.dump(obj, output, -1)

def sigmoid(x):
    return 1.0/(1.0 + exp(-x))

def sigmoidPrime(x):
    return sigmoid(x) + (1.0-sigmoid(x))
