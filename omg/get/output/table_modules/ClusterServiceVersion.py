# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_display(res):
    return dget(res, ["res", "spec", "displayName"])


def _col_version(res):
    return dget(res, ["res", "spec", "version"])


def _col_replaces(res):
    return dget(res, ["res", "spec", "replaces"])


def _col_phase(res):
    return dget(res, ["res", "status", "phase"])


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "DISPLAY": _col_display,
    "VERSION": _col_version,
    "REPLACES": _col_replaces,
    "PHASE": _col_phase
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
