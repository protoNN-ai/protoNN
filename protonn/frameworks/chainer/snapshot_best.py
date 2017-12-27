import os
import shutil
import tempfile
import math

from chainer.serializers import npz
from chainer.training import extension
from chainer.training.extensions._snapshot import _snapshot_object

MIN_LOSS = math.inf

def snapshot_best(savefun=npz.save_npz,
             filename='snapshot_best'):
    """Returns a trainer extension to take snapshots of the trainer if current loss is at its minimum.
    
    This extension serializes the trainer object and saves it to the output
    directory. It is used to support resuming the training loop from the saved
    state.

    This extension is called once per epoch by default. To take a
    snapshot at a different interval, a trigger object specifying the
    required interval can be passed along with this extension
    to the `extend()` method of the trainer.

    The default priority is -100, which is lower than that of most
    built-in extensions.

    .. note::
       This extension first writes the serialized object to a temporary file
       and then rename it to the target file name. Thus, if the program stops
       right before the renaming, the temporary file might be left in the
       output directory.

    Args:
        savefun: Function to save the trainer. It takes two arguments: the
            output file path and the trainer object.
        filename (str): Name of the file into which the trainer is serialized.
            It can be a format string, where the trainer object is passed to
            the :meth:`str.format` method.

    """
    @extension.make_extension(trigger=(1, 'epoch'), priority=-100)
    def snapshot(trainer):
        _snapshot_best(trainer, trainer, filename.format(trainer), savefun)

    return snapshot


def _snapshot_best(trainer, target, filename, savefun):
    global MIN_LOSS
    val_loss = trainer.observation['validation/main/loss']
    if val_loss < MIN_LOSS:
        MIN_LOSS = val_loss
        _snapshot_object(trainer, target, filename, savefun)

