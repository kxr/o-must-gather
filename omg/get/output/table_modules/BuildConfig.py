# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_type(res):
    return dget(res, ["res", "spec", "strategy", "type"], "Unknown")


def _col_from(res):
    return dget(res, ["res", "spec", "source", "type"], "Unknown")


def _col_latest(res):
    return dget(res, ["res", "status", "lastVersion"], "Unknown")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "TYPE": _col_type,
    "FROM": _col_from,
    "LATEST": _col_latest
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
