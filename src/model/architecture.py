"""Module """
import glob
import logging
import os
import shutil

import pandas as pd

import config
import src.functions.objects
import src.model.derivations


class Architecture:
    """
    <b>Class Architecture</b><br>
    -------------------<br>

    Selects the best architecture, i.e., the best model.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        # Configurations
        self.__configurations = config.Config()
        self.__storage = os.path.join(self.__configurations.numerics_, 'best')

        # A JSON (JavaScript Object Notation) read & write instance
        self.__objects = src.functions.objects.Objects()

    def __cases(self, tree: str) -> pd.DataFrame:
        """

        :param tree:
        :return:
        """

        path = os.path.join(tree, self.__configurations.branch)

        return self.__objects.frame(path=path, orient='index')

    @staticmethod
    def __median_mcc(cases: pd.DataFrame) -> float:
        """

        :param cases: Each instance represents a distinct tag; tag = annotation &#x29FA; category.<br>
        :return:
        """

        matthews: pd.Series = src.model.derivations.Derivations(cases=cases).matthews()

        return matthews.median()

    @staticmethod
    def __architecture(data: pd.DataFrame) -> str:
        """

        :param data: Whence the best is selected from.
        :return:
        """

        selection: pd.Series = data.copy().loc[data['median'].idxmax(), :]

        return selection['architecture']

    def __get_artefacts_of_best(self, architecture: str):
        """

        :param architecture:
        :return:
        """

        __src = os.path.join(os.getcwd(), 'data', 'artefacts', architecture, 'prime', 'model')
        __dst = os.path.join(self.__storage, 'model')

        try:
            message = shutil.copytree(
                src=__src, dst=__dst, symlinks=False, ignore_dangling_symlinks=True, dirs_exist_ok=True)
        except RuntimeError as err:
            raise err from err
        logging.info(message)

    def __save(self, architecture: str):
        """

        :param architecture:
        :return:
        """

        path = os.path.join(self.__storage, 'architecture.json')
        message = self.__objects.write(nodes={'name': architecture}, path=path)
        logging.info(message)

    def exc(self) -> str:
        """

        :return:
        """

        # The directories within the self.__configurations.artefacts_ directory.  Each directory
        # represents an architecture.
        trees = glob.glob(os.path.join(self.__configurations.artefacts_, '*'), recursive=False)

        # Each tree/architecture has a testing/fundamental.json dictionary
        computations = []
        for tree in trees:
            cases = self.__cases(tree=tree)
            values = {"median": self.__median_mcc(cases=cases),
                      "architecture": os.path.basename(tree)}
            computations.append(values)

        data = pd.DataFrame.from_records(computations)
        architecture = self.__architecture(data=data)

        self.__save(architecture=architecture)
        self.__get_artefacts_of_best(architecture=architecture)

        return architecture
