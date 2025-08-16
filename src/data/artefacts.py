"""Module artefacts.py"""
import os

import numpy as np
import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.keys


class Artefacts:
    """
    The artefacts per architecture
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service:
        :param s3_parameters:
        """

        self.__service = service
        self.__s3_parameters = s3_parameters

        # Configurations
        self.__configurations = config.Config()

    def __keys(self) -> list:
        """

        :return:
        """

        listings = src.s3.keys.Keys(service=self.__service, bucket_name=self.__s3_parameters.internal).excerpt(
            prefix=self.__s3_parameters.path_internal_artefacts, delimiter='/')

        return listings

    @staticmethod
    def __excerpt(keys: list) -> list:
        """

        :param keys:
        :return:
        """

        listings = [[prefix + partition]
                    for partition in ['data', 'prime/model', 'prime/metrics']
                    for prefix in keys]
        listings = sum(listings, [])

        return listings

    def __strings(self, sources: np.ndarray):
        """

        :param sources: An array of Amazon S3 (Simple Storage Service) prefixes
        :return:
        """

        # A data frame consisting of the S3 keys ...
        frame = pd.DataFrame(data={'source': sources})

        # ... and local storage area.  For the local storage area, ensure that the
        # appropriate directory separator is in place.
        frame = frame.assign(destination=frame['source'])
        frame = frame.assign(destination=frame['destination'].replace(to_replace='/', value=os.path.sep))
        frame = frame.assign(destination=self.__configurations.data_ + os.path.sep + frame['destination'])

        return frame

    def exc(self):
        """
        Determining the unique segments of fine-tuned models

        :return:
        """

        # The keys within the <artefacts> prefix
        keys = self.__keys()

        # Focusing on the keys within the model & metrics paths
        keys = self.__excerpt(keys=keys)

        # Hence, the distinct model & metrics sources/paths
        sources = np.array(keys)

        # Source & Destination
        strings = self.__strings(sources=sources)

        return strings
