"""Module text.py"""
import collections
import os

import dask
import datasets
import pandas as pd

import config
import src.abstracts.tce
import src.elements.text_attributes
import src.functions.objects
import src.functions.streams


class Text:
    """
    Text
    """

    def __init__(self, parts: datasets.DatasetDict):
        """

        :param parts:
        """

        self.__parts = parts
        self.__names = list(self.__parts.keys())

        # Instances
        self.__configurations = config.Config()
        self.__tce = src.abstracts.tce.TCE()

    @dask.delayed
    def __elements(self, data: pd.DataFrame, code: int) -> pd.DataFrame:
        """

        :param data:
        :param code:
        :return:
        """

        return self.__tce.exc(data=data, code=code)

    @dask.delayed
    def __dictionary(self, data: pd.DataFrame) -> list:
        """

        :param data:
        :return:
        """

        frequencies: dict = data['elements'].str.upper().str.split(pat=',', n=-1, expand=False).map(collections.Counter).sum()
        dictionary = [{'name': key, 'weight': value} for key, value in frequencies.items() if key != '']

        return dictionary

    def __persist(self, nodes: dict, name: str) -> str:
        """

        :param nodes: The strings cloud drawing data, as structurally required.
        :param name:
        :return:
        """

        return src.functions.objects.Objects().write(
            nodes=nodes,
            path=os.path.join(self.__configurations.metrics_, 'abstracts', 'text', f'{name}.json'))

    def exc(self, code: int, category: str) -> str:
        """

        :param code:
        :param category:
        :return:
        """

        computation = []
        for name in self.__names:
            data: pd.DataFrame = self.__parts[name].to_pandas()
            data: pd.DataFrame = self.__elements(data=data, code=code)
            dictionary = self.__dictionary(data=data)
            computation.append({f'{name}': dictionary})

        sections: list[dict] = dask.compute(computation, scheduler='threads')[0]

        nodes = {key: {'data': value} for section in sections for key, value in section.items()}

        return self.__persist(nodes=nodes, name=category)
