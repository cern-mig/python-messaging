"""
Directory Queue Normal
======================

:py:class:`DQN` - abstraction of a :py:class:`dirq.queue.Queue`
message queue.

Synopsis
--------

Example::

  from messaging.message import Message
  from messaging.queue.dqn import DQN

  # create a message queue
  mq = DQN(path = "/some/where")

  # add a message to the queue
  msg = Message(body="hello world")
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
from the :py:class:`dirq.queue.Queue` module that provides a generic
directory-based queue.

It uses the following :py:class:`dirq.queue.Queue` schema to store a
message::

  schema = {
      "header" = "table",
      "binary" = "binary?",
      "text"   = "string?",
  }

The message header is therefore stored as a table and the message body
is stored either as a text or binary string.

Copyright (C) CERN 2013-2021
"""

from messaging.message import Message
from dirq.queue import Queue


class DQN(Queue):
    """
    Abstraction of a Normal Queue message queue.
    """

    def __init__(self, **data):
        """
        Return a new :py:class:`DQN` object.
        """
        data["schema"] = {"header": "table",
                          "binary": "binary?",
                          "text": "string?", }
        super(DQN, self).__init__(**data)

    def add_message(self, msg):
        """
        Add the given message (a :py:class:`messaging.message.Message` object)
        to the queue and return the corresponding element name.

        Raise:
            :py:class:`TypeError` if the parameter is not a
            :py:class:`messaging.message.Message`.
        """
        if not isinstance(msg, Message):
            raise TypeError("Message expected: %s" % msg)
        data = {"header": msg.header}
        if msg.text:
            data['text'] = msg.body
        else:
            data['binary'] = msg.body
        return self.add(data)

    def get_message(self, element):
        """
        Get the message from the given element (which must be locked) and
        return a :py:class:`messaging.message.Message` object.
        """
        data = self.get(element)
        if "text" in data:
            body = data["text"]
        else:
            body = data.get("binary", None)
        return Message(header=data["header"], body=body)

    def dequeue_message(self, element):
        """
        Dequeue the message from the given element and
        return a :py:class:`messaging.message.Message` object.

        Raise:
            :py:class:`TypeError` if the parameter is not a :py:mod:`string`.
        """
        if not isinstance(element, str):
            raise TypeError("string expected: %s" % element)
        data = self.dequeue(element)
        if "text" in data:
            body = data["text"]
        else:
            body = data.get("binary", None)
        return Message(header=data["header"], body=body)
