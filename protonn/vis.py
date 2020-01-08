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


def filter_by(df, filters):
    df_plot = df
    for key in filters:
        df_plot = df_plot[df_plot[key] == filters[key]]
    return df_plot


df = df_from_dir(Path("/home/blackbird/Projects/Performance/log_debug"))
print(df)
