"""Tests for parameters"""

import unittest
import logging

import protonn
from protonn.parameters.core import view, observe, dump

logger = logging.getLogger(__name__)


class Tests(unittest.TestCase):

    def test_observe(self):
        logger.info("test view")

        @view
        def my_scope():
            x = 5
            return x
        my_scope()

        logger.info("test observe")
        y = 23
        # name = observe(y)
        # assert name == "y"
        dump("/tmp/protonn")

    def test_observe2(self):

        @view
        def my_scope():
            class Spam:
                my_very_important_param = None
            Spam.my_very_important_param = 5  # type: Observed
            Spam.my_very_important_param = 10
            return Spam.my_very_important_param

        self.assertIn('Spam.my_very_important_param', protonn.parameters._parameters)
        self.assertEqual(protonn.parameters._parameters['Spam.my_very_important_param'], None)
        my_scope()
        self.assertEqual(protonn.parameters._parameters['Spam.my_very_important_param'], 10)
