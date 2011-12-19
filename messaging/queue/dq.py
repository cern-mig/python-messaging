"""
Directory Queue
===============

:py:class:`DQ` - abstraction of a :py:class:`dirq.queue.Queue`
message queue.

Synopsis
--------

Example::

  from messaging.message import Message
  from messaging.queue.dq import DQ

  # create a message queue
  mq = DQ(path = "/some/where")

  # add a message to the queue
  msg = Message(body="hello world")
  print("msg added as %s" % mq.add_message(msg))

  # browse the queue
  for name in mq:
      if mq.lock(name):
          msg = mq.get_message(name)
      # one could use mq.unlock(name) to only browse the queue...
      mq.remove(name)

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

Copyright (C) 2011 CERN
"""

from messaging.message import Message, deserialize
from dirq.queue import Queue

class DQ(Queue):
    """
    Abstraction of a Queue message queue.
    """
    
    def __init__(self, **data):
        """
        Return a new :py:class:`DQ` object.
        """
        data["schema"] = { "header" : "table",
                          "body" : "binary?",
                          "text" : "string?", }
        super(DQ, self).__init__(**data)
    
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
        data = {"header" : msg.header}
        if msg.text:
            data['text'] = msg.body
        else:
            data['body'] = msg.body
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
            body = data.get("body", None)
        return Message(header = data["header"], body = body)
    
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
            body = data.get("body", None)
        return Message(header = data["header"], body = body)
