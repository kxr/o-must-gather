# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_signername(res):
    return dget(res, ["res", "spec", "signerName"], "")


def _col_requestor(res):
    return dget(res, ["res", "spec", "username"], "")


def _col_condition(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        return ",".join([c["type"] for c in conds])
    return "Pending"


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "AGE": None,
    "SIGNERNAME": _col_signername,
    "REQUESTOR": _col_requestor,
    "CONDITION": _col_condition
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
