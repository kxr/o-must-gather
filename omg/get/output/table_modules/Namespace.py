# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_disp_name(res):
    return dget(res, ["res", "metadata", "annotations", "openshift.io/display-name"], "")


def _col_status(res):
    return dget(res, ["res", "status", "phase"], "")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by _build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "DISPLAY NAME": _col_disp_name,
    "STATUS": _col_status,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
