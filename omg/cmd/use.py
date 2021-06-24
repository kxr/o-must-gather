# -*- coding: utf-8 -*-
import os

from omg.common.config import Config


def use(mg_path, cwd, session):
    if mg_path is None:
        if cwd is True:
            # If --cwd is set we will blindly assume current working directory
            # to be the must-gather to use
            c = Config(fail_if_no_path=False, session=session)
            c.save(path='.')
            print("Using your current working directory")
        else:
            # If no args are passed after `omg use`
            # we print the info about currently selected must-gather
            path = Config().path
            project = Config().project
            print('Current must-gather: %s' % path)
            print('    Current Project: %s' % project)
            if Config().session:
                print('      Using Session: %s' % Config().session)
            try:
                from omg.cmd.get_main import get_resources

                infra = get_resources("Infrastructure")
                apiServerURL = [i["res"]["status"]["apiServerURL"] for i in infra]
                platform = [i["res"]["status"]["platform"] for i in infra]
                print("    Cluster API URL: %s" % str(apiServerURL))
                print("   Cluster Platform: %s" % str(platform))
            except:
                print("[ERROR] Unable to determine cluster API URL and Platform.")
    else:
        c = Config(fail_if_no_path=False, session=session)
        p = mg_path
        # We traverse up to 3 levels to find the must-gather
        # At each leve if it has only one dir and we check inside it
        # When we see see the dir /namespaces and /cluster-scoped-resources, we assume it
        for _ in [1, 2, 3]:
            if os.path.isdir(p):
                dirs = [d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d))]
                if "namespaces" in dirs or "cluster-scoped-resources" in dirs:
                    full_path = os.path.abspath(p)
                    c.save(path=full_path)
                    print("Using: ", p)
                    break
                elif len(dirs) == 1:
                    p = os.path.join(p, dirs[0])
                elif len(dirs) > 1:
                    print("[ERROR] Multiple directories found:", dirs)
                    break
                else:
                    print(
                        "[ERROR] Invalid must-gather path. Please point to the extracted must-gather directory"
                    )
                    break
            else:
                print(
                    "[ERROR] Invalid path. Please give path to the extracted must-gather"
                )
                break
