"""
:py:class:`Queue` - abstraction of a message queue

Synopsis
========

Example::

  import messaging.queue as queue

  mq = queue.new({"type":"Foo", ... options ...});
  # is identical too
  mq = queue.foo.Foo(... options ...);

Description
===========

This module provides an abstraction of a message queue. Its only
purpose is to offer a unified method to create a new queue. The
functionality is implemented in child modules such as
:py:mod:`messaging.queue.dqs.DQS`.

Copyright (C) CERN 2013-2021
"""

import sys


def new(option):
    """
    Create a new message queue object; options must contain the type of
    queue (which is the name of the child class), see above.
    """
    options = option.copy()
    qtype = options.pop("type", "DQS")
    try:
        __import__("messaging.queue.%s" % (qtype.lower()))
    except SyntaxError:
        raise SyntaxError("error importing dirq type: %s" % qtype)
    except ImportError:
        raise ImportError(
            "you must install %s dependencies before using this module" %
            (qtype, ))
    try:
        module = sys.modules["messaging.queue.%s" % (qtype.lower())]
        return getattr(module, qtype)(**options)
    except KeyError:
        pass
    raise ValueError("queue type not valid: %s" % qtype)
