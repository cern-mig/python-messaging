# -*- coding: utf-8 -*-
"""
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

 Copyright (C) CERN 2013-2021
"""

from messaging.message import Message, deserialize, destringify, dejsonify


def handle_message():
    """
    Example that shows how to handle messages
    """
    print("handle message")

    msg1 = Message(body="hello world!".encode("utf-8"), header={"h1": "val1"})

    msg2 = Message(body="hello world!".encode("utf-8"), header={"h1": "val1"})
    assert(msg1 == msg2)
    msg2 = msg1.serialize()
    msg2 = deserialize(msg2)
    assert(msg1 == msg2)

    msg3 = deserialize('{"body": "hello world!", "header": {"h1": "val1"}}')
    assert(msg1 == msg3)

    tmp = msg1.stringify()
    msg4 = destringify(tmp)
    assert(msg1 == msg4)

    msg5 = msg1.jsonify()
    assert(isinstance(msg5, dict))
    msg5 = dejsonify(msg5)
    assert(msg1 == msg5)

    print("...handle message OK!")


def main():
    """ main """
    handle_message()


if __name__ == "__main__":
    main()
