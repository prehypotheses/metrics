"""config.py"""
import os
import numpy as np


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor<br>
        ------------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, etc.<br><br>
        """

        # Template
        self.s3_parameters_key = 's3_parameters.yaml'

        # Temporary storage area for the artefacts
        self.data_: str = os.path.join(os.getcwd(), 'data')
        self.artefacts_: str = os.path.join(self.data_, 'artefacts')

        # The self.__artefacts_ directory branch for the fundamental error matrix frequencies
        self.branch = os.path.join('prime', 'metrics', 'testing', 'fundamental.json')

        # Temporary storage area for the mathematical & business metrics
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.numerics_ = os.path.join(self.warehouse, 'numerics')
        self.graphs_ = [os.path.join(self.numerics_, 'best', 'model'),
                        os.path.join(self.numerics_, 'card', 'bullet'),
                        os.path.join(self.numerics_, 'card', 'spider'),
                        os.path.join(self.numerics_, 'cost', 'fnr'),
                        os.path.join(self.numerics_, 'cost', 'fpr'),
                        os.path.join(self.numerics_, 'abstracts')]

        # Rates, self.__rates: np.ndarray = self.__rates[..., None]
        # :param rates: An array of rate values; (0, 1\]<br>
        self.rates: np.ndarray = np.linspace(start=0, stop=1, num=101)
        self.rates: np.ndarray = (self.rates[1:])[..., None]
