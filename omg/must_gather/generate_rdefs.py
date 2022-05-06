import os
import yaml
from loguru import logger as lg
from omg.utils.dget import dget
from omg.must_gather.load_resources import load_res
from omg.must_gather.exceptions import FailedGeneratingRdefFile


def generate_rdefs(path, dest=None):
    """Generate resource definitions from the crds present in path

    Args:
        path (str): must-gather path

        dest (str, optional): Optional destination directory for the rdef file.
                              By default .rdef.yaml file is placed in must-gather
    """
    lg.debug("FUNC_INIT: {}".format(locals()))

    if dest is None:
        rdef_file = os.path.join(path, ".rdefs.yaml")
    else:
        rdef_file = os.path.join(dest, ".rdefs.yaml")

    lg.debug("Generating rdef: {}".format(rdef_file))

    rdefs = []
    try:
        crds = load_res(path, "crd")

        # if not crds:
        #     raise Exception("No crds found in {}".format(path))

        if crds:
            for crd in crds:

                res = dget(crd, ["res"])

                rdef = {}
                rdef["kind"] = dget(
                    res, ["spec", "names", "kind"])
                rdef["singular"] = dget(
                    res, ["spec", "names", "singular"])
                rdef["plural"] = dget(
                    res, ["spec", "names", "plural"])
                rdef["group"] = dget(
                    res, ["spec", "group"])
                rdef["scope"] = dget(
                    res, ["spec", "scope"])
                rdef["shortNames"] = dget(
                    res, ["spec", "names", "shortNames"], [])
                lg.trace("Adding new rdef: {}".format(rdef))

                rdefs.append(rdef)

            with open(rdef_file, "w") as rdf:
                yaml.dump(rdefs, rdf, default_flow_style=False)
                lg.debug("{} rdefs written to: {}".format(len(rdefs), rdef_file))

    except Exception as e:
        # lg.warning("Unable to generate rdef file {}: {}".format(rdef_file, e))
        raise FailedGeneratingRdefFile(e)
