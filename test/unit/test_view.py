"""
A set of unit tests for the view module in the src.client package.
"""

__docformat__ = 'reStructuredText'



import unittest
import pytest

from io import StringIO
from unittest.mock import patch

pytest.importorskip("PyQt5")
from src.client.view import (
    getStyle, getSocket
)


class ViewTest(unittest.TestCase):
    """
    Unittests for the standalone functions in the view module.
    """

    def testGetStyle(self):
        """
        A limited amount of testing since this method is influenced by the
        operating system; checks whether a style is found.
        """
        self.assertNotEqual(getStyle(), [])

    @patch("os.path.exists")
    @patch("builtins.open")
    def testGetSocket(self, mockOpen, mockPathExists):
        """
        Tests whether a server socket is readable from a mock
        configuration file.
        """
        properSettings = "[Network]\n" \
                         "serversocket=127.0.0.1:8000"
        blankSettings = "[Network]\n" \
                        "serversocket= "

        mockPathExists.return_value = True

        mockOpen.return_value = StringIO(properSettings)
        self.assertEqual(getSocket(), "127.0.0.1:8000")

        mockOpen.return_value = StringIO(blankSettings)
        self.assertEqual(getSocket(), "")



