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
import unittest


class MessageTest(unittest.TestCase):
    """ test messaging.generator """

    def setUp(self):
        """ setup the test environment """

    def tearDown(self):
        """ restore the test environment """

    def test_rndint(self):
        """ test generator.rndint() """
        print("checking integers randomization")
        for index in range(1000):
            integer = int(generator.rndint(index))
            self.assertTrue(integer >= 0 and integer <= index * 2,
                            "size not expected")
        print("...integers randomization ok")

    def test_rndbin(self):
        """ test generator.rndbin() """
        print("checking binary string creation")
        for index in range(1000):
            binary = generator.rndbin(index)
            self.assertTrue(len(binary) == index, "size not expected")
        print("...binary string creation ok")

    def test_rndb64(self):
        """ test generator.rndb64() """
        print("checking base64 string creation")
        for index in range(1000):
            b64 = generator.rndb64(index)
            self.assertTrue(len(b64) == index, "size not expected")
        print("...base64 string creation ok")

    def test_rndstr(self):
        """ test generator.rndstr() """
        print("checking string creation")
        for index in range(1000):
            string = generator.rndstr(index)
            self.assertTrue(len(string) == index, "size not expected")
        print("...string creation ok")

    def test_generator(self):
        """ test message generation """
        print("checking message generation")
        bctypes = ['index', 'text', 'binary', 'base64']
        for bctype in bctypes:
            for bsize in [0, 1024, 10240, 102400]:
                for header_count in [1, 10]:
                    gen = Generator(body_content=bctype,
                                    body_size=bsize,
                                    header_count=header_count)
                    for i in range(5):
                        msg = gen.message()
                        if bctype != 'index':
                            self.assertEqual(len(msg.body), bsize,
                                             "body size not expected")
                        else:
                            if bsize == 0:
                                cor = 0
                            else:
                                cor = len("%d" % i)
                            self.assertEqual(len(msg.body), cor,
                                             "body size not expected")
        print("...message generation ok")


if __name__ == "__main__":
    unittest.main()
