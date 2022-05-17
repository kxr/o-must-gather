# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_revision(res):
    return dget(res, ["res", "status", "latestVersion"])


def _col_desired(res):
    return dget(res, ["res", "spec", "replicas"])


def _col_current(res):
    return dget(res, ["res", "status", "readyReplicas"])


def _col_triggered_by(res):
    triggers = dget(res, ["res", "spec", "triggers"], [])
    trig_list = []
    for trig in triggers:
        if trig["type"] == "ConfigChange":
            trig_list.append("config")
        elif trig["type"] == "ImageChange":
            img = dget(trig, ["imageChangeParams", "from", "name"])
            trig_list.append("image({})".format(img))
        else:
            trig_list.append(str(trig["type"]))
    return ",".join(trig_list)


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "REVISION": _col_revision,
    "DESIRED": _col_desired,
    "CURRENT": _col_current,
    "TRIGGERED BY": _col_triggered_by,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
