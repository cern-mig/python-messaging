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

from messaging.generator import Generator
import messaging.generator as generator


def generate_messages():
    """
    Example that shows how to generate random messages with the modules
    provided.
    Generator takes different parameters:
        body_content: content type of the body between
                      ['index', 'text', 'binary', 'base64']
        body_size: the size of the body
        header_count: the number of header fields to be generated
        header_name_size: the size of the header key to be generated
        header_value_size: the size of the header value to be generated
        header_name_prefix: the prefix to be added to generated header fields
    """
    print("generating random message")
    gen = Generator(body_content="text",
                    body_size=1024,
                    header_count=6,
                    header_name_size=-16,
                    header_value_size=-32,
                    header_name_prefix="rnd-")
    msg = gen.message()
    assert(len(msg.body) == 1024)
    assert(len(msg.header) == 6)
    print("...message generation OK!")


def generate_int():
    """
    Example which shows how to generate integers in a distribution between
    0 and 2 * given value.
    For more information:
        see Irwin-Hall in http://en.wikipedia.org/wiki/Normal_distribution
    """
    print("generating integers")
    index = 100
    for counter in range(1000):  # pylint: disable=W0612
        integer = generator.rndint(100)
        assert(integer >= 0 and integer <= index * 2)
    print("...integers generation OK!")


def generate_bin():
    """
    Example which shows how to generate binary strings of given length.
    """
    print("generating binary string")
    length = 1024
    binstr = generator.rndbin(length)
    assert(len(binstr) == length)
    print("...binary string generation OK!")


def generate_b64():
    """
    Example which shows how to generate base64 strings of given length.
    """
    print("generating base64 string")
    length = 1024
    b64str = generator.rndb64(length)
    assert(len(b64str) == length)
    print("...base64 string generation OK!")


def generate_str():
    """
    Example which shows how to generate strings of given length.
    """
    print("generating string")
    length = 1024
    string = generator.rndstr(length)
    assert(len(string) == length)
    print("...string generation OK!")


def main():
    """ main """
    generate_int()
    generate_bin()
    generate_b64()
    generate_str()
    generate_messages()


if __name__ == "__main__":
    main()
