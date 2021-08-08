from Model.enumerations import Dataset
from StrategyFactory.iStrategy import IStrategy
from Exception.inputOutputException import InputException


class SaveDatabaseStrategy(IStrategy):

    def __init__(self, logger, model, arguments):
        arguments[1] = arguments[1]
        self.check_input_values(arguments)

        self.logger = logger
        self.model = model
        self.__show_arguments_entered(arguments)

        self.pickel_name = arguments[0]
        self.dataset = Dataset(arguments[1])
        self.environments_separated = (arguments[2] == "true")
        self.as_gray = (arguments[3] == "true")

    def __show_arguments_entered(self, arguments):
        info_arguments = "Arguments entered:\n" \
                         "\t* Pickel's name: " + arguments[0] + "\n" \
                         "\t* Dataset: " + arguments[1] + "\n" \
                         "\t* Environments separated: " + arguments[2] + "\n" \
                         "\t* Save dataset in gray colors: " + arguments[3]
        self.logger.write_info(info_arguments)

    def check_input_values(self, arguments):
        if arguments[1] not in list(map(lambda c: c.value, Dataset)):
            raise InputException("Check help strategy to know the possible datasets to use")

        if not self.__is_boolean_argument_correct(arguments[2]) or not self.__is_boolean_argument_correct(arguments[3]):
            raise InputException("The third and fourth arguments of this execution needs to be true or false")

    def execute(self):
        self.model.create_pickle(self.pickel_name, self.dataset, self.environments_separated, self.as_gray)
        self.logger.write_info("Test and Train pickles have been created")

    @staticmethod
    def __is_boolean_argument_correct(value):
        return value.lower() == "true" or value.lower() == "false"
