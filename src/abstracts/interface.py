"""Module interface.py"""
import glob
import os

import pandas as pd

import config
import src.abstracts.tree
import src.abstracts.text
import src.abstracts.bars
import src.functions.objects


class Interface:
    """
    The interface to the data package's classes
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def __m_config(self, architecture: str) -> dict:
        """

        :return:
        """

        objects = src.functions.objects.Objects()
        uri = os.path.join(self.__configurations.artefacts_, architecture, 'prime', 'model', 'config.json')

        return objects.read(uri=uri)

    def exc(self, architecture: str, tags: pd.DataFrame):
        """

        :param architecture:
        :param tags:
        :return:
        """

        m_config = self.__m_config(architecture=architecture)
        uri_ = glob.glob(pathname=os.path.join(self.__configurations.artefacts_, architecture, 'data', '*.csv'))

        # An approximate spread of strings
        codes = [m_config['label2id'][key] for key in ['B-geo', 'I-geo']]
        src.abstracts.text.Text().exc(uri_=uri_, codes=codes)

        # Distributions of tags.
        src.abstracts.tree.Tree(tags=tags).exc(uri_=uri_)
        src.abstracts.bars.Bars(tags=tags).exc(uri_=uri_)
