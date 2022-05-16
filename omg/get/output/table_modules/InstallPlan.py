# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_csv(res):
    csv = dget(res, ["res", "spec", "clusterServiceVersionNames"])
    if csv:
        return csv[0]


def _col_approval(res):
    return dget(res, ["res", "spec", "approval"])


def _col_approved(res):
    return dget(res, ["res", "spec", "approved"])


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "CSV": _col_csv,
    "APPROVAL": _col_approval,
    "APPROVED": _col_approved
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
