from loguru import logger as lg
from omg.config import config
from omg.utils.dget import dget
from omg.must_gather.locate_yamls import locate_project


def cmd(name):
    cfg = config.get()
    c_paths = dget(cfg, ["paths"])
    c_project = dget(cfg, ["project"])

    # print current project
    if name is None:
        if c_project is None:
            print("No project selected")
        else:
            print("Using project {}".format(c_project))
    # set current project
    else:
        if name == c_project:
            print("Already using project {}".format(c_project))
        else:
            select_project = None
            for path in c_paths:
                projs_in_path = locate_project(path, tell="names")
                if name in projs_in_path:
                    select_project = name
                    break
            if select_project:
                print("Now using project {}".format(select_project))
                config.save(project=name)
            else:
                lg.error("Project {} not found in {} must-gather paths".format(
                    name, len(c_paths)))
