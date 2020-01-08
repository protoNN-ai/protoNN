import pandas
import json
from pathlib import Path
from pandas.io.json import json_normalize


def load_json(path):
    f = open(path)
    s_data = f.read()
    data = json.loads(s_data)
    f.close()
    return data


def df_from_file(path):
    try:
        data = load_json(path)
    except Exception as e:
        print(f"can't load {str(path)}")
        raise e
    dframe = json_normalize(data)

    # TODO: drop heavy columns before or after normalization
    return dframe


def df_from_dir(path):
    dfs = []
    dfs = [df_from_file(f) for f in path.glob("**/*.json")]
    if len(dfs) == 0:
        raise RuntimeError("no data to load")
    dframe = pandas.concat(dfs, sort=True)
    return dframe


def pivot_dataframe(df, key_target, key_primary, key_secondary):
    groupby_items = [key_secondary, key_primary]
    group = df.groupby(groupby_items)
    means = group.mean()
    means.reset_index(inplace=True)
    means = means.loc[:, groupby_items + [key_target]]
    # TODO: aggregate according to strategy for each column individually 
    unstacked = means.groupby(groupby_items)[key_target].aggregate('first').unstack()
    return unstacked


def filter_by(df, filters):
    df_plot = df
    for key in filters:
        df_plot = df_plot[df_plot[key] == filters[key]]
    return df_plot
