import math
from chainer.training import util


class MinValueTrigger(object):

    def __init__(self, key, tail_len=7, trigger=(1, 'epoch')):
        self._key = key
        self._cur_tail_len = tail_len
        self._start_tail_len = tail_len
        self._best_value = math.inf
        self._interval_trigger = util.get_trigger(trigger)
        self._compare = lambda min_value, new_value: new_value < min_value

    def __call__(self, trainer):
        observation = trainer.observation
        key = self._key

        if not self._interval_trigger(trainer):
            return False

        if key not in observation:
            raise ValueError("Key must be in observation.")

        value = observation[key]

        if self._compare(self._best_value, value):
            self._best_value = value
            self._cur_tail_len = self._start_tail_len
        else:
            self._cur_tail_len -= 1

        if self._cur_tail_len == 0:
            return True
        return False
