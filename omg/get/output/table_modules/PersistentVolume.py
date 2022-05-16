# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_capacity(res):
    return dget(res, ["res", "spec", "capacity", "storage"])


def _col_access_modes(res):
    am = dget(res, ["res", "spec", "accessModes"], [])
    return ",".join([
        a
        .replace("Read", "R")
        .replace("Write", "W")
        .replace("Many", "X")
        .replace("Once", "O")
        for a in am
    ])


def _col_reclaim_policy(res):
    return dget(res, ["res", "spec", "persistentVolumeReclaimPolicy"], "Unknown")


def _col_status(res):
    return dget(res, ["res", "status", "phase"], "")


def _col_claim(res):
    claim = "{}/{}".format(
        dget(res, ["res", "spec", "claimRef", "namespace"], ""),
        dget(res, ["res", "spec", "claimRef", "name"], "")
    )
    if claim == "/":
        return ""
    else:
        return claim


def _col_storageclass(res):
    return dget(res, ["res", "spec", "storageClassName"], "")


def _col_reason(res):
    return dget(res, ["res", "status", "reason"], "")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "CAPACITY": _col_capacity,
    "ACCESS MODES": _col_access_modes,
    "RECLAIM POLICY": _col_reclaim_policy,
    "STATUS": _col_status,
    "CLAIM": _col_claim,
    "STORAGECLASS": _col_storageclass,
    "REASON": _col_reason,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
