"""Module interface.py"""
import typing

import boto3

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.cache
import src.functions.service
import src.preface.setup
import src.s3.configurations
import src.s3.s3_parameters


class Interface:
    """
    Interface
    """

    def __init__(self):

        self.__configurations = config.Config()

    def __arguments(self, connector: boto3.session.Session) -> dict:
        """

        :param connector:
        :return:
        """

        return src.s3.configurations.Configurations(connector=connector).objects(
            key_name=self.__configurations.arguments_key)

    def exc(self) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict]:
        """

        :return:
        """

        connector = boto3.session.Session()
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()

        arguments = self.__arguments(connector=connector)

        # Setting up the cloud storage area
        src.preface.setup.Setup(service=service, s3_parameters=s3_parameters).exc()

        return connector, s3_parameters, service, arguments
