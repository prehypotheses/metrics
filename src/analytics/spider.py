"""Module spider.py"""
import logging
import os

import dask
import pandas as pd

import config
import src.functions.directories
import src.functions.objects


class Spider:
    """
    Class Spider
    """

    def __init__(self):
        """
        <b>Notes</b><br>
        -------<br>

        <ul>
            <li>self.__objects: An instance for reading & writing JSON (JavaScript Object Notation) files.</li>
            <li>self.__path: The directory wherein the data files, for the spider graphs, are stored.</li>
        </ul>
        """

        # Setting-up
        self.__objects = src.functions.objects.Objects()
        self.__path = os.path.join(config.Config().numerics_, 'card', 'spider')

        # The metrics in focus
        self.__names = {'precision': "Precision", 'sensitivity': "Sensitivity", 'specificity': 'Specificity',
                        'fscore': 'F Score', 'balanced_accuracy': 'Balanced Accuracy',
                        'standard_accuracy': 'Standard Accuracy'}

    def __save(self, nodes: dict, name: str) -> str:
        """

        :param nodes: The dictionary of values for the spider graph
        :param name: The name of the file; filename & extension.
        :return:
        """

        return self.__objects.write(nodes=nodes, path=os.path.join(self.__path, name))

    @dask.delayed
    def __build(self, excerpt: pd.DataFrame, name: str) -> str:
        """

        :param excerpt:
        :param name:
        :return:
        """

        excerpt.rename(columns=self.__names, inplace=True)

        # The dictionary of the instances
        nodes = excerpt.to_dict(orient='tight')

        # Save
        return self.__save(nodes=nodes, name=f'{name}.json')

    def exc(self, derivations: pd.DataFrame, definitions: dict):
        """

        :param derivations: A data frame consisting of error matrix frequencies & metrics, alongside
                            tags & categories identifiers.
        :param definitions: A dict wherein key === category code, value === category code definition
        :return:
        """

        data = derivations.copy()

        # The unique tag categories
        categories = data['category'].unique()

        # The tag & category values are required for data structuring
        data.set_index(keys=['tag', 'category'], drop=False, inplace=True)

        # Hence
        computations = []
        for category in categories:
            name = definitions[category]
            excerpt: pd.DataFrame = data.loc[data['category'] == category, self.__names.keys()]
            message = self.__build(excerpt=excerpt, name=name)
            computations.append(message)

        messages = dask.compute(computations, scheduler='threads')[0]
        logging.info(messages)
