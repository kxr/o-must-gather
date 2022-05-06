# -*- coding: utf-8 -*-
from omg.utils.dget import dget
from omg.utils.age import age


def _col_type(res):
    return dget(res, ["res", "spec", "strategy", "type"], "Unknown")


def _col_from(res):
    return dget(res, ["res", "spec", "source", "type"], "Unknown")


def _col_status(res):
    return dget(res, ["res", "status", "phase"], "Unknown")


def _col_started(res):
    stt = dget(res, ["res", "status", "startTimestamp"])
    if stt:
        yfile_ts = dget(res, ["yfile_ts"])
        return age(stt, yfile_ts)


def _col_duration(res):
    dur = dget(res, ["res", "status", "duration"])
    if dur:
        return str(int(dur/1000000000)) + "s"


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "TYPE": _col_type,
    "FROM": _col_from,
    "STATUS": _col_status,
    "STARTED": _col_started,
    "DURATION": _col_duration
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
