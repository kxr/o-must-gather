import sys, yaml, json
from omg.common.config import Config
from omg.common.resource_map import map_res

# The high level function that gets called for any "get" command
# This function processes/identifies the objects, they can be in various formats e.g:
#   get pod httpd
#   get pods httpd1 httpd2
#   get dc/httpd pod/httpd1
#   get routes
#   get pod,svc
# We get all these args (space separated) in the array a.objects
# We'll process them and normalize them in a python dict (objects)
# Once we have one of more object to get,
# and call the respective get function
# (this function is looked up from common/resource_map)
def get_main(a):
    # a = args passed from cli
    # Check if -A/--all-namespaces is set
    # else, Set the namespace
    # -n/--namespace takes precedence over current project 
    if a.all_namespaces is True:
        ns = '_all'
    else:
        if a.namespace is not None:
            ns = a.namespace
        elif Config().project is not None:
            ns = Config().project
        else:
            ns = None

    # We collect the resources types/names in this dict
    # e.g for `get pod httpd1 httpd2` this will look like:
    #   objects = { 'pod': ['httpd1', 'httpd2'] }
    # e.g, for `get pod,svc` this will look like:
    #   objects = { 'pod': ['_all'], 'service': ['_all'] }
    objects = {}

    last_object = []
    all_types = ['pod', 'rc', 'svc', 'ds', 'deployment', 'rs', 'statefulset', 'hpa', 'job', 'cronjob', 'dc', 'bc', 'build', 'is']
    for o in a.objects:
        # Case where we have a '/'
        # e.g omg get pod/httpd
        if '/' in o:
            if not last_object:
                pre = o.split('/')[0]
                r_type = map_res(pre)['type']
                r_name = o.split('/')[1]
                # If its a valid resource type, apppend it to objects
                if r_type is not None:
                    if r_type in objects:
                        objects[r_type].append(r_name)
                    else:
                        objects[r_type] = [r_name]
                else:
                    print("[ERROR] Invalid object type: ",pre)
                    sys.exit(1)
            else:
                # last_object was set, meaning this should be object name
                print("[ERROR] There is no need to specify a resource type as a separate argument when passing arguments in resource/name form")
                sys.exit(1)
                
        # Convert 'all' to list of resource types in a specific order
        elif o == 'all':
            for rt in all_types:
                check_rt = map_res(rt)
                if check_rt is None:
                    print("[ERROR] Invalid object type: ",rt)
                    sys.exit(1)
                else:
                    last_object.append(check_rt['type'])

        # Case where we have a ',' e.g `get dc,svc,pod httpd`
        # These all will be resource_types, not names,
        # resource_name will come it next iteration (if any)
        elif ',' in o:
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
                        print("[ERROR] Invalid object type: ",rt)
                        sys.exit(1)
                    else:
                        last_object.append(check_rt['type'])
            else:
                # last_object was set, meaning this should be object name
                print("[ERROR] Invalid resources to get: ", a.objects)
                sys.exit(1)

        # Simple word (without , or /)
        # If last_object was not set, means this is a resource_type
        elif not last_object:
            check_rt = map_res(o)
            if check_rt is not None:
                last_object = [ check_rt['type'] ]
            else:
                print("[ERROR] Invalid resource type to get: ", o)
        # Simple word (without , or /)
        # If the last_object was set, means we got resource_type last time,
        # and this should be a resource_name. 
        elif last_object:
            for rt in last_object:
                if rt in objects:
                    objects[rt].append(o)
                else:
                    objects[rt] = [o]
            #last_object = []
        else:
            # Should never happen
            print("[ERROR] Invalid resources to get: ", o)
            sys.exit(1)
    # If after going through all the args, we have last_object set
    # and there was no entry in objects[] for this, it
    # means we didn't get a resource_name for this resource_type.
    # i.e, we need to get all names
    if last_object:
        for rt in last_object:
            check_rt = map_res(rt)
            if check_rt['type'] not in objects or len(objects[check_rt['type']]) == 0:
                objects[check_rt['type']] = ['_all']

    # Debug
    # print(objects)

    # Object based routing
    # i.e, call the get function for all the requested types
    # then call the output function or simply print if its yaml/json
    
    # If printing multiple objects, add a blank line between each
    mult_objs_blank_line = False
    for rt in objects.keys():
        rt_info = map_res(rt)
        get_func = rt_info['get_func']
        getout_func = rt_info['getout_func']
        yaml_loc = rt_info['yaml_loc']
        need_ns = rt_info['need_ns']

        # Call the get function to get the resoruces
        res = get_func(rt, ns, objects[rt], yaml_loc, need_ns)

        # Error out if no objects/resources were collected
        if len(res) == 0 and len(objects) == 1:
            print('No resources found for type "%s" in %s namespace'%(rt,ns))
        elif len(res) > 0:
            # If printing multiple objects, add a blank line between each
            if mult_objs_blank_line == True:
                print('')
            # Yaml dump if -o yaml
            if a.output == 'yaml':
                if len(res) == 1:
                    print(yaml.dump(res[0]['res']))
                elif len(res) > 1:
                    print(yaml.dump({'apiVersion':'v1','items':[cp['res']for cp in res]}))
            # Json dump if -o json
            elif a.output == 'json':
                if len(res) == 1:
                    print(json.dumps(res[0]['res'],indent=4))
                elif len(res) > 1:
                    print(json.dumps({'apiVersion':'v1','items':[cp['res']for cp in res]},indent=4))
            # Call the respective output function if -o is not set or -o wide
            elif a.output in [None, 'wide']:
                # If we displaying more than one resource_type,
                # we need to display resource_type with the name (type/name)
                if len(objects) > 1:
                    show_type = True
                else:
                    show_type = False
                getout_func(rt, ns, res, a.output, show_type)
            # Flag to print multiple objects
            if mult_objs_blank_line == False:
                mult_objs_blank_line = True
    # Error out once if multiple objects/resources requested and none collected
    if mult_objs_blank_line == False and len(objects) > 1:
        print('No resources found in %s namespace'%(ns))
