# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_status(res):
    return dget(res, ["res", "status", "phase"], "")


def _col_volume(res):
    return dget(res, ["res", "spec", "volumeName"], "")


def _col_capacity(res):
    return dget(res, ["res", "status", "capacity", "storage"], "Unkown")


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


def _col_storageclass(res):
    return dget(res, ["res", "spec", "storageClassName"], "")


def _col_volumemode(res):
    return dget(res, ["res", "spec", "volumeMode"], "Unknow")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "STATUS": _col_status,
    "VOLUME": _col_volume,
    "CAPACITY": _col_capacity,
    "ACCESS MODES": _col_access_modes,
    "STORAGECLASS": _col_storageclass,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
    "VOLUMEMODE": _col_volumemode
}
