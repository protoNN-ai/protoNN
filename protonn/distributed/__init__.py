import torch


class DistAdapter:
    _adapter = None

    def init(self, backend) -> None:
        if backend == "hvd":
            from . import horovod_adapter

            self._adapter = horovod_adapter
        self._adapter.init()

    def rank(self) -> int:
        return self._adapter.rank()

    def world_size(self) -> int:
        return self._adapter.world_size()

    def allreduce(self, tensor: torch.Tensor) -> torch.Tensor:
        return self._adapter.allreduce(tensor)


dist_adapter = DistAdapter()
