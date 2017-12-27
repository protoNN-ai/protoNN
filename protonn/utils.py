import datetime
import os
import sys
import shutil
import json
import re


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


def save_options(options, path):
    save_data_json(options, os.path.join(path, "options.json"))


def detect_local_imports():
    r = re.compile('\nimport \w+|from \w+')
    with open(sys.argv[0]) as f:
        code = f.read()
    imports = [i.split(' ')[-1] for i in r.findall(code)]
    dirs = [f.split('.')[0] for f in os.listdir() if '.py' in f]
    return [dir + '.py' for dir in set(dirs).intersection(imports)]


def save_code(path):
    os.makedirs(path, exist_ok=True)
    shutil.copy2(sys.argv[0], os.path.join(path, sys.argv[0]))
    for im in detect_local_imports():
        shutil.copy2(im, os.path.join(path, im))
