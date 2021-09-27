import os
from tensorflow import keras
from Model.modelEnum import Environment
from Exception.modelException import EnvironmentException
from Structures.iUtilStructure import IUtilStructure, Structure
from Constraints.path import TMP_BINARY_NEURAL_NETWORK_MODEL_PATH
from Constraints.path import CATEGORICAL_NEURAL_NETWORK_MODEL_PATH
from Exception.inputOutputException import PathDoesNotExistException
from Structures.NeuralNetworks.neuralNetworkEnum import NeuralNetworkTypeEnum


class NeuralNetworkUtil(IUtilStructure):

    def __init__(self, logger, model):
        self.logger = logger
        self.model = model

    def train_model(self, sequential_model, batch_size=128, epochs=10, is_categorical=False):
        loss = ('binary_crossentropy', 'categorical_crossentropy')[is_categorical]

        # looking at the model summary
        sequential_model.summary()

        # compiling the sequential model
        sequential_model.compile(loss=loss, metrics=['accuracy'], optimizer='adam')

        # training the model
        sequential_model.fit(self.model.get_x(Environment.TRAIN), self.model.get_y(Environment.TRAIN),
                             batch_size=batch_size, epochs=epochs)

        return sequential_model

    def load_model(self, name_model):

        nn_model_path = CATEGORICAL_NEURAL_NETWORK_MODEL_PATH + name_model

        if not os.path.exists(nn_model_path):
            raise PathDoesNotExistException("The model needs to exists to be able to use it")

        pickles, nn_type = super(NeuralNetworkUtil, self).get_pickles_used(Structure.CategoricalNeuralNetwork,
                                                                           name_model)
        self.model.set_pickles_name(pickles)

        keras_model = self.read_model(nn_model_path)

        return keras_model, NeuralNetworkTypeEnum(nn_type)

    def save_model(self, model, neural_network_type):
        model_path, model_name = self.__get_keras_model_path(neural_network_type)

        model.save(model_path + model_name)

        super(NeuralNetworkUtil, self).save_pickles_used(Structure.CategoricalNeuralNetwork,
                                                         self.model.get_pickles_name(),
                                                         model_name)

        self.logger.write_info("A new categorical neural network model has been created with the name of: " + model_name
                               + "\nIn the path: " + model_path + "\nThis is the name that will be needed in the "
                               "other strategies if you want to work with this model.")

    def get_pickles_used_in_binary_zip(self, name_model):
        pickles = super(NeuralNetworkUtil, self).get_pickles_used(Structure.BinaryNeuralNetwork, name_model)
        return pickles

    def record_binary_model(self, file_name, file_path, restriction):

        super(NeuralNetworkUtil, self).save_pickles_used(Structure.BinaryNeuralNetwork, self.model.get_pickles_name(),
                                                         file_name, restriction=restriction)

        self.logger.write_info("A new set of binary neural network models have been created with the name of: " +
                               file_name + "\nIn the path: " + file_path + "\nThis is the name that will be needed in "
                               "the other strategies if you want to work with these models.")

        return TMP_BINARY_NEURAL_NETWORK_MODEL_PATH

    @staticmethod
    def read_model(nn_model_path):
        return keras.models.load_model(nn_model_path)

    def __get_keras_model_path(self, neural_network_type):
        if not isinstance(neural_network_type, NeuralNetworkTypeEnum):
            raise EnvironmentException("Environment used is not a valid one")

        file_name = neural_network_type.value + "_" + self.model.get_pickles_name() + "_model"

        return CATEGORICAL_NEURAL_NETWORK_MODEL_PATH, file_name + ".h5"
