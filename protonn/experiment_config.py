import logging
import os
import platform
import sys
from pathlib import Path

import yaml

from protonn.utils import get_time_str


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
    def __init__(self, name_task, param_path=None, is_master=True):
        self._is_master = is_master
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
        self.read_from_yaml_and_set_default(path, name_task)
        # TODO(vatai): create base trainer
        print("WARRNING: seed not set.  This will be implemented in trainer.base class")

    def init_experiment(self, cluster_env):
        self.add_distributed_info(cluster_env.world_size())
        self.maybe_create_unique_path()
        if "process_group_backend" in self["ddp_strategy_params"]:
            _logger = logging.getLogger(__name__)
            _logger.warning(
                f"'ddp_strategy_params.process_group_backend' was defined in the config file but will be ignore! Environment variable 'PROTONN_DISTRIBUTED_BACKEND={cluster_env.distributed_backend}' takes precedence!"
            )
        self["ddp_strategy_params"]["process_group_backend"] = cluster_env.distributed_backend
        cluster_env.barrier()

    # TODO: we have near identical method in langmo
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
        self["cnt_workers"] = cnt_workers
        # TODO: we remove this because accumulate batches is now dynamic
        # batch_size = self["batch_size"]
        # acc_batches = self["accumulate_batches"]
        # self["batch_size_effective"] = batch_size * cnt_workers * acc_batches

    def set_defaults(self):
        self.defaults = dict()
        self.defaults["seed"] = 0
        self.defaults["path_base"] = "./logs"
        self.defaults["path_results"] = None
        # if path results is defined - use it over base
        # self.defaults["create_unique_path"] = True
        self.defaults["ddp_strategy_params"] = {}
        self.required_options = set()
