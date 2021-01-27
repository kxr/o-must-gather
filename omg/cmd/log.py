import os, sys

from click import Context

from omg.common.config import Config
from omg.cmd.get_main import get_resource_names


def complete_pods(ctx: Context, args, incomplete):
    """
    Callback for pod name (within an ns) autocompletion
    :return: List of matching pod names or empty list.
    """
    # Get current project and filter Pods
    c = Config()
    ns = ctx.params.get("namespace") or c.project
    pod_listing = os.listdir(os.path.join(c.path, "namespaces", ns, "pods"))
    suggestions = [pod for pod in pod_listing if incomplete in pod]
    return suggestions


def complete_containers(ctx: Context, args, incomplete):
    """
    Callback for container name (within a pod and ns) autocompletion
    :return: List of matching container names or empty list
    """
    c = Config()
    if len(ctx.args) != 1:  # If there's no pod specified yet, can't autocomplete a container name
        return []
    ns = ctx.params.get("namespace") or c.project
    pod = ctx.args[0]
    container_listing = os.listdir(os.path.join(c.path, "namespaces", ns, "pods", pod))
    suggestions = [c for c in container_listing if incomplete in c and not c.endswith(".yaml")]  # skip .yaml files
    return suggestions


def log(resource, container, previous, namespace, all_namespaces):
    if all_namespaces is True:
        print('[ERROR] All Namespaces is not supported with log')
        sys.exit(1)
    else:
        if namespace is not None:
            ns = namespace
        elif Config().project is not None:
            ns = Config().project
        else:
            # ns not set
            print('[ERROR] Namespaces/project not set')
            sys.exit(1)

    ns_dir = os.path.join(Config().path,'namespaces', ns)

    # check if ns directory exists
    if not os.path.isdir(ns_dir):
        print('[ERROR] Namespace not found:', ns)
        sys.exit(1)
    
    # pod
    if '/' in resource:
        r_type = resource.split('/')[0]
        pod = resource.split('/')[1]
        if r_type not in ['pod','pods']:
            print('[ERROR] Can not print logs of type:',r_type)
            sys.exit(1)
    else:
        pod = resource

    # check if top pod directory exits
    pod_dir = os.path.join(ns_dir, 'pods', pod)
    if not os.path.isdir(pod_dir):
        print('[ERROR] Pod directory not found:', pod_dir)
        sys.exit(1)
    
    # Containers are dirs in pod_dir
    containers = [ c for c in os.listdir(pod_dir) 
                    if os.path.isdir(os.path.join(pod_dir,c))]
    # If we have > 1 containers and -c/--container is not specified, error out
    if len(containers) == 0:
        print('[ERROR] No container directory not found in pod directory:', pod_dir)
        sys.exit(1)
    elif len(containers) > 1:
        if container is None:
            print('[ERROR] This pod has more than one containers:')
            print('       ', str(containers))
            print('        Use -c/--container to specify the container')
            sys.exit(1)
        else:
            con_to_log = container
    else: # len(containers) == 1
        con_to_log = containers[0]

    if previous:
        log_f = 'previous.log'
    else:
        log_f = 'current.log'

    file_to_cat = os.path.join(pod_dir,con_to_log,con_to_log,'logs',log_f)
    if not os.path.isfile(file_to_cat):
        print('[ERROR] Log file missing: ', file_to_cat)
        sys.exit(1)
    
    # ouput the log file
    print(file_to_cat)

    with open(file_to_cat, 'r') as ol:
            print(ol.read())
