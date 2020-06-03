import uuid


def schedule_job(command):
    path_scripts = "~/.local/protonn/scripts"
    os.makedirs(path_scripts, exist_ok=True)
    unique_name = uuid.uuid4().hex + ".sh"
    path_script = os.path.join(path_scripts, unique_name)
    # write launch params to job file
    # run job scheduler
    with open(path_script, "w") as f:
        f.write(" ".join(map(str, command)))
