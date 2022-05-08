import os
from loguru import logger as lg

from omg.config import config


def cmd(ceph_args, output, com):
    cfg = config.get()
    mg_paths = cfg["paths"]

    if output in ["json", "json-pretty"]:
        commands_dir = "must_gather_commands_json_output"
        json_add = "_--format_json-pretty"
    else:
        commands_dir = "must_gather_commands"
        json_add = ""

    ceph_file = os.path.join(
        "ceph", commands_dir,
        "{}_{}{}".format(com, "_".join(ceph_args), json_add))

    lg.debug("ceph_file: {}".format(ceph_file))

    ceph_cmd_paths = {}
    i = 1
    for p in mg_paths:
        ceph_cmd_path = os.path.join(p, ceph_file)
        if os.path.isfile(ceph_cmd_path):
            lg.info("Command output file found: {}".format(ceph_cmd_path))
            ceph_cmd_paths[i] = ceph_cmd_path
        i += 1

    if ceph_cmd_paths:
        for i, cp in ceph_cmd_paths.items():
            with open(cp, "r") as lf:
                print(lf.read())
            if len(mg_paths) > 1:
                lg.opt(colors=True).success("^^^<e>[{}]</>^^^\n".format(i))
    else:
        suggestions = []
        for p in mg_paths:
            try:
                files = os.listdir(os.path.join(p, "ceph", "must_gather_commands"))
                file_match = "{}_{}".format(com, "_".join(ceph_args))
                suggestions.extend([
                    "omg " + f.replace("_", " ")
                    for f in files if f.startswith(file_match)])
            except Exception:
                pass
        if suggestions:
            lg.success("\nNote: Output of following commands are available:")
            lg.success("\n".join(suggestions))
        else:
            lg.error(
                "Command output not found in any of the"
                " {} must-gather paths".format(len(mg_paths))
            )
