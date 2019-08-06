import itertools
import subprocess
import tempfile
import yaml
import os


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


def launch_with_parameters(params):
    print("launching with", params)
    target_dir = "/home/blackbird/Projects_heavy/Scry/beholder"
    os.chdir(target_dir)
    name_file_target = 'accuracy_config.yml'
    with open(name_file_target, 'w') as outfile:
        yaml.dump(params, outfile, default_flow_style=False)

    out_file = tempfile.TemporaryFile()
    err_file = tempfile.TemporaryFile()
    command = ["./boot.sh"]
    proc = subprocess.Popen(command, stdout=out_file, stderr=err_file)
    proc.wait()
    # out_file.seek(0)
    # out = out_file.read().decode()
    # err_file.seek(0)
    # err = err_file.read().decode()
    out_file.close()
    err_file.close()
    # TODO: abstraction for job
    # save unique file name
    # run/schedule experiment


def load_yaml(path):
    with open(path, 'r') as stream:
        return yaml.safe_load(stream)


def main():
    print("protonn optimizer")
    # load yml with all parameters
    params_original = load_yaml("/home/blackbird/Projects_heavy/Scry/beholder/accuracy_config_base.yml")
    # TODO: define syntax for specifying ranges
    params_ranges = {}
    params_ranges["aligner_left_eye"] = [[x, x] for x in [0.30, 0.31]]
    params_ranges["detection_padding"] = [0, 0.1, 0.15, 0.2]
    for param_instance in product_dict(**params_ranges):
        params_result = params_original.copy()
        params_result.update(param_instance)
        launch_with_parameters(params_result)


if __name__ == "__main__":
    main()
