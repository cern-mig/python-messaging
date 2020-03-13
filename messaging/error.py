"""
Errors used in the module.

Copyright (C) CERN 2013-2020
"""


class MessageError(Exception):
    """
    Raised when errors occurs during Message handling.
    """
    pass


class GeneratorError(Exception):
    """
    Raised when errors occurs during Generator handling.
    """
    pass
