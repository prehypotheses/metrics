"""Module properties.py"""
import os

import pandas as pd

import config
import src.elements.model as ml
import src.functions.objects
import src.model.derivations


class Properties:
    """
    Determines the error measures & metrics of a model
    """

    def __init__(self, architecture: str):
        """

        :param architecture: The best model/architecture
        """

        self.__architecture = architecture

        # Configurations
        self.__configurations = config.Config()

    def __cases(self) -> pd.DataFrame:
        """

        :return: Each instance represents a distinct tag; tag = annotation &#x29FA; category.
                 The frame must include the error matrix frequencies is tp, tn, fp, & fn.
        """

        path = os.path.join(
            self.__configurations.artefacts_, self.__architecture, self.__configurations.branch)
        cases = src.functions.objects.Objects().frame(path=path, orient='index')

        return cases

    @staticmethod
    def __derivations(cases: pd.DataFrame) -> pd.DataFrame:
        """
        Appends a series of metrics to each instance.

        :param cases: Each instance represents a distinct tag; tag = annotation &#x29FA; category.
                      The frame must include the error matrix frequencies is tp, tn, fp, & fn.
        :return:
        """

        derivations = src.model.derivations.Derivations(cases=cases).exc()
        derivations.reset_index(drop=False, inplace=True)
        derivations.rename(columns={'index': 'tag'}, inplace=True)
        derivations['tag'] = derivations['tag'].str.upper()

        return derivations

    def exc(self, tags: pd.DataFrame) -> ml.Model:
        """

        :param tags: A data frame summarising the projects tags, alongside each tag's annotation and category details.
        :return:
        """

        # A category column.
        values = tags[['tag', 'category']].set_index(keys='tag').to_dict(orient='dict')

        # The error matrix frequencies per case/category; and their error metrics derivations.
        cases = self.__cases()
        derivations = self.__derivations(cases=cases)
        derivations = derivations.assign(category=derivations['tag'].map(values['category']))

        return ml.Model(architecture=self.__architecture, derivations=derivations)
