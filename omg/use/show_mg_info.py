import re
from loguru import logger as lg
from omg.config import config
from omg.must_gather.load_resources import load_res
from omg.must_gather.locate_yamls import locate_project
from omg.utils.dget import dget


def _hide_hash(path):
    """Hide the image hash in the path for better readability."""
    return re.sub("sha256-[a-z0-9]*", "sha256*", path)


def _show_info(path):

    out = lg.opt(colors=True).success

    proj_count = len(locate_project(path, "yamls"))
    out("            <e>Projects:</> {}".format(proj_count))

    try:
        infra = load_res(path, "infrastructure")
        if infra:
            api_url = [
                dget(i, ["res", "status", "apiServerURL"]) for i in infra
            ]
            platform = [
                dget(i, ["res", "status", "platform"]) for i in infra
            ]
            out("             <e>API URL:</> {}".format(api_url))
            out("            <e>Platform:</> {}".format(platform))

        c_ver = load_res(path, "clusterversion")
        if c_ver:
            cluster_id = [
                dget(cv, ["res", "spec", "clusterID"]) for cv in c_ver
            ]
            desired_v = [
                dget(cv, ["res", "status", "desired", "version"]) for cv in c_ver
            ]
            out("          <e>Cluster ID:</> {}".format(cluster_id))
            out("     <e>Desired Version:</> {}".format(desired_v))
        out("")
    except Exception as e:
        lg.warning("Error loading cluster info: {}".format(e))


def show_mg_info(cfile=None):
    """
    Shows the info of current selected must-gather(s)
    """
    lg.debug("FUNC_INIT: {}".format(locals()))

    cfg = config.get(cfile=cfile)
    lg.debug("Loaded config file: {}".format(cfg))

    paths = cfg["paths"]
    project = cfg["project"]

    out = lg.opt(colors=True).success

    if "cwd" in cfg and cfg["cwd"]:
        out("<e>-=[CWD Mode]=-</>")
        out("")

    if len(paths) > 1:
        out("<e>-=[MultiDir Mode]=-</>")
        out("")
        out("<e>Selected must-gather paths:</>")
        i = 1
        for path in paths:
            out(" <e>[{}]</> {}".format(i, _hide_hash(path)))
            i = i + 1
            _show_info(path)
        out("")
        out("<e>Current Project:</> {}".format(project))

    elif len(paths) == 1:
        out("<e>Selected must-gather:</> {}".format(_hide_hash(paths[0])))
        _show_info(paths[0])
        out("     <e>Current Project:</> {}".format(project))
