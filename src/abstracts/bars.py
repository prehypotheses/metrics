"""Module bars.py"""
import collections
import json
import os
import pathlib

import pandas as pd

import config
import src.elements.text_attributes as txa
import src.functions.objects
import src.functions.streams


class Bars:
    """
    Creates the data structure for drawing grouped & stacked bar graphs
    """

    def __init__(self, tags: pd.DataFrame):
        """

        :param tags:
        """

        self.__tags = tags

        # Instances
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

        # Graphing categories
        self.__categories = ['training', 'validating', 'testing']

    def __data(self, uri: str) -> pd.DataFrame:
        """

        :param uri:
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)

        return self.__streams.read(text=text)

    @staticmethod
    def __frequencies(data: pd.DataFrame, stem: str):
        """

        :param data:
        :return:
        """

        # Tags: tag/annotation/annotation_name/category/category_name
        frequencies = data['tagstr'].str.upper().str.split(pat=',', n=-1, expand=False).map(collections.Counter).sum()
        items = [[k, frequencies[k]] for k, v in frequencies.items()]

        # As a data frame
        frame = pd.DataFrame(data=items, columns=['tag', 'frequency'])
        frame.rename(columns={'frequency': stem}, inplace=True)
        frame.set_index(keys='tag', drop=True, inplace=True)

        return frame

    def __get_section(self, values: pd.Series):
        """

        :param values:
        :return:
        """

        string = values[self.__categories].to_json(orient='split')
        section = json.loads(string)
        section.pop('index', None)

        if section['name'] == 'O':
            section['stack'] = 'other/miscellaneous'
            section['visible'] = False
        else:
            section['stack'] = values['annotation_name']
            section['visible'] = True

        return section

    def __structure(self, computations: list[pd.DataFrame]) -> pd.DataFrame:
        """

        :param computations:
        :return:
        """

        frame = pd.concat(computations, axis=1, ignore_index=False)
        frame.reset_index(drop=False, inplace=True)
        data = frame.copy().merge(self.__tags.copy()[['tag', 'annotation_name', 'group']], how='left', on='tag')
        data.set_index(keys='tag', drop=True, inplace=True)

        return data

    def exc(self, uri_: list):
        """

        :param uri_:
        :return:
        """

        # Determining frequencies of tags per data set
        computations = []
        for uri in uri_:
            data = self.__data(uri=uri)
            frequencies = self.__frequencies(data=data, stem=pathlib.Path(uri).stem)
            computations.append(frequencies)
        frame = self.__structure(computations=computations)

        # Convert each row into a dict of values vis-à-vis an annotation scheme
        sections = []
        for i in range(frame.shape[0]):
            values: pd.Series = frame.loc[frame.index[i], :]
            sections.append(self.__get_section(values=values.copy()))

        # Persist
        nodes = {'categories': self.__categories, 'series': sections}
        src.functions.objects.Objects().write(
            nodes=nodes, path=os.path.join(self.__configurations.numerics_, 'abstracts', 'bars.json'))
