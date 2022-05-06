# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_ready(res):
    cont_total = len(dget(res, ["res", "spec", "containers"], ""))
    cont_ready = len([
            r for r in
            dget(res, ["res", "status", "containerStatuses"], "")
            if dget(r, ["ready"]) is True
        ])
    return "{}/{}".format(cont_ready, cont_total)


def _col_status(res):
    return dget(res, ["res", "status", "phase"], "")


def _col_restarts(res):
    con_statuses = dget(res, ["res", "status", "containerStatuses"])
    if con_statuses:
        return max([
            dget(r, ["restartCount"], 0)
            for r in con_statuses
        ])
    else:
        return 0


def _col_ip(res):
    return dget(res, ["res", "status", "podIP"], "")


def _col_node(res):
    return dget(res, ["res", "spec", "nodeName"])


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "READY": _col_ready,
    "STATUS": _col_status,
    "RESTARTS": _col_restarts,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
    "IP": _col_ip,
    "NODE": _col_node
}
