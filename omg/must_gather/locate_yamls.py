""" locate_yamls.py

This module helps in locating yaml files as we expect them to be
in a must-gather. We don't look whats inside. Simply return the
paths to relevant yaml files for a specific resource type.

The main function is locate_yamls. It uses locate_project if
resource type is project.

yaml files are located calculated as per following pattern:

    <must-gather>/
        [namespaces|cluster-scoped-resources]/
            group/
                [plural.yaml | plural/*.yaml]

_detect_yamls "detects" if plural.yaml is present or plural/*.yaml
"""

from os.path import join, isdir, isfile
from os import listdir
from loguru import logger as lg
from omg.must_gather.get_rdef import get_rdef
from omg.must_gather.exceptions import UnkownResourceType, NameSpaceRequired


def _detect_yamls(path, plural):
    """Detects if yaml file(s) are present as plural.yaml or plural/*.yaml.

    First priority is given to plural.yaml and if its not present,
    plural/*.yaml files are scanned. TODO: Ensure this order is correct

    Args:
        path (str): Path where yaml needs to be detected
        plural (str): Plural name of the resrouce we are detecting

    Returns:
        list[str]: List of yaml paths that were detected
                   Returns None if none were detected
    """
    lg.debug("FUNC_INIT: {}".format(locals()))
    # potential yaml file
    pot_y = join(path, plural+".yaml")
    # potential yaml dir
    pot_d = join(path, plural)
    if isfile(pot_y):
        lg.debug("detected yaml file: {}".format(pot_y))
        return [pot_y]
    if isdir(pot_d):
        lg.debug("detected yaml dir {}".format(pot_d))
        y_in_d = [join(pot_d, y) for y in listdir(pot_d) if y.endswith(".yaml")]
        lg.debug("{} yamls found".format(len(y_in_d)))
        lg.trace("yamls_in_dir: {}".format(y_in_d))
        return y_in_d
    return None


def locate_project(path, tell):
    """Special function to locate project yamls

    project yamls are present in must-gather/namespaces/<ns-name>/<ns-name>.yaml,
    unlike for other res_types, project type needs separate/special function to
    locate the yamls.

    This function can return yamls, paths or just the project names. depending on
    what is asked in arg tell=""

    Args:
        path (str)): Absolute must-gather path

        tell (str): What to tell/return? Possible options are:
                        "yamls": yaml files of the projects
                        "paths": paths of project directories
                        "names": names of the projects present

    Returns:
        list: List of requested item (yamls/paths/names)
    """
    lg.debug("FUNC_INIT: {}".format(locals()))
    result = []
    lg.debug("Looking for projects in {}".format(path))
    p_nss = join(path, "namespaces")
    if isdir(p_nss):
        lg.debug("Found namspaces in {}".format(path))
        for proj in listdir(p_nss):
            p_nss_proj = join(p_nss, proj)
            if isdir(p_nss_proj):
                if tell == "names" and proj not in result:
                    if proj not in result:
                        result.append(proj)
                elif tell == "paths":
                    result.append(p_nss_proj)
                elif tell == "yamls":
                    p_nss_proj_y = join(p_nss_proj, proj+".yaml")
                    if isfile(p_nss_proj_y):
                        result.append(p_nss_proj_y)
                    else:
                        # ns dir exists but yaml is missing
                        # we will append a special dict with ns name
                        # instead of the path of the yaml
                        result.append({"yaml_missing": proj})
                else:
                    raise ValueError("Invalid arg(tell): {}".format(tell))
    lg.trace("result: {}".format(result))
    return result


def locate_yamls(path, r_type, ns=None):
    """Find yaml for a particular resource type in paths.

    Args:
        path (str): Absolute must-gather path

        r_type (str): Resource type e.g, pod, node.

        ns (str): Namespace. Required if r_type is namespace scoped.
                  Value of '_all' denotes all namespaces.
                  Ignored for cluster scoped resource types.

    Returns:
        dict, list: rdef and List of paths of yamls located in paths.
    """
    lg.debug("FUNC_INIT: {}".format(locals()))

    yaml_paths = []

    # r_type == project | namespace
    if r_type.lower() in ["project", "projects", "namespace", "ns"]:
        yaml_paths = locate_project(path, "yamls")
        rdef = {
            "kind": "Namespace",
            "group": "core",
            "singular": "namespace",
            "plugral": "namespaces"
        }
    # r_type != project
    else:
        rdef = get_rdef(r_type)
        if not rdef:
            raise UnkownResourceType("Unknown resource type: {}".format(r_type))

        lg.debug("rdef: {}".format(rdef))
        # kind = rdef["kind"]
        plural = rdef["plural"]
        group = rdef["group"]
        scope = rdef["scope"]

        if scope == "Namespaced":
            if not ns:
                raise NameSpaceRequired(
                    "{} is Namespaced but ns/project is not set".format(r_type))
            if ns == "_all":  # all namespaces
                all_proj_paths = locate_project(path, tell="paths")
                for app in all_proj_paths:
                    ymls = _detect_yamls(join(app, group), plural)
                    if ymls:
                        yaml_paths.extend(ymls)
            else:  # specific ns
                ymls = _detect_yamls(join(path, "namespaces", ns, group), plural)
                if ymls:
                    yaml_paths.extend(ymls)
        else:
            # scope == "Cluster"
            ymls = _detect_yamls(join(path, "cluster-scoped-resources", group), plural)
            if ymls:
                yaml_paths.extend(ymls)
    lg.trace("rdef: {}, yaml_paths: {}".format(rdef, yaml_paths))
    return rdef, yaml_paths
