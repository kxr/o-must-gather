# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_reference(res):
    return "{}/{}".format(
        dget(res, ["res", "spec", "scaleTargetRef", "kind"], ""),
        dget(res, ["res", "spec", "scaleTargetRef", "name"], "")
    )


def _col_targets(res):
    return "{}%/{}%".format(
        dget(res, ["res", "status", "currentCPUUtilizationPercentage"], "Unknown"),
        dget(res, ["res", "spec", "targetCPUUtilizationPercentage"], "Unkown")
    )


def _col_minpods(res):
    return dget(res, ["res", "spec", "minReplicas"])


def _col_maxpods(res):
    return dget(res, ["res", "spec", "maxReplicas"])


def _col_replicas(res):
    return dget(res, ["res", "status", "currentReplicas"])


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "REFERENCE": _col_reference,
    "TARGETS": _col_targets,
    "MINPODS": _col_minpods,
    "MAXPODS": _col_maxpods,
    "REPLICAS": _col_replicas,
    "AGE": None,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
