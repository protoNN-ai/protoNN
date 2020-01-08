import logging
import os
import pandas
from pandas.io.json import json_normalize
from vecto.utils.data import load_json


def df_from_file(path):
    data = load_json(path)
    # meta = [["experiment_setup", "task"],
    #         ["experiment_setup", "subcategory"],
    #         ["experiment_setup", "method"],
    #         ["experiment_setup", "embeddings"]]
    dframe = json_normalize(data)
    #if "details" in dframe:
    #    dframe.drop("details", axis="columns", inplace=True)
    #default_measurement = "accuracy"
    #try:
    #    default_measurement = dframe["experiment_setup.default_measurement"].unique()[0]
    #except KeyError:
    #    logger.warning(f"default_measurement not specified in {path}")
    #dframe["result"] = dframe["result." + default_measurement]
    # df["reciprocal_rank"] = 1 / (df["rank"] + 1)
    return dframe

df = df_from_file("/home/blackbird/Projects/Performance/log_debug/1.json")
print(df)
