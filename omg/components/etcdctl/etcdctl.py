import os
from importlib import import_module
from loguru import logger as lg
from omg.utils.load_json import load_json

from omg.config import config


def cmd(etcdctl_args, output):
    cfg = config.get()
    mg_paths = cfg["paths"]

    if output is None:
        output = "table"

    command = "_".join(etcdctl_args)
    etcd_file = os.path.join(
        "etcd_info", "{}.json".format(command))

    lg.debug("etcd_file: {}".format(etcd_file))

    etcd_cmd_paths = {}
    i = 1
    for p in mg_paths:
        ceph_cmd_path = os.path.join(p, etcd_file)
        if os.path.isfile(ceph_cmd_path):
            lg.info("Command output file found: {}".format(ceph_cmd_path))
            etcd_cmd_paths[i] = ceph_cmd_path
        i += 1
    if etcd_cmd_paths:
        for i, cp in etcd_cmd_paths.items():
            try:
                j_data = load_json(cp)
                table_mod = import_module(
                    "omg.components.etcdctl.output.{}".format(command))
                table_mod.etcdctl_out(j_data, output)
            except Exception as e:
                lg.warning("Error generating output for {}: {}".format(command, e))
                lg.success("\nHere is the raw file ({}):".format(cp))
                with open(cp, "r") as cf:
                    print(cf.read())
            if len(mg_paths) > 1:
                lg.opt(colors=True).success("^^^<e>[{}]</>^^^\n".format(i))
    else:
        suggestions = {}
        i = 1
        for p in mg_paths:
            try:
                files = os.listdir(os.path.join(p, "etcd_info"))
                file_match = "_".join(etcdctl_args)
                sugg = []
                sugg.extend([
                    "omg etcdctl " + f.replace("_", " ").replace(".json", "")
                    for f in files if f.startswith(file_match)])
                if sugg:
                    suggestions[i] = sugg
            except Exception:
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
