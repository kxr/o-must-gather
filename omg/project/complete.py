from omg.must_gather.locate_yamls import locate_project
from omg.config import config
from omg.utils.dget import dget
from loguru import logger as lg


def complete_projects(ctx, args, incomplete):
    """
    Callback for project name autocompletion
    :return: List of matching namespace names or empty list.
    """
    lg.remove()

    def _get_all_projects():
        cfg = config.get()
        c_paths = dget(cfg, ["paths"])
        if c_paths:
            projects = []
            for path in c_paths:
                projects.extend(locate_project(path, tell="names"))
            return projects
        return []

    if incomplete is not None:
        projects = _get_all_projects()
        suggestions = [ns for ns in projects if ns.startswith(incomplete)]
        return suggestions
    return []
