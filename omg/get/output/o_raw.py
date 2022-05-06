from loguru import logger as lg
from omg.config import config
from omg.utils.dget import dget
import yaml
import json


def o_raw(resd_from_paths, output):
    lg.debug("FUNC_INIT: {}".format(locals()))

    cfg = config.get()
    paths = cfg["paths"]

    for i, path_resd in resd_from_paths.items():
        all_res = []
        for r_type in path_resd:
            res = path_resd[r_type]
            if res:
                all_res.extend(res)

        if all_res:
            if len(all_res) == 1:
                out_res = dget(all_res[0], ["res"])
            elif len(all_res) > 1:
                out_res = {
                        "apiVersion": "v1",
                        "kind": "List",
                        "items": [dget(res, ["res"]) for res in all_res]
                    }
            else:
                continue

            if output == "yaml":
                print(yaml.dump(out_res))
            elif output == "json":
                print(json.dumps(out_res))
            elif output == "name":
                for res in all_res:
                    group = dget(res, ["rdef", "group"])
                    singular = dget(res, ["rdef", "singular"])
                    if group == "core":
                        out_type = singular
                    else:
                        out_type = str(singular) + "." + str(group)
                    name = dget(res, ["res", "metadata", "name"])
                    print(
                        str(out_type) + "/" + str(name)
                    )

            if (len(paths) > 1):
                lg.opt(colors=True).success("^^^<e>[{}]</>^^^\n".format(i))
