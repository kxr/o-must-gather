# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_phase(res):
    return dget(res, ["res", "status", "phase"], "")


def _col_type(res):
    return dget(res, ["res", "metadata", "labels", "machine.openshift.io/instance-type"], "")


def _col_region(res):
    return dget(res, ["res", "metadata", "labels", "machine.openshift.io/region"], "")


def _col_zone(res):
    return dget(res, ["res", "metadata", "labels", "machine.openshift.io/zone"], "")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "PHASE": _col_phase,
    "TYPE": _col_type,
    "REGION": _col_region,
    "ZONE": _col_zone,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
