"""

:py:class:`Message` - abstraction of a *message*

Synopsis
--------

Example::

  import messaging.message as message

  # constructor + setters
  msg = message.Message()
  msg.body = "hello world"
  msg.header = {"subject" : "test"}
  msg.header["message-id"] = "123"

  # fancy constructor
  msg = message.Message(
      body = "hello world",
      header = {
          "subject" : "test",
          "message-id" : "123",
      },
  )

  # getters
  if (msg.body) {
      ...
  }
  id = msg.header["message-id"]

  # serialize it
  msg.serialize()
  # serialize it and compress the body with zlib
  msg.serialize({"compression" : "zlib"})
  # serialize it and compress the body with lz4
  msg.serialize({"compression" : "lz4"})
  # serialize it and compress the body with snappy
  msg.serialize({"compression" : "snappy"})


Description
===========

This module provides an abstraction of a *message*, as used in
messaging, see for instance:
http://en.wikipedia.org/wiki/Enterprise_messaging_system.

A message consists of header fields (collectively called "the header
of the message") and a body.

Each header field is a key/value pair where the key and the value are
text strings. The key is unique within the header so we can use a dict
to represent the header of the message.

The body is either a text string or a binary string. This distinction
is needed because text may need to be encoded (for instance using
UTF-8) before being stored on disk or sent across the network.

To make things clear:

- a *text string* (aka *character string*) is a sequence of Unicode characters

- a *binary string* (aka *byte string*) is a sequence of bytes

Both the header and the body can be empty.


Json Mapping
============

In order to ease message manipulation (e.g. exchanging between
applications, maybe written in different programming languages), we
define here a standard mapping between a Message object and a JSON object.

A message as defined above naturally maps to a JSON object with the
following fields:

header
    the message header as a JSON object (with all values being JSON
    strings).

body
    the message body as a JSON string.

text
    a JSON boolean specifying whether the body is text string (as opposed
    to binary string) or not.

encoding
    a JSON string describing how the body has been encoded (see below).

All fields are optional and default to empty/false if not present.

Since JSON strings are text strings (they can contain any Unicode
character), the message header directly maps to a JSON object. There
is no need to use encoding here.

For the message body, this is more complex. A text body can be put
as-is in the JSON object but a binary body must be encoded beforehand
because JSON does not handle binary strings. Additionally, we want to
allow body compression in order to optionally save space. This is
where the encoding field comes into play.

The encoding field describes which transformations have been applied
to the message body. It is a *+* separated list of transformations
that can be:

base64
    :py:mod:`base64` encoding (for binary body or compressed body).

lz4
    :py:mod:`lz4` compression.

snappy
    :py:mod:`snappy` (http://code.google.com/p/snappy/).

utf8
    :py:mod:`utf8` encoding (only needed for a compressed text body).

zlib
    :py:mod:`zlib` compression.

Here is for instance the JSON object representing an empty message
(i.e. the result of :py:meth:`Message`)::

  {}

Here is a more complex example, with a binary body::

  {
    "header":{"subject":"demo","destination":"/topic/test"},
    "body":"YWJj7g==",
    "encoding":"base64"
  }

You can use the :py:meth:`Message.jsonify` method to convert a
:py:class:`Message` object into a dict representing the equivalent
JSON object.

Conversely, you can create a new :py:class:`Message` object from a
compatible JSON object (again, a :py:class:`dict`) with the
:py:meth:`dejsonify` method.

Using this JSON mapping of messages is very convenient because you can
easily put messages in larger JSON data structures. You can for
instance store several messages together using a JSON array of these
messages.

Here is for instance how you could construct a message containing in
its body another message along with error information::

  try:
      import simplejson as json
  except ImportError:
      import json
  import time
  # get a message from somewhere...
  msg1 = ...
  # jsonify it and put it into a simple structure
  body = {
      "message" : msg1.jsonify(),
      "error"   : "an error message",
      "time"    : time.time(),
  }
  # create a new message with this body
  msg2 = message.Message(body = json.dumps(body))
  msg2.header["content-type"] = "message/error"

A receiver of such a message can easily decode it::

  try:
      import simplejson as json
  except ImportError:
      import json
  # get a message from somewhere...
  msg2 = ...
  # extract the body which is a JSON object
  body = json.loads(msg2.body)
  # extract the inner message
  msg1 = message.dejsonify(body['message'])


Stringification and Serialization
=================================

In addition to the JSON mapping described above, we also define how to
*stringify* and *serialize* a message.

A *stringified message* is the string representing its equivalent
JSON object. A stringified message is a text string and can for
instance be used in another message. See the :py:meth:`Message.stringify`
and :py:func:`destringify` methods.

A *serialized message* is the UTF-8 encoding of its stringified
representation. A serialized message is a binary string and can for
instance be stored in a file. See the :py:meth:`Message.serialize`
and :py:func:`deserialize` methods.

For instance, here are the steps needed in order to store a message
into a file:

#. transform the programming language specific abstraction of the message
   into a JSON object
#. transform the JSON object into its (text) string representing
#. transform the JSON text string into a binary string using UTF-8
   encoding


*1* is called :py:meth:`Message.jsonify`, *1 + 2* is called
:py:meth:`Message.stringify` and *1 + 2 + 3* is called
:py:meth:`Message.serialize`.

To sum up::

            Message object
                 |  ^
       jsonify() |  | dejsonify()
                 v  |
          JSON compatible dict
                 |  ^
     JSON encode |  | JSON decode
                 v  |
             text string
                 |  ^
    UTF-8 encode |  | UTF-8 decode
                 v  |
            binary string

Copyright (C) CERN 2013-2021
"""

