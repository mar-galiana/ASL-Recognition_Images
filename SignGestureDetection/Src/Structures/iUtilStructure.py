import os
import json
from enum import Enum
from abc import abstractmethod
from path import MODEL_PICKELS_FILE
from Exception.structureException import StructureException, StructureFileElementDoesNotExists
from Exception.inputOutputException import PathDoesNotExistException


class IUtilStructure(object):

    @staticmethod
    def save_pickels_used(structure, pickels_name, model_name):
        data = {}

        if os.path.exists(MODEL_PICKELS_FILE):
            with open(MODEL_PICKELS_FILE) as file:
                data = json.load(file)
                file.close()

        if structure is Structure.NeuralNetwork:
            data[structure.value][model_name] = {
                NeuralNetworkInformation.Pickel: pickels_name,
                NeuralNetworkInformation.Type: pickels_name.split("_")[0]
            }

        elif structure is Structure.DecisionTree:
            data[structure.value][model_name] = pickels_name

        else:
            raise StructureException("Structure selected is not a valid one")

        with open(MODEL_PICKELS_FILE, 'w') as file:
            json.dump(data, file)
            file.close()

    @staticmethod
    def get_pickels_used(structure, model_name):
        if not os.path.exists(MODEL_PICKELS_FILE):
            raise PathDoesNotExistException("File " + MODEL_PICKELS_FILE + "not found")

        with open(MODEL_PICKELS_FILE) as file:
            data = json.load(file)
            file.close()

        if structure.value not in data or model_name not in data[structure.value]:
            raise StructureFileElementDoesNotExists("There is no " + structure.value + " with the " + model_name +
                                                    " model")

        if structure is Structure.NeuralNetwork:
            neural_network = data[structure.value][model_name]
            pickels = neural_network[NeuralNetworkInformation.Pickel.value].split("-")
            nn_type = neural_network[NeuralNetworkInformation.Type.value]
            values = pickels, nn_type

        elif structure is Structure.NeuralNetwork:
            pickels = data[structure.value][model_name].split("-")
            values = pickels

        else:
            raise StructureException("Structure selected is not a valid one")

        return values

    @abstractmethod
    def save_model(self, model):
        pass

    @abstractmethod
    def load_model(self, name_model):
        pass

    @abstractmethod
    def resize_single_image(self, image):
        pass


class Structure(Enum):
    DecisionTree = "decision_tree"
    NeuralNetwork = "neural_network"


class NeuralNetworkInformation(Enum):
    Pickel = "pickel"
    Type = "type"
