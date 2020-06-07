import sys, os
from .config import Config

def use(a):
    path = a.mg_path
    c = Config()
    if os.path.isdir(path) and os.path.isfile(path+'/version'):
        c.save(path=os.path.abspath(path))
    elif os.path.isdir(path) and os.path.isfile(path + '/' + str(os.listdir(path)[0]) + '/version'):
        c.save(path=os.path.abspath(path + '/' + str(os.listdir(path)[0])))
    else:
        print("[ERROR] Invalid must-gather path. Please point to the extracted must-gather directory")
        sys.exit(1)