# SPDX-License-Identifier: MIT


# Custom exceptions.
class InvalidServerTypeError(Exception):
    def __str__(self) -> str:
        return 'Unknown server type specified.'


class UnstableInternetError(Exception):
    def __str__(self) -> str:
        return 'You must have a stable internet connection before proceeding to use the library.'


class DataNotFoundError(Exception):
    def __init__(self, data_type: str) -> None:
        self.data_type = data_type

    def __str__(self) -> str:
        return f'{self.data_type} data not found.'
