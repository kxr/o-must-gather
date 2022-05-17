# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_data(res):
    return len(dget(res, ["res", "data"], []))


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "DATA": _col_data,
    "AGE": None,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
