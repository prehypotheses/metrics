"""Module text.py"""
import collections
import os
import pathlib

import dask
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

    def __init__(self):
        """
        Constructor
        """

        # Instances
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()
        self.__tce = src.abstracts.tce.TCE()

    @dask.delayed
    def __data(self, uri: str) -> pd.DataFrame:
        """

        :param uri: A list of uniform resource identifiers, i.e., local <path> + <file name & extension> strings.
        :return:
            A training, validating, or testing data set, which includes a field of sentences alongside a field of
            each sentence's tags & tag codes.
        """

        text = src.elements.text_attributes.TextAttributes(uri=uri, header=0)

        return self.__streams.read(text=text)

    @dask.delayed
    def __string(self, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        frame = data.copy()
        frame['string'] = frame['sentence'].str.split().map(','.join)

        return frame

    @dask.delayed
    def __elements(self, data: pd.DataFrame, codes: list[int]) -> pd.DataFrame:
        """

        :param data:
        :param codes:
        :return:
        """

        return self.__tce.exc(data=data, codes=codes)

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
            path=os.path.join(self.__configurations.numerics_, 'abstracts', f'{name}.json'))

    def exc(self, uri_: list[str], codes: list[int]):
        """

        :param uri_: A list of uniform resource identifiers, i.e., local <path> + <file name & extension> strings.
        :param codes: The tag codes in focus; normally tag codes associated with the same category.
        :return:
        """

        computation = []
        for uri in uri_:
            stem = pathlib.Path(uri).stem
            data: pd.DataFrame = self.__data(uri=uri)
            data: pd.DataFrame = self.__string(data=data)
            data: pd.DataFrame = self.__elements(data=data, codes=codes)
            dictionary = self.__dictionary(data=data)

            computation.append({f'{stem}': dictionary})

        sections: list[dict] = dask.compute(computation, scheduler='threads')[0]

        nodes = {key: {'data': value} for section in sections for key, value in section.items()}

        self.__persist(nodes=nodes, name='text')
