# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_ready(res):
    replicas = dget(res, ["res", "spec", "replicas"], "?")
    readyReplicas = dget(res, ["res", "status", "readyReplicas"], "0")
    return "{}/{}".format(readyReplicas, replicas)


def _col_uptodate(res):
    return dget(res, ["res", "status", "updatedReplicas"], "0")


def _col_available(res):
    return dget(res, ["res", "status", "availableReplicas"], "0")


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


def _col_selector(res):
    labels = dget(res, ["res", "spec", "selector", "matchLabels"])
    selector = []
    for k, v in labels.items():
        selector.append("{}={}".format(k, v))
    return ",".join(selector)


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "READY": _col_ready,
    "UP-TO-DATE": _col_uptodate,
    "AVAILABLE": _col_available,
    "AGE": None,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
    "CONTAINERS": _col_containers,
    "IMAGES": _col_images,
    "SELECTOR": _col_selector
}
