import sys, os
from omg.common.config import Config

def use(a):
    c = Config(fail_if_no_path=False)
    p = a.mg_path
    # We traverse up to 3 levels to find the must-gather
    # At each leve if it has only one dir and we check inside it
    # When we see see the dir /namespaces and /cluster-scoped-resources, we assume it
    for i in [1,2,3]:
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
        
