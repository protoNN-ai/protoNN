import itertools


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


def main():
    print("protonn optimizer")
    # load yml with all parameters
    params_original = {"a": 1, "padding": 7}
    # TODO: define syntax for specifying ranges
    params_ranges = {}
    params_ranges["aligner_left_eye"] = [[x, x] for x in [0.30, 0.31]]
    params_ranges["padding"] = [0, 0.5, 1.0, 1.5]
    for param_instance in product_dict(**params_ranges):
        params_result = params_original.copy()
        params_result.update(param_instance)
        print(params_result)
        # inject modified parameters
        # save unique file name
        # run/schedule experiment


if __name__ == "__main__":
    main()
