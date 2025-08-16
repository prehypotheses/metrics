"""Module tree.py"""
import collections
import os
import pathlib

import pandas as pd

import config
import src.elements.text_attributes as txa
import src.functions.objects
import src.functions.streams


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
        self.__streams = src.functions.streams.Streams()

    def __data(self, uri: str) -> pd.DataFrame:
        """

        :param uri:
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)

        return self.__streams.read(text=text)

    def __frequencies(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        # Tags: tag/annotation/annotation_name/category/category_name
        descriptions = self.__tags[['tag', 'group']].set_index('tag').to_dict()['group']
        frequencies = data['tagstr'].str.upper().str.split(pat=',', n=-1, expand=False).map(collections.Counter).sum()
        items = [[k, frequencies[k], descriptions[k]] for k, v in frequencies.items()]

        # As a data frame
        frame = pd.DataFrame(data=items, columns=['tag', 'frequency', 'group'])
        frame = frame.copy().merge(self.__tags[['tag', 'annotation_name']], on='tag', how='left')

        return frame

    @staticmethod
    def __restructuring(frequencies: pd.DataFrame) -> dict:
        """

        :param frequencies:
        :return:
        """

        excerpt = frequencies.loc[frequencies['tag'] != 'O', :]
        frame: pd.DataFrame = excerpt.pivot(index='group', columns='annotation_name', values='frequency')
        node = frame.to_dict(orient='index')

        miscellaneous = frequencies.loc[frequencies['tag'] == 'O', 'frequency'].values[0]
        node['Miscellaneous'] = {'beginning': int(miscellaneous), 'inside': 0}

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

    def exc(self, uri_: list):
        """

        :return:
        """

        computation = collections.ChainMap()

        for uri in uri_:
            stem = pathlib.Path(uri).stem
            data = self.__data(uri=uri)
            frequencies = self.__frequencies(data=data)
            node = self.__restructuring(frequencies=frequencies)
            computation.update({f'{stem}': node})
        nodes = dict(computation)

        self.__persist(nodes=nodes, name='tree')