import base64
import copy
try:
    import hashlib
    md5_hash = hashlib.md5
except ImportError:
    import md5
    md5_hash = md5.md5
import re
try:
    import json
except ImportError:
    import simplejson as json
import sys
from messaging.error import MessageError

COMPRESSORS_SUPPORTED = {
    "lz4": "lz4.block",
    "snappy": "snappy",
    "zlib": "zlib",
}
AVAILABLE_DECODING = list(COMPRESSORS_SUPPORTED.keys())
AVAILABLE_DECODING.extend(["base64", "utf8"])
_COMPRESSORS = dict()
for name, module in COMPRESSORS_SUPPORTED.items():
    try:
        spec = module.split('.')
        if len(spec) == 1:
            _COMPRESSORS[name] = __import__(module)
        else:
            _COMPRESSORS[name] = __import__(module, fromlist=[spec[1]])
    except ImportError:
        pass
    except SystemError:
        pass
COMPRESSORS = _COMPRESSORS.keys()
_COMPRESSORS_RE = re.compile("^(%s)" % "|".join(_COMPRESSORS.keys()))

_EX_ASCII_RE = re.compile("[\x80-\xff]")
_EX_BASE64_RE = re.compile("[\x00-\x1f\x7f-\xff]")

_py2 = sys.hexversion < 0x03000000
_py3 = not _py2

DEFAULT_BODY = ''.encode()


def is_ascii(string):
    """ Returns True is the string is ascii. """
    try:
        if _py3 and is_bytes(string):
            string = string.decode()
        string.encode("ascii")
        return True
    except UnicodeDecodeError:
        return False
    except UnicodeEncodeError:
        return False


def is_bytes(string):
    """ Check if given string is a byte string. """
    if _py2:
        return not isinstance(string, unicode)
    else:  # python 3
        return isinstance(string, bytes)


def dejsonify(obj):
    """ Returns a message from json structure. """
    is_text = False
    try:
        if obj.get('text'):
            is_text = True
    except AttributeError:
        raise MessageError("dict expected: %s" % obj)
    header = obj.get('header', dict())
    body = obj.get('body', DEFAULT_BODY)
    encoding = list()
    o_encoding = obj.get('encoding')
    if o_encoding:
        encoding = o_encoding.split('+')
        if not is_bytes(body):
            body = body.encode()
    for token in encoding:
        if token not in AVAILABLE_DECODING:
            raise MessageError("decoding not supported: %s" % token)
        elif (token in COMPRESSORS_SUPPORTED and token not in COMPRESSORS):
            raise MessageError("decoding supported but not installed: %s" %
                               token)
    if 'base64' in encoding:
        body = base64.b64decode(body)
    for method in _COMPRESSORS:
        if method in encoding:
            if 'decompress' in dir(_COMPRESSORS[method]):
                body = _COMPRESSORS[method].decompress(body)
            else:
                body = _COMPRESSORS[method].uncompress(body)
    if 'utf8' in encoding:
        body = body.decode('utf-8')
    if is_bytes(body):
        if is_text:
            body = body.decode()
    elif not is_text:
        body = body.encode()
    return Message(body, header)


def destringify(string):
    """ Destringify the given message. """
    try:
        jsonified = json.loads(string)
    except ValueError:
        error = sys.exc_info()[1]
        raise MessageError("not a valid json string provided: %s" % error)
    return dejsonify(jsonified)


def deserialize(binary):
    """ Deserialize a message. """
    decoded = binary
    try:
        if is_bytes(decoded):
            decoded = decoded.decode("utf-8")
    except UnicodeDecodeError:
        error = sys.exc_info()[1]
        raise MessageError("not a valid binary string %s: %s"
                           % (binary, error))
    return destringify(decoded)


