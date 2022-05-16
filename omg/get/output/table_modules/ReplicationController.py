# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_desired(res):
    return dget(res, ["res", "status", "replicas"], "0")


def _col_current(res):
    return dget(res, ["res", "status", "fullyLabeledReplicas"], "0")


def _col_ready(res):
    return dget(res, ["res", "status", "readyReplicas"], "0")


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
    "DESIRED": _col_desired,
    "CURRENT": _col_current,
    "READY": _col_ready,
    "AGE": None,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
    "CONTAINERS": _col_containers,
    "IMAGES": _col_images,
    "SELECTOR": _col_selector
}
