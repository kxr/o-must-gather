import os
from loguru import logger as lg
from omg.config import config
from omg.utils.dget import dget


def cmd(resource, container, previous):
    lg.debug("FUNC_INIT: {}".format(locals()))

    cfg = config.get()
    paths = dget(cfg, ["paths"])
    ns = dget(cfg, ["project"])

    if not paths:
        lg.error("No must-gather selected")
        raise SystemExit(1)

    if ns == "_all":
        lg.error("All Namespaces is not supported with `omg log ...` ")
        raise SystemExit(1)
    elif ns is None:
        lg.error("No namespace/project selected")
        raise SystemExit(1)

    if "/" in resource:
        r_type = resource.split("/")[0]
        pod = resource.split("/")[1]
        if r_type not in ["pod", "pods"]:
            lg.error("Can not print logs of type:", r_type)
            raise SystemExit(1)
    else:
        pod = resource

    if not ns:
        lg.error("Namespace/Project not set")
        raise SystemExit(1)

    log_files = []
    for path in paths:

        proj_path = os.path.join(path, "namespaces", ns)
        if not os.path.isdir(proj_path):
            continue

        pod_dir = os.path.join(proj_path, "pods", pod)
        if not os.path.isdir(pod_dir):
            # lg.warning("Pod directory not found: {}".format(pod_dir))
            continue

        con_dirs = [
            c for c in os.listdir(pod_dir)
            if os.path.isdir(os.path.join(pod_dir, c))
        ]

        if not con_dirs:
            lg.warning("No container directory not found in {}".format(pod_dir))
            continue
        elif len(con_dirs) == 1:
            con_dir = con_dirs[0]
            if container and container != con_dir:
                lg.warning("Container directory {} not found in {}".format(
                    container, pod_dir))
                continue
        elif len(con_dirs) > 1:
            if container is None:
                lg.error(
                    "This pod has more than one containers:" +
                    str(con_dirs) + "\n"
                    "Use -c/--container to specify the container"
                )
                raise SystemExit(1)
            elif container not in con_dirs:
                lg.warning("Container directory {} not found in {}".format(
                    container, pod_dir))
                continue
            else:
                con_dir = container

        if previous:
            log_files.append(
                os.path.join(pod_dir, con_dir, con_dir, "logs", "previous.log")
            )
        else:
            log_files.append(
                os.path.join(pod_dir, con_dir, con_dir, "logs", "current.log")
            )

    if not log_files:
        lg.error("No log files found")

    for logfile in log_files:
        if not os.path.isfile(logfile):
            lg.warning("Log file not found: {}".format(logfile))
        else:
            lg.info(logfile)
            with open(logfile, "r") as lf:
                print(lf.read())
        if len(log_files) > 1:
            print("")
            print("~~~")
            print("")
