# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_host(res):
    return dget(res, ["res", "host"])


def _col_ip(res):
    return dget(res, ["res", "hostIP"])


def _col_subnet(res):
    return dget(res, ["res", "subnet"])


def _col_cidrs(res):
    return dget(res, ["res", "egressCIDRs"])


def _col_egress_ips(res):
    return dget(res, ["res", "egressIPs"])


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "HOST": _col_host,
    "HOST IP": _col_ip,
    "SUBNET": _col_subnet,
    "EGRESS CIDRS": _col_cidrs,
    "EGRESS IPS": _col_egress_ips,
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
