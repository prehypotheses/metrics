"""
This is data type Model
"""
import typing

import pandas as pd


class Model(typing.NamedTuple):
    """
    The data type class ⇾ Best

    Attributes
    ----------
    architecture : str
      The underlying architecture, and name, of the best model

    derivations : pandas.DataFrame
      A frame of error matrix frequencies and error matrix metrics, per classification category

    """

    architecture: str
    derivations: pd.DataFrame
