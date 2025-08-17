"""Module tags.py"""
import logging

import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.elements.text_attributes as txa
import src.functions.streams


class Tags:
    """
    Notes<br>
    ------<br>

    Retrieves the <tags> inventory
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters
        self.__configurations = config.Config()

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        # Setting up
        uri = 's3://' + self.__s3_parameters.configurations + f'/{self.__configurations.tags_key}'
        text = txa.TextAttributes(uri=uri, header=0)

        # Read the tags data
        streams = src.functions.streams.Streams()
        tags = streams.read(text=text)

        # Preview
        logging.info(tags)

        return tags
