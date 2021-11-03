"""
Directory Queue Simple
======================

:py:class:`DQS` - abstraction of a :py:class:`dirq.QueueSimple.QueueSimple`
message queue.

Synopsis
--------

Example::

  from messaging.message import Message
  from messaging.queue.dqs import DQS

  # create a message queue
  mq = DQS(path = "/some/where")

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
from the :py:class:`dirq.QueueSimple.QueueSimple` module that provides
a generic directory-based queue.

It simply stores the serialized message (with optional compression) as
a :py:class:`dirq.QueueSimple.QueueSimple` element.

Copyright (C) CERN 2013-2021
"""

from messaging.message import Message, deserialize
from dirq.QueueSimple import QueueSimple


class DQS(QueueSimple):
    """
    Abstraction of a :py:class:`dirq.QueueSimple.QueueSimple` message queue.
    """

    def __init__(self, **data):
        """
        Return a new :py:class:`DQS` object.
        """
        self.__compression = data.pop('compression', None)
        super(DQS, self).__init__(**data)

    def add_message(self, msg):
        """
        Add the given message (a :py:class:`messaging.message.Message` object)
        to the queue and return the corresponding element name.

        Raise:
            TypeError if the parameter is not a
            :py:class:`messaging.message.Message`.
        """
        if not isinstance(msg, Message):
            raise TypeError("message type not expected: %s" % msg)
        compression = self.__compression
        if compression:
            return self.add(msg.serialize({'compression': compression}))
        else:
            return self.add(msg.serialize())

    def get_message(self, element):
        """
        Dequeue the message from the given element and
        return a :py:class:`messaging.message.Message` object.
        """
        msg = self.get(element)
        return deserialize(msg)
