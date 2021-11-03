================
python-messaging
================

.. image:: https://github.com/cern-mig/python-messaging/actions/workflows/test.yml/badge.svg


Overview
========

Messaging is a set of Python modules useful to deal with
"messages", as used in messaging, see for instance:

    http://en.wikipedia.org/wiki/Enterprise_messaging_system

The modules include a transport independent message abstraction, a
versatile message generator and several message queues/spools to
locally store messages.

An Perl implementation of the same abstractions and queue algorithms
is available in CPAN:

    http://search.cpan.org/dist/Messaging-Message/

Install
=======

To install this module, run the following commands::

    python setup.py install

To test the module, run the following command::

    python setup.py test


Support and documentation
=========================

After installing, you can find documentation for this module with the
standard python help function command or at:

    https://messaging.readthedocs.org/

License and Copyright
=====================

Copyright (C) CERN 2013-2021

Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at 

    http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
either express or implied. 
See the License for the specific language governing permissions and 
limitations under the License.
