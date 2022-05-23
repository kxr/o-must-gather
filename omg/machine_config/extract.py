import os
import yaml
from loguru import logger as lg

from omg.config import config
from omg.utils.dget import dget
from omg.get.get_resources import get_all_resources
from omg.machine_config.decode_content import decode


def _write_unit(systemd_path, unit):
    os.makedirs(systemd_path, exist_ok=True)
    name = unit["name"]
    if "enabled" in unit:
        if unit["enabled"] is not True:
            name += ".disabled"
    if "content" in unit:
        abs_fil = os.path.join(systemd_path, name)
        with open(abs_fil, "w") as fh:
            print(abs_fil)
            fh.write(unit["contents"])


def _write_mc(emc_path, mc):
    lg.debug("Writing MC with keys: {}".format(mc.keys()))
    lg.trace("{}".format(mc))

    mc_name = dget(mc, ["metadata", "name"])
    mc_config = dget(mc, ["spec", "config"])

    if not (mc_name and mc_config):
        lg.warning("Skipping invalid MachineConfig")
        return

    mc_path = os.path.join(emc_path, mc_name)
    os.makedirs(mc_path, exist_ok=True)

    # storage
    storage = dget(mc, ["spec", "config", "storage"])
    if storage:
        storage_path = os.path.join(mc_path, "storage")
        if "files" in storage:
            for fi in storage["files"]:
                path = fi["path"]
                rel_fil = path[1:]
                rel_dir = os.path.dirname(rel_fil)
                abs_dir = os.path.join(storage_path, rel_dir)
                abs_fil = os.path.join(storage_path, rel_fil)
                os.makedirs(abs_dir, exist_ok=True)
                with open(abs_fil, "w") as fh:
                    print(abs_fil)
                    fh.write(decode(fi["contents"]["source"]))
    # systemd
    systemd_u = dget(mc, ["spec", "config", "systemd", "units"])
    if systemd_u:
        for unit in systemd_u:
            dropins = dget(systemd_u, ["dropins"])
            if dropins:
                systemd_path = os.path.join(
                    mc_path,
                    "systemd/" + dget(unit, ["name"], "") + ".d"
                )
                for d_unit in dropins:
                    _write_unit(systemd_path, d_unit)
            if dget(unit, ["name"]) and dget(unit, ["contents"]):
                systemd_path = os.path.join(mc_path, "systemd")
                _write_unit(systemd_path, unit)
    # passwd
    passwd = dget(mc, ["spec", "config", "passwd"])
    if passwd:
        passwd_path = os.path.join(mc_path, "passwd")
        if "users" in passwd:
            for user in passwd["users"]:
                os.makedirs(passwd_path, exist_ok=True)
                name = user["name"]
                abs_fil = os.path.join(passwd_path, name)
                with open(abs_fil, "w") as fh:
                    print(abs_fil)
                    fh.write(yaml.dump(user))
        # TODO groups
    # TODO networkd
    # TODO directories, links, disks, raid, filesystems


def mc_extract(m):

    cfg = config.get()
    paths = cfg["paths"]

    if m:
        mc_names = list(m)
    else:
        mc_names = []

    all_mcs = get_all_resources({"mc": mc_names})

    # {1: {"mc": [...]}, 2: {"mc": [...] }}
    for i, mc_res in all_mcs.items():

        mg_path = paths[i-1]
        emc_path = os.path.join(mg_path, "extracted-machine-configs")

        # {"mc": [{"res": {}, "yfile_ts": "..."}, ... ]}
        for _, mc_data in mc_res.items():
            if mc_data:
                try:
                    os.makedirs(emc_path, exist_ok=True)
                except PermissionError as e:
                    lg.warning(e)
                    continue
                for mc in mc_data:
                    mc_rd = mc["res"]
                    _write_mc(emc_path, mc_rd)
