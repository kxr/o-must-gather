# -*- coding: utf-8 -*-
import os
import sys
import yaml

CONFIG_FILE = os.getenv("HOME") + "/.omgconfig"
SESSION_FILE = os.getenv("PWD") + "/.omgsession"


class Config:
    path = None
    project = None
    session = False

    def __init__(self, fail_if_no_path=True, session=False):
        """
        Initialize Config from global config file or local session file.
        Session file (.omgsession) resides on directory that the program
        was called, in general same of must-gather. Sessions allow run
        multiple runtimes without needing to run 'omg use' every time to
        overwrite global config. Sessions has precedence than global config,
        to remove a session just remove the .omgsession file.
        """
        def setup_config(path):
            with open(path, 'r') as cf:
                c = yaml.safe_load(cf)
                if c is not None:
                    if 'path' in c:
                        Config.path = c['path']
                    if 'project' in c:
                        Config.project = c['project']

        self.session = session
        if os.path.exists(SESSION_FILE):
            setup_config(SESSION_FILE)
            self.session = True
        elif os.path.exists(CONFIG_FILE):
            setup_config(CONFIG_FILE)

        if fail_if_no_path:
            if Config.path is None:
                print("[ERROR] You have not selected a must-gather")
                print()
                print(
                    "Use `omg use </path/to/must-gather>` to point to an extracted must-gather."
                )
                sys.exit(1)
            elif Config.path == ".":
                if not (
                    os.path.isdir(os.path.join(".", "namespaces"))
                    or os.path.isdir(os.path.join(".", "cluster-scoped-resources"))
                ):
                    print(
                        "[ERROR] Current working directory is not a valid must-gather"
                    )
                    print()
                    sys.exit(1)

    def save(self, path=None, project=None):
        c = {}
        if path is not None:
            Config.path = path
            c["path"] = path
        else:
            c["path"] = Config.path

        if project is not None:
            Config.project = project
            c["project"] = project
        else:
            c["project"] = Config.project
        try:
            if self.session:
                current_config = SESSION_FILE
            else:
                current_config = CONFIG_FILE
            with open(current_config, 'w') as cf:
                yaml.dump(c, cf, default_flow_style=False)
        except IOError:
            print("[ERROR] Could not write config file:", current_config)
