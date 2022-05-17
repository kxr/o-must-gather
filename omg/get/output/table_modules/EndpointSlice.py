# -*- coding: utf-8 -*-
from omg.utils.dget import dget


def _col_addresstype(res):
    return dget(res, ["res", "addressType"])


def _col_ports(res):
    ports = [
        str(dget(p, ["port"]))
        for p in dget(res, ["res", "ports"]) or []
    ]
    port_string = ""
    if ports:
        while len(ports) > 0:
            port = ports.pop()
            if len(port_string) + len(port) <= 30:
                if port_string:
                    port_string = ",".join([port_string, port])
                else:
                    port_string = port
            else:
                port_string = "{} + {} more...".format(
                    port_string,
                    len(ports) + 1
                )
        return port_string
    return "<none>"


def _col_endpoints(res):
    addresses = [
        addr
        for ep in dget(res, ["res", "endpoints"]) or []
        for addr in dget(ep, ["addresses"]) or []
    ]
    ep_string = ""
    if addresses:
        while len(addresses) > 0:
            ep = addresses.pop()
            if len(ep_string) + len(ep) <= 30:
                if ep_string:
                    ep_string = ",".join([ep_string, ep])
                else:
                    ep_string = ep
            else:
                ep_string = "{} + {} more...".format(
                    ep_string,
                    len(addresses) + 1
                )
                break
    return ep_string


# Default columns (without -o wide)
# NAME and AGE cols, if present, with None value,
# will be handled by build_table function that will
# fill them with the common name/age column functions
DEFAULT_COLUMNS = {
    "NAME": None,
    "ADDRESSTYPE": _col_addresstype,
    "PORTS": _col_ports,
    "ENDPOINTS": _col_endpoints,
    "AGE": None
}

# Wide columns (with -o wide)
# In addition to the default columns
WIDE_COLUMNS = {
}
