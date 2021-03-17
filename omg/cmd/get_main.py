import yaml
import json
import sys
from click import Context

from omg.common.config import Config
from omg.common.resource_map import map_res, map
from omg.cmd.get import parse

def get_resources(r_type, r_name='_all', ns=None, print_warnings=True):
    rt_info = map_res(r_type)
    get_func = rt_info['get_func']
    yaml_loc = rt_info['yaml_loc']
    need_ns = rt_info['need_ns']

    return get_func(ns, r_name, yaml_loc, need_ns, print_warnings)

def get_resource_names(r_type, r_name='_all', ns=None):
    res = get_resources(r_type, r_name, ns, False)
    res_names = [ r['res']['metadata']['name'] for r in res ]
    return res_names


# The high level function that gets called for any "get" command
def get_main(objects, output, namespace, all_namespaces,show_labels):
    # Check if -A/--all-namespaces is set
    # else, Set the namespace
    # -n/--namespace takes precedence over current project 
    if all_namespaces is True:
        ns = '_all'
    else:
        if namespace is not None:
            ns = namespace
        elif Config().project is not None:
            ns = Config().project
        else:
            ns = None

    # Parse get args and get normalized resources to get
    try:
        _, resource_list = parse.parse_get_resources(objects)
    except parse.ResourceParseError as e:
        print(e)
        return

    # Call the get function for all the requested types
    # then call the output function or simply print if its yaml/json
    
    # Flag to mark if we have already printed something
    printed_something = False

    for r_type, r_name in resource_list:

        res = get_resources(r_type, r_name, ns)

        if len(res) > 0:
            # If printing multiple objects, add a blank line between each
            if printed_something:
                print('')
            # Yaml dump if -o yaml
            if output == 'yaml':
                if len(res) == 1:
                    print(yaml.dump(res[0]['res']))
                elif len(res) > 1:
                    print(yaml.dump({'apiVersion':'v1','items':[cp['res']for cp in res]}))
            # Json dump if -o json
            elif output == 'json':
                if len(res) == 1:
                    print(json.dumps(res[0]['res'],indent=4))
                elif len(res) > 1:
                    print(json.dumps({'apiVersion':'v1','items':[cp['res']for cp in res]},indent=4))
            # Call the respective output function if -o is not set or -o wide
            elif output in [None, 'wide']:
                # If we displaying more than one resource_type,
                # we need to display resource_type with the name (type/name)
                if len(resource_list) > 1:
                    show_type = True
                else:
                    show_type = False
                getout_func = map_res(r_type)['getout_func']
                getout_func(r_type, ns, res, output, show_type, show_labels)
            
            # We printed something
            printed_something = True

    # Error out if nothing was printed
    if not printed_something:
        print('No resources found in %s namespace' % ns)
