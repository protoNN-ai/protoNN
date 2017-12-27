"""Tests for misc"""
import unittest
import logging
import protonn
from protonn.utils import save_data_json

logger = logging.getLogger(__name__)


class Tests(unittest.TestCase):

    def test_main(self):
        logger.info("test save json")
        data = {"i": 34}
        save_data_json(data, "/tmp/protonn/data.json")
