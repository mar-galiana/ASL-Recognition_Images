import os
import joblib
import numpy as np
from skimage import io
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from Exception.modelException import DatasetException
from Model.enumerations import Environment, Image, Dataset


class OutputModel:
    BASE_PATH = f"{os.getcwd()}/Assets/Dataset/"
    IMAGES_SRC = BASE_PATH + "Images/"
    PICKELS_SRC = BASE_PATH + "Pickels/"

    def __init__(self, width=150, height=None):
        self.width = width
        self.height = (height, width)[height is None]

    def create_pickle(self, pickel_name, dataset, environments_separated, as_gray):
        base_pickle_src = f"{self.PICKELS_SRC}{pickel_name}/"
        data = self.__get_data(dataset, environments_separated, as_gray)

        if not os.path.isdir(base_pickle_src):
            os.mkdir(base_pickle_src)

        base_pickle_src = f"{base_pickle_src}{pickel_name}_%s.pkl"

        self.__write_data_into_pickle(data[Environment.TEST][Image.DATA.value],
                                      data[Environment.TEST][Image.LABEL.value],
                                      Environment.TEST.value,
                                      base_pickle_src)
        self.__write_data_into_pickle(data[Environment.TRAIN][Image.DATA.value],
                                      data[Environment.TRAIN][Image.LABEL.value],
                                      Environment.TRAIN.value,
                                      base_pickle_src)

    def __get_data(self, dataset, environments_separated, as_gray):

        if not isinstance(dataset, Dataset):
            raise DatasetException("Dataset selected is not a valid one")

        data = {
            'description': f"resized ({int(self.width)}x{int(self.height)}) sign images from {dataset.value} dataset."
        }

        image_path = f"{self.IMAGES_SRC}{dataset.value[0]}/"
        if environments_separated:
            data[Environment.TEST] = self.__read_images(image_path + "test/", as_gray)
            data[Environment.TRAIN] = self.__read_images(image_path + "train/", as_gray)
        else:
            images_data = self.__read_images(image_path, as_gray)
            data[Environment.TEST], data[Environment.TRAIN] = self.__split_data_into_test_and_train(images_data)

        return data

    @staticmethod
    def __split_data_into_test_and_train(data):
        x = np.array(data[Image.DATA.value])
        y = np.array(data[Image.LABEL.value])
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, shuffle=True, random_state=42)

        test_data = {Image.DATA.value: x_test, Image.LABEL.value: y_test}
        train_data = {Image.DATA.value: x_train, Image.LABEL.value: y_train}

        return test_data, train_data

    def __read_images(self, path, as_gray):
        images_data = {
            Image.LABEL.value: [],
            Image.DATA.value: []
        }

        # read all images in PATH, resize and write to DESTINATION_PATH
        for subdir in os.listdir(path):
            current_path = os.path.join(path, subdir)

            if os.path.isfile(current_path):
                continue

            for file in os.listdir(current_path):
                src = os.path.join(current_path, file)
                image = io.imread(src, as_gray=as_gray)
                image = resize(image, (self.width, self.height))
                images_data[Image.LABEL.value].append(subdir)
                images_data[Image.DATA.value].append(image)

        return images_data

    def __write_data_into_pickle(self, x, y, environment, base_pickle_src):
        environment_data = {
            'description': f"resized ({int(self.width)}x{int(self.height)}) {environment}ing sign images in rgb ",
            Image.LABEL.value: y,
            Image.DATA.value: x
        }

        joblib.dump(environment_data, base_pickle_src % environment)
