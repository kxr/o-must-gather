# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_attachrequired(res):
    return dget(res, ["res", "spec", "attachRequired"], "Unknown")


def _col_podinfoonmount(res):
    return dget(res, ["res", "spec", "podInfoOnMount"], "Unknown")


def _col_modes(res):
    return ",".join(dget(res, ["res", "spec", "volumeLifecycleModes"], []))


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "ATTACHREQUIRED": _col_attachrequired,
    "PODINFOONMOUNT": _col_podinfoonmount,
    "MODES": _col_modes,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
