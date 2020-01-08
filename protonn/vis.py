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
                 keys_average=[]):
        self.key_target = key_target
        self.key_primary = key_primary
        self.key_secondary = key_secondary
        self.keys_maximize = keys_maximize
        self.keys_average = keys_average

    def get_maxed(self, df):
        return df

    def get_averaged(self, df):
        print("averaging")
        print(df)
        print("becomes")
        idx_max = df[self.key_target].idxmax()
        row_max = df.loc[idx_max]
        for key in self.keys_maximize:
            df = df[df[key] == row_max[key]]
        print(df)
        print()
        return df
#        g = df.groupby(self.groupby_items + self.keys_average)
 #       r = g.mean()
        #r = df.mean()
  #      print(r)
   #     print()
    #    return r

    def pivot_dataframe(self, df):
        self.groupby_items = [self.key_secondary, self.key_primary]
        group = df.groupby(self.groupby_items)
        maxed = group.apply(self.get_averaged)
        #maxed.drop(self.key_primary, axis="columns", inplace=True)
        #maxed.drop(self.key_secondary, axis="columns", inplace=True)
        for key in self.keys_maximize + self.keys_average:
            maxed.drop(key, axis="columns", inplace=True)
        maxed.reset_index(drop=True, inplace=True)
        # TODO: warn about unknown keys
#        return maxed
        print("===========")
        print(maxed)
        maxed = maxed.loc[:, [self.key_primary, self.key_secondary, self.key_target]]
        print("===========")
        print(maxed)
        # TODO: aggregate according to strategy for each column individually 
        unstacked = maxed.groupby([self.key_primary, self.key_secondary])[self.key_target].aggregate('mean').unstack()
        return unstacked


def filter_by(df, filters):
    df_plot = df
    for key in filters:
        df_plot = df_plot[df_plot[key] == filters[key]]
    return df_plot
