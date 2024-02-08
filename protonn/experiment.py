import os

from protonn.pl.cluster_mpi import MPIClusterEnvironment


class Experiment:
    def __init__(self, name_task):
        self.cluster_env = MPIClusterEnvironment()
        self.name_task = name_task

    @property
    def is_master(self):
        return self.cluster_env.global_rank() == 0

    def maybe_create_unique_path(self):
        # THIS SHOULD JUST GET PATH FROM CONFIG
        if self.params["path_results"] is None:
            self.params["path_results"] = self.params.get_run_folder()
        if self.is_master:
            self.params["path_results"].mkdir(parents=True, exist_ok=True)
            if "WANDB_MODE" not in os.environ or os.environ["WANDB_MODE"].lower() != "disabled":
                path_wandb = self.params["path_results"] / "wandb"
                path_wandb.mkdir(parents=True, exist_ok=True)

    # load config
    # create directories
    # create PL trainer
    # train
    # optionally resume
