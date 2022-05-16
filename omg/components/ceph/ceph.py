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

    file_name = "{}_{}{}".format(com, "_".join(ceph_args), json_add)
    if file_name.startswith("ceph_config_show_"):
        file_name = file_name.replace("ceph_config_show_", "config_")

    ceph_file = os.path.join("ceph", commands_dir, file_name)

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
        suggestions = {}
        i = 1
        for p in mg_paths:
            try:
                files = os.listdir(os.path.join(p, "ceph", "must_gather_commands"))
                file_match = "{}_{}".format(com, "_".join(ceph_args))
                sugg = []
                sugg.extend([
                    "omg " + f.replace("_", " ")
                    for f in files if f.startswith(file_match)])
                sugg.extend([
                    "omg ceph config show {}".format(f.replace("config_", ""))
                    for f in files if f.startswith("config_")
                ])
                if sugg:
                    suggestions[i] = sugg
            except Exception as e:
                lg.debug(e)
                pass
            i += 1
        if suggestions:
            lg.success("\nNote: Output of following commands are available:\n")
            for i, sugg in suggestions.items():
                lg.success("\n".join(sugg))
                lg.opt(colors=True).success("^^^<e>[{}]</>^^^\n".format(i))
        else:
            lg.error(
                "Command output not found in any of the"
                " {} must-gather paths".format(len(mg_paths))
            )
