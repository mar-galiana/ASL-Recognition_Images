from enum import Enum


class NeuralNetworkEnum(Enum):
    CNN = "cnn"
    NN = "nn"
    IMPROVED_CNN = "improved_cnn"


class AttributeToTune(Enum):
    BATCH_SIZE_AND_EPOCHS = "batch_and_epoch"
    OPTIMIZATION_ALGORITHMS = "optimization_algorithms"
    LEARN_RATE_AND_MOMENTUM = "learn_rate_and_momentum"
    NETWORK_WEIGHT_INITIALIZATION = "network_weight_initialization"
    NEURON_ACTIVATION_FUNCTION = "neuron_activation_function"
    DROPOUT_REGULARIZATION = "dropout_regularization"
    NUMBER_NEURONS = "number_neurons"
