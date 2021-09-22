import os
from StrategyFactory.iStrategy import IStrategy
from Exception.inputOutputException import InputException
from Structures.NeuralNetworks.neuralNetworkEnum import AttributeToTuneEnum
from Structures.NeuralNetworks.hyperparameterOptimization import HyperparameterOptimization


class HyperparameterOptimizationStrategy(IStrategy):

    def __init__(self, logger, model, nn_util, arguments):
        self.logger = logger
        self.model = model

        self.__show_arguments_entered(arguments)

        if arguments[0] not in AttributeToTuneEnum._value2member_map_:
            raise InputException(arguments[0] + "is not a possible parameter optimization.")

        self.attribute_tune = AttributeToTuneEnum(arguments[0])
        self.pickles = arguments[1:]
        self.hyperparameterOptimization = HyperparameterOptimization(logger, model, nn_util)

    def __show_arguments_entered(self, arguments):
        info_arguments = "Arguments entered:\n" \
                         "\t* Attribute to tune: " + arguments[0] + "\n" \
                         "\t* Pickles selected: " + ", ".join(arguments[1:])
        self.logger.write_info(info_arguments)

    def execute(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        self.model.set_pickles_name(self.pickles)
        self.model.read_reduced_pickles()

        self.hyperparameterOptimization.calculate_best_hyperparameter_optimization(self.attribute_tune)

        self.logger.write_info("Strategy executed successfully")
