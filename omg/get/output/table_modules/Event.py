# -*- coding: utf-8 -*-
from omg.utils.dget import dget
from omg.utils.age import age


def _col_last_seen(res):
    return age(
        dget(res, ["res", "lastTimestamp"]),
        dget(res, ["yfile_ts"])
    )


def _col_type(res):
    return dget(res, ["res", "type"])


def _col_reason(res):
    return dget(res, ["res", "reason"])


def _col_object(res):
    obj = "{}/{}".format(
        dget(res, ["res", "involvedObject", "kind"], ""),
        dget(res, ["res", "involvedObject", "name"], "")
    )
    if obj == "/":
        return "<none>"
    else:
        return obj


def _col_message(res):
    return dget(res, ["res", "message"], "<none>")


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "LAST SEEN": _col_last_seen,
    "TYPE": _col_type,
    "REASON": _col_reason,
    "OBJECT": _col_object,
    "MESSAGE": _col_message
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
