# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_package(res):
    return dget(res, ["res", "spec", "name"])


def _col_source(res):
    return dget(res, ["res", "spec", "source"])


def _col_channel(res):
    return dget(res, ["res", "spec", "channel"])


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "PACKAGE": _col_package,
    "SOURCE": _col_source,
    "CHANNEL": _col_channel
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
