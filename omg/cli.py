import sys, argparse
from .config import Config

from .cmd_use import use
from .cmd_project import project, projects
from .cmd_get import get
from .cmd_describe import describe
from .cmd_log import log
from .cmd_whoami import whoami

def main():
    # Common parser, with shared arguments for all subcommands:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-n", "--namespace", dest="namespace")
    common.add_argument("-A", "--all-namespaces", dest="all_namespaces",action='store_true')

    # Main Parser for sub commands
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # omg use </path/to/must-gather>
    p_use = subparsers.add_parser('use', parents=[common], aliases=['login'],
                                  help='Select the must-gather to use')
    p_use.add_argument('mg_path', metavar='must-gather-location', type=str)
    p_use.set_defaults(func=use)

    # omg project
    p_project = subparsers.add_parser('project', parents=[common],
                                      help='Display information about the current active project and existing projects')
    p_project.set_defaults(func=project)

    # omg projects
    p_projects = subparsers.add_parser('projects', parents=[common],
                                       help='Display information about the current active project and existing projects')
    p_projects.set_defaults(func=projects)

    # omg get <object(s)>
    p_get = subparsers.add_parser('get', parents=[common],
                                  help='Display one or many resources')
    p_get.add_argument('objects', nargs='*', type=str)
    p_get.add_argument("-o", "--output", dest="output",
                       choices=['yaml', 'json', 'wide'] )
    p_get.set_defaults(func=get)

    # omg describe <object(s)>
    p_describe = subparsers.add_parser('describe', parents=[common],
                                       help='This command joins many API calls together to form a detailed description of a given resource.')
    p_describe.add_argument('object', nargs='*', type=str)
    p_describe.set_defaults(func=describe)

    # omg log <pod>
    p_log = subparsers.add_parser('log', parents=[common],
                                  help='Display one or many resources')
    p_log.set_defaults(func=log)

    # omg whoami
    p_whoami = subparsers.add_parser('whoami', parents=[common],
                                  help='Display who you are')
    p_whoami.set_defaults(func=whoami)

    # process args and call the corresponding function
    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)
