import numpy as np


def make_channels_first(img):
    axes = img.shape
    img = np.rollaxis(img, axes.index(min(axes)), 0)
    return img


def make_channels_last(img):
    axes = img.shape
    img = np.rollaxis(img, 0, len(axes))
    return img
