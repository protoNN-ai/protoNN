import datetime
import os
import sys
import shutil
import json
import re
import inspect
import pathlib
import logging


_LOG = logging.getLogger(__name__)


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
