from typing import Optional

import torch
import torch.distributed as dist

ALLREDUCE_OPS = [dist.ReduceOp.SUM]


def init() -> None:
    if dist.is_mpi_available():
        backend = "mpi"
    elif (
        torch.cuda.is_available()
        and dist.is_nccl_available()
        and torch.cuda.device_count() > 0
    ):
        backend = "nccl"
    elif dist.is_gloo_available():
        backend = "gloo"
    dist.init_process_group(backend)


def rank() -> int:
    return dist.get_rank()


def world_size() -> int:
    return dist.get_world_size()


def allreduce(tensor: torch.Tensor, op: Optional[int]) -> torch.Tensor:
    if op is None:
        dist.all_reduce(tensor)
        tensor /= dist.get_world_size()
    else:
        dist.all_reduce(tensor, op=ALLREDUCE_OPS[op])
    return tensor


def broadcast(tensor: torch.Tensor, src_rank: int) -> torch.Tensor:
    dist.broadcast(tensor, src_rank)
    return tensor
