# -*- coding: utf-8 -*-
import os

from omg.common.config import Config


def use_cwd():
    # If --cwd is set we will blindly assume current working directory
    # to be the must-gather to use
    c = Config(fail_if_no_path=False)
    c.save(path='.')
    print("Using your current working directory")


def use_current_cfg():
    # If no args are passed after `omg use`
    # we print the info about currently selected must-gather
    path = Config().path
    project = Config().project
    print('Current must-gather: %s' % path)
    print('    Current Project: %s' % project)
    try:
        from omg.cmd.get_main import get_resources
        infra = get_resources('Infrastructure')
        apiServerURL = [ i['res']['status']['apiServerURL'] for i in infra ]
        platform = [ i['res']['status']['platform'] for i in infra ]
        print('    Cluster API URL: %s' % str(apiServerURL))
        print('   Cluster Platform: %s' % str(platform))
    except:
        print('[ERROR] Unable to determine cluster API URL and Platform.')


def use_setup_path(mg_path):
    # setup using file path
    c = Config(fail_if_no_path=False)
    p = mg_path
    # We traverse up to 3 levels to find the must-gather
    # At each leve if it has only one dir and we check inside it
    # When we see see the dir /namespaces and /cluster-scoped-resources, we assume it
    for _ in [1,2,3]:
        if os.path.isdir(p):
            dirs = [d for d in os.listdir(p) if os.path.isdir(os.path.join(p,d))]
            if 'namespaces' in dirs or 'cluster-scoped-resources' in dirs:
                full_path = os.path.abspath(p)
                c.save(path=full_path)
                print('Using: ',p)
                break
            elif len(dirs) == 1:
                p = os.path.join(p,dirs[0])
            elif len(dirs) > 1:
                print('[ERROR] Multiple directories found:', dirs)
                break
            else:
                print('[ERROR] Invalid must-gather path. Please point to the extracted must-gather directory')
                break
        else:
            print('[ERROR] Invalid path. Please give path to the extracted must-gather')
            break


def use_session(session, mg_path=None):
    if mg_path:
        print(f"[TODO] setup a new session {session} to path {mg_path}")
        return

    print(f"[TODO] retrieve current session {session}")
    return


def use(mg_path, cwd, session):
    """
    use (--cmd|--session s_name mg_path)
    use will setup a working directory. When session is defined
    a new session will be saved on Config, otherwise the default
    will be set.
    """
    if mg_path is None:
        if cwd == True:
            return use_cwd()

        if session:
            return use_session(session)

        return use_current_cfg()

    if session:
        return use_session(session, mg_path=mg_path)

    return use_setup_path(mg_path)
