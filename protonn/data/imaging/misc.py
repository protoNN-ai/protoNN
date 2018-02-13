import numpy as np


def make_channels_first(img):
    axes = img.shape
    img = np.rollaxis(img, axes.index(min(axes)), 0)
    return img


def make_channels_last(img):
    axes = img.shape
    img = np.rollaxis(img, 0, len(axes))
    return img


def set_size(img, shape):
    res = img
    # pad1 = dim_max - img.shape[0]
    # pad1 = max(0, pad1)
    # pad2 = dim_max - img.shape[1]
    # pad2 = max(0, pad2)
    # res = np.lib.pad(img, ((0, pad1), (0, pad2), (0, 0)), 'constant', constant_values=value)
    return res
