"""Module dictionary.py"""
import glob
import logging
import os

import pandas as pd


class Dictionary:
    """
    Class Dictionary
    """

    def __init__(self):
        """
        Constructor
        """

        _scores = ('A spider graph data set for outlining precision, specificity, sensitivity, f score, '
                   'standard accuracy, and balanced accuracy.')
        _best = ('The (a) architecture name of the best model, architecture.json, and (b) the '
                 'timestamp of the model, latest.json.')

        # Metadata
        self.__metadata = {
            'abstracts': {'desc': 'Frequency metrics of the model development data.'},
            'best': {'desc': _best},
            'text': {'desc': 'The frequencies of strings, text pieces, etc.'},
            'model': {'desc': 'The details of the best model, for inference.'},
            'bullet': {'desc': 'A metrics data set for false negative rate and false positive rate bullet graphs.'},
            'scores': {'desc': _scores},
            'fnr': {'desc': 'The data for illustrating possible false negative rate costs at varying rate points.'},
            'fpr': {'desc': 'The data for illustrating possible false positive rate costs at varying rate points.'}}

    @staticmethod
    def __local(path: str, extension: str) -> pd.DataFrame:
        """

        :param path: The path wherein the files of interest lie
        :param extension: The extension type of the files of interest
        :return:
        """

        splitter = os.path.basename(path) + os.path.sep

        # The list of files within the path directory, including its child directories.
        files: list[str] = glob.glob(pathname=os.path.join(path, '**', f'*.{extension}'),
                                     recursive=True)

        details: list[dict] = [
            {'file': file,
             'vertex': file.rsplit(splitter, maxsplit=1)[1],
             'section': os.path.basename(os.path.dirname(file))}
            for file in files]

        return pd.DataFrame.from_records(details)

    def exc(self, path: str, extension: str, prefix: str) -> pd.DataFrame:
        """

        :param path: The path wherein the files of interest lie
        :param extension: The extension type of the files of interest
        :param prefix: The Amazon S3 (Simple Storage Service) where the files of path are heading
        :return:
        """

        logging.info(path)

        local: pd.DataFrame = self.__local(path=path, extension=extension)

        # Building the Amazon S3 strings
        frame = local.assign(key=prefix + local["vertex"])

        # The metadata dict strings
        frame['metadata'] = frame['section'].map(self.__metadata)

        return frame[['file', 'key', 'metadata']]
