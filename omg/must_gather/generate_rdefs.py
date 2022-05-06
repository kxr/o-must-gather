import os
import yaml
from loguru import logger as lg
from omg.utils.dget import dget
from omg.must_gather.load_resources import load_res


def generate_rdefs(path):
    """Generate resource definitions from the crds present in path

    Args:
        path (str): must-gather path

        dest (str, optional): Optional destination directory for the rdef file.
                              By default .rdef.yaml file is placed in must-gather
    """
    lg.debug("FUNC_INIT: {}".format(locals()))

    rdefs_f = os.path.join(os.getenv("HOME"), ".omg.rdefs")

    lg.debug("Generating rdef: {}".format(rdefs_f))

    rdefs = []
    # Load existing rdefs
    if os.path.isfile(rdefs_f):
        try:
            with open(rdefs_f, "r") as r_f:
                rdefs.extend(yaml.safe_load(r_f))
        except Exception:
            pass

    try:
        crds = load_res(path, "crd")

        if crds:
            for crd in crds:

                res = dget(crd, ["res"])

                rdef = {}
                rdef["kind"] = dget(res, ["spec", "names", "kind"])
                rdef["singular"] = dget(res, ["spec", "names", "singular"])
                rdef["plural"] = dget(res, ["spec", "names", "plural"])
                rdef["group"] = dget(res, ["spec", "group"])
                rdef["scope"] = dget(res, ["spec", "scope"])
                rdef["shortNames"] = dget(res, ["spec", "names", "shortNames"], [])

                if rdef not in rdefs:
                    rdefs.append(rdef)

            with open(rdefs_f, "w") as rdf:
                yaml.dump(rdefs, rdf, default_flow_style=False)
                lg.debug("{} rdefs written to: {}".format(len(rdefs), rdefs_f))

    except Exception:
        # lg.warning("Unable to generate rdef file {}: {}".format(rdefs_f, e))
        pass
