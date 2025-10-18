"""Module setup.py"""

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.directories
import src.s3.bucket
import src.s3.keys
import src.s3.prefix


class Setup:
    """
    Description
    -----------

    Sets up local & cloud environments
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__bucket_name = self.__s3_parameters.external
        self.__configurations = config.Config()

        # Directories instance
        self.__directories = src.functions.directories.Directories()

    def __s3(self) -> bool:
        """
        Prepares the relevant path within an Amazon S3 (Simple Storage Service) bucket.

        :return:
        """

        # An instance for interacting with Amazon S3 buckets.
        bucket = src.s3.bucket.Bucket(service=self.__service, location_constraint=self.__s3_parameters.location_constraint,
                                      bucket_name=self.__bucket_name)

        # If the bucket exist, the prefix path is cleared.  Otherwise, the bucket is created.
        if bucket.exists():
            return True

        return bucket.create()

    def __data(self) -> bool:
        """
        Prepares a temporary directory for ...

        :return:
        """

        # Probably
        self.__directories.cleanup(path=self.__configurations.artefacts_)

        return self.__directories.create(path=self.__configurations.artefacts_)

    def __local(self) -> bool:
        """
        Prepares the local, but temporary, storage repository of results

        :return:
        """

        # Clean-up, then re-create
        self.__directories.cleanup(path=self.__configurations.warehouse)
        self.__directories.create(path=self.__configurations.warehouse)

        successful = []
        for value in self.__configurations.graphs_:
            successful.append(self.__directories.create(value))

        return all(successful)

    def exc(self) -> bool:
        """

        :return:
        """

        return self.__s3() & self.__local() & self.__data()
