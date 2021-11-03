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

from messaging.message import Message
import messaging.generator as generator
import messaging.queue as queue
import os
import shutil

PATH = "%s/%s" % (os.getcwd(), generator.rndstr(10))


def dirq_normal():
    """
    Example that shows how to use a normal dirq
    """
    print("dirq normal")
    # creating a couple of messages
    msg1 = Message(body="hello world".encode("utf-8"), header={"h1": "val1"})
    msg2 = Message(body="hello world 2".encode("utf-8"), header={"h2": "val2"})

    # creating a normal queue
    option = {"type": "DQN",
              "path": "%s/%s" % (PATH, "normal"), }
    dirq = queue.new(option)

    # adding the two messages
    element1 = dirq.add_message(msg1)
    element2 = dirq.add_message(msg2)

    # getting back the messages and checking they are as expected
    post_msg2 = None
    if dirq.lock(element2):
        post_msg2 = dirq.get_message(element2)
    assert(post_msg2 == msg2)
    post_msg1 = None
    if dirq.lock(element1):
        post_msg1 = dirq.get_message(element1)
    assert(post_msg1 == msg1)
    print("...dirq normal OK!")


def dirq_simple():
    """
    Example that shows how to use a simple dirq
    """
    print("dirq simple")
    # creating a couple of messages
    msg1 = Message(body="hello world".encode("utf-8"), header={"h1": "val1"})
    msg2 = Message(body="hello world 2".encode("utf-8"), header={"h2": "val2"})

    # creating a simple queue
    option = {"type": "DQS",
              "path": "%s/%s" % (PATH, "simple"), }
    dirq = queue.new(option)

    # adding the two messages
    element1 = dirq.add_message(msg1)
    element2 = dirq.add_message(msg2)

    # getting back the messages and checking they are as expected
    post_msg2 = None
    if dirq.lock(element2):
        post_msg2 = dirq.get_message(element2)
    assert(post_msg2 == msg2)
    post_msg1 = None
    if dirq.lock(element1):
        post_msg1 = dirq.get_message(element1)
    assert(post_msg1 == msg1)
    print("...dirq simple OK!")


def main():
    """ main """
    shutil.rmtree(PATH, ignore_errors=True)
    dirq_normal()
    dirq_simple()
    shutil.rmtree(PATH, ignore_errors=True)


if __name__ == "__main__":
    main()
