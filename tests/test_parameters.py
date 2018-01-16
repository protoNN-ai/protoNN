"""Tests for parameters"""
import unittest
import logging
from protonn.parameters.core import view

logger = logging.getLogger(__name__)


class Tests(unittest.TestCase):

    def test_observe(self):
        logger.info("test_view")

        @view
        def my_scope():
            x = 5
            return x
        my_scope()
