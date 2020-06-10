import os, sys

from omg.common.config import Config

def log(a):
    if a.all_namespaces is True:
        print('[ERROR] All Namespaces is not supported with log')
        sys.exit(1)
    else:
        if a.namespace is not None:
            ns = a.namespace
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
    if '/' in a.resource:
        r_type = a.resource.split('/')[0]
        pod = a.resource.split('/')[1]
        if r_type not in ['pod','pods']:
            print('[ERROR] Can not print logs of type:',r_type)
            sys.exit(1)
    else:
        pod = a.resource

    # check if top pod directory exits
    pod_dir = os.path.join(ns_dir, 'pods', pod)
    if not os.path.isdir(pod_dir):
        print('[ERROR] Pod directory not found:', pod_dir)
        sys.exit(1)
    
    # Containers are dirs in pod_dir
    containers = [ c for c in os.listdir(pod_dir) 
                    if os.path.isdir(os.path.join(pod_dir,c))]
    # If we have > 1 containers and -c/--container is not speficied, error out
    if len(containers) == 0:
        print('[ERROR] No container directory not found in pod direcotry:', pod_dir)
        sys.exit(1)
    elif len(containers) > 1:
        if a.container is None:
            print('[ERROR] This pod has more than one containers:')
            print('       ', str(containers))
            print('        Use -c/--container to specify the container')
            sys.exit(1)
        else:
            con_to_log = a.container
    else: # len(containers) == 1
        con_to_log = containers[0]

    if a.previous:
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
