from tabulate import tabulate
from loguru import logger as lg
from os import getenv
from omg.config import config
from omg.get.output.build_table import build_table


def o_table(resd_from_paths, ns, output, show_labels):
    """Handles table output.
       Both simple (without -o) and wide (-o wide)

    Args:
        parsed_objects (dict):  Contains parsed dictionary of objects to get.
                                This dict is the one we get from parse.py module.

        ns (str): Namespace is needed if we are showing output for all-namespaces.

        output (str):   This is passed from click (-o). We need to know if the output
                        is simple (-o not set) or wide (-o wide).

        show_labels (bool):     This is passed from click (--show-labels)
    """
    lg.debug("FUNC_INIT: {}".format(locals()))

    cfg = config.get()
    paths = cfg["paths"]

    tablefmt = getenv("OMG_TABLE_FMT") or "plain"

    show_type = False
    if max([len(resd_from_paths[i]) for i in resd_from_paths]) > 1:
        show_type = True

    for i, path_resd in resd_from_paths.items():
        table_all_res = None
        for r_type in path_resd:
            res = path_resd[r_type]
            if res:
                res_table = build_table(res, ns, output, show_type, show_labels)
                if table_all_res:
                    table_all_res += [[""]] + res_table
                else:
                    table_all_res = res_table
        if table_all_res:
            print(tabulate(table_all_res, tablefmt=tablefmt))
            if (len(paths) > 1):
                lg.opt(colors=True).success("^^^<e>[{}]</>^^^\n".format(i))
