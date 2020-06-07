import sys, os, yaml, json, tabulate
from tabulate import tabulate
from .config import Config
from .resource_map import check_res
from .helper import locate_ns
from .helper import age

# This function gets the simple namespace bound resource types like:
# pod, event, configmap, secret, etc.
def simple(ns, yaml_loc, names):
    # We need ns for this resource type
    if ns is None:
        print('[ERROR] No namespaces selected. Use `omg project` or specify -n')
        sys.exit(1)
    ns_path = locate_ns(ns)
    # Collect the resources
    collected=[]
    for n in ns_path:
        yaml_file = n + yaml_loc
        # record when was this yaml generated (to calc age)
        gen_ts = os.path.getmtime(yaml_file)
        try:
            with open(yaml_file, 'rb') as yf:
                try:
                    res = yaml.safe_load(yf)
                except:
                    print("[ERROR] Parsing error in ", yaml_file)
                    sys.exit(1)
        except:
            print("[ERROR] Could not read file:", yaml_file)
            sys.exit(1)
        collected.extend([ {'res':r,'gen_ts':gen_ts} for r in res['items'] if r['metadata']['name'] in names or '_all' in names ])
    return collected

def simple_out(res, ns, output):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','AGE'])
    # resources
    for r in res:
        p = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(p['metadata']['namespace'])
        # name
        row.append(p['metadata']['name'])
        # age
        try:
            ct = p['metadata']['creationTimestamp']
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))


def pod_out(res, ns, output):
    # Generate output table if -o not set or 'wide'
    # We will create an array of array and then print if with tabulate
    if output in [None,'wide']:
        output_pods=[[]]
        # header
        if ns == '_all':
            output_pods[0].append('NAMESPACE')
        if output == 'wide':
            output_pods[0].extend(['NAME','READY','STATUS','RESTARTS','AGE','IP','NODE'])
        else:
            output_pods[0].extend(['NAME','READY','STATUS','RESTARTS','AGE'])
        # pods
        for pod in res:
            p = pod['res']
            row = []
            # namespace (for --all-namespaces)
            if ns == '_all':
                row.append(p['metadata']['namespace'])
            # name
            row.append(p['metadata']['name'])
            # containers/ready count
            containers = str(len(p['spec']['containers']))
            containers_ready = str(len([ r for r in p['status']['containerStatuses']  if r['ready'] == True ]))
            row.append(containers_ready+'/'+containers)
            # status
            row.append(p['status']['phase'])
            # restarts
            row.append(max([ r['restartCount'] for r in p['status']['containerStatuses'] ]))
            # age
            pod_ct = p['metadata']['creationTimestamp']
            gen_ts = pod['gen_ts']
            row.append(age(pod_ct,gen_ts))
            # pod ip and node (if -o wide)
            if output == "wide":
                row.append(p['status']['podIP'])
                row.append(p['spec']['nodeName'])

            output_pods.append(row)

        print(tabulate(output_pods,tablefmt="plain"))



# The high level function that gets called for any "get" command
# Checks what objects to get,
# and call the respective omg_get_<obj> function
def get(a):
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

    # Process the objects, they can be in various formats e.g:
    #   pod httpd, dc/httpd, routes , svc/httpd, pod,svc etc.
    # We get all these args (space separated) in the array args.objects
    # We'll process them and normalize them in a python dict
    objects = {}

    last_object = []
    for o in a.objects:
        # Case where we have a '/'
        # e.g omg get pod/httpd
        if '/' in o:
            o_type = check_res(o.split('/')[0])
            o_name = o.split('/')[1]
            if o_type is not None:
                if o_type['type'] in objects:
                    objects[o_type['type']].append(o_name)
                else:
                    objects[o_type['type']] = [o_name]
            else:
                print("[ERROR] Invalid object type: ",o.split('/')[0])
                sys.exit(1)
        # Case where we have a ','
        # e.g omg get dc,svc httpd
        elif ',' in o:
            if not last_object:
                o_types = o.split(',')
                for ot in o_types:
                    if check_res(ot) is None:
                        print("[ERROR] Invalid object type: ",ot)
                        sys.exit(1)
                last_object = [ check_res(x)['type'] for x in o_types]
            else:
                # last_object was set, meaning this should be object name
                print("[ERROR] Invalid resources to get: ", a.objects)
                sys.exit(1)
        # Simple word that is an object type
        # meaning previous word should not have been an object type
        # i.e, last_object should be None
        elif check_res(o) is not None and not last_object:
            last_object = [ o ]
        # Simple word that is not an object type
        # meaning previous word should have been an object type
        # i.e, last_object should not be None
        elif check_res(o) is None and last_object:
            for lo in last_object:
                o_type = check_res(lo)
                if o_type['type'] in objects:
                    objects[o_type['type']].append(o)
                else:
                    objects[o_type['type']] = [o]
            last_object = []
        else:
            print("[ERROR] Invalid resources to get: ", o)
            sys.exit(1)
    # If after going through all the args, we have last_object set
    # We should process that (request of object type without name)
    # e.g, omg get pods or omg get pods,dc,svc etc.
    if last_object:
        for lo in last_object:
            o_type = check_res(lo)
            objects[o_type['type']] = ['_all']

    # Object based routing
    # i.e, call the function specific to the object type
    for o in objects.keys():
        get_func = check_res(o)['get_func']
        getout_func = check_res(o)['getout_func']
        yaml_loc = check_res(o)['yaml_loc']
        output = a.output

        res = get_func(ns, yaml_loc, objects[o])

        # Error out if no objects/resources were collected
        if len(res) == 0:
            print("No resources found.")
            sys.exit(1)
        # Genereate yaml if -o yaml
        elif output == 'yaml':
            if len(res) == 1:
                print(yaml.dump(res[0]['res']))
            elif len(res) > 1:
                print(yaml.dump({'apiVersion':'v1','items':[cp['res']for cp in res]}))
        # Generate json if -o json
        elif output == 'json':
            if len(res) == 1:
                print(json.dumps(res[0]['res'],indent=4))
            elif len(res) > 1:
                print(json.dumps({'apiVersion':'v1','items':[cp['res']for cp in res]},indent=4))
        # output using the getout_func
        else:
            getout_func(res, ns, output)