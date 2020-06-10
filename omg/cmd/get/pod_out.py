from tabulate import tabulate

from omg.common.helper import age

# Special function to output pod
# Generate output table if -o not set or 'wide'
# We will create an array of array and then print if with tabulate
def pod_out(t, ns, res, output, show_type):
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
        if show_type:
            row.append(t + '/' + p['metadata']['name'])
        else:
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
