""" load_resources.py """

from os.path import getmtime
from loguru import logger as lg

from omg.must_gather.locate_yamls import locate_yamls
from omg.must_gather.exceptions import InvalidResource
from omg.utils.load_yaml import load_yaml
from omg.utils.dget import dget


def _is_valid_k8_res(res):
    if isinstance(res, dict):
        if dget(res, ["metadata"]) or dget(res, ["items"]):
            return True
    return False


def load_res_from_yaml(yfile, rdef=None):
    """Load k8 resources from a single yaml file

    The yaml file is expected to be a dict when loaded with yaml.load

    Args:
        yfile (str): Path to a yaml file.

        rdef (dict, optional): If a yaml file has multiple kind=xx resources,
                              this can be used to filter a specific one.
                              Generally must-gather, yamls only have one type
                              per file, this is just as a precaution.
    Return:
        list[dict]: list of dictionary [ {'res': <>, 'yfile_ts': <>, rdef}, ...]
                        res:       k8 resource
                        yfile_ts:   timestamp of the yaml file from
                                    which the resource was loaded
                                    (used for age calculation)
                        rdef:       resrouce definition of the resource
    """
    lg.debug("FUNC_INIT: {}".format(locals()))

    ydata = load_yaml(yfile)

    if not _is_valid_k8_res(ydata):
        raise InvalidResource(
            "Resource loaded from {} is not valid".format(yfile))

    lg.debug("ydata.keys(): {}".format(ydata.keys()))

    yfile_ts = getmtime(yfile)
    lg.debug("Yaml file's timestamp: {}".format(yfile_ts))

    kind = dget(rdef, ["kind"])

    res = []
    # List in yaml (kind: List)
    if "items" in ydata:
        lg.debug("'items' in ydata (we got a list)")
        lg.debug("len of items: {}".format(len(ydata["items"] or [])))

        if ydata["items"] is not None and len(ydata["items"]) > 0:
            res.extend(
                [
                    {"res": r, "yfile_ts": yfile_ts, "rdef": rdef}
                    for r in ydata["items"]
                    if kind is None or ("kind" in r and r["kind"] == kind)
                ])
        # else:
        #     lg.warning("No items in yaml file {}, skipping".format(yfile))

    # Single resource in yaml
    elif "metadata" in ydata:

        lg.debug("'metadata' in ydata (we got a single item)")
        lg.debug("ydata.keys(): {}".format(ydata.keys()))

        if kind is None or ("kind" in ydata and ydata["kind"] == kind):
            res.extend([{"res": ydata, "yfile_ts": yfile_ts, "rdef": rdef}])
        else:
            lg.warning("Yaml file {} didnt contain kind {}".format(yfile, kind))
    else:
        raise InvalidResource(
            "Invalid yaml file {}. Didn't get 'items' or 'metadata'".format(yfile))

    lg.debug("resources loaded length: {}".format(len(res)))
    lg.trace("res: {}".format(res))

    return res


def load_res(path, r_type, r_name=None, ns=None):
    """Load specific resource type from a must-gather path

    This function first calls locate yamls to locate the yamls of the
    r_type object. Then it calls load_res_from_yaml to load the
    k8 resources from these yamls. Finally it filters for r_name if is
    not None, and returns the array.

    Args:
        path (str): Absolute must-gather path

        r_type (str): Resource type e.g, pod, node.

        r_name (list[str], optional): Resource names to filter.
                                      All names are returned if None (Default).

        ns (str): Namespace if the the object is namespace scoped.
                  If the r_type is ns-scoped but ns is None, we use Config().project
                  '_all' would mean all namespaces.
                  Ignored for cluster scoped resource types.

    Returns:
        list[dict]: list of dictionary [ {'res': <>, 'yfile_ts': <>, rdef}, ...]
                        res:       k8 resource
                        yfile_ts:   timestamp of the yaml file from
                                    which the resource was loaded
                                    (used for age calculation)
                        rdef:       resrouce definition of the resource
    """
    lg.debug("FUNC_INIT: {}".format(locals()))

    rdef, yamls = locate_yamls(path, r_type, ns=ns)

    lg.debug("Found {} yamls".format(len(yamls)))

    # Load resources from these yamls and save in res
    # after filtering names if r_name is set
    res = []

    # total counters
    t_matched = 0
    t_not_matched = 0

    for y in yamls:

        # per yaml counters
        matched = 0
        not_matched = 0

        # Handling Partial namespace directory with missing yaml
        if (
                dget(rdef, ["kind"]) == "Namespace"
                and type(y) is dict
                and dget(y, ["yaml_missing"])
           ):
            ns_name = dget(y, ["yaml_missing"])
            res_yd = [{
                "res": {
                    "apiVersion": "v1",
                    "kind": "Namespace",
                    "metadata": {
                        "name": ns_name
                    }
                }
            }]
        else:
            try:
                res_yd = load_res_from_yaml(y, rdef)
            except InvalidResource as e:
                lg.warning(e)
                continue

        if not r_name:
            # res name is not set, get all from yaml
            lg.debug("Matching all resource names")
            matched += len(res_yd)
            t_matched += matched
            res.extend(res_yd)
        else:
            # res name is set, filter name from yaml
            lg.debug("Matching resources with name: {}".format(r_name))
            for r in res_yd:
                if (
                    "res" in r
                    and "metadata" in r["res"]
                    and "name" in r["res"]["metadata"]
                    and r["res"]["metadata"]["name"] in r_name
                ):
                    matched += 1
                    res.append(r)
                else:
                    not_matched += 1
            t_matched += matched
            t_not_matched += not_matched

        lg.info("{}/{} from yaml file: {}".format(matched, matched+not_matched, y))

    return res
