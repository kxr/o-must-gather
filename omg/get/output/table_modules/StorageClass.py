# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_provisioner(res):
    return dget(res, ["res", "provisioner"])


def _col_reclaimpolicy(res):
    return dget(res, ["res", "reclaimPolicy"])


def _col_volumebindingmode(res):
    return dget(res, ["res", "volumeBindingMode"])


def _col_allowvolumeexpansion(res):
    return dget(res, ["res", "allowVolumeExpansion"], "false")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "PROVISIONER": _col_provisioner,
    "RECLAIMPOLICY": _col_reclaimpolicy,
    "VOLUMEBINDINGMODE": _col_volumebindingmode,
    "ALLOWVOLUMEEXPANSION": _col_allowvolumeexpansion,
    "AGE": None,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
