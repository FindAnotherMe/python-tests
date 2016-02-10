#!/usr/bin/python
# coding=utf-8
"""Tests to demonstrate correct and incorrect unicode handling."""

from __future__ import print_function

import os
import six
import sys
import unittest
import locale
from subprocess import Popen, call, PIPE


class TestUnicode(unittest.TestCase):
    """Tests to demonstrate correct and incorrect unicode handling."""

    test_message = u"汉语/漢語"
    encoding = "utf-8"
    dev_null = open(os.devnull, "w")

    def test_exception_incorrect(self):
        """Incorrect encoding of a unicode exception message."""

        message = self.test_message

        if six.PY2:
            # failure to encode in Python 2
            self.assertTrue(isinstance(message, unicode))

        if six.PY3:
            # extraneous encoding in Python 3
            self.assertTrue(isinstance(message, str))
            message = message.encode(self.encoding)
            self.assertTrue(isinstance(message, bytes))

        try:
            raise AssertionError(message)

        except AssertionError as ex:
            if six.PY2:
                # we can get our exception message as unicode
                self.assertEqual(unicode(ex), message)
                # but not as str
                self.assertRaises(UnicodeEncodeError, str, ex)
                # and we can't print it either
                self.assertRaises(UnicodeEncodeError, print, ex)
                return

            if six.PY3:
                # we'll get a str representation of bytes
                self.assertTrue(str(ex).startswith("b'"))
                # we can't get it as bytes though
                self.assertRaises(TypeError, bytes, ex)
                return

        self.fail()

    def test_exception_correct(self):
        """Correct encoding of a unicode exception message."""

        message = self.test_message

        if six.PY2:
            # encode for Python 2
            self.assertTrue(isinstance(message, unicode))
            message = message.encode(self.encoding)
            self.assertTrue(isinstance(message, str))

        if six.PY3:
            # do not encode for Python 3
            self.assertTrue(isinstance(message, str))

        try:
            raise AssertionError(message)

        except AssertionError as ex:
            # we can get our exception message as str
            self.assertEqual(str(ex), message)
            return

        self.fail()

    def test_execute_argument_incorrect(self):
        """Incorrect passing of a unicode string argument to a command."""

        message = self.test_message

        if sys.version_info[0] > 2 or sys.version_info[1] >= 7:
            if locale.getdefaultlocale()[1] == 'utf-8':
                # no issues with Python 2.7 and later when encoding is utf-8
                call(["echo", message], stdout=self.dev_null)
            else:
                # but if the encoding is different an exception is raised
                kwds = {"stdout": self.dev_null}
                self.assertRaises(TypeError, call, ["echo", message], kwds)
        else:
            # unicode must be encoded in Python 2.6 and earlier
            kwds = {"stdout": self.dev_null}
            self.assertRaises(TypeError, call, ["echo", message], kwds)

    def test_execute_argument_correct(self):
        """Correct passing of a unicode string argument to a command."""

        message = self.test_message

        # always encode arguments to commands
        message = message.encode(self.encoding)

        call(["echo", message], stdout=self.dev_null)

    def test_execute_stdin_incorrect(self):
        """Incorrect encoding of unicode input to a command."""

        message = self.test_message

        process = Popen(["cat", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)

        if six.PY2:
            # failure to encode stdin for a command
            self.assertRaises(UnicodeEncodeError, process.communicate, message)
            return

        if six.PY3:
            # failure to encode stdin for a command
            self.assertRaises(TypeError, process.communicate, message)
            return

        self.fail()

    def test_execute_stdin_correct(self):
        """Correct encoding of unicode input to a command."""

        message = self.test_message

        # always encode stdin for a command
        message = message.encode(self.encoding)

        process = Popen(["cat", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)

        process.communicate(message)

    def test_execute_stdout_incorrect(self):
        """Incorrect decoding of unicode output from a command."""

        message = self.test_message

        # always encode stdin for a command
        message = message.encode(self.encoding)

        process = Popen(["cat", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)

        (stdout, stderr) = process.communicate(message)

        if six.PY2:
            # our input was properly encoded unicode
            self.assertTrue(isinstance(self.test_message, unicode))
            # but our output is str instead of unicode
            self.assertTrue(isinstance(stdout, str))
            self.assertTrue(isinstance(stderr, str))
            return

        if six.PY3:
            # our input was properly encoded str
            self.assertTrue(isinstance(self.test_message, str))
            # but our output is bytes insted of str
            self.assertTrue(isinstance(stdout, bytes))
            self.assertTrue(isinstance(stderr, bytes))
            return

        self.fail()

    def test_execute_stdout_correct(self):
        """Correct decoding of unicode output from a command."""

        message = self.test_message

        # always encode stdin for a command
        message = message.encode(self.encoding)

        process = Popen(["cat", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)

        (stdout, stderr) = process.communicate(message)

        # always decode stdout/stderr from a command
        self.assertEqual(stdout.decode(self.encoding), message.decode(self.encoding))
        self.assertEqual(stderr.decode(self.encoding), "")

if __name__ == "__main__":
    unittest.main()
