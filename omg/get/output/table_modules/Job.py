# -*- coding: utf-8 -*-
from omg.utils.dget import dget
from omg.utils.age import age


def _col_completions(res):
    return "{}/{}".format(
        dget(res, ["res", "status", "succeeded"], 0),
        dget(res, ["res", "spec", "completions"], 1)
    )


def _col_duration(res):
    st = dget(res, ["res", "status", "startTime"])
    ct = dget(res, ["res", "status", "completionTime"])
    if st and ct:
        return age(st, ct, ts1_type="iso", ts2_type="iso")
    else:
        return ""


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "COMPLETIONS": _col_completions,
    "DURATION": _col_duration,
    "AGE": None,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
