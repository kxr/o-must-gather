# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_desired(res):
    return dget(res, ["res", "status", "desiredNumberScheduled"])


def _col_current(res):
    return dget(res, ["res", "status", "currentNumberScheduled"])


def _col_ready(res):
    return dget(res, ["res", "status", "numberReady"])


def _col_uptodate(res):
    return dget(res, ["res", "status", "updatedNumberScheduled"], "0")


def _col_available(res):
    return dget(res, ["res", "status", "numberAvailable"], "0")


def _col_node_selector(res):
    nselector = dget(res, ["res", "spec", "template", "spec", "nodeSelector"], {})
    selector = []
    for k, v in nselector.items():
        selector.append("{}={}".format(k, v))
    if selector:
        return ",".join(selector)
    else:
        return ""


def _col_containers(res):
    conts = [c["name"] for c in dget(res, ["res", "spec", "template", "spec", "containers"])]
    if conts:
        return ",".join(conts)
    return ""


def _col_images(res):
    images = [c["image"] for c in dget(res, ["res", "spec", "template", "spec", "containers"])]
    if images:
        return ",".join(images)
    return ""


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "DESIRED": _col_desired,
    "CURRENT": _col_current,
    "READY": _col_ready,
    "UP-TO-DATE": _col_uptodate,
    "AVAILABLE": _col_available,
    "NODE SELECTOR": _col_node_selector,
    "AGE": None,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
    "CONTAINERS": _col_containers,
    "IMAGES": _col_images,
}
