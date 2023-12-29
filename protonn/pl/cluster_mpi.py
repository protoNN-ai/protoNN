import os
import socket
import sys

# torch import is not used but should be here for mpi4py to precced mpi init from mpi4py
import torch  # noqa # pylint: disable=unused-import
from lightning.pytorch.plugins.environments import ClusterEnvironment
from mpi4py import MPI


# Global error handler
def global_except_hook(exctype, value, traceback):
    import sys

    try:
        import mpi4py.MPI

        sys.stderr.write("\n*****************************************************\n")
        sys.stderr.write(
            "Uncaught exception was detected on rank {}. \n".format(
                mpi4py.MPI.COMM_WORLD.Get_rank()
            )
        )
        from traceback import print_exception

        print_exception(exctype, value, traceback)
        sys.stderr.write("*****************************************************\n\n\n")
        sys.stderr.write("\n")
        sys.stderr.write("Calling MPI_Abort() to shut down MPI processes...\n")
        sys.stderr.flush()
    finally:
        try:
            import mpi4py.MPI

            mpi4py.MPI.COMM_WORLD.Abort(1)
        except Exception as e:
            sys.stderr.write("*****************************************************\n")
            sys.stderr.write("Sorry, we failed to stop MPI, this process will hang.\n")
            sys.stderr.write("*****************************************************\n")
            sys.stderr.flush()
            raise e


def get_address():
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
        sys.excepthook = global_except_hook
        self.comm = MPI.COMM_WORLD
        self.distributed_backend = os.environ["PROTONN_DISTRIBUTED_BACKEND"]

        self.ranks_per_node = int(os.environ["NUM_GPUS_PER_NODE"])
        if self.ranks_per_node == 0:
            self.ranks_per_node = 1
        master_addr = get_address() if self.distributed_backend != "MPI" else ""
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

    @property
    def is_master(self):
        return self.global_rank() == 0
