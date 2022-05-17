from loguru import logger as lg

from omg.config import config
from omg.utils.dget import dget
from omg.must_gather.load_resources import load_res
from omg.must_gather.exceptions import NameSpaceRequired, UnkownResourceType


def get_all_resources(parsed_objects, ns=None):
    """Get resources from all paths

    Args:
        parsed_objects (dict): Parsed object
        ns (string): Namespace/project

    Returns:
        list:   for each r_type, list of resources from each path
                (list of dict of list)
                For example:
                    [
                        # resources_from_path1
                        {   'pod': [ res1, res2 ... ],
                            'svc': [ res1, ... ],
                            ...
                        },
                        # resources_from_path2
                        ...
                    ]
    """
    lg.debug("FUNC_INIT: {}".format(locals()))

    cfg = config.get()
    paths = cfg["paths"]

    # Resources dicts from selected paths
    # resd_from_paths = []
    resd_from_paths = {}

    i = 0
    for path in paths:
        i += 1
        resd = {}
        for r_type in parsed_objects:
            r_names = parsed_objects[r_type]

            try:
                res = load_res(path, r_type, r_names, ns)
            except NameSpaceRequired as e:
                lg.error(e)
                raise SystemExit(1)
            except UnkownResourceType:
                lg.error("Unknow resource type: {}".format(r_type))
                raise SystemExit(1)
            else:
                resd[r_type] = res
        # resd_from_paths.append(resd)
        resd_from_paths[i] = resd
    return resd_from_paths


def get_all_resource_names(parsed_objects, ns=None):

    resd_from_paths = get_all_resources(parsed_objects, ns)

    all_names = []
    for i, path_resd in resd_from_paths.items():
        for r_type in path_resd:
            res = path_resd[r_type]
            if res:
                for r in res:
                    name = dget(r, ["res", "metadata", "name"])
                    if name:
                        all_names.append(name)
    return all_names
