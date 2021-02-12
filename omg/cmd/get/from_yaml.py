import sys, os

from omg.common.config import Config
from omg.common.helper import load_yaml_file

# This function finds the respective yamls and returns the resouces that match
def from_yaml(ns, names, yaml_loc, need_ns, print_warnings=True):
    mg_path = Config().path
    yaml_path = os.path.join(mg_path, yaml_loc)
    if need_ns:
        # Error out if it needs ns and its not set.
        if ns is None:
            if print_warnings:
                print("[ERROR] Namespace not set. Select a project (omg project) or specify a namespace (-n)")
            sys.exit(1)
        # Get all namespace names if we need all
        elif ns == '_all':
            nses = os.listdir( os.path.join(mg_path, 'namespaces') )
            yaml_paths = [ yaml_path%(n) for n in nses ]
        else:
            yaml_paths = [ yaml_path%(ns) ]
    else:
        yaml_paths = [ yaml_path ]

    yamls = []
    for ym in yaml_paths:
        # if yaml_paths is a dir, we will read all yamls from this dir
        if os.path.isdir(ym):
            yamls.extend(
                [ os.path.join(ym, y) for y in os.listdir(ym) if y.endswith('.yaml') ]
            )
        elif os.path.isfile(ym) and ym.endswith('.yaml'):
            yamls.append( ym )

    #Debug
    # print(yamls)
    
    # Collect the resources
    collected=[]
    for yp in yamls:
        try:
            # record when was this yaml generated (to calc age)
            gen_ts = os.path.getmtime(yp)
            res = load_yaml_file(yp, print_warnings)
        except:
            if print_warnings:
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


def from_yaml_dir(t, ns, names):
    pass