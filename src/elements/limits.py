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
      This frame is in relation to documents, and the total number of words
      therein; annually.  The frame encodes the approximate percentage
      of words that fall into each category; each category has a minimum &
      maximum approximation.

    error : pandas.DataFrame
      The preferred false negative rate & false positive rate error limit per category.

    documents : pandas.DataFrame
        The approximate number of documents, and approximate of words/strings
        per document, expected annually.

    """

    costs: pd.DataFrame
    frequencies: pd.DataFrame
    error: pd.DataFrame
    documents: pd.DataFrame
