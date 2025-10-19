"""Module bars.py"""
import logging
import collections
import json
import os

import datasets
import pandas as pd

import config
import src.functions.objects


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

        # Graphing categories
        self.__categories = ['train', 'validation', 'test']

    @staticmethod
    def __frequencies(data: pd.DataFrame, name: str):
        """

        :param data:
        :return:
        """

        # tags: tag|category|category_name|group & fine_ner_tags
        frequencies = data['fine_ner_tags'].map(collections.Counter).sum()
        items = [[k, frequencies[k]] for k, v in frequencies.items()]

        # As a data frame
        frame = pd.DataFrame(data=items, columns=['fine_ner_tags', 'frequency'])
        frame.rename(columns={'frequency': name}, inplace=True)
        frame.set_index(keys='fine_ner_tags', drop=True, inplace=True)

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
            section['stack'] = 'entities'
            section['visible'] = True

        return section

    def __structure(self, computations: list[pd.DataFrame]) -> pd.DataFrame:
        """

        :param computations:
        :return:
        """

        frame = pd.concat(computations, axis=1, ignore_index=False)
        frame.reset_index(drop=False, inplace=True)
        data = frame.copy().merge(self.__tags.copy()[['fine_ner_tags', 'tag']], how='left', on='fine_ner_tags')
        data.set_index(keys='tag', drop=True, inplace=True)

        return data

    def exc(self, parts: datasets.DatasetDict):
        """

        :param parts:
        :return:
        """

        # Determining frequencies of tags per data set
        computations = []
        for name in list(parts.keys()):
            data = parts[name].to_pandas()
            frequencies = self.__frequencies(data=data, name=name)
            computations.append(frequencies)
        frame = self.__structure(computations=computations)

        # Convert each row into a dict of values vis-à-vis tags
        sections = []
        for i in range(frame.shape[0]):
            values: pd.Series = frame.loc[frame.index[i], :]
            sections.append(self.__get_section(values=values.copy()))

        # Persist
        nodes = {'categories': self.__categories, 'series': sections}
        message = src.functions.objects.Objects().write(
            nodes=nodes, path=os.path.join(self.__configurations.metrics_, 'abstracts', 'bars.json'))
        logging.info('distribution bars graph: %s', message)
