import yaml
import json

from click import Context

from omg.common.config import Config
from omg.common.resource_map import map_res, map
from omg.cmd.get import parse


def complete_get(ctx: Context, args, incomplete):
    """
    Pull out objects args from Click context and return completions.
    """
    c = Config()
    objects = ctx.params.get("objects")
    return generate_completions(c, objects, incomplete)


def generate_completions(config, objects, incomplete):
    """
    Given a config, tuple of args, and incomplete input from user, generate a list of completions.

    This function should not print stack traces or do any error logging (without turning it on explicitly)
    since shell completion should be transparent to user.
    """
    try:
        resource_list = parse.ResourceList(objects)
    except:
        # Swallow any error since we don't want to spam terminal during autcompletion.
        return []

    # We're completing something like `oc get pod/name`.
    if "/" in incomplete:
        restypein = incomplete.split("/")[0]
        resname = incomplete.split("/")[1]
        restype = map_res(restypein)
        resources = restype['get_func']('items', config.project, '_all', restype['yaml_loc'], restype['need_ns'])
        return [restypein + "/" + r['res']['metadata']['name'] for r in resources if r['res']['metadata']['name'].startswith(resname)]

    if len(resource_list) == 0 and "," in incomplete:
        # This is a NOP like oc
        return []
    elif resource_list.get_method == parse.Method.SINGLE_TYPE or \
            resource_list.get_method == parse.Method.ALL:
        # Autocomplete resource names based on the type: oc get pod mypod1 mypod2
        restypein, _ = next(resource_list)
        restype = map_res(restypein)
        resources = restype['get_func']('items', config.project, '_all', restype['yaml_loc'], restype['need_ns'])
        return [r['res']['metadata']['name'] for r in resources if
                r['res']['metadata']['name'].startswith(incomplete)]
    else:
        # Return completions for resource types
        # TODO: Include aliases
        fullset = set(parse.ALL_TYPES + [t['type'] for t in map])
        return [t for t in fullset if t.startswith(incomplete)]


# The high level function that gets called for any "get" command
# This function processes/identifies the objects, they can be in various formats e.g:
#   get pod httpd
#   get pods httpd1 httpd2
#   get dc/httpd pod/httpd1
#   get routes
#   get pod,svc
# We get all these args (space separated) in the array objects
# We'll process them and normalize them in a python dict (objects)
# Once we have one of more object to get,
# and call the respective get function
# (this function is looked up from common/resource_map)
def get_main(objects, output, namespace, all_namespaces):
    # a = args passed from cli
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

    try:
        resource_list = parse.ResourceList(objects)
    except parse.ResourceParseError as e:
        print(e)
        return

    # Object based routing
    # i.e, call the get function for all the requested types
    # then call the output function or simply print if its yaml/json
    
    # If printing multiple objects, add a blank line between each
    mult_objs_blank_line = False

    for r_type, res_set in resource_list:
        rt_info = map_res(r_type)
        get_func = rt_info['get_func']
        getout_func = rt_info['getout_func']
        yaml_loc = rt_info['yaml_loc']
        need_ns = rt_info['need_ns']

        # Call the get function to get the resoruces
        res = get_func(r_type, ns, res_set, yaml_loc, need_ns)

        # Error out if no objects/resources were collected
        if len(res) == 0 and resource_list.get_method is not parse.Method.ALL:
            print('No resources found for type "%s" in %s namespace' % (r_type, ns))
        elif len(res) > 0:
            # If printing multiple objects, add a blank line between each
            if mult_objs_blank_line:
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
                if resource_list.is_multitype():
                    show_type = True
                else:
                    show_type = False
                getout_func(r_type, ns, res, output, show_type)
            # Flag to print multiple objects
            if not mult_objs_blank_line:
                mult_objs_blank_line = True

    # Error out once if multiple objects/resources requested and none collected
    if not mult_objs_blank_line and resource_list.get_method == parse.Method.ALL:
        print('No resources found in %s namespace' % ns)
