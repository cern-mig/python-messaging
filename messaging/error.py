"""
Errors used in the module.

Copyright (C) 2012 CERN
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
