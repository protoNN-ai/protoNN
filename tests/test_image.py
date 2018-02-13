"""Tests for imaging"""
import unittest
import logging
import protonn
import numpy as np

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Tests(unittest.TestCase):

    def test_channels(self):
        logger.info("test image channels")
        img = np.random.random((80, 100, 3)).astype(np.float32)
        shape1 = img.shape
        logger.info("original shape: {}".format(img.shape))
        img = protonn.data.imaging.misc.make_channels_first(img)
        logger.info("new shape: {}".format(img.shape))
        img = protonn.data.imaging.misc.make_channels_last(img)
        logger.info("resored shape: {}".format(img.shape))
        shape2 = img.shape
        assert shape1 == shape2

    def test_crop_pad(self):
        a = np.ones((6, 6, 6))
        shape = (3, 4, 8)
        result = protonn.data.imaging.misc.set_size(a, shape)
        self.assertEqual(shape, result.shape)
