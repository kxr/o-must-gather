# -*- coding: utf-8 -*-
from omg.utils.dget import dget
from omg.utils.age import age


def _col_schedule(res):
    return dget(res, ["res", "spec", "schedule"])


def _col_suspend(res):
    return dget(res, ["res", "spec", "suspend"])


def _col_active(res):
    return len(dget(res, ["res", "status", "active"], []))


def _col_last_schedule(res):
    last_sched = dget(res, ["res", "status", "lastScheduleTime"])
    if last_sched:
        return age(
            last_sched,
            dget(res, ["yfile_ts"])
        )
    return ""


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "SCHEDULE": _col_schedule,
    "SUSPEND": _col_suspend,
    "ACTIVE": _col_active,
    "LAST SCHEDULE": _col_last_schedule,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
