import datetime
# import re
import inspect
import json
import logging
import os
import pathlib
import shutil
import sys

_LOG = logging.getLogger(__name__)


def describe_var(var):
    # print("called on", var)
    result = ""
    result = f"{type(var).__name__}"
    if hasattr(var, 'shape'):
        result += f" shape={var.shape}"
    elif hasattr(var, '__len__'):
        result += f" len={len(var)}"
    if isinstance(var, tuple) or isinstance(var, list):
        result += "\n"
        for child in var[:5]:
            descr_child = describe_var(child)
            for line in descr_child.split("\n"):
                if len(line) > 1:
                    result += "  " + line + "\n"
    if isinstance(var, dict):
        result += "\n"
        for key in var:
            descr_child = describe_var(var[key])
            lines = descr_child.strip().split("\n")
            result += f"  {key}:""\n"
            for line in lines:
                result += f"    " + line + "\n"

    return result


def get_time_str():
    d = datetime.datetime.now()
    s = d.strftime("%y.%m.%d_%H.%M.%S")
    return s


def save_data_json(data, name_file):
    path = os.path.realpath(os.path.dirname(name_file))
    os.makedirs(path, exist_ok=True)
    s = json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)
    f = open(name_file, 'w')
    print(s, file=f)
    f.close()


def load_json(path):
    f = open(path)
    s_data = f.read()
    data = json.loads(s_data)
    f.close()
    return data


# def _detect_local_imports():
#    r = re.compile('\nimport \w+|from \w+')
#    with open(sys.argv[0]) as f:
#        code = f.read()
#    imports = [i.split(' ')[-1] for i in r.findall(code)]
#    dirs = [f.split('.')[0] for f in os.listdir() if '.py' in f]
#    return [dir + '.py' for dir in set(dirs).intersection(imports)]


def _get_caller_folder(stack_level: int = 1) -> pathlib.Path:
    """Determine folder in which the caller module of a function is located."""
    frame_info = inspect.getouterframes(inspect.currentframe())[stack_level]
    caller_path = frame_info[1]  # frame_info.filename

    here = pathlib.Path(caller_path).absolute().resolve()
    if not here.is_file():
        raise RuntimeError('path "{}" was expected to be a file'.format(here))
    here = here.parent
    if not here.is_dir():
        raise RuntimeError('path "{}" was expected to be a directory'.format(here))
    return here


def save_code(path, stack_level: int = 1):
    os.makedirs(path, exist_ok=True)
    path_caller = _get_caller_folder(stack_level + 1)
    _LOG.debug("path_caller: " + str(path_caller))
    # major, minor, _, _, _ = 
    if sys.version_info[:2] < (3, 6):  # TODO: remove this when we drop py 3.5 support
        path_caller = str(path_caller)
    for root, dirs, files in os.walk(path_caller):
        rel_root = os.path.relpath(root, path_caller)
        for file in files:
            if file.endswith(".py"):
                os.makedirs(os.path.join(path, rel_root), exist_ok=True)
                path_dest = os.path.join(path, rel_root, file)
                shutil.copy2(os.path.join(root, file), path_dest)
                # print(os.path.join(root, file))
                # current_file = os.path.realpath(__file__)


# TODO: implement this properly
def num_to_str_with_suffix(num):
    if num >= 1000000:
        return f"{num // 1000000}M"
    else:
        return f"{num // 1000}K"
