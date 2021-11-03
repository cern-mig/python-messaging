"""
Directory Queue Null
====================

:py:class:`NULL` - abstraction of a :py:class:`dirq.QueueNull.QueueNull`
message queue.

Synopsis
--------

Example::

  from messaging.message import Message
  from messaging.queue.null import NULL

  # create a message queue
  mq = NULL()

  # add a message to the queue
  msg = Message(body = "hello world")
  mq.add_message(msg)


Description
-----------

This module provides an abstraction of a message queue. It derives
from the :py:class:`dirq.QueueNull.QueueNull` module that provides
a generic "black hole" queue: added messages will disappear
immediately so the queue will therefore always appear empty.

Copyright (C) CERN 2013-2021
"""

from messaging.message import Message
from dirq.QueueNull import QueueNull


class NULL(QueueNull):
    """
    Abstraction of a :py:class:`dirq.QueueNull.QueueNull` message queue.
    """

    def __init__(self, **data):
        """ Return a new :py:class:`NULL` object. """
        super(NULL, self).__init__(**data)

    def add_message(self, msg):
        """
        Add the given message (a :py:class:`messaging.message.Message` object)
        to the queue.

        Raise:
            TypeError if the parameter is not a
            :py:class:`messaging.message.Message`.
        """
        if not isinstance(msg, Message):
            raise TypeError("message type not expected: %s" % msg)
        return self.add(msg)

    def get_message(self, element):
        """ Not supported method. """
        raise NotImplementedError("unsupported method: get_message()")
