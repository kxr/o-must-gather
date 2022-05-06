""" config.py """

import yaml
from os import path, getenv
from loguru import logger as lg
from omg.utils.dget import dget
from omg.must_gather.scan_mg import scan_mg, NoValidMgFound

_default_cfile = path.join(getenv("HOME") or "", ".omgconfig")

# -p, --path
filtered_path = 0

# -n, --namespace
namespace = None

# -A, --all-namespaces
all_namespaces = False


class NoMgSelected(Exception):
    """
    Error raised when no must-gather is selected
    """
    pass


class InvalidConfig(Exception):
    """
    Error raised when config is invalid
    """
    pass


def _load_config(cfile):
    """Load config from file.

    If file doesn't exist MgConfigNotFound is raised.

    Args:
        cfile (str): Config file

    Returns:
        dict: Config dict
    """
    lg.debug("FUNC_INIT: {}".format(locals()))

    if not cfile:
        cfile = _default_cfile

    config = {"paths": None, "project": None}

    if path.isfile(cfile):
        try:
            with open(cfile, "r") as c_f:
                lg.debug("Loading config from: {}".format(cfile))
                lconf = yaml.safe_load(c_f)
                lg.debug("Loaded config from file: {}".format(lconf))

            config["paths"] = dget(lconf, ["paths"], None)
            config["project"] = dget(lconf, ["project"], None)
        except Exception as e:
            raise InvalidConfig(e)

    if not dget(config, ["paths"], None):
        raise NoMgSelected("Please select a must-gather (omg use </path/to/must-gather>)")

    return config


def _dump_config(config, cfile):
    """Dump config to file

    Args:
        config (dict): Config dict
        cfile (str): Config file
    """
    if not cfile:
        cfile = _default_cfile
    try:
        with open(cfile, "w") as c_f:
            yaml.dump(config, c_f, default_flow_style=False)
            lg.debug("Config dumped to {}".format(cfile))
    except Exception as e:
        lg.error(e)
        raise SystemExit(1)


def get(cfile=None):
    """Get config from file.

    Args:
        cfile (str, optional): Config file. Defaults to None.

    Raises:
        SystemExit: If paths is not found in config file

    Returns:
        dict: Config dict
    """
    if not cfile:
        env_config = getenv("OMGCONFIG")
        if env_config:
            cfile = env_config
        else:
            cfile = _default_cfile

    try:
        config = _load_config(cfile)
    except NoMgSelected as e:
        lg.error(e)
        raise SystemExit(1)

    if config["paths"] == ["."]:
        try:
            v_mgs = scan_mg(["."])
            config["paths"] = v_mgs
            config["cwd"] = True
        except NoValidMgFound as e:
            lg.error(e)
            raise SystemExit(1)

    if filtered_path:
        config["paths"] = [config["paths"][filtered_path - 1]]

    if namespace:
        config["project"] = namespace

    if all_namespaces:
        config["project"] = "_all"

    return config


def save(paths=None, project=None, cfile=None):
    """Save config to file

    Args:
        paths (list[str], optional): Must-gather paths. Defaults to None.
        project ([type], optional): Project. Defaults to None.
        cfile ([type], optional): Config file. Defaults to None.
    """

    try:
        config = _load_config(cfile)
    except (NoMgSelected, InvalidConfig):
        c_paths = None
        c_project = None
    else:
        c_paths = dget(config, ["paths"])
        c_project = dget(config, ["project"])

    if paths:
        save_paths = paths
    else:
        save_paths = c_paths

    if project:
        save_project = project
    else:
        save_project = c_project

    _dump_config(
        {"paths": save_paths, "project": save_project}, cfile)
