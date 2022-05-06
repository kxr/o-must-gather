""" get_rdef.py

RDEFS is a built-in list of dictionaries containing resource definitions.
We also generate rdefs for crds in .rdefs.yaml in each must-gather path.

If an rdef is found in built-in RDEF, we don't have to lookup for
generated rdefs in .rdefs.yaml. Hence the more definitions we have in
built-in RDEFS the better (perfromance wise).

An rdef dict consists of the following keys:

    kind:       Case-sensitive "kind" that is found in the k8 object.
                This is matched when loading resource from the yaml.

    singular:   Singular name of the resource.

    plural:     Plural name of the resource.

    shortNames: (Optional) List of short names for the resource.

    scope:      Scope of the object ("Cluster" or "Namespaced").

    group:      API Group of the resource.

get_rdef() function finds, matches and returns the matching dict for
a specific resource type, searching built-in rdefs first.

"""

import os
from loguru import logger as lg

from omg.must_gather.RDEFS import RDEFS
from omg.utils.load_yaml import load_yaml
from omg.utils.dget import dget


def _match_rdef(r_type, rdef):
    if isinstance(r_type, str) and isinstance(rdef, dict):
        # kind = dget(rdef, ["kind"])
        singular = dget(rdef, ["singular"])
        plural = dget(rdef, ["plural"])
        group = dget(rdef, ["group"])
        shortNames = dget(rdef, ["shortNames"])

        if "." in r_type:
            r_type_kind = r_type.split(".")[0]
            r_type_group_list = r_type.split(".")[1:]
            r_def_group_list = group.split(".")
            if r_type_kind.lower() in [str(singular), str(plural)]:
                for rtgl in r_type_group_list:
                    if rtgl != r_def_group_list[r_type_group_list.index(rtgl)]:
                        return False
                return True
        else:
            if (
                r_type == singular or
                r_type == plural or
                (shortNames and r_type in shortNames)
            ):
                return True
    return False


def _find_rdef(r_type, rdefs):
    if rdefs:
        for rdef in rdefs:
            if _match_rdef(r_type, rdef):
                return rdef
    return None


def get_generated_rdefs():
    rdefs_f = os.path.join(os.getenv("HOME") or "/tmp/", ".omg.rdefs")

    try:
        if os.path.isfile(rdefs_f):
            rdefs_y = load_yaml(rdefs_f)
            if rdefs_y and type(rdefs_y) is list:
                return rdefs_y
    except FileNotFoundError:
        lg.warning("Unable to load rdefs file from {}".format(rdefs_f))

    return []


def get_rdef(r_type):
    """Find Resource Definition (rdef) for a resource type.

    Args:
        r_type (str): Resource type to lookup

    Returns:
        dict: rdef dictionary of the resource type
    """
    lg.debug("FUNC_INIT: {}".format(locals()))

    r_type = r_type.lower()

    # Lookup rdef in internal RDEFS
    rdef = _find_rdef(r_type, RDEFS)
    if rdef:
        lg.debug("rdef for {} found internally: {}".format(r_type, rdef))
        return rdef

    lg.debug("rdef for {} not found internally. Trying generated ones".format(
        r_type
    ))

    # Find rdefs from generated rdefs file

    rdef = _find_rdef(r_type, get_generated_rdefs())

    if rdef:
        lg.debug("rdef for {} found in generated rdef: {}".format(r_type, rdef))
        return rdef

    lg.debug("rdef for {} was not found!".format(r_type))
    return None
