#!/usr/bin/python
"""Verify the Python version being tested."""

from __future__ import print_function

import six
import sys
import unittest


class TestVersion(unittest.TestCase):
    """Verify the version being tested."""

    def test_version(self):
        """Verify the version being tested."""

        print()
        print(sys.version_info)

        if six.PY2:
            print("Python 2")

        if six.PY3:
            print("Python 3")

if __name__ == "__main__":
    unittest.main()
