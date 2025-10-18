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
    def __fnr(self, tag: str) -> dict:
        """

        :param tag:
        :return:
        """

        excerpt = self.__derivations.loc[self.__derivations['tag'] == tag, ['tag', 'fnr']].set_index(keys='tag')
        rates = excerpt.to_dict(orient='dict')['fnr']
        boundary = self.__limits.error.loc[tag, 'fnr']

        return self.__cfn.exc(tag=tag, rates=rates, boundary=boundary)

    @dask.delayed
    def __fpr(self, tag: str) -> dict:
        """

        :param tag:
        :return:
        """

        excerpt = self.__derivations.loc[self.__derivations['tag'] == tag, ['tag', 'fpr']].set_index(keys='tag')
        rates = excerpt.to_dict(orient='dict')['fpr']
        boundary = self.__limits.error.loc[tag, 'fpr']

        return self.__cfp.exc(tag=tag, rates=rates, boundary=boundary)

    @dask.delayed
    def __persist(self, nodes: dict, metric: str, name: str) -> str:
        """

        :param nodes: The graph data.
        :param metric: fnr (false negative rate) or fpr (false positive rate)
        :param name:
        :return:
        """

        # The file name, and path; path = directory + file name
        path = os.path.join(self.__configurations.metrics_, 'cost', metric, f'{name}.json')

        return self.__objects.write(nodes=nodes, path=path)

    def exc(self, definitions: dict):
        """

        :param definitions: A dict wherein key === tag, value === category
        :return:
        """

        tags = list(self.__numbers.index)
        computations = []
        for tag in tags:
            fnr = self.__fnr(tag=tag)
            _fnr = self.__persist(nodes=fnr, metric='fnr', name=definitions[tag])
            fpr = self.__fpr(tag=tag)
            _fpr = self.__persist(nodes=fpr, metric='fpr', name=definitions[tag])
            computations.append([_fnr, _fpr])

        calculations = dask.compute(computations, scheduler='threads')[0]
        logging.info('cost:\n%s', calculations)
