"""Module tce.py"""
import logging

import pandas as pd


class TCE:
    """
    Text Cloud Elements
    """

    def __init__(self):
        pass

    @staticmethod
    def __elements(instance: pd.Series, code: int) -> str:
        """

        :param instance: The parts are 'sentence' & 'code_per_tag'
        :param code:
        :return:
        """

        logging.info('Latest: %s, %s',
                     instance['tokens'].shape, instance['fine_ner_tags'].shape)

        # A temporary frame that associates each text piece with its tag code
        frame = pd.DataFrame(
            data={'element': instance['tokens'],
                  'code': instance['fine_ner_tags']})

        # The elements associated with the tags in focus
        frame: pd.DataFrame = frame.copy().loc[frame['code'] == code, :]

        # Hence, the text cloud elements
        elements = ','.join(frame['element'].to_list())

        return elements

    def exc(self, data: pd.DataFrame, code: int) -> pd.DataFrame:
        """

        :param data:
        :param code:
        :return:
        """

        frame = data.copy()

        frame['elements'] = frame[['tokens', 'fine_ner_tags']].apply(self.__elements, code=code, axis=1)

        return frame
