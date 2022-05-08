import json
from loguru import logger as lg


def load_json(jfile):
    try:
        with open(jfile, "r") as j_f:
            j_d = j_f.read()
            j_data = json.loads(j_d)
            return j_data
    except Exception as e:
        lg.warning("Error loading json file ({}): {}".format(jfile, e))
    return None
