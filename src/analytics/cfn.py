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

        :param costs: A dataframe of cost per tag, and per rate type
              <ul>
                <li>Tags: Of this project &rarr; <b>art</b>: art, etc</li>
                <li>Rate Types: false negative rate (fnr), false positive rate (fpr)</li>
              </ul><br>
        :param numbers: Per tag, and per annum, it summarises the approximate minimum & maximum expected
                        occurrences of words of a tag.<br>
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

    def exc(self, tag: str, rates: dict, boundary: float) -> dict:
        """

        :param tag:
        :param rates: The false negative rate estimates of a category.
        :param boundary: The upper boundary of a false negative rate
        :return:
        """

        # False Negative Rate Cost per tag
        cost: int = self.__costs.loc['fnr', tag]

        # The approximate minimum & maximum ...
        boundaries: pd.DataFrame = self.__numbers.loc[tag, :]

        # Hence
        estimates = self.__estimates_fnr(cost=cost, boundaries=boundaries)
        nodes = self.__nodes(estimates=estimates)
        nodes['cost'] = int(cost)
        nodes['approximate_annual_numbers'] = boundaries.to_numpy().tolist()
        nodes['rates'] = rates
        nodes['boundary'] = boundary

        return nodes
