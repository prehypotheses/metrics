"""Module interface.py"""
import logging
import sys

import dask
import pandas as pd

import src.data.artefacts
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.directives


class Interface:
    """
    Notes<br>
    ------<br>

    The data, i.e., models artefacts, retrieval interface.
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__service = service
        self.__s3_parameters = s3_parameters

        # Directives
        self.__directives = src.s3.directives.Directives()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)30d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    @dask.delayed
    def __get_assets(self, origin: str, target: str) -> int:
        """

        :param origin:
        :param target:
        :return:
        """

        return self.__directives.synchronise(
            source_bucket=self.__s3_parameters.internal, origin=origin, target=target)

    def __data(self, strings: pd.DataFrame) -> None:
        """

        :param strings:
        :return:
        """

        # Hence, retrieve the artefacts
        computation = []
        for origin, target in zip(strings['source'], strings['destination']):
            code = self.__get_assets(origin=origin, target=target)
            computation.append(code)
        executions = dask.compute(computation, scheduler='threads')[0]

        if all(executions) == 0:
            self.__logger.info('Artefacts of models retrieved.')
        else:
            sys.exit('Unsuccessful artefacts download attempt.')

    def exc(self) -> None:
        """

        :return:
        """

        # Get the artefacts metadata
        strings = src.data.artefacts.Artefacts(
            service=self.__service, s3_parameters=self.__s3_parameters).exc()
        logging.info(strings)

        # The artefacts
        self.__data(strings=strings)
