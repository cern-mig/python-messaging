"""
Directory Queue Redis
======================

:py:class:`DQR` - abstraction of a :py:class:`dirq.QueueRedis.QueueRedis`
message queue.

Synopsis
--------

Example::

  from messaging.message import Message
  from messaging.queue.dqr import DQR

  # create a message queue
  mq = DQR(host="localhost", port=6379)

  # add a message to the queue
  msg = Message(body = "hello world")
  print("msg added as %s" % mq.add_message(msg))

  # browse the queue
  for name in mq:
      if mq.lock(name):
          msg = mq.get_message(name)
          # unlock the element
          mq.unlock(name)
          # othwerwise, if you want to remove the element
          # mq.remove(name)

Description
-----------

This module provides an abstraction of a message queue. It derives
from the :py:class:`dirq.QueueRedis.QueueRedis` module that provides
a generic directory-based queue.

It simply stores the serialized message (with optional compression) as
a :py:class:`dirq.QueueRedis.QueueRedis` element.

Copyright (C) 2012 CERN
"""

from messaging.message import Message, deserialize
from dirq.QueueRedis import QueueRedis


class DQR(QueueRedis):
    """
    Abstraction of a :py:class:`dirq.QueueRedis.QueueRedis` message queue.
    """

    def __init__(self, **data):
        """
        Return a new :py:class:`DQR` object.
        """
        self.__compression = data.pop('compression', None)
        super(DQR, self).__init__(**data)

    def add_message(self, message):
        """
        Add the given message (a :py:class:`messaging.message.Message` object)
        to the queue and return the corresponding element name.

        Raise:
            TypeError if the parameter is not a
            :py:class:`messaging.message.Message`.
        """
        if not isinstance(message, Message):
            raise TypeError("message type not expected: %s" % message)
        compression = self.__compression
        if compression:
            return self.add(message.serialize({'compression': compression}))
        else:
            return self.add(message.serialize())

    def get_message(self, element):
        """
        Dequeue the message from the given element and
        return a :py:class:`messaging.message.Message` object.
        """
        message = self.get(element)
        return deserialize(message)
