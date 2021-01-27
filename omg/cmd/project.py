import sys, os
from omg.common.config import Config
from omg.cmd.get_main import get_resource_names


def complete_projects(ctx, args, incomplete):
    """
    Callback for project name autocompletion
    :return: List of matching namespace names or empty list.
    """
    if incomplete is not None:
        ns_listing = get_resource_names('project')
        suggestions = [ns for ns in ns_listing if ns.startswith(incomplete)]
        return suggestions
    return []


def project(name):
    c = Config()
    ns_dir = os.path.join(c.path,'namespaces')
    if name is None:
        # print current project
        if c.project is None:
            print('No project selected')
        else:
            print('Using project "%s" on must-gather "%s"' % (c.project,c.path))
    else:
        # Set current project
        if os.path.isdir(os.path.join(ns_dir, name)):
            if name == c.project:
                print('Already on project "%s" on server "%s"' % (c.project,c.path))
            else:
                c.save(project=name)
                print('Now using project "%s" on must-gather "%s"' % (c.project,c.path))
        else:
            print('[ERROR] Project %s not found in %s'%(name,ns_dir))


def projects():
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
