import sys, os, yaml

CONFIG_FILE = os.getenv("HOME") + "/.omgconfig"

class Config:

    path = None
    project = None

    def __init__(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as cf:
                c = yaml.safe_load(cf)
                if 'path' in c:
                    Config.path = c['path']
                if 'project' in c:
                    Config.project = c['project']

    def save(self, path=None, project=None):
        c = {}
        if path is not None:
            Config.path = path
            c['path'] = path
        if project is not None:
            Config.project = project
            c['project'] = project
        try:
            with open(CONFIG_FILE, 'w') as cf:
                yaml.dump(c, cf, default_flow_style=False)
        except IOError:
            print("[ERROR] Could not write config file:", CONFIG_FILE)
