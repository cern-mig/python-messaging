"""
DQ - abstraction of a Queue message queue

========
SYNOPSIS
========

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

===========
DESCRIPTION
===========

This module provides an abstraction of a message queue. It derives
from the dirq.Queue module that provides a generic directory-based queue.

It uses the following Queue schema to store a message:

  schema = {
      "header" = "table",
      "binary" = "binary?",
      "text"   = "string?",
  }

The message header is therefore stored as a table and the message body
is stored either as a text or binary string.

Copyright (C) 2011 CERN
"""
__version__ = "$Revision: 1 $"
# $Source$

from messaging.message import Message, deserialize
from dirq.queue import Queue

class DQ(Queue):
    """
    Abstraction of a Queue message queue.
    """
    
    def __init__(self, **data):
        """
        Return a new DQ object.
        """
        data["schema"] = { "header" : "table",
                          "body" : "binary?",
                          "text" : "string?", }
        super(DQ, self).__init__(**data)
    
    def add_message(self, msg):
        """
        Add the given message (a Message object) to the queue and
        return the corresponding element name.
        Raise:
        - TypeError if the parameter is not a Message.
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
        return a Message object.
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
        return a Message object.
        Raise:
        TypeError if the parameter is not a string.
        """
        if not isinstance(element, str):
            raise TypeError("string expected: %s" % element)
        data = self.dequeue(element)
        if "text" in data:
            body = data["text"]
        else:
            body = data.get("body", None)
        return Message(header = data["header"], body = body)
