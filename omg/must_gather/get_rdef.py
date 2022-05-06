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
            # print(r_type_group_list)
            r_def_group_list = group.split(".")
            # print(r_def_group_list)
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


def get_rdefs_from_path(path):
    lg.debug("FUNC_INIT: {}".format(locals()))

    # Lookup rdef in must-gather's .rdef.yaml
    rdef_file = os.path.join(path, ".rdefs.yaml")

    lg.debug("rdef_file: {}".format(rdef_file))

    # This block will generate if rdef file is missing (e.g, cwd mode)
    # If the generation fails (e.g, mg dir not writable), it will generate
    # a rdef file in /tmp and use that
    if not os.path.isfile(rdef_file):
        from omg.must_gather.generate_rdefs import generate_rdefs
        from omg.must_gather.exceptions import FailedGeneratingRdefFile
        try:
            generate_rdefs(path)
        except FailedGeneratingRdefFile as e:
            lg.warning(
                "Failed generating rdef file: {} Reason: {}".format(rdef_file, e))
            lg.warning("Generating temporary rdef file in /tmp")
            generate_rdefs(path, dest="/tmp")
            rdef_file = "/tmp/.rdefs.yaml"

    rdefs_y = []
    try:
        if os.path.isfile(rdef_file):
            rdefs_y = load_yaml(rdef_file)
    except FileNotFoundError:
        lg.warning("Unable to load .rdefs file from {}".format(path))
        return []
    else:
        return rdefs_y


def get_rdef(r_type, path):
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

    # Find rdefs from generated rdefs in path
    rdefs_y = get_rdefs_from_path(path)
    rdef = _find_rdef(r_type, rdefs_y)

    if rdef:
        lg.debug("rdef for {} found in generated rdef: {}".format(r_type, rdef))
        return rdef

    lg.debug("rdef for {} was not found!".format(r_type))
    return None
