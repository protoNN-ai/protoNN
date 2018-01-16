"""Tests for parameters"""
import unittest
import logging
from protonn.parameters.core import view, observe

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
        #name = observe(y)
        #assert name == "y"
