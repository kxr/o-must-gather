import sys, os
from omg.common.config import Config


def project(a):
    c = Config()
    ns_dir = os.path.join(c.path,'namespaces')
    if a is None or a.project is None:
        # print current project
        if c.project is None:
            print('No project selected')
        else:
            print('Using project "%s" on must-gather "%s"' % (c.project,c.path))
    else:
        # Set current project
        if os.path.isdir(os.path.join(ns_dir, a.project)):
            if a.project == c.project:
                print('Already on project "%s" on server "%s"' % (c.project,c.path))
            else:
                c.save(project=a.project)
                print('Now using project "%s" on must-gather "%s"' % (c.project,c.path))
        else:
            print('[ERROR] Project %s not found in %s'%(a.project,ns_dir))


def projects(a):
    c = Config()
    ns_dir = os.path.join(c.path,'namespaces')
    projects = [ p for p in os.listdir(ns_dir) 
                    if os.path.isdir(os.path.join(ns_dir,p)) ]
    print("You have access to the following projects and can switch between them with 'omg project <projectname>':")
    print()
    for proj in projects:
        if proj == c.project:
            print('  * ',proj)
        else:
            print('    ',proj)
    print()
    project(None)
