# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_netid(res):
    return dget(res, ["res", "netid"])


def _col_egress_ips(res):
    return dget(res, ["res", "egressIPs"])


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "NETID": _col_netid,
    "EGRESS IPS": _col_egress_ips
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
