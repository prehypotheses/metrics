"""Module bullet.py"""
import logging
import os

import dask
import pandas as pd

import config
import src.functions.directories
import src.functions.objects


class Bullet:
    """
    Description<br>
    ------------<br>
    Prepares the data for the <b>False Negative Rate</b> & <b>False Positive Rate</b> bullet graphs.
    """

    def __init__(self, error: pd.DataFrame):
        """
        <b>Notes</b><br>
        -------<br>

        <ul>
            <li>self.__objects: An instance for reading & writing JSON (JavaScript Object Notation) files.</li>
            <li>self.__path: The directory wherein the data files, for the bullet graphs, are stored.</li>
        </ul>

        :param error: A data frame of false negative rate & false positive rate limits per
                      category; and implicitly per tag associated with a category.
        """

        # The metrics in focus.
        self.__names = {'fnr': 'False Negative Rate', 'fpr': 'False Positive Rate'}
        error = error[self.__names.keys()]
        error.rename(columns=self.__names, inplace=True)
        self.__error = error

        # Setting-up
        self.__objects = src.functions.objects.Objects()
        self.__path = os.path.join(config.Config().metrics_, 'card', 'bullet')

    def __save(self, nodes: dict, name: str) -> str:
        """

        :param nodes: The dictionary of values for the spider graph
        :param name: The name of the file; filename & extension.
        :return:
        """

        return self.__objects.write(nodes=nodes, path=os.path.join(self.__path, name))

    @dask.delayed
    def __build(self, excerpt: pd.DataFrame, name: str, tag: str) -> str:
        """

        :param excerpt:
        :param name:
        :param tag:
        :return:
        """

        excerpt.rename(columns=self.__names, inplace=True)

        # The dictionary of the instances
        nodes = excerpt.to_dict(orient='split')
        nodes['target'] = self.__error.loc[tag, nodes['columns']].to_list()

        return self.__save(nodes=nodes, name=f'{name}.json')

    def exc(self, derivations: pd.DataFrame, definitions: dict):
        """

        :param derivations: A data frame consisting of error matrix frequencies & metrics, alongside
                            tags & categories identifiers.
        :param definitions: A dict wherein key === tag, value === category
        :return:
        """

        data = derivations.copy()

        # The unique tag categories
        tags = data['tag'].unique()

        # The tag & category values are required for data structuring
        data.set_index(keys=['tag'], drop=False, inplace=True)

        # Hence
        computations = []
        for tag in tags:
            name = definitions[tag]
            excerpt: pd.DataFrame = data.loc[data['tag'] == tag, self.__names.keys()]
            message = self.__build(excerpt=excerpt, name=name, tag=tag)
            computations.append(message)

        messages = dask.compute(computations, scheduler='threads')[0]
        logging.info('bullet:\n%s', messages)
