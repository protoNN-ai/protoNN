import pandas
import json
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


class PivotTable():
    def __init__(self,
                 key_target,
                 key_primary,
                 key_secondary,
                 keys_maximize=[],
                 keys_average=[],
                 keys_drop=[]):
        self.key_target = key_target
        self.key_primary = key_primary
        self.key_secondary = key_secondary
        self.keys_maximize = keys_maximize
        self.keys_average = keys_average
        self.keys_drop = keys_drop

    def get_maxed(self, df):
        return df

    def get_averaged(self, df):
        print("averaging")
        print(df)
        print("becomes")
        g = df.groupby(self.groupby_items + self.keys_average)
        r = g.mean()
        #r = df.mean()
        print(r)
        print()
        return r

    def pivot_dataframe(self, df):
        # TODO: warn about unknown keys
        self.groupby_items = [self.key_secondary, self.key_primary]
        group = df.groupby(self.groupby_items)
        r = group.apply(self.get_averaged)
        return r
        #group = df.groupby("device")
        #means = group.agg({framew})
        #means = group.agg({"device": "first"})
        # for i in group:
        #     print("g")
        #     ip[]
        #     print(type(i[1]))
        #     print(i)
        # print(group.aggregate("first"))
        exit(1)
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
