"""Module binaries.py"""
import glob
import logging
import os
import zipfile

import config


class Binaries:
    """
    <b>Notes</b><br>
    ------<br>

    Unpacks the .bin files of the model artefacts
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

        listings = glob.glob(pathname=os.path.join(self.__configurations.artefacts_, '**', '*.bin'), recursive=True)

        for listing in listings:

            logging.info('Extracting %s ...', listing)

            with zipfile.ZipFile(file=listing, mode='r') as disk:
                disk.extractall(path=os.path.dirname(listing))
