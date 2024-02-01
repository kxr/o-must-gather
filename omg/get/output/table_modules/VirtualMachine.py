# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_ready(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        ready = [c["status"] for c in conds if c["type"] == "Ready"]
        if ready:
            return ready[0]
    return "Unknown"


def _col_status(res):
    return dget(res, ["res", "status", "printableStatus"], "")

# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "AGE": None,
    "STATUS": _col_status,
    "READY": _col_ready,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
