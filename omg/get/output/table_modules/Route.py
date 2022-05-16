# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_host_port(res):
    return dget(res, ["res", "spec", "host"])


def _col_path(res):
    return dget(res, ["res", "spec", "path"])


def _col_services(res):
    return dget(res, ["res", "spec", "to", "name"])


def _col_port(res):
    return dget(res, ["res", "spec", "port", "targetPort"], "<all>")


def _col_termination(res):
    return "/".join([
        dget(res, ["res", "spec", "tls", "termination"], ""),
        dget(res, ["res", "spec", "tls", "insecureEdgeTerminationPolicy"], "")
    ])


def _col_wildcard(res):
    return dget(res, ["res", "spec", "wildcardPolicy"])


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "HOST/PORT": _col_host_port,
    "PATH": _col_path,
    "SERVICES": _col_services,
    "PORT": _col_port,
    "TERMINATION": _col_termination,
    "WILDCARD": _col_wildcard,
    "AGE": None,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
