import sys, os, yaml, glob

from omg.common.config import Config
from omg.common.helper import load_yaml_file


# Special function to handle `omg get project`
def get_project(ns, names, yaml_loc, need_ns, print_warnings=True):
    import glob
    mg_path = Config().path
    yaml_path = os.path.join(mg_path, yaml_loc)
    # we neeed all namespaces regardless if -A is set or not
    ns="_all"

    yamls = glob.glob(yaml_path)
    # Collect the resources
    collected=[]
    for yp in yamls:
        try:
            # record when was this yaml generated (to calc age)
            gen_ts = os.path.getmtime(yp)
            res = load_yaml_file(yp, print_warnings)
        except:
            print("[ERROR] Could not read file:", yp)
            sys.exit(1)

        # add objects to collected if name matches
        # or if we want to get all the objects (e.g `get pods`)
        if 'items' in res:
            # we got a list
            if res['items'] is not None and len(res['items']) > 0:
                collected.extend(
                    [ {'res':r,'gen_ts':gen_ts}
                        for r in res['items']
                            if r['metadata']['name'] in names or '_all' in names ]
                )
            # else the list was empty/none, we dont' add anything to collected
        elif 'metadata' in res:
            # we got a single item
            collected.extend(
                [ {'res':res,'gen_ts':gen_ts} ] 
                if res['metadata']['name'] in names or '_all' in names else []
            )
    return collected