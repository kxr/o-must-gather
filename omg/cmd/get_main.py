import sys, yaml, json, enum, shlex
from click import Context

from omg.common.config import Config
from omg.common.resource_map import map_res, map

all_types = ['pod', 'rc', 'svc', 'ds', 'deployment', 'rs', 'statefulset', 'hpa', 'job', 'cronjob', 'dc', 'bc', 'build',
             'is']


class ResourceParseError(Exception):
    pass


class GetResourceList:
    class Method(enum.Enum):
        SINGLE_TYPE = 1                 # e.g. omg get pod/mypod
        MULTI_TYPE_SINGLE_RESOURCE = 2  # e.g. omg get svc,ep,ds dns-default
        MULTI_TYPE_MULTI_RESOURCE = 3   # e.g. omg get pod mypod myotherpod
    """
    Takes in a string of arguments for the `omg get` command. Provides interface for parsing and handling.
    #   get pod httpd
    #   get pods httpd1 httpd2
    #   get dc/httpd pod/httpd1
    #   get routes
    #   get pod,svc
    """
    def __init__(self, objects):
        # objects var can look like:
        # ('pods)
        # ('pods,svc')
        # ('pods', 'mypod')
        # ('pod/test')
        self.objects = objects
        self.object_dict = {}
        self.method = None

        self.__parse()

    def __parse(self):
        if len(self.objects) == 0:
            # We've nothing to parse right now.
            return

        last_object = []

        for o in self.objects:
            # Case where we have a '/'
            # e.g omg get pod/httpd
            if '/' in o:
                self.method = self.Method.MULTI_TYPE_MULTI_RESOURCE
                if not last_object:
                    pre = o.split('/')[0]
                    r_type = map_res(pre)['type']
                    r_name = o.split('/')[1]
                    # If its a valid resource type, append it to objects
                    if r_type is not None:
                        if r_type in self.object_dict:
                            self.object_dict[r_type].append(r_name)
                        else:
                            self.object_dict[r_type] = [r_name]
                    else:
                        raise ResourceParseError("[ERROR] Invalid object type: ", pre)
                else:
                    # last_object was set, meaning this should be object name
                    raise ResourceParseError("[ERROR] There is no need to specify a resource type as a separate "
                                             "argument when passing arguments in resource/name form")

            # Convert 'all' to list of resource types in a specific order
            elif o == 'all':
                for rt in all_types:
                    check_rt = map_res(rt)
                    if check_rt is None:
                        raise ResourceParseError("[ERROR] Invalid object type: ", rt)
                    else:
                        last_object.append(check_rt['type'])

            # Case where we have a ',' e.g `get dc,svc,pod httpd`
            # These all will be resource_types, not names,
            # resource_name will come it next iteration (if any)
            elif ',' in o:
                self.method = self.method.MULTI_TYPE_SINGLE_RESOURCE
                if not last_object:
                    r_types = o.split(',')
                    # if all is present, we will replace it with all_types
                    if 'all' in r_types:
                        ai = r_types.index('all')
                        r_types.remove('all')
                        r_types[ai:ai] = all_types
                    for rt in r_types:
                        check_rt = map_res(rt)
                        if check_rt is None:
                            raise ResourceParseError("[ERROR] Invalid object type: ", rt)
                        else:
                            last_object.append(check_rt['type'])
                else:
                    # last_object was set, meaning this should be object name
                    raise ResourceParseError("[ERROR] Invalid resources to get: ", self.objects)

            # Simple word (without , or /)
            # If last_object was not set, means this is a resource_type
            elif not last_object:
                self.method = self.Method.SINGLE_TYPE
                check_rt = map_res(o)
                if check_rt is not None:
                    last_object = [check_rt['type']]
                else:
                    print("[ERROR] Invalid resource type to get: ", o)
            # Simple word (without , or /)
            # If the last_object was set, means we got resource_type last time,
            # and this should be a resource_name.
            elif last_object:
                self.method = self.Method.SINGLE_TYPE
                for rt in last_object:
                    if rt in self.object_dict:
                        self.object_dict[rt].append(o)
                    else:
                        self.object_dict[rt] = [o]
                # last_object = []
            else:
                # Should never happen
                raise ResourceParseError("[ERROR] Invalid resources to get: ", o)

            # If after going through all the args, we have last_object set
            # and there was no entry in objects[] for this, it
            # means we didn't get a resource_name for this resource_type.
            # i.e, we need to get all names
        if last_object:
            for rt in last_object:
                check_rt = map_res(rt)
                if check_rt['type'] not in self.object_dict or len(self.object_dict[check_rt['type']]) == 0:
                    self.object_dict[check_rt['type']] = ['_all']


def list_get(ctx: Context, args, incomplete):
    c = Config()
    objects = ctx.params.get("objects")

    try:
        g = GetResourceList(objects)
    except ResourceParseError as e:
        return []

    if "/" in incomplete:
        # Scenario B above
        restypein = incomplete.split("/")[0]
        resname = incomplete.split("/")[1]
        restype = map_res(restypein)
        resources = restype['get_func']('items', c.project, '_all', restype['yaml_loc'], restype['need_ns'])
        return [restypein + "/" + r['res']['metadata']['name'] for r in resources if resname in r['res']['metadata']['name']]

    if len(g.object_dict) == 0 and "," in incomplete:
        # This is a NOP like oc
        return []
    elif g.method == g.Method.SINGLE_TYPE or \
            (len(g.object_dict) == 1 and ["_all"] in g.object_dict.values()):
        # Autocomplete resource names based on the type (first arg)
        restypein = list(g.object_dict)[0]
        restype = map_res(restypein)
        resources = restype['get_func']('items', c.project, '_all', restype['yaml_loc'], restype['need_ns'])
        return [r['res']['metadata']['name'] for r in resources if
                incomplete in r['res']['metadata']['name']]
    else:
        # Return completions for resource types
        # TODO: There has to be a better way
        # TODO: Include aliases
        fullset = set(all_types + [t['type'] for t in map])
        return [t for t in fullset if incomplete in t]

    return []


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

    s = GetResourceList(objects)
    obj_dict = s.object_dict

    # Debug
    # print(objects)

    # Object based routing
    # i.e, call the get function for all the requested types
    # then call the output function or simply print if its yaml/json
    
    # If printing multiple objects, add a blank line between each
    mult_objs_blank_line = False
    for rt in obj_dict.keys():
        rt_info = map_res(rt)
        get_func = rt_info['get_func']
        getout_func = rt_info['getout_func']
        yaml_loc = rt_info['yaml_loc']
        need_ns = rt_info['need_ns']

        # Call the get function to get the resoruces
        res = get_func(rt, ns, obj_dict[rt], yaml_loc, need_ns)

        # Error out if no objects/resources were collected
        if len(res) == 0 and len(obj_dict) == 1:
            print('No resources found for type "%s" in %s namespace'%(rt,ns))
        elif len(res) > 0:
            # If printing multiple objects, add a blank line between each
            if mult_objs_blank_line == True:
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
                if len(obj_dict) > 1:
                    show_type = True
                else:
                    show_type = False
                getout_func(rt, ns, res, output, show_type)
            # Flag to print multiple objects
            if mult_objs_blank_line == False:
                mult_objs_blank_line = True
    # Error out once if multiple objects/resources requested and none collected
    if mult_objs_blank_line == False and len(obj_dict) > 1:
        print('No resources found in %s namespace'%(ns))
