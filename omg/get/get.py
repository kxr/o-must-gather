from loguru import logger as lg
from omg.get.parse import parse_get_args, ParseError
from omg.config import config
from omg.get.output.o_raw import o_raw
from omg.get.output.o_table import o_table
from omg.utils.dget import dget
from omg.get.get_resources import get_all_resources


def cmd(objects, output, show_labels):
    lg.debug("FUNC_INIT: {}".format(locals()))

    # Parse objects
    try:
        parsed_objects = parse_get_args(objects)
    except ParseError as e:
        lg.error(e)
        return 2

    lg.debug("parsed_objects: {}".format(parsed_objects))

    # Set namespace
    ns = dget(config.get(), ["project"])

    lg.debug("Namespace resolved to: {}".format(ns))

    # Collect resources
    all_res_d = get_all_resources(parsed_objects, ns)

    # No resource type found e.g:
    # all_res_d == [{}, {}, ..<paths>.. ]
    if not any(all_res_d):
        lg.error("Unkown resource type")
        return 2

    # Resource type found, but no resources found e.g:
    # [{'pods': []}, {'pods': []}, ..<paths>..]
    if not any([bool(all_res_d[i][rtype]) for i in all_res_d for rtype in all_res_d[i]]):
        print("No resources found")
        return 2

    # Pass the parsed object to respective output function
    if output in ["yaml", "json", "name"]:
        o_raw(all_res_d, output)
    elif output is None or output == "wide":
        o_table(all_res_d, ns, output, show_labels)
    else:
        lg.error("Unknow output type: {}".format(output))
