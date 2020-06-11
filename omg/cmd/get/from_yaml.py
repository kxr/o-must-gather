import sys, os, yaml

from omg.common.config import Config

# This function finds the respective yamls and returns the resouces that match
# args = resource_type (e.g pod), namespace, resource_names (e.g, httpd)
def from_yaml(rt, ns, names, yaml_loc, need_ns):
    mg_path = Config().path
    yaml_path = os.path.join(mg_path, yaml_loc)
    if need_ns:
        # Error out if it needs ns and its not set.
        if ns is None:
            print("[ERROR] Namespace not set. Select a project (omg project) or specify a namespace (-n)")
            sys.exit(1)
        # Get all namespace names if we need all
        elif ns == '_all':
            nses = os.listdir( os.path.join(mg_path, 'namespaces') )
            yaml_paths = [ yaml_path%(n) for n in nses if os.path.isfile(yaml_path%(n)) ]
        else:
            yaml_paths = [ yaml_path%(ns) ] if os.path.isfile(yaml_path%(ns)) else []
    else:
        # if yaml_loc in resource_map is a dir, we will read all yamls from this dir
        if os.path.isdir(yaml_path):
            yaml_paths = [ os.path.join(yaml_path, y) for y in os.listdir(yaml_path) if y.endswith('.yaml') ]
        else:
            yaml_paths = [ yaml_path ] if os.path.isfile(yaml_path) else []

    #Debug
    # print(yaml_paths)
    
    # Collect the resources
    collected=[]
    for yp in yaml_paths:
        try:
            # record when was this yaml generated (to calc age)
            gen_ts = os.path.getmtime(yp)
            with open(yp, 'rb') as yf:
                try:
                    res = yaml.safe_load(yf)
                except:
                    print("[ERROR] Parsing error in ", yp)
                    sys.exit(1)
        except:
            print("[ERROR] Could not read file:", yp)
            sys.exit(1)

        # add objects to collected if name matches
        # or if we want to get all the objects (e.g `get pods`)
        if 'items' in res:
            collected.extend(
                [ {'res':r,'gen_ts':gen_ts}
                    for r in res['items']
                        if r['metadata']['name'] in names or '_all' in names ]
            )
        elif 'metadata' in res:
            collected.extend(
                [ {'res':res,'gen_ts':gen_ts} ] 
                if res['metadata']['name'] in names or '_all' in names else []
            )

    return collected


def from_yaml_dir(t, ns, names):
    pass