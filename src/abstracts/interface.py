"""Module interface.py"""
import logging
import glob
import os
import warnings

import datasets
import pandas as pd

import config
import src.abstracts.bars
import src.abstracts.text
import src.abstracts.tree
import src.elements.s3_parameters as s3p
import src.functions.objects


class Interface:
    """
    The interface to the data package's classes
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters

        self.__configurations = config.Config()

    def __m_config(self, architecture: str) -> dict:
        """

        :return:
        """

        objects = src.functions.objects.Objects()
        uri = os.path.join(self.__configurations.artefacts_, architecture, 'optimal', 'model', 'config.json')

        return objects.read(uri=uri)

    def __get_data(self, architecture: str) -> datasets.DatasetDict:
        """

        :return:
        """

        # The data
        dataset_path = ('s3://' + self.__s3_parameters.internal + '/' +
                        self.__s3_parameters.path_internal_artefacts + architecture + '/data')
        warnings.filterwarnings("ignore", message="promote has been superseded by promote_options='default'.",
                                category=FutureWarning, module="awswrangler")

        return datasets.load_from_disk(dataset_path=dataset_path)

    def exc(self, architecture: str, tags: pd.DataFrame):
        """

        :param architecture:
        :param tags:
        :return:
        """

        # The model's configuration details
        m_config = self.__m_config(architecture=architecture)

        # Get the numeric code, i.e., `fine_ner_tag`, of each text label, i.e., `tag`
        tags = tags.assign(fine_ner_tags=tags['tag'].map(m_config['label2id']))

        # Get the modelling data
        data = self.__get_data(architecture=architecture)
        logging.info(data)

        # An approximate spread of strings
        # codes = [m_config['label2id'][key] for key in ['location-GPE']]
        # src.abstracts.text.Text().exc(uri_=uri_, codes=codes)

        # Distributions of tags.
        src.abstracts.tree.Tree(tags=tags).exc(parts=data)
        # src.abstracts.bars.Bars(tags=tags).exc(uri_=uri_)
