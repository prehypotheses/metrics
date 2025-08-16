"""Module cost.py"""
import logging
import os

import dask
import pandas as pd

import config
import src.analytics.cfn
import src.analytics.cfp
import src.elements.limits as lm
import src.functions.objects


class Cost:
    """
    Class Costs
    """

    def __init__(self, limits: lm.Limits, numbers: pd.DataFrame, derivations: pd.DataFrame):
        """

        :param limits: Refer to src.elements.limits
        :param numbers:
        :param derivations: A data frame consisting of error matrix frequencies & metrics, alongside
                     tags & categories identifiers.
        """

        self.__limits = limits
        self.__numbers = numbers
        self.__derivations = derivations

        # Configurations
        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        # Instances
        self.__cfn = src.analytics.cfn.CFN(costs=self.__limits.costs, numbers=self.__numbers)
        self.__cfp = src.analytics.cfp.CFP(costs=self.__limits.costs, numbers=self.__numbers)

    @dask.delayed
    def __fnr(self, category: str) -> dict:
        """

        :param category:
        :return:
        """

        excerpt = self.__derivations.loc[self.__derivations['category'] == category, ['tag', 'fnr']].set_index(keys='tag')
        rates = excerpt.to_dict(orient='dict')['fnr']
        boundary = self.__limits.error.loc[category, 'fnr']

        return self.__cfn.exc(category=category, rates=rates, boundary=boundary)

    @dask.delayed
    def __fpr(self, category: str) -> dict:
        """

        :param category:
        :return:
        """

        excerpt = self.__derivations.loc[self.__derivations['category'] == category, ['tag', 'fpr']].set_index(keys='tag')
        rates = excerpt.to_dict(orient='dict')['fpr']
        boundary = self.__limits.error.loc[category, 'fpr']

        return self.__cfp.exc(category=category, rates=rates, boundary=boundary)

    @dask.delayed
    def __persist(self, nodes: dict, metric: str, name: str) -> str:
        """

        :param nodes: The graph data.
        :param metric: fnr (false negative rate) or fpr (false positive rate)
        :param name:
        :return:
        """

        # The file name, and path; path = directory + file name
        path = os.path.join(self.__configurations.numerics_, 'cost', metric, f'{name}.json')

        return self.__objects.write(nodes=nodes, path=path)

    def exc(self, definitions: dict):
        """

        :param definitions: A dict wherein key === category code, value === category code definition
        :return:
        """

        categories = list(self.__numbers.index)
        computations = []
        for category in categories:

            fnr = self.__fnr(category=category)
            _fnr = self.__persist(nodes=fnr, metric='fnr', name=definitions[category])
            fpr = self.__fpr(category=category)
            _fpr = self.__persist(nodes=fpr, metric='fpr', name=definitions[category])

            computations.append([_fnr, _fpr])

        calculations = dask.compute(computations, scheduler='threads')[0]
        logging.info(calculations)
