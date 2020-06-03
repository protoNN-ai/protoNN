import os
import subprocess
import uuid


def run_locally(command):
    proc = subprocess.Popen(command, shell=False)
    proc.communicate()


def schedule_job(command, job_name="job_name"):
    path_home = os.path.expanduser("~")
    path_scripts = os.path.join(path_home, ".local/protonn/scripts")
    os.makedirs(path_scripts, exist_ok=True)
    # TODO: use project name + timestamp + short random str
    unique_name = uuid.uuid4().hex + ".sh"
    path_script = os.path.join(path_scripts, unique_name)
    # get this params from some options
    with open(path_script, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#$ -cwd\n")
        f.write("#$ -l rt_F=1\n")
        f.write("#$ -l h_rt=4:00:00\n")
        f.write(f"#$ -N {job_name}\n")
        f.write("#$ -j y\n")
        f.write("#$ -o $JOB_NAME.o$JOB_ID\n")
        f.write("\nsource ~/.bashrc\n")
        # TODO: do nice line breaks
        f.write(" ".join(map(str, command)))
        f.write("\n")
        f.write("path_scrypt=$(pwd)/$0\n")
        f.write("\nrm $path_scrypt\n")
        f.write("\n")

    os.chmod(path_script, 0o766)
    # run job scheduler
