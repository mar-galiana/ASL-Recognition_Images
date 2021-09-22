import os
from StrategyFactory.iStrategy import IStrategy
from Exception.inputOutputException import InputException
from Structures.NeuralNetworks.neuralNetworkEnum import NeuralNetworkTypeEnum
from Structures.NeuralNetworks.artificialNeuralNetwork import ArtificialNeuralNetwork
from Structures.NeuralNetworks.convolutionalNeuralNetwork import ConvolutionalNeuralNetwork


class TrainCategoricalNeuralNetworkStrategy(IStrategy):

    def __init__(self, logger, model, nn_util, arguments):
        self.logger = logger
        self.model = model
        self.nn_util = nn_util
        self.__show_arguments_entered(arguments)

        self.nn_type = arguments[0]
        self.pickles = arguments[1:]

        self.algorithm_switcher = {
            NeuralNetworkTypeEnum.ANN.value: ArtificialNeuralNetwork(self.logger, self.model, self.nn_util),
            NeuralNetworkTypeEnum.CNN.value: ConvolutionalNeuralNetwork(self.logger, self.model, self.nn_util),
            NeuralNetworkTypeEnum.IMPROVED_CNN.value: ConvolutionalNeuralNetwork(self.logger, self.model, self.nn_util,
                                                                                improved_nn=True)
        }

    def __show_arguments_entered(self, arguments):
        info_arguments = "Arguments entered:\n" \
                         "\t* Neural Network type: " + arguments[0] + "\n" \
                         "\t* Pickles selected: " + ", ".join(arguments[1:])
        self.logger.write_info(info_arguments)

    def execute(self):
        if self.nn_type not in self.algorithm_switcher:
            raise InputException(self.nn_type + " is not a valid strategy")

        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        self.model.set_pickles_name(self.pickles)

        algorithm_execution = self.algorithm_switcher.get(self.nn_type)
        algorithm_execution.train_neural_network()

        self.logger.write_info("Strategy executed successfully")
