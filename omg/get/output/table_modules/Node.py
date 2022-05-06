# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_status(res):
    status = "Unknown"
    conds = dget(res, ["res", "status", "conditions"])
    if conds:
        for c in conds:
            if dget(c, ["type"]) == "Ready":
                if dget(c, ["status"]) == "True":
                    status = "Ready"
                elif dget(c, ["status"]) == "False":
                    status = "NotReady"

    if dget(res, ["res", "spec", "unschedulable"]):
        status += ",SchedulingDisabled"
    return status


def _col_roles(res):
    roles = []
    labels = dget(res, ["res", "metadata", "labels"])
    if labels:
        for label in labels:
            if label.startswith("node-role.kubernetes.io/"):
                roles.append(label.split("/")[1])
    return ",".join(roles)


def _col_version(res):
    return dget(
        res,
        ["res", "status", "nodeInfo", "kubeletVersion"],
        "Unknown"
    )


def _col_iip(res):
    iip = "<none>"
    addresses = dget(res, ["res", "status", "addresses"])
    if addresses:
        for adr in addresses:
            if dget(adr, ["type"]) == "InternalIP":
                iip = dget(adr, ["address"])
                break
    return iip


def _col_eip(res):
    eip = "<none>"
    addresses = dget(res, ["res", "status", "addresses"])
    if addresses:
        for adr in addresses:
            if dget(adr, ["type"]) == "ExternalIP":
                eip = dget(adr, ["address"])
                break
    return eip


def _col_osimg(res):
    return dget(
        res,
        ["res", "status", "nodeInfo", "osImage"],
        "Unknown"
    )


def _col_kerver(res):
    return dget(
        res,
        ["res", "status", "nodeInfo", "kernelVersion"],
        "Unknown"
    )


def _col_crt(res):
    return dget(
        res,
        ["res", "status", "nodeInfo", "containerRuntimeVersion"],
        "Unknown"
    )


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "STATUS": _col_status,
    "ROLES": _col_roles,
    "AGE": None,
    "VERSION": _col_version
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
    "INTERNAL-IP": _col_iip,
    "EXTERNAL-IP": _col_eip,
    "OS-IMAGE": _col_osimg,
    "KERNEL-VERSION": _col_kerver,
    "CONTAINER-RUNTIME": _col_crt,
}
