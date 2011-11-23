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
"""

from messaging.message import Message, deserialize, destringify, dejsonify
import time
try:
    range = xrange
except NameError:
    pass

TIME = 1

def fixed_header():
    """ Return a fixed "reasonable" header. """
    return {
       "destination"        : "/topic/application.component.destination",
       "message-id"         : "ID:broker.acme.com-49839-1277292910818-2:4231860:-1:1:1",
       "content-length"     : "1234",
       "timestamp"          : "2011-12-13T12:34:56.000Z",
       "expires"            : "1277292910818",
       "priority"           : "3",
       "JMSXUserID"         : "joe.publisher",
       "sender.site"        : "ACME.COM",
       "x-message-type"     : "monitoring.data",
       "x-message-encoding" : "text/json",
    }
    
def body_ascii(length):
    """ Return a "reasonable" ASCII body """
    body = ""
    xor = 21;
    
    while len(body) < length:
        body += "".join(filter(lambda x : ord(x) > 31 and ord(x) < 127,
                               map(lambda x : chr(x ^ xor), range(255))))
        xor = (xor + 13) % 255
    return body[0:length]

def body_text(length):
    """ Return a "reasonable" text body """
    text = list("бвайкиосцз")
    body = list(body_ascii(length))
    for i in range(int(length / 100)):
        body[i * 100 - 1] = text[i % 10]
    return str(body)

#def test(name, times, func, args=dict()):
#    t1 = time.time()
#    for i in range(times):
#        func(**args)
#    t2 = time.time()
#    delta = t2 - t1
#    print("%s x %d : %.2fs @ %.2f/s" %
#          (name, times, delta, times / delta))
    
def test(name, times, func, args=dict()):
    t1 = time.time()
    counter = 0
    oldargs = args.copy()
    while time.time() - t1 < TIME:
        assert args == oldargs
        func(**args)
        counter += 1
    t2 = time.time()
    delta = t2 - t1
    print("%s : %.2fs @ %.2f/s (n=%d)" %
          (name, delta, counter / delta, counter))

def main():
    """ Benchmark it! """
    header = fixed_header()
    TIMES = 100000
    test("new()", TIMES, Message, {})
    for size in [100, 10000, 1000000]:
        body = body_ascii(size)
        msg = Message(header=header, body=body)
        test("new(B%d)" % size, TIMES, Message, {"header" : header, "body" : body})
        json = msg.jsonify()
        test("jsonify(B%d)" % size, TIMES, msg.jsonify, {})
        test("dejsonify(B%d)" % size, TIMES, dejsonify, {'obj' : json})
        string = msg.serialize()
        test("serialize(B%d)" % size, TIMES, msg.serialize, {})
        test("deserialize(B%d)" % size, TIMES, deserialize, {'binary' : string})
        if size == 100:
            continue
        json = msg.jsonify({'compression' : 'zlib'})
        test("jsonify(B%d+zlib)" % size, TIMES, msg.jsonify, { 'option' : {'compression' : 'zlib'}})
        test("dejsonify(B%d+zlib)" % size, TIMES, dejsonify, {'obj' : json})
        string = msg.serialize({'compression' : 'zlib'})
        test("serialize(B%d+zlib)" % size, TIMES, msg.serialize, { 'option' : {'compression' : 'zlib'}})
        test("deserialize(B%d+zlib)" % size, TIMES, deserialize, {'binary' : string})
    size = 10000
    body = body_text(size)
    msg = Message(header=header, body=body)
    test("new(T%d)" % size, TIMES, Message, {"header" : header, "body" : body})
    json = msg.jsonify()
    test("jsonify(T%d)" % size, TIMES, msg.jsonify, {})
    test("dejsonify(T%d)" % size, TIMES, dejsonify, {'obj' : json})
    string = msg.serialize()
    test("serialize(T%d)" % size, TIMES, msg.serialize, {})
    test("deserialize(T%d)" % size, TIMES, deserialize, {'binary' : string})

if __name__ == "__main__":
    validate = body_ascii(10)
    assert len(validate) == 10
    main()
