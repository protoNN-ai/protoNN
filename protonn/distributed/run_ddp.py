import os
import socket
import sys

from mpi4py import MPI


def get_address():

    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
        raise RuntimeError("can't determine routable IP")
    finally:
        st.close()
    return IP


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print("starting ddp")

    os.environ["MASTER_PORT"] = "31415"
    os.environ["NODE_RANK"] = str(rank)
    os.environ["CNT_NODES"] = str(size)
    # PL_TORCH_DISTRIBUTED_BACKEND=gloo
    master_addr = get_address()
    master_addr = comm.bcast(master_addr, root=0)
    if rank != 0:
        os.environ["MASTER_ADDR"] = master_addr
    else:
        # TODO: check if port is availalbe
        pass

    os.system(" ".join(sys.argv[1:]))


if __name__ == "__main__":
    main()
