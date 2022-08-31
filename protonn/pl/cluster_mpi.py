import os
import socket

# torch import is not used but should be here for mpi4py to precced mpi init from mpi4py
import torch
from mpi4py import MPI
from pytorch_lightning.plugins.environments import ClusterEnvironment


def get_address():

    if os.environ["PL_TORCH_DISTRIBUTED_BACKEND"] == "MPI":
        return ""

    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(("10.255.255.255", 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
        raise RuntimeError("can't determine routable IP")
    finally:
        st.close()
    return IP


class MPIClusterEnvironment(ClusterEnvironment):
    def __init__(self, **kwargs):
        self.comm = MPI.COMM_WORLD
        # TODO: automate this
        self.ranks_per_node = int(os.environ["NUM_GPUS_PER_NODE"])
        if self.ranks_per_node == 0:
            self.ranks_per_node = 1
        master_addr = get_address()
        self.master_addr = self.comm.bcast(master_addr, root=0)
        os.environ["RANK"] = str(self.comm.Get_rank())

    @property
    def creates_processes_externally(self) -> bool:
        """Return True if the cluster is managed (you don't launch processes yourself)"""
        return True

    @staticmethod
    def detect():
        return True

    def world_size(self) -> int:
        return self.comm.Get_size()

    def global_rank(self) -> int:
        return self.comm.Get_rank()

    def local_rank(self) -> int:
        return self.comm.Get_rank() % self.ranks_per_node

    def node_rank(self) -> int:
        # TODO: make sure processes allocate like this
        return self.comm.Get_rank() // self.ranks_per_node

    @property
    def main_address(self) -> str:
        return self.master_addr

    @property
    def main_port(self) -> int:
        return 31415

    def cnt_nodes(self) -> int:
        return self.comm.Get_size() // self.ranks_per_node

    def set_world_size(self, size: int) -> None:
        # raise(NotImplementedError("why would you set world size"))
        print("why would you set world size to ", size)

    def set_global_rank(self, rank: int) -> None:
        # raise(NotImplementedError(f"why would you set global rank to {rank}"))
        print("why would you set global rank to ", rank)
        # if rank == 2:
        #     traceback.print_stack()

    def barrier(self) -> None:
        self.comm.barrier()
