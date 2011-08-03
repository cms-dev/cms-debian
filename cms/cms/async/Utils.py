#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programming contest management system
# Copyright © 2010-2011 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
# Copyright © 2010-2011 Stefano Maggiolo <s.maggiolo@gmail.com>
# Copyright © 2010-2011 Matteo Boscariol <boscarim@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Random utility and logging facilities.

"""

import os
import sys

import simplejson
from collections import namedtuple
from random import choice


Address = namedtuple("Address", "ip port")


class ServiceCoord(namedtuple("ServiceCoord", "name shard")):
    """A compact representation for the name and the shard number of a
    service (thus identifying it).

    """
    def __repr__(self):
        return "%s,%d" % (self.name, self.shard)


def random_string(length):
    """Returns a random string of ASCII letters of specified length.

    """
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    string = ""
    for i in range(length):
        string += choice(letters)
    return string


def mkdir(path):
    """Make a directory without complaining for errors.

    path (string): the path of the directory to create
    returns (bool): True if the dir is ok, False if it is not

    """
    try:
        os.mkdir(path)
        return True
    except OSError:
        if os.path.isdir(path):
            return True
    return False


def encode_length(length):
    """Encode an integer as a 4 bytes string

    length (int): the integer to encode
    return (string): a 4 bytes representation of length

    """
    try:
        s = ""
        tmp = length / (1 << 24)
        s += chr(tmp)
        length -= tmp * (1 << 24)
        tmp = length / (1 << 16)
        s += chr(tmp)
        length -= tmp * (1 << 16)
        tmp = length / (1 << 8)
        s += chr(tmp)
        length -= tmp * (1 << 8)
        s += chr(length)
        return s
    except Exception as e:
        print >> sys.stderr, "Can't encode length: %d %s" % (length, repr(e))
        raise ValueError


def decode_length(string):
    """Decode an integer from a 4 bytes string

    string (string): a 4 bytes representation of an integer
    return (int): the corresponding integer

    """
    try:
        return ord(string[0]) * (2 << 24) + \
               ord(string[1]) * (2 << 16) + \
               ord(string[2]) * (2 << 8) + \
               ord(string[3])
    except:
        print >> sys.stderr, "Can't decode length"
        raise ValueError


def encode_json(obj):
    """Encode a dictionary as a JSON string; on failure, returns None.

    obj (object): the object to encode
    return (string): an encoded string

    """
    try:
        return simplejson.dumps(obj)
    except:
        print >> sys.stderr, "Can't encode JSON: %s" % repr(obj)
        raise ValueError


def decode_json(string):
    """Decode a JSON string to a dictionary; on failure, raises an
    exception.

    string (string): the Unicode string to decode
    return (object): the decoded object

    """
    try:
        string = string.decode("utf8")
        return simplejson.loads(string)
    except simplejson.JSONDecodeError:
        print >> sys.stderr, "Can't decode JSON: %s" % string
        raise ValueError


def encode_binary(string):
    """Encode a string for binary transmission - escape character is
    '\\' and we escape '\r' as '\\r', so we can use again '\r\n' as
    terminator string.

    string (string): the binary string to encode
    returns (string): the escaped string

    """
    try:
        return string.replace('\\', '\\\\').replace('\r', '\\r')
    except:
        print >> sys.stderr, "Can't encode binary."
        raise ValueError


def decode_binary(string):
    """Decode an escaped string to a usual string.

    string (string): the escaped string to decode
    return (object): the decoded string
    """
    try:
        return string.replace('\\r', '\r').replace('\\\\', '\\')
    except:
        print >> sys.stderr, "Can't decode binary."
        raise ValueError

def get_compilation_command(language, source_filename, executable_filename):
    """For compiling in 32-bit mode under 64-bit OS: add
    '-march=i686', '-m32' for gcc/g++. Don't know about
    Pascal. Anyway, this will require some better support from the
    evaluation environment (particularly the sandbox, which has to be
    compiled in a different way depending on whether it will execute
    32- or 64-bit programs).
     
    """
    if language == "c":
        command = ["/usr/bin/gcc", "-DEVAL", "-static", "-O2","-lm",
                   "-o", executable_filename, source_filename]
    elif language == "cpp":
        command = ["/usr/bin/g++", "-DEVAL", "-static", "-O2",
                   "-o", executable_filename, source_filename]
    elif language == "pas":
        command = ["/usr/bin/fpc", "-dEVAL", "-XS", "-O2",
                   "-o%s" % (executable_filename), source_filename]
    return command


def filter_ansi_escape(s):
    """Remove ansi codes from a string.

    s (string): the input string

    return (string): s without ansi codes.

    """
    ansi_mode = False
    res = ''
    for c in s:
        if c == u'\x1b':
            ansi_mode = True
        if not ansi_mode:
            res += c
        if c == u'm':
            ansi_mode = False
    return res
