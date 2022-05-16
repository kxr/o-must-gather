# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_desired(res):
    return dget(res, ["res", "spec", "replicas"], "")


def _col_current(res):
    return dget(res, ["res", "status", "replicas"], "")


def _col_ready(res):
    return dget(res, ["res", "status", "readyReplicas"], "")


def _col_available(res):
    return dget(res, ["res", "status", "availableReplicas"], "")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "DESIRED": _col_desired,
    "CURRENT": _col_current,
    "READY": _col_ready,
    "AVAILABLE": _col_available,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
