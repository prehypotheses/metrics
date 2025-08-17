"""Module cfp.py"""
import numpy as np
import pandas as pd

import config


class CFP:
    """
    False Positive Rate Cost
    """

    def __init__(self, costs: pd.DataFrame, numbers: pd.DataFrame):
        """

        :param costs: A dataframe of cost per category, and per rate type
              <ul>
                <li>Categories: Of this project &rarr; <b>art</b>: art, etc.</li>
                <li>Rate Types: false negative rate (fnr), false positive rate (fpr)</li>
              </ul><br>
        :param numbers: Per category, and per annum, it summarises the approximate minimum & maximum expected
                        occurrences of words in the category.<br>
        """

        self.__rates = config.Config().rates
        self.__costs = costs
        self.__numbers = numbers

    def __estimates_fpr(self, cost: int, boundaries: np.ndarray) -> np.ndarray:
        """

        :param cost:
        :param boundaries:
        :return:
        """

        numbers: np.ndarray = np.multiply(self.__rates, np.expand_dims(boundaries, axis=0))
        liabilities: np.ndarray = cost * numbers
        estimates = np.concat((self.__rates, liabilities), axis=1)

        return estimates

    def exc(self, category: str, rates: dict, boundary: float) -> dict:
        """

        :param category:
        :param rates: The false positive rate estimates of a category.
        :param boundary: The upper boundary of a false positive rate
        :return:
        """

        # False Positive Rate Cost per Category
        cost = self.__costs.loc['fpr', category]

        # The approximate minimum & maximum ...
        boundaries = self.__numbers.loc[category, :].to_numpy()

        # Hence
        estimates = self.__estimates_fpr(cost=cost, boundaries=boundaries)

        # Nodes
        nodes = pd.DataFrame(data=estimates, columns=['x', 'low', 'high']).to_dict(orient='tight')
        nodes['cost'] = int(cost)
        nodes['approximate_annual_numbers'] = boundaries.tolist()
        nodes['rates'] = rates
        nodes['boundary'] = boundary

        return nodes
