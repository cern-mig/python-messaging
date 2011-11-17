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

from messaging.generator import Generator
import messaging.generator as generator
from messaging.message import Message, deserialize, destringify, dejsonify
import time
try:
    range = xrange
except NameError:
    pass

CREATION_TIMES = 1000000

def benchmark_creation():
    t1 = time.time()
    for i in range(CREATION_TIMES):
        Message()
    t2 = time.time()
    delta = t2 - t1
    print("Message() x %d : %.2fs @ %.2f/s" %
          (CREATION_TIMES, delta, CREATION_TIMES / delta))
    
def measure(func, times, args=dict()):
    t1 = time.time()
    for i in range(times):
        func(**args)
    t2 = time.time()
    return t2 - t1
    
def benchmark_operation():
    variants = {"binary" : [{"body_size" : 25600, "times" : 10000},
                            {"body_size" : 256000, "times" : 100},
                            {"body_size" : 2560000, "times" : 100}],
                "text" : [{"body_size" : 9500, "times" : 10000},
                          {"body_size" : 95000, "times" : 1000},
                          {"body_size" : 950000, "times" : 100}]}
    operation_options = [{}, {"compression":"zlib"}]
    header = dict()
    for i in range(10):
        header["dummy-key-%d" % i]= "dummy-value-%d" % i
    for option in operation_options:
        print("OPTIONS : %s" % option)
        for key, value in variants.items():
            for option in value:
                g = Generator(body_size=option["body_size"], 
                              body_content=key, header_count=0)
                msg = g.message()
                assert(len(msg.body) == option["body_size"])
                msg.header = header
                
                times = option["times"]
                args = {"option" : option}
                delta = measure(msg.jsonify, times, args)
                print("msg[%s%d].jsonify() x %d : %.2fs @ %.2f/s" %
                      (key, option["body_size"], times, delta, times / delta))
                
                times = option["times"]
                args = {"obj" : msg.jsonify(option)}
                delta = measure(dejsonify, times, args)
                print("dejsonify(msg[%s%d]) x %d : %.2fs @ %.2f/s" %
                      (key, option["body_size"], times, delta, times / delta))
                
                times = option["times"]
                args = {"option" : option}
                delta = measure(msg.stringify, times)
                print("msg[%s%d].stringify() x %d : %.2fs @ %.2f/s" %
                      (key, option["body_size"], times, delta, times / delta))
                
                times = option["times"]
                args = {"string" : msg.stringify(option)}
                delta = measure(destringify, times, args)
                print("destringify(msg[%s%d]) x %d : %.2fs @ %.2f/s" %
                      (key, option["body_size"], times, delta, times / delta))
                
                times = option["times"]
                args = {"option" : option}
                delta = measure(msg.serialize, times)
                print("msg[%s%d].serialize() x %d : %.2fs @ %.2f/s" %
                      (key, option["body_size"], times, delta, times / delta))
                
                times = option["times"]
                args = {"binary" : msg.serialize(option)}
                delta = measure(deserialize, times, args)
                print("deserialize(msg[%s%d]) x %d : %.2fs @ %.2f/s" %
                      (key, option["body_size"], times, delta, times / delta))


def main():
    benchmark_creation()
    benchmark_operation()

if __name__ == "__main__":
    main()
