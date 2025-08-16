"""Module pickles.py"""
import glob
import logging
import os
import pickle

import config


class Pickles:
    """
    <b>Notes</b><br>
    ------<br>

    Unpacks the .pkl files of the model artefacts
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def exc(self):
        """

        :return:
        """

        listings = glob.glob(pathname=os.path.join(self.__configurations.artefacts_, '**', '*.pkl'), recursive=True)

        for listing in listings:

            logging.info('Extracting %s ...', listing)

            with open(file=listing, mode='rb') as disk:
                content = pickle.load(disk)

            logging.info(content)
