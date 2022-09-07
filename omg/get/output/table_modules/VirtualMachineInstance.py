# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_ready(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        ready = [c["status"] for c in conds if c["type"] == "Ready"]
        if ready:
            return ready[0]


def _col_phase(res):
    return dget(res, ["res", "status", "phase"], "")


def _col_ip(res):
    interfaces = dget(res, ["res", "status", "interfaces"])
    if interfaces:
        return interfaces[0]["ipAddresses"][0]


def _col_node(res):
    return dget(res, ["res", "status", "nodeName"])


def _col_live_migratable(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        LiveMigratable = [c["status"] for c in conds if c["type"] == "LiveMigratable"]
        if LiveMigratable:
            return LiveMigratable[0]


def _col_paused(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        Paused  = [c["status"] for c in conds if c["type"] == "Paused"]
        if Paused:
            return Paused[0]


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "AGE": None,
    "PHASE": _col_phase,
    "IP": _col_ip,
    "NODE": _col_node,
    "READY": _col_ready
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
    "LIVE-MIGRATABLE": _col_live_migratable,
    "PAUSED" : _col_paused
}
