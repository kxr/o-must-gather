# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_config(res):
    return dget(res, ["res", "spec", "configuration", "name"], "")


def _col_updated(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        updated = [c["status"] for c in conds if c["type"] == "Updated"]
        if updated:
            return updated[0]
    return "Unknown"


def _col_updating(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        updating = [c["status"] for c in conds if c["type"] == "Updating"]
        if updating:
            return updating[0]
    return "Unknown"


def _col_degraded(res):
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        degraded = [c["status"] for c in conds if c["type"] == "Degraded"]
        if degraded:
            return degraded[0]
    return "Unknown"


def _col_machinecount(res):
    return dget(res, ["res", "status", "machineCount"], "Unknown")


def _col_readymachinecount(res):
    return dget(res, ["res", "status", "readyMachineCount"], "Unknown")


def _col_updatedmachinecount(res):
    return dget(res, ["res", "status", "updatedMachineCount"], "Unknown")


def _col_degradedmachinecount(res):
    return dget(res, ["res", "status", "degradedMachineCount"], "Unknown")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "CONFIG": _col_config,
    "UPDATED": _col_updated,
    "UPDATING": _col_updating,
    "DEGRADED": _col_degraded,
    "MACHINECOUNT": _col_machinecount,
    "READYMACHINECOUNT": _col_readymachinecount,
    "UPDATEDMACHINECOUNT": _col_updatedmachinecount,
    "DEGRADEDMACHINECOUNT": _col_degradedmachinecount,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
