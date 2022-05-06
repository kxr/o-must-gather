# -*- coding: utf-8 -*-
from omg.utils.dget import dget
from omg.utils.age import age


def _col_version(res):
    vers = dget(res, ["res", "status", "versions"])
    if vers:
        operator_v = [v["version"] for v in vers if v["name"] == "operator"]
        if operator_v:
            return operator_v[0]
    return ""


def _col_available(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        available = [c["status"] for c in conds if c["type"] == "Available"]
        if available:
            return available[0]
    return "Unknown"


def _col_progressing(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        prog = [c["status"] for c in conds if c["type"] == "Progressing"]
        if prog:
            return prog[0]
    return "Unknown"


def _col_degraded(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        degraded = [c["status"] for c in conds if c["type"] == "Degraded"]
        if degraded:
            return degraded[0]
    return "Unknown"


def _col_since(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        ltt = [c["lastTransitionTime"] for c in conds if c["type"] == "Available"]
        if ltt:
            yfile_ts = dget(res, ["yfile_ts"])
            return age(ltt[0], yfile_ts)
    return "Unknown"


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "VERSION": _col_version,
    "AVAILABLE": _col_available,
    "PROGRESSING": _col_progressing,
    "DEGRADED": _col_degraded,
    "SINCE": _col_since
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
