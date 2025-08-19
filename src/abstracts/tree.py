"""Module tree.py"""
import collections
import os

import datasets
import pandas as pd

import config
import src.functions.objects


class Tree:
    """
    Class Distributions
    """

    def __init__(self, tags: pd.DataFrame):
        """

        :param tags:
        """

        self.__tags = tags

        # Instances
        self.__configurations = config.Config()

    def __frequencies(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        # tags: tag|category|category_name|group & fine_ner_tags
        descriptions = self.__tags[['fine_ner_tags', 'category_name']].set_index('fine_ner_tags').to_dict()['category_name']

        # frequencies dictionary: Each key is a fine entity tag, whilst each value is the tag count
        frequencies = data['fine_ner_tags'].map(collections.Counter).sum()
        items = [[k, frequencies[k], descriptions[k]] for k, v in frequencies.items()]

        # As a data frame
        frame = pd.DataFrame(data=items, columns=['fine_ner_tags', 'frequency', 'category_name'])
        frame = frame.copy().merge(self.__tags[['fine_ner_tags', 'tag', 'group']], on='fine_ner_tags', how='left')

        return frame

    @staticmethod
    def __restructuring(frequencies: pd.DataFrame) -> dict | list[dict]:
        """

        :param frequencies:
        :return:
        """


        node = frequencies.to_dict(orient='records')

        return node

    def __persist(self, nodes:dict, name: str):
        """

        :param nodes: The tree drawing data, as structurally required
        :param name:
        :return:
        """

        src.functions.objects.Objects().write(
            nodes=nodes,
            path=os.path.join(self.__configurations.numerics_, 'abstracts', f'{name }.json'))

    def exc(self, parts: datasets.DatasetDict):
        """

        :param parts:
        :return:
        """

        computation = collections.ChainMap()

        for name in list(parts.keys()):
            data = parts[name].to_pandas()
            frequencies = self.__frequencies(data=data)
            node = self.__restructuring(frequencies=frequencies)
            computation.update({f'{name}': node})
        nodes = dict(computation)

        self.__persist(nodes=nodes, name='tree')
