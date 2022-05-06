# -*- coding: utf-8 -*-
from omg.utils.dget import dget
from omg.utils.age import age


def _col_version(res):
    hist = dget(res, ["res", "status", "history"])
    if hist:
        cluster_v = [h["version"] for h in hist if h["state"] == "Completed"]
        if cluster_v:
            return cluster_v[0]
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


def _col_since(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        ltt = [c["lastTransitionTime"] for c in conds if c["type"] == "Available"]
        if ltt:
            yfile_ts = dget(res, ["yfile_ts"])
            return age(ltt[0], yfile_ts)
    return "Unknown"


def _col_status(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        status = [c["message"] for c in conds if c["type"] == "Progressing"]
        if status:
            return status[0]
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
    "SINCE": _col_since,
    "STATUS": _col_status
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
