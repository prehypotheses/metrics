"""Module latest.py"""
import glob
import logging
import os
import time
import sys

import config
import src.functions.objects


class Latest:
    """
    Retrieves the timestamp of the latest/best model
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        # The path to the latest best model ...
        self.__latest_ = os.path.join(self.__configurations.numerics_, 'best')

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    @staticmethod
    def __get_time(pathstr: str) -> str:
        """

        :param pathstr: The {directory} + {file name} + {extension} of a file.
        :return:
        """

        seconds: float = os.path.getmtime(pathstr)
        stamp: str = time.ctime(seconds)
        structure: time.struct_time = time.strptime(stamp)
        text: str = time.strftime('%Y-%m-%d %H:%M:%S', structure)

        return text

    def __persist(self, nodes: dict) -> str:
        """

        :param nodes: A dict encoding the time the model was saved.
        :return:
        """

        message = src.functions.objects.Objects().write(
            nodes=nodes, path=os.path.join(self.__latest_, 'latest.json'))

        return message

    def exc(self):
        """
        
        :return: 
        """

        listing = glob.glob(pathname=os.path.join(self.__latest_, 'model', '*.safetensors'))

        # Asset time stamp; determining a file's modification or creation/re-creation date & time stamp
        if len(listing) == 1:
            text = self.__get_time(pathstr=listing[0])
            message = self.__persist(nodes={"time": text})
            self.__logger.info(message)
        else:
            self.__logger.info('A *.safetensors model file was not found in %s', self.__latest_ + os.sep + 'model' + os.sep)
            sys.exit(1)
