import os
from omg.common.config import Config


def use(mg_path, cwd):
    if mg_path is None:
        if cwd == True:
            # If --cwd is set we will blidly assume current working directory
            # to be the must-gather to use
            c = Config(fail_if_no_path=False)
            c.save(path='.')
            print("Using your current working directory")
        else:
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
    else:
        c = Config(fail_if_no_path=False)
        p = mg_path
        # We traverse up to 3 levels to find the must-gather
        # At each leve if it has only one dir and we check inside it
        # When we see see the dir /namespaces and /cluster-scoped-resources, we assume it
        for _ in [1,2,3]:
            if os.path.isdir(p):
                if ( os.path.isdir( os.path.join(p, 'namespaces')) and
                    os.path.isdir( os.path.join(p, 'cluster-scoped-resources')) ):
                    full_path = os.path.abspath(p)
                    c.save(path=full_path)
                    print('Using: ',p)
                    break
                elif len(os.listdir(p)) == 1:
                    p = os.path.join(p,os.listdir(p)[0])
                else:
                    print('[ERROR] Invalid must-gather path. Please point to the extracted must-gather directory')
                    break
            else:
                print('[ERROR] Invalid path. Please give path to the extracted must-gather')
                break
