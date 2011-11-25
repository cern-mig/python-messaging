"""
DQS - abstraction of a QueueSimple message queue

========
SYNOPSIS
========

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
      # one could use mq.unlock(name) to only browse the queue...
      mq.remove(name)

===========
DESCRIPTION
===========

This module provides an abstraction of a message queue. It derives
from the QueueSimple module that provides a generic
directory-based queue.

It simply stores the serialized message (with optional compression) as
a QueueSimple element.
"""
__version__ = "$Revision: 1 $"
# $Source$

from messaging.message import Message, deserialize
from dirq.QueueSimple import QueueSimple

class DQS(QueueSimple):
    """
    Abstraction of a QueueSimple message queue.
    """
    
    def __init__(self, **data):
        """
        Return a new DQS object.
        """
        self.__compression = data.pop('compression', None)
        super(DQS, self).__init__(**data)
    
    def add_message(self, msg):
        """
        Add the given message (a Message object) to the queue and
        return the corresponding element name.
        """
        if not isinstance(msg, Message):
            raise TypeError("message type not expected: %s" % msg)
        compression = self.__compression
        if compression:
            return self.add(msg.serialize({'compression' : compression}))
        else:
            return self.add(msg.serialize())
    
    def get_message(self, element):
        """
        Dequeue the message from the given element and
        return a Message object.
        """
        msg = self.get(element)
        return deserialize(msg)
