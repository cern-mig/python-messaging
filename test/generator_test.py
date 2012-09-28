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
import re
import unittest


class MessageTest(unittest.TestCase):

    def setUp(self):
        """ setup the test environment """

    def tearDown(self):
        """ restore the test environment """

    def test_rndint(self):
        print("checking integers randomization")
        for index in range(1000):
            integer = int(generator.rndint(index))
            self.assert_(integer >= 0 and integer <= index * 2,
                         "size not expected")
        print("...integers randomization ok")

    def test_rndbin(self):
        print("checking binary string creation")
        for index in range(1000):
            bin = generator.rndbin(index)
            self.assert_(len(bin) == index, "size not expected")
        print("...binary string creation ok")

    def test_rndb64(self):
        print("checking base64 string creation")
        for index in range(1000):
            b64 = generator.rndb64(index)
            self.assert_(len(b64) == index, "size not expected")
        print("...base64 string creation ok")

    def test_rndstr(self):
        print("checking string creation")
        for index in range(1000):
            string = generator.rndstr(index)
            self.assert_(len(string) == index, "size not expected")
        print("...string creation ok")

    def test_generator(self):
        print("checking message generation")
        types = ['index', 'text', 'binary', 'base64']
        for type in types:
            for size in [0, 1024, 10240, 102400]:
                for header_count in [1, 10]:
                    gen = Generator(body_content=type,
                                    body_size=size,
                                    header_count=header_count)
                    for iter in range(5):
                        msg = gen.message()
                        if type != 'index':
                            self.assertEqual(len(msg.body), size,
                                             "body size not expected")
                        else:
                            if size == 0:
                                cor = 0
                            else:
                                cor = len("%d" % iter)
                            self.assertEqual(len(msg.body), cor,
                                             "body size not expected")
        print("...message generation ok")

if __name__ == "__main__":
    unittest.main()
