"""Module tce.py"""
import pandas as pd


class TCE:
    """
    Text Cloud Elements
    """

    def __init__(self):
        pass

    @staticmethod
    def __elements(instance: pd.Series, codes: list[int]) -> str:
        """

        :param instance: The parts are 'sentence' & 'code_per_tag'
        :param codes:
        :return:
        """

        # A temporary frame that associates each text piece with its tag code
        frame = pd.DataFrame(
            data={'element': instance['sentence'].split(maxsplit=-1),
                  'code': instance['code_per_tag'].split(',', maxsplit=-1)})

        # Casting the tag code; str -> int
        frame['code'] = frame['code'].astype(dtype=int)

        # The elements associated with the tags in focus
        frame: pd.DataFrame = frame.copy().loc[frame['code'].isin(codes), :]

        # Hence, the text cloud elements
        elements = ','.join(frame['element'].to_list())

        return elements

    def exc(self, data: pd.DataFrame, codes: list[int]) -> pd.DataFrame:
        """

        :param data:
        :param codes:
        :return:
        """

        frame = data.copy()

        frame['elements'] = frame[['sentence', 'code_per_tag']].apply(self.__elements, codes=codes, axis=1)

        return frame
