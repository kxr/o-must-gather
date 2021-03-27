from tabulate import tabulate

from omg.common.helper import age


# Simple out put with just name and age
def ss_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','READY','AGE'])
    if output == 'wide':
        output_res[0].extend(['CONTAINERS','IMAGES'])
    # resources
    for r in res:
        ss = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(ss['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + ss['metadata']['name'])
        else:
            row.append(ss['metadata']['name'])
        # ready
        ready = ss['status']['readyReplicas']
        replicas = ss['status']['replicas']
        row.append( str(ready) + '/' + str(replicas) )
        # age
        try:
            ct = str(ss['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # -o wide
        if output == 'wide':
            # container:
            conts = [ c['name'] for c in ss['spec']['template']['spec']['containers'] ]
            row.append(','.join(conts))
            # images:
            images = [ c['image'] for c in ss['spec']['template']['spec']['containers'] ]
            row.append(','.join(images))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
