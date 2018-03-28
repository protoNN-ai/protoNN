#  this is assuming chainer format
import pandas
import os
import json


def load_single_run(path):
    df = pandas.read_json(os.path.join(path, "log"))
    with open(os.path.join(path, "params.json")) as f:
        d = json.load(f)
    time_elapsed = df["elapsed_time"]
    time_epoch = [y - x for x, y in zip(time_elapsed, time_elapsed[1:])]
    time_epoch = [df["elapsed_time"][0]] + time_epoch
    df["epoch_time"] = time_epoch
    for key in d:
        try:
            df[key] = d[key]
        except:
            print("could not export key ", key)
        # TODO: flatten hierarchical metadata entries
    return df


def load_multiple_runs(path):
    experiments = []
    for d in sorted(os.listdir(path)):
        try:
            experiments.append(load_single_run(os.path.join(path, d)))
        except Exception as e:
            print("could not load ", d)
            pass
            # raise e
    return experiments
