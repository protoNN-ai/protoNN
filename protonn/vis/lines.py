from protonn.vis import df_from_dir, PivotTable, filter_by
from protonn.vis.styles import colors, line_styles
from matplotlib import pyplot as plt


def plot_lines(df, key_target, key_first, key_second, key_third):
    # print(key_target, key_first, key_second, key_third)
    vals_third = sorted(df[key_third].unique())
    dic_style = {f: s for f, s in zip(vals_third, line_styles)}
    # TODO: move this to extra args
    x_ticks = None
    vals_second = df[key_second].unique()
    for color, value_second in zip(colors, vals_second):
        # print("plotting ", device)
        df_filtered = filter_by(df, {key_second: value_second})
        pt = PivotTable(key_target=key_target,
                        keys_argument=[key_first, key_third],
                        keys_average=[])
        df_mean, df_max, df_std = pt.pivot_dataframe(df_filtered)
        # print(df_mean)
        if x_ticks is None:
            x_ticks = df_mean.index
        for col in sorted(df_mean.columns):
            plt.plot(df_mean.index, df_mean[col],
                     linestyle=dic_style[col],
                     linewidth=1.2,
                     color=color,
                     label=f"{value_second} / {col}")
    plt.ylabel(key_target)
    #plt.xticks(x_ticks[8:], rotation=90)
    # TODO: make this customi
    plt.xlabel(key_first)
    # plt.legend()
