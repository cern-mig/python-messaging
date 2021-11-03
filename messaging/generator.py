"""
Synopsis
========

Example::

  import messaging.generator as generator;

  # create the generator
  mg = generator.Generator(
      body_content = "binary",
      body_size = 1024,
  )

  # use it to generate 10 messages
  for i in range(10):
      msg = mg.message()
      ... do something with it ...


Description
===========

This module provides a versatile message generator that can be useful
for stress testing or benchmarking messaging brokers or libraries.

Copyright (C) CERN 2013-2021
"""

import base64
import binascii
from messaging.error import GeneratorError
from messaging.message import Message
import os
import random


def rndint(size):
    """
    Returns a random integer between 0 and 2*size with a normal distribution.

    See Irwin-Hall in http://en.wikipedia.org/wiki/Normal_distribution
    """
    rnd = random.random() + random.random() + random.random() \
        + random.random() + random.random() + random.random() \
        + random.random() + random.random() + random.random() \
        + random.random() + random.random() + random.random()
    return int(rnd * size / 6 + 0.5)


def maybe_randomize(size):
    """ Maybe randomize int. """
    if size is not None and size < 0:
        return rndint(-size)
    else:
        return size


def rndbin(size):
    """
    Returns a random binary string of the given size.
    """
    binay = binascii.hexlify(os.urandom(int(size / 2) + 1))
    return binay[0:size]


def rndb64(size):
    """
    Returns a random text string of the given size (Base64 characters).
    """
    rnd = base64.b64encode(rndbin(int(size * 0.75 + 1))).decode()
    return rnd[0:size]


def rndstr(size):
    """
    Returns a random text string of the given size (all printable characters).
    """
    rnd = ''
    while size > 0:
        binary = rndbin(int(size * 1.4 + 1)).decode()
        rnd += ''.join([char for char in binary
                        if ord(char) > 31 and ord(char) < 127])
        size -= len(binary)
    if size:
        rnd = rnd[0:size]
    return rnd


class Generator(object):
    """ A message generator tool. """

    def __init__(self, **kwargs):
        """ Returns a message generator. """
        self.__option = dict()
        if isinstance(kwargs, dict):
            self.__option['body_content'] = kwargs.get(
                'body_content', 'index')
            try:
                self.__option['body_size'] = kwargs['body_size']
            except KeyError:
                pass
            try:
                self.__option['header_count'] = kwargs['header_count']
            except KeyError:
                pass
            self.__option['header_value_size'] = kwargs.get(
                'header_value_size', -32)
            self.__option['header_name_size'] = kwargs.get(
                'header_name_size', -16)
            self.__option['header_name_prefix'] = kwargs.get(
                'header_name_prefix', 'rnd-')
        self.__index = 0

    def set(self, option, value):
        """ Set Generator option to value provided. """
        self.__option[option] = value

    def message(self):
        """
        Returns a newly generated Message object

        Options

        When creating a message generator, the following options can be given:

        body-content

            * string: specifying the body content type; depending on this
              value, the body will be made of:
            * base64: only Base64 characters
            * binary: anything
            * index: the message index number, starting at 1, optionally
              adjusted to match the C<body-size> (this is the default)
            * text: only printable 7-bit ASCII characters

        body-size
            integer specifying the body size

        header-count
            integer specifying the number of header fields

        header-value-size
            integer specifying the size of each header field value
            (default is -32)

        header-name-size
            integer specifying the size of each header field name
            (default is -16)

        header-name-prefix
            string to prepend to all header field names
            (default is C<rnd->)


        Note: all integer options can be either positive (meaning exactly this
        value) or negative (meaning randomly distributed around the value).

        For instance::

          mg = Generator(
              header_count = 10,
              header_value_size = -20,
          )

        It will generate messages with exactly 10 random header fields, each
        field value having a random size between 0 and 40 and normally
        distributed around 20.
        """
        size = self.__option.get('body_size')
        size = maybe_randomize(size)
        what = self.__option.get('body_content')
        if size is not None:
            if size == 0:
                body = ''.encode()
            elif what == 'base64':
                body = rndb64(size)
            elif what == 'text':
                body = rndstr(size)
            elif what == 'binary':
                body = rndbin(size)
            elif what == 'index':
                body = "%d" % self.__index
            else:
                raise GeneratorError("invalid body content: %s" % what)
        else:
            body = "%d" % self.__index
        count = self.__option.get('header_count', 0)
        count = maybe_randomize(count)
        header = dict()
        if count is None:
            return Message(body, header)
        for _ in range(count):
            size = self.__option.get('header_name_size')
            size = maybe_randomize(size)
            what = rndb64(size)
            what = what.replace('+', '-').replace('/', '_')
            size = self.__option.get('header_value_size')
            size = maybe_randomize(size)
            header[self.__option.get('header_name_prefix') + what] = \
                rndstr(size)
        self.__index += 1
        return Message(body, header)
