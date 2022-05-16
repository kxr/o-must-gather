# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_drivers(res):
    drivers = dget(res, ["res", "spec", "drivers"])
    if drivers:
        return len(drivers)
    return "0"


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "DRIVERS": _col_drivers,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
