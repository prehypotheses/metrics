"""
This is data type Limits
"""
import typing

import pandas as pd


class Limits(typing.NamedTuple):
    """
    The data type class ⇾ Limits

    Attributes
    ----------
    costs : pandas.DataFrame
      The false negative rate & false positive rate cost per category.

    frequencies : pandas.DataFrame
      In relation to a set of documents, and the total number of words therein.  This records the approximate
      percentage of words that fall into each category; each category has a minimum & maximum approximation.

    error : pandas.DataFrame
      The preferred false negative rate & false positive rate error limit per category.

    dispatches : pandas.DataFrame
        The approximate

    """

    costs: pd.DataFrame
    frequencies: pd.DataFrame
    error: pd.DataFrame
    dispatches: pd.DataFrame
