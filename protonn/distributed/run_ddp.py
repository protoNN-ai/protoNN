import os
import socket

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

    if rank != 0:
        os.environ["MASTER_PORT"] = "31415"
    else:
        # TODO: check if port is availalbe
        pass
    os.environ["WORLD_SIZE"] = str(size)
    os.environ["NODE_RANK"] = str(rank)
    master_addr = get_address()
    # cMASTER_ADDR - required (except for NODE_RANK 0); address of NODE_RANK 0 node
    print(master_addr)


if __name__ == "__main__":
    main()
