import logging
import os
import platform
import sys
from pathlib import Path

import yaml
from protonn.utils import get_time_str
# this should be reimplemented in protonn
from transformers import set_seed


def parse_float(dic, key):
    if key in dic:
        if isinstance(dic[key], str):
            dic[key] = float(dic[key])


def load_yaml_file(path):
    with open(path, "r") as cfg:
        # TODO: isn't this the place to support fancy floats?
        data = yaml.load(cfg, Loader=yaml.SafeLoader)
    return data


# TODO: need better name
def load_yaml_config(path_config):
    params_user = load_yaml_file(path_config)
    parse_float(params_user, "initial_lr")
    parse_float(params_user, "max_lr")
    parse_float(params_user, "eps")
    parse_float(params_user, "beta1")
    parse_float(params_user, "beta2")
    return params_user


class BaseConfig(dict):
    def __init__(self, name_task, cluster_env, param_path=None):
        self["name_task"] = name_task
        if int(os.environ["NUM_GPUS_PER_NODE"]) > 0:
            self["devices"] = -1
            self["accelerator"] = "gpu"
        else:
            self["devices"] = 1
            self["accelerator"] = "cpu"
        if len(sys.argv) < 2 and param_path is None:
            print("run main.py config.yaml")
            print("or")
            print("run main.py logs/path/to/snapshot/epoc10_step42000")
            exit(-1)
        if param_path is None:
            path = Path(sys.argv[1])
        else:
            path = Path(param_path)
        self.set_defaults()
        self._is_master = cluster_env.global_rank() == 0
        self.read_from_yaml_and_set_default(path, name_task)
        self.add_distributed_info(cluster_env.world_size())
        self.maybe_create_unique_path()
        set_seed(self["seed"])
        cluster_env.barrier()

    def get_run_folder(self):
        timestamp = self["timestamp"][:-3]
        hostname = platform.node().split(".")[0]
        bs = self["batch_size_effective"]
        lr = self["max_lr"] * self["cnt_workers"]
        seed = self["seed"]
        run_folder = f"{timestamp}_bs{bs}_lr{lr:.4f}_s{seed}_{hostname}"
        # TODO: make this trully unique
        return run_folder

    def maybe_create_unique_path(self):
        if self["create_unique_path"]:
            self["path_results"] = os.path.join(self["path_results"], self["name_project"])
            # TODO: extract nicemodel name from metadata
            # model_name = self["model_name"].split("/")[-1]
            # self["path_results"] = os.path.join(self["path_results"], model_name)
            run_dir = self.get_run_folder()
            self["path_results"] = os.path.join(self["path_results"], run_dir)
        else:
            # TODO: chech if the folder is empty
            pass
        if "WANDB_MODE" in os.environ and os.environ["WANDB_MODE"].lower() != "disabled":
            if self._is_master:
                path_wandb = Path(self["path_results"]) / "wandb"
                path_wandb.mkdir(parents=True, exist_ok=True)

    def read_from_yaml_and_set_default(self, path, name_project):
        self["name_project"] = name_project
        self["timestamp"] = get_time_str()
        _logger = logging.getLogger(__name__)
        user_config = load_yaml_config(path)
        for key, value in user_config.items():
            if key not in self.defaults and key not in self.required_options and key != "suffix":
                raise RuntimeError(f"got unexpected key in user config\t{key}: {value}")
            # print(key, value)
        for key in self.required_options:
            if key not in user_config:
                raise RuntimeError(f"required key not in config {key}")
        for key, value in self.defaults.items():
            if key not in user_config:
                if self._is_master:
                    _logger.warning(f"setting parameter {key} to default value {value}")
                self[key] = value

        self.update(user_config)

    def add_distributed_info(self, cnt_workers):
        batch_size = self["batch_size"]
        acc_batches = self["accumulate_batches"]
        self["cnt_workers"] = cnt_workers
        self["batch_size_effective"] = batch_size * cnt_workers * acc_batches

    def set_defaults(self):
        self.defaults = dict()
        self.defaults["seed"] = 0
        self.defaults["create_unique_path"] = True
        self.required_options = set()
