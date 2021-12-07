from typing import Optional

import torch


class DistAdapter:
    _adapter = None

    SUM = 0

    def init(self, backend) -> None:
        if backend == "horovod":
            from . import horovod_adapter

            self._adapter = horovod_adapter

        elif backend in ["dp", "ddp", "ddp2", "ddp_spawn"]:
            from . import torch_distributed_adapter

            self._adapter = torch_distributed_adapter

        else:
            raise ValueError("Unknown backend")

        self.backend = backend
        self._adapter.init()

    def rank(self) -> int:
        return self._adapter.rank()

    def world_size(self) -> int:
        return self._adapter.world_size()

    def allreduce(self, tensor: torch.Tensor, op: Optional[int] = None) -> torch.Tensor:
        return self._adapter.allreduce(tensor, op)

    def get_backend_as_pl_strategy(self):
        return self.backend

    def broadcast(self, tensor: torch.Tensor, src_rank: int) -> torch.Tensor:
        return self._adapter.broadcast(tensor, src_rank)


dist_adapter = DistAdapter()
