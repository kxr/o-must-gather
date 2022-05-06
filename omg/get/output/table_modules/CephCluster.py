# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_datadirhostpath(res):
    return dget(res, ["res", "spec", "dataDirHostPath"], "Unknown")


def _col_moncount(res):
    return dget(res, ["res", "spec", "mon", "count"], "Unknown")


def _col_phase(res):
    return dget(res, ["res", "status", "phase"], "Unknown")


def _col_message(res):
    return dget(res, ["res", "status", "message"], "Unknown")


def _col_health(res):
    return dget(res, ["res", "status", "ceph", "health"], "Unknown")


def _col_external(res):
    return dget(res, ["res", "spec", "external", "enable"], "")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "DATADIRHOSTPATH": _col_datadirhostpath,
    "MONCOUNT": _col_moncount,
    "AGE": None,
    "PHASE": _col_phase,
    "MESSAGE": _col_message,
    "HEALTH": _col_health,
    "EXTERNAL": _col_external
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
