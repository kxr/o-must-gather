# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_generatedbycontroller(res):
    return dget(res, [
        "res", "metadata", "annotations",
        "machineconfiguration.openshift.io/generated-by-controller-version"],
        "")


def _col_ignitionversion(res):
    return dget(res, ["res", "spec", "config", "ignition", "version"], "Unknown")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "GENERATEDBYCONTROLLER": _col_generatedbycontroller,
    "IGNITIONVERSION": _col_ignitionversion,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
