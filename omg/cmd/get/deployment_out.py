from tabulate import tabulate

from omg.common.helper import age, extract_labels


# Simple out put with just name and age
def deployment_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    if show_labels:
        output_res[0].extend(['NAME','READY','UP-TO-DATE','AVAILABLE','AGE','LABELS'])
    else:
        output_res[0].extend(['NAME','READY','UP-TO-DATE','AVAILABLE','AGE'])
    if output == 'wide':
        output_res[0].extend(['CONTAINERS','IMAGES'])
    # resources
    for r in res:
        dep = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(dep['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + dep['metadata']['name'])
        else:
            row.append(dep['metadata']['name'])
        # ready
        try:
            ready = dep['status']['readyReplicas']
            replicas = dep['status']['replicas']
            row.append( str(ready) + '/' + str(replicas) )
        except:
            row.append('??')
        # up-to-date
        try:
            row.append(dep['status']['updatedReplicas'])
        except:
            row.append('??')
        # available
        try:
            row.append(dep['status']['availableReplicas'])
        except:
            row.append('??')
        # age
        try:
            ct = str(dep['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # -o wide
        if output == 'wide':
            # container:
            conts = [ c['name'] for c in dep['spec']['template']['spec']['containers'] ]
            row.append(','.join(conts))
            # images:
            images = [ c['image'] for c in dep['spec']['template']['spec']['containers'] ]
            row.append(','.join(images))
        # show-labels
        if show_labels:
            row.append(extract_labels(dep))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
