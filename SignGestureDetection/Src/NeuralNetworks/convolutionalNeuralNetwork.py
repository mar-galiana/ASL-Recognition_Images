"""
One major advantage of using CNNs over NNs is that you do not need to flatten the input images to 1D as they are capable
of working with image data in 2D.
"""

import numpy as np
from keras.models import Sequential
from Src.Model.enumerations import Environment
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten
from Src.NeuralNetworks.iNeuralNetwork import INeuralNetwork
from Src.NeuralNetworks.enumerations import NeuralNetworkEnum
from Src.NeuralNetworks.neuralNetworkUtil import NeuralNetworkUtil


class ConvolutionalNeuralNetwork(INeuralNetwork):

    def __init__(self, logger, model):
        self.model = model
        self.logger = logger
        self.nn_util = NeuralNetworkUtil(self.model)

    def resize_data(self, environment):
        shape = self.model.get_x(environment).shape
        x_data = self.model.get_x(environment).reshape(shape[0], shape[1], shape[2], 1)
        return x_data

    def execute(self):
        n_classes = self.__prepare_images()
        sequential_model = self.__build_sequential_model(n_classes)
        self.nn_util.save_keras_model(sequential_model, NeuralNetworkEnum.CNN)

    def __prepare_images(self):
        # Flattening the images from the 150x150 pixels to 1D 787 pixels
        x_train = self.resize_data(Environment.TRAIN)
        x_test = self.resize_data(Environment.TEST)

        self.model.set_x(Environment.TRAIN, x_train)
        self.model.set_x(Environment.TEST, x_test)

        n_classes = self.nn_util.convert_to_one_hot_data()

        return n_classes

    def __build_sequential_model(self, n_classes):
        shape_train = self.model.get_x(Environment.TRAIN).shape

        # building a linear stack of layers with the sequential model
        sequential_model = Sequential()

        # convolutional layer
        sequential_model.add(Conv2D(25, kernel_size=(3, 3), strides=(1, 1), padding='valid', activation='relu',
                                    input_shape=(shape_train[1], shape_train[2], 1)))
        sequential_model.add(MaxPool2D(pool_size=(1, 1)))

        # flatten output of conv
        sequential_model.add(Flatten())

        # hidden layer
        sequential_model.add(Dense(100, activation='relu'))

        # output layer
        sequential_model.add(Dense(n_classes, activation='softmax'))

        sequential_model = self.nn_util.train_model(sequential_model)

        return sequential_model
