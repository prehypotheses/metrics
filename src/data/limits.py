"""Module limits.py"""
import pandas as pd

import src.elements.limits as lm
import src.elements.s3_parameters as s3p


class Limits:
    """
    Description<br>
    ------------<br>
    Retrieves a <limits> file from its Amazon S3 (Simple Storage Service) bucket.<br>
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters

        # The Amazon S3 (Simple Storage Service) path.
        self.__path = f's3://{self.__s3_parameters.configurations}/numerics/'

    def __get_data(self, filename: str, orient: str):
        """

        :param filename: The file of interest.
        :param orient: The read-in orientation.
        :return:
        """

        try:
            frame = pd.read_json(path_or_buf=(self.__path + filename), orient=orient)
        except FileNotFoundError as err:
            raise err from err

        return frame

    def exc(self) -> lm.Limits:
        """

        :return:
        """

        costs: pd.DataFrame = self.__get_data(filename='costs.json', orient='split')
        frequencies: pd.DataFrame = self.__get_data(filename='frequencies.json', orient='index')
        error: pd.DataFrame = self.__get_data(filename='error.json', orient='index')
        documents: pd.DataFrame = self.__get_data(filename='documents.json', orient='split')

        return lm.Limits(costs=costs, frequencies=frequencies, error=error, documents=documents)
