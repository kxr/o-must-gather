""" load_resources_from_yaml.py """

import yaml
import os
from loguru import logger as lg

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    lg.warning("yaml.CSafeLoader failed to load, using SafeLoader")
    from yaml import SafeLoader


def load_yaml(yfile):
    """Load yaml file and return python object

    Args:
        yfile (str): Yaml file path

    Returns:
        (str|list|dict): Python object loaded from yaml
    """
    lg.debug("yfile: {}".format(yfile))

    if not os.path.isfile(yfile):
        raise Exception("File not found: {}".format(yfile))

    ydata = None
    with open(yfile, "r") as y_f:
        lg.debug("Opened yaml file: " + yfile)
        y_d = y_f.read()
        try:
            ydata = yaml.load(y_d, Loader=SafeLoader)
        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            # yaml load/parse failed
            # try skipping lines from the bottom
            # Until we are able to load the yaml file
            # We will try until > 1 lines are left
            lines_total = y_d.count("\n")
            lines_skipped = 0
            while y_d.count("\n") > 1:
                # skip last line
                y_d = y_d[:y_d.rfind("\n")]
                lines_skipped += 1
                try:
                    ydata = yaml.load(y_d, Loader=SafeLoader)
                except (yaml.scanner.ScannerError, yaml.parser.ParserError):
                    pass
                else:
                    lg.warning("Skipped " +
                               str(lines_skipped) + "/" + str(lines_total) +
                               " lines from the end of " + yfile +
                               " to the load the yaml file properly")
                    break

    lg.debug("yaml file loaded in ydata. type: " + str(type(ydata)))
    lg.trace("ydata: " + str(ydata))

    # if not ydata:
    #     raise Exception("Unable to load yaml file: {}".format(yfile))

    return ydata
