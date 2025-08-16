"""Module cfn.py"""
import numpy as np
import pandas as pd

import config


class CFN:
    """
    False Negative Rate Cost
    """

    def __init__(self, costs: pd.DataFrame, numbers: pd.DataFrame):
        """

        :param costs: A dataframe of cost per category, and per rate type
              <ul>
                <li>Categories: Of this project &rarr; <b>GEO</b>: geographic, <b>GPE</b>: geopolitical,
                    <b>ORG</b>: organisation, <b>PER</b>: person, <b>TIM</b>: time, <b>O</b>: miscellaneous</li>
                <li>Rate Types: false negative rate (fnr), false positive rate (fpr)</li>
              </ul><br>
        :param numbers: Per category, and per annum, it summarises the approximate minimum & maximum expected
                        occurrences of words in the category.<br>
        """

        self.__rates = config.Config().rates
        self.__costs = costs
        self.__numbers = numbers

    def __estimates_fnr(self, cost: int, boundaries: pd.DataFrame) -> np.ndarray:
        """

        :param cost:
        :param boundaries:
        :return:
        """

        n_inflection = 500

        # Possible missed classifications range per rate value of a static annual frequency range
        numbers = np.multiply(
            self.__rates, np.expand_dims(boundaries.to_numpy(), axis=0))

        # Hence
        factors = cost * (1 + 0.5*(numbers > n_inflection).astype(int))
        liabilities = np.multiply(factors, numbers)
        estimates = np.concat((self.__rates, liabilities), axis=1)

        return estimates

    @staticmethod
    def __nodes(estimates: np.ndarray) -> dict:
        """

        :param estimates:
        :return:
        """

        # x: rate, low: ~ minimum cost, high: ~ maximum cost
        data = pd.DataFrame(data=estimates, columns=['x', 'low', 'high'])
        nodes = data.to_dict(orient='tight')

        return nodes

    def exc(self, category: str, rates: dict, boundary: float) -> dict:
        """

        :param category:
        :param rates: The false negative rate estimates of a category; split by
                annotation type, i.e., I (inside), B (beginning)
        :param boundary: The upper boundary of a false negative rate
        :return:
        """

        # False Negative Rate Cost per Category
        cost: int = self.__costs.loc['fnr', category]

        # The approximate minimum & maximum ...
        boundaries: pd.DataFrame = self.__numbers.loc[category, :]

        # Hence
        estimates = self.__estimates_fnr(cost=cost, boundaries=boundaries)
        nodes = self.__nodes(estimates=estimates)
        nodes['cost'] = int(cost)
        nodes['approximate_annual_numbers'] = boundaries.to_numpy().tolist()
        nodes['rates'] = rates
        nodes['boundary'] = boundary

        return nodes
