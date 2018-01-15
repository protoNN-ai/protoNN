"""Tests for utls"""
import unittest
import logging
# import protonn
from protonn.utils import save_data_json, get_time_str, save_code

logger = logging.getLogger(__name__)


class Tests(unittest.TestCase):

    def test_timestamp(self):
        stamp = get_time_str()
        logger.info("test_timestamp: " + stamp)

    def test_save_code(self):
        save_code("/tmp/protonn/saved_code")

    def test_main(self):
        logger.info("test save json")
        data = {"i": 34}
        save_data_json(data, "/tmp/protonn/data.json")
