# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_activemds(res):
    return dget(res, ["res", "spec", "metadataServer", "activeCount"], "Unknown")


def _col_phase(res):
    return dget(res, ["res", "status", "phase"], "Unknown")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "ACTIVEMDS": _col_activemds,
    "AGE": None,
    "PHASE": _col_phase,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
