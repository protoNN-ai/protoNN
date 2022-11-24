import signal
from queue import Queue
from threading import Thread

import _thread


class ThreadedIterator:
    def __init__(self, batches_per_epoch):
        self.batches_per_epoch = batches_per_epoch
        self.cnt_batches_produced = 0
        self._queue = Queue(maxsize=5)
        self._thread = Thread(target=self.thread, args=(), daemon=True)
        self._thread.start()

    def __iter__(self):
        return self

    def __next__(self):
        if self.cnt_batches_produced >= self.batches_per_epoch:
            self.cnt_batches_produced = 0
            raise StopIteration()
        batch = self._queue.get(block=True, timeout=300)
        if batch is None:
            # self._thread.join()
            raise StopIteration()
        self.cnt_batches_produced += 1
        return batch

    def thread(self):
        try:
            for batch in self.yield_next_batch():
                self._queue.put(batch)
            self._queue.put(None)
        except Exception as e:
            print(e)
            _thread.interrupt_main()