def _base64_it(obj):
    """ Try to base64 if required. """
    if _py2 and not _EX_BASE64_RE.search(obj['body']):
        return
    try:
        if _py3 and not _EX_BASE64_RE.search(str(obj['body'], "utf-8")):
            return
    except UnicodeDecodeError:
        pass
    obj['body'] = base64.b64encode(obj['body'])
    obj['encoding']['base64'] = True


def _utf8_it(obj):
    """ UTF-8 if necesary. """
    if _py3 or _EX_ASCII_RE.match(obj['body']):
        obj["body"] = obj["body"].encode("utf-8")
        obj["encoding"]["utf8"] = True


def _compress_it(compression, obj):
    """ Try to compress the body and check if worth it. """
    body_len = len(obj["body"])
    if body_len < 255:
        return
    tmp = _COMPRESSORS[compression].compress(obj["body"])
    if (float(len(tmp)) / body_len) < 0.9:
        obj["body"] = tmp
        obj["encoding"][compression] = True


class Message(object):
    """ A Message abstraction class. """

    def __init__(self, body=DEFAULT_BODY, header=None):
        """ Initialize the object """
        self.body = body
        self.header = header
        # self.text = not is_bytes(body) #done setting the body

    def get_body(self):
        """ Returns the body of the message. """
        return self.__body

    def set_body(self, value):
        """ Set the message body to new value. """
        if value is None:
            self.__body = DEFAULT_BODY
        else:
            self.__body = value
        self.text = not is_bytes(self.__body)
    body = property(get_body, set_body)

    def get_header(self):
        """ Return the header of the message. """
        return self.__header

    def set_header(self, value):
        """ Set the message header to new value. """
        if value is None:
            value = dict()
        self.__header = value
    header = property(get_header, set_header)

    def get_text(self):
        """ Is it a text message? """
        if self.body is None:
            return False
        return self.__text

    def is_text(self):
        """ Is it a text message? """
        return self.get_text()

    def set_text(self, value):
        """ Set if the message is text. """
        self.__text = value
    text = property(get_text, set_text)

    def jsonify(self, option=dict()):
        """ Transforms the message to JSON. """
        compression = option.get('compression')
        if compression is not None and not _COMPRESSORS_RE.match(compression):
            raise MessageError("unsupported compression type: %s"
                               % compression)
        obj = dict()
        if self.header:
            obj["header"] = self.header
        if not self.body:
            return obj
        obj["body"] = self.body
        if self.text:
            obj["text"] = True
            if compression:
                obj["encoding"] = dict()
                _utf8_it(obj)
                tmp_encoding = len(obj.get("encoding", dict()))
                _compress_it(compression, obj)
                if tmp_encoding != len(obj.get("encoding", dict())):
                    _base64_it(obj)
                else:
                    obj["body"] = self.body
                    del(obj["encoding"])
        else:  # binary body
            obj["encoding"] = dict()
            if compression:
                _compress_it(compression, obj)
            _base64_it(obj)
        if "encoding" in obj:
            if obj["encoding"]:
                obj["encoding"] = "+".join(obj["encoding"].keys())
            else:
                del(obj["encoding"])
        return obj

    def stringify(self, option=dict()):
        """ Transforms the message to string. """
        jsonified = self.jsonify(option)
        body = jsonified.get("body", "")
        if is_bytes(body):
            jsonified["body"] = body.decode("utf-8")
        return json.dumps(jsonified)

    def serialize(self, option=dict()):
        """ Serialize message. """
        stringified = self.stringify(option)
        return stringified.encode("utf-8")

    def __repr__(self):
        """ Return a string representation of the object """
        return self.stringify()

    def size(self):
        """ Returns an approximation of the message size. """
        size = len(self.body) + 1
        size += sum([len(str(key)) + len(str(value)) + 2
                     for (key, value) in self.header.items()])
        return size

    def clone(self):
        """ Returns a clone of the message. """
        return copy.deepcopy(self)

    def md5(self):
        """ Return the checksum of the message. """
        header_c = ''.join(["%s:%s\n" % (key, self.header[key])
                            for key in sorted(self.header.keys())])
        header_c = md5_hash(header_c.encode("utf-8")).hexdigest()
        if self.is_text():
            body_c = md5_hash(self.body.encode("utf-8")).hexdigest()
        else:
            body_c = md5_hash(self.body).hexdigest()
        composed = "%d%s%s" % (self.is_text(), header_c, body_c)
        return md5_hash(composed.encode("utf-8")).hexdigest()

    def __eq__(self, other):
        """ Check if the message is equal to the given one. """
        if not isinstance(other, Message):
            return False
        if self.text != other.text or self.body != other.body:
            return False
        if self.header is not None:
            if other.header is None:
                return False
            for (key, value) in self.header.items():
                if value != other.header.get(key):
                    return False
        else:
            return self.header == other.header
        return True

    def equals(self, other):
        """ Check if the message is equal to the given one. """
        return self.__eq__(other)
