import numpy as np


def make_channels_first(img):
    axes = img.shape
    img = np.rollaxis(img, axes.index(min(axes)), 0)
    return img


def make_channels_last(img):
    axes = img.shape
    img = np.rollaxis(img, 0, len(axes))
    return img


def set_size(img, shape, value=1):
    slices_crop = tuple(slice(0, i) for i in shape)
    res = img[slices_crop]
    pads = tuple((0, max(shape[i] - img.shape[i], 0)) for i in range(len(shape)))
    res = np.lib.pad(res, pads, 'constant', constant_values=value)
    return res
