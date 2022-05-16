# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_type(res):
    return dget(res, ["res", "spec", "type"], "Unkown")


def _col_cluster_ip(res):
    return dget(res, ["res", "spec", "clusterIP"], "")


def _col_external_ip(res):
    en = dget(res, ["res", "spec", "externalName"])
    if en:
        return en
    ei = dget(res, ["res", "spec", "externalIP"])
    if ei:
        return ei
    return "<none>"


def _col_ports(res):
    return ",".join(
        "{}/{}".format(p["port"], p["protocol"])
        for p in dget(res, ["res", "spec", "ports"], [])
    )


def _col_selector(res):
    labels = dget(res, ["res", "spec", "selector"], {})
    selector = []
    for k, v in labels.items():
        selector.append("{}={}".format(k, v))
    return ",".join(selector) or "<none>"


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "TYPE": _col_type,
    "CLUSTER-IP": _col_cluster_ip,
    "EXTERNAL-IP": _col_external_ip,
    "PORT(S)": _col_ports,
    "AGE": None,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
    "SELECTOR": _col_selector
}
