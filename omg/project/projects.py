from loguru import logger as lg
from omg.config import config
from omg.utils.dget import dget
from omg.must_gather.locate_yamls import locate_project


def cmd():
    lg.debug("FUNC_INIT: {}".format(locals()))

    cfg = config.get()
    c_paths = dget(cfg, ["paths"])
    c_project = dget(cfg, ["project"])

    if c_paths:
        for path in c_paths:
            projs_in_path = locate_project(path, tell="names")
            print("{} projects in {}".format(
                len(projs_in_path), path))
        print("")
        print("Selected project: {}".format(c_project))
