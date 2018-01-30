# this example shows different ways to track a parameter

import protonn.parameters


@protonn.parameters.view
def main():
    parameter_1 = 42  # type: Observed
    print(parameter_1)


if __name__ == "main":
    main()
