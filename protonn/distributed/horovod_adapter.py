import horovod.torch as hvd
import torch


def init() -> None:
    hvd.init()


def rank() -> int:
    return hvd.rank()


def world_size() -> int:
    return hvd.size()


def allreduce(tensor: torch.Tensor) -> torch.Tensor:
    return hvd.allreduce(tensor)
