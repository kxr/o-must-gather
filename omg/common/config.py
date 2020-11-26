import sys, os, yaml

CONFIG_FILE = os.getenv("HOME") + "/.omgconfig"

class Config:

    path = None
    project = None

    def __init__(self, fail_if_no_path=True):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as cf:
                c = yaml.safe_load(cf)
                if c is not None:
                    if 'path' in c:
                        Config.path = c['path']
                    if 'project' in c:
                        Config.project = c['project']
        if fail_if_no_path:
            if Config.path is None:
                print('[ERROR] You have not selected a must-gather')
                print()
                print('Use `omg use </path/to/must-gather>` to point to an extracted must-gather.')
                sys.exit(1)
            elif Config.path == '.':
                if not ( os.path.isdir( os.path.join( '.', 'namespaces')) and
                         os.path.isdir( os.path.join( '.', 'cluster-scoped-resources')) ):
                    print('[ERROR] Current working directory is not a valid must-gather')
                    print()
                    sys.exit(1)



    def save(self, path=None, project=None):
        c = {}
        if path is not None:
            Config.path = path
            c['path'] = path
        else:
            c['path'] = Config.path

        if project is not None:
            Config.project = project
            c['project'] = project
        else:
            c['project'] = Config.project
        try:
            with open(CONFIG_FILE, 'w') as cf:
                yaml.dump(c, cf, default_flow_style=False)
        except IOError:
            print("[ERROR] Could not write config file:", CONFIG_FILE)
