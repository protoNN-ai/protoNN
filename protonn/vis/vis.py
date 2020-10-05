import pandas
import json
import logging
from pandas import json_normalize
logger = logging.getLogger(__name__)
from ..utils import load_json


def df_from_file(path):
    try:
        data = load_json(path)
    except Exception as e:
        logger.error(f"can't load {str(path)}")
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
                 keys_argument=[],
                 keys_maximize=[],
                 keys_average=[]):
        self.key_target = key_target
        self.keys_argument = keys_argument
        self.keys_maximize = keys_maximize
        self.keys_average = keys_average

    def get_maxed(self, df):
        idx_max = df[self.key_target].idxmax()
        row_max = df.loc[idx_max]
        for key in self.keys_maximize:
            df = df[df[key] == row_max[key]]
        return df

    def pivot_dataframe(self, df):
        self.groupby_items = self.keys_argument
        group = df.groupby(self.groupby_items)
        maxed = group.apply(self.get_maxed)
        for key in self.keys_maximize + self.keys_average:
            maxed.drop(key, axis="columns", inplace=True)
        maxed.reset_index(drop=True, inplace=True)
        keys_allowed = self.groupby_items + [self.key_target]
        for key in maxed.columns:
            if key not in keys_allowed:
                try:
                    if len(maxed[key].unique()) > 1:
                        logger.warning(f"unmanaged col {key} is not unique!")
                except:
                    logger.warning(f"can't check if key {key} is unuque")
        maxed = maxed.loc[:, keys_allowed]
        unstacked = maxed.groupby(self.groupby_items)
        df_mean = unstacked[self.key_target].aggregate('mean')
        df_max = unstacked[self.key_target].aggregate('max')
        df_std = unstacked[self.key_target].aggregate('std')
        if df_mean.index.nlevels > 1:
            df_mean = df_mean.unstack()
            df_max = df_max.unstack()
            df_std = df_std.unstack()
        return df_mean, df_max, df_std.fillna(0)


def filter_by(df, filters, drop=True):
    df_plot = df
    for key in filters:
        df_plot = df_plot[df_plot[key] == filters[key]]
        if drop:
            df_plot = df_plot.drop(key, axis="columns")
    return df_plot
