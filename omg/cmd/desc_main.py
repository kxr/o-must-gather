import sys, yaml, json
from omg.common.config import Config
from omg.common.resource_map import map_res
from omg.cmd.get import parse

# The high level function that gets called for any "describe" command
def desc_main(objects, namespace, all_namespaces):
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

    # Parse describe args and get normalized resources to describe
    try:
        _, resource_list = parse.parse_get_resources(objects)
    except parse.ResourceParseError as e:
        print(e)
        return

    
    # Flag to mark if we have already printed something
    printed_something = False

    for r_type, r_name in resource_list:

        # If printing multiple objects, add a blank line between each
        if printed_something:
            print('')

        rmap = map_res(r_type)

        if 'desc_func' in rmap:
            desc_func = rmap['desc_func']
            desc_func(r_name, ns)
        else:
            print('[SORRY] Describing %s is not yet implemented' % (r_type) )
        
        # We printed something
        printed_something = True

    # Error out if nothing was printed
    if not printed_something:
        print('No resources found in %s namespace' % ns)
