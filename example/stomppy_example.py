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
from messaging.stomppy import MessageListener
import stomp
import time


class MyListener(MessageListener):
    """
    Example listener class
    """
    def __init__(self):
        self.uuid = None
        self.done = False

    def error(self, message):
        print("received an error %s" % message)

    def message(self, message):
        if message.header.get("x-uuid") == self.uuid:
            self.done = True
        print("received message %s" % message)


def stomppy_test():
    """
    Example that shows how to handle messages
    """
    print("stomppy example")
    conn = stomp.Connection([("localhost", 61613)])
    listener = MyListener()
    conn.set_listener("", listener)
    conn.start()
    conn.connect()

    msg = Message(body="stomppy_test".decode(),
                  header={'destination': '/topic/test.stomppy',
                          'x-uuid': "%s" % time.time()})
    listener.uuid = msg.header['x-uuid']
    conn.subscribe(destination='/topic/test.stomppy', ack='auto')
    conn.send(msg.body, **msg.header)
    print("sending message %s" % msg)

    start = time.time()
    while not listener.done and (time.time() - start < 2):
        time.sleep(0.1)
    conn.disconnect()
    print("...stomppy example ok")


if __name__ == "__main__":
    stomppy_test()
