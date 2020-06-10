from tabulate import tabulate

from omg.common.helper import age

# Special function to output node
# Generate output table if -o not set or 'wide'
# We will create an array of array and then print if with tabulate
def node_out(t, ns, res, output, show_type):
    output_nodes=[]
    # header
    # we will append the header array at last after sorting
    if output == 'wide':
        header = ['NAME','STATUS','ROLES','AGE','VERSION',
            'INTERNAL-IP','EXTERNAL-IP','OS-IMAGE','KERNEL-VERSION','CONTAINER-RUNTIME']
    else:
        header = ['NAME','STATUS','ROLES','AGE','VERSION']
    # pods
    for node in res:
        n = node['res']
        row = []
        # name
        if show_type:
            row.append(t + '/' + n['metadata']['name'])
        else:
            row.append(n['metadata']['name'])
        # status
        ready = next( c['status'] for c in n['status']['conditions'] if c['type'] == 'Ready')
        if ready == 'True':
            status = "Ready"
        else:
            status = "NotReady"
        if 'unschedulable' in n['spec'] and n['spec']['unschedulable']:
            status += ",SchedulingDisabled"
        row.append(status)
        # roles
        roles = ''
        for label in n['metadata']['labels']:
            if label.startswith('node-role.kubernetes.io'):
                roles += label.split('/')[1]
        row.append(roles)
        # age
        ct = n['metadata']['creationTimestamp']
        ts = node['gen_ts']
        row.append(age(ct,ts))
        # version
        ver = n['status']['nodeInfo']['kubeletVersion']
        row.append(ver)
        if output == "wide":
            # internal/external ip
            i_ip = '<none>'
            e_ip = '<none>'
            addresses = n['status']['addresses']
            for a in addresses:
                if a['type'] == 'InternalIP':
                    i_ip = a['address']
                if a['type'] == 'ExternalIP':
                    e_ip = a['address']
            row.append(i_ip)
            row.append(e_ip)
            # os-image
            osimg = n['status']['nodeInfo']['osImage']
            row.append(osimg)
            # kernelVersion
            kver = n['status']['nodeInfo']['kernelVersion']
            row.append(kver)
            crt = n['status']['nodeInfo']['containerRuntimeVersion']
            row.append(crt)
        output_nodes.append(row)

    # sort by 2nd column (role)
    sorted_output = sorted(output_nodes, key=lambda x: x[2])
    sorted_output.insert(0,header)

    print(tabulate(sorted_output,tablefmt="plain"))
