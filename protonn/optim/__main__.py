import itertools


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


def main():
    print("hi")
    # TODO: define syntax for specifying ranges
    params = {}
    params["aligner_left_eye"] = [[x, x] for x in [0.30, 0.31]]
    params["padding"] = [0, 0.5, 1.0, 1.5]
    for param_instance in product_dict(**params):
        print(param_instance)



if __name__ == "__main__":
    main()
