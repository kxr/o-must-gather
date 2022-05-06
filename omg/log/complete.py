from omg.config import config
from omg.utils.dget import dget
import os
from loguru import logger as lg


def complete_pods(ctx, args, incomplete):
    """
    Callback for pod name (within a ns) autocompletion
    :return: List of matching pod names or empty list.
    """
    lg.remove()
    cfg = config.get()
    c_paths = dget(cfg, ["paths"])
    c_project = dget(cfg, ["project"])

    ns = ctx.params.get("namespace") or c_project
    suggestions = []
    for path in c_paths:
        pod_dir = os.path.join(path, "namespaces", ns, "pods")
        if os.path.isdir(pod_dir):
            pod_listing = os.listdir(pod_dir)
            if pod_listing:
                suggestions.extend([pod for pod in pod_listing if incomplete in pod])
    return suggestions


def complete_containers(ctx, args, incomplete):
    """
    Callback for container name (within a pod and ns) autocompletion
    :return: List of matching container names or empty list
    """
    lg.remove()
    cfg = config.get()
    c_paths = dget(cfg, ["paths"])
    c_project = dget(cfg, ["project"])

    if (
        len(ctx.args) != 1
    ):
        # If there's no pod specified yet, can't autocomplete a container name
        return []

    ns = ctx.params.get("namespace") or c_project

    pod = ctx.args[0]

    container_listing = []
    for path in c_paths:
        container_dir = os.path.join(path, "namespaces", ns, "pods", pod)
        if os.path.isdir(container_dir):
            containers = os.listdir(container_dir)
            if containers:
                container_listing.extend(containers)

    suggestions = [
        c for c in container_listing if incomplete in c and not c.endswith(".yaml")
    ]  # skip .yaml files
    return suggestions
