# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_created_at(res):
    return dget(res, ["res", "metadata", "creationTimestamp"], "Unknown")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "CREATED AT": _col_created_at
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
