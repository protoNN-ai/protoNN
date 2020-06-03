import os
import subprocess
import uuid
from protonn.config import load_config


# TODO: get job scheduler parameters from config
# group_name = "gcb50300"


def run_locally(command):
    proc = subprocess.Popen(command, shell=False)
    proc.communicate()


# TODO: allow override some of default parameters like group name
def schedule_job(command, job_name="job_name", cnt_nodes=1):
    config = load_config()
    group_name = config.qsub.group
    path_home = os.path.expanduser("~")
    path_scripts = os.path.join(path_home, ".local/protonn/scripts")
    os.makedirs(path_scripts, exist_ok=True)
    # TODO: use project name + timestamp + short random str
    unique_name = uuid.uuid4().hex + ".sh"
    path_script = os.path.join(path_scripts, unique_name)
    # TODO: get this params from some options
    # TODO: optionally wrap into MPI call depending on configuration
    with open(path_script, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#$ -cwd\n")
        f.write(f"#$ -l rt_F={cnt_nodes}\n")
        f.write("#$ -l h_rt=4:00:00\n")
        f.write(f"#$ -N {job_name}\n")
        f.write("#$ -j y\n")
        f.write("#$ -o $JOB_NAME.o$JOB_ID\n")
        f.write("\nsource ~/.bashrc\n")
        # TODO: do nice line breaks
        f.write(" ".join(map(str, command)))
        f.write("\n")
        f.write("path_scrypt=$(pwd)/$0\n")
        f.write("rm $path_scrypt\n")
        f.write("\n")

    os.chmod(path_script, 0o766)
    # TODO: get group name from config
    cmd_schedule = ["qsub",
                    "-g",
                    group_name,
                    path_script]
    run_locally(cmd_schedule)
