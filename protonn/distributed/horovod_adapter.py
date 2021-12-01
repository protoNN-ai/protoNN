from typing import Optional

import horovod.torch as hvd
import torch

ALLREDUCE_OPS = [hvd.Sum]


def init() -> None:
    hvd.init()


def rank() -> int:
    return hvd.rank()


def world_size() -> int:
    return hvd.size()


def allreduce(tensor: torch.Tensor, op: Optional[int]) -> torch.Tensor:
    hvd_op = ALLREDUCE_OPS[op] if op is not None else None
    return hvd.allreduce(tensor, op=hvd_op)


def broadcast(tensor: torch.Tensor, src_rank: int) -> torch.Tensor:
    return hvd.broadcast(tensor, src_rank)
