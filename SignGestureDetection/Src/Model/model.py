import os
import numpy as np
from tensorflow import keras
from Model.signs import Signs
from Model.enumerations import Image
from Model.inputModel import InputModel
from Model.outputModel import OutputModel
from Model.enumerations import Environment
from sklearn.preprocessing import LabelEncoder
from tensorflow.python.keras.utils import np_utils
from Exception.modelException import EnvironmentException


class Model:

    def __init__(self, width=150, height=None):
        self.signs = Signs()
        self.output_model = OutputModel(width, height)
        self.input_model = InputModel()

    def create_pickle(self, pickel_name, dataset, environments_separated, as_gray):
        self.output_model.create_pickle(pickel_name, dataset, environments_separated, as_gray)

    def set_pickels_name(self, names):
        self.input_model.set_pickels_name(names)

    def get_pickels_name(self):
        return self.input_model.get_pickels_name()

    def save_reduced_pickels(self):
        self.input_model.combine_pickels_reducing_size(Environment.TRAIN)
        self.input_model.combine_pickels_reducing_size(Environment.TEST)

    def load_image(self, src, as_gray):
        return self.output_model.load_image(src, as_gray)

    def get_x(self, environment):
        data = self.input_model.get_data(environment)
        return np.array(data[Image.DATA.value])

    def get_y(self, environment):
        data = self.input_model.get_data(environment)
        return np.array(data[Image.LABEL.value])

    def set_x(self, environment, data):
        self.input_model.set_x(environment, data)

    def set_y(self, environment, label):
        self.input_model.set_y(environment, label)

    def get_sign_values(self, labels):
        return self.signs.transform_labels_to_sign_values(labels)

    def get_categorical_vectors(self, environment, n_classes):
        if not isinstance(environment, Environment):
            raise EnvironmentException("Environment used is not a valid one")

        label_encoder = LabelEncoder()

        vectors = self.get_sign_values(self.get_y(environment))
        # vectors = label_encoder.fit_transform(labels)
        y_data = np_utils.to_categorical(vectors, num_classes=n_classes)
        return y_data

    def convert_to_one_hot_data(self):
        x_train = self.get_x(Environment.TRAIN).astype('float32')
        x_test = self.get_x(Environment.TEST).astype('float32')

        # normalizing the data to help with the training
        x_train /= 255
        x_test /= 255

        # one-hot encoding using keras' numpy-related utilities
        n_classes = np.unique(self.get_y(Environment.TRAIN)).shape[0] + 1
        y_train = self.get_categorical_vectors(Environment.TRAIN, n_classes)
        y_test = self.get_categorical_vectors(Environment.TEST, n_classes)

        self.set_y(Environment.TRAIN, y_train)
        self.set_y(Environment.TEST, y_test)

        return n_classes
