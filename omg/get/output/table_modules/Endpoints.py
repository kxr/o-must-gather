# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_endpoints(res):
    endpoints = [
        "{}:{}".format(
            dget(addr, ["ip"]),
            dget(port, ["port"])
        )
        for subset in dget(res, ["res", "subsets"], [])
        for addr in dget(subset, ["addresses"], [])
        for port in dget(subset, ["ports"], [])
    ]
    ep_string = ""
    while len(endpoints) > 0:
        ep = endpoints.pop()
        if len(ep_string) + len(ep) <= 40:
            if ep_string:
                ep_string = ",".join([ep_string, ep])
            else:
                ep_string = ep
        else:
            ep_string = "{} + {} more...".format(
                ep_string,
                len(endpoints) + 1
            )
            break
    return ep_string


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "ENDPOINTS": _col_endpoints,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
