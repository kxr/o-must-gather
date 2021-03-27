from tabulate import tabulate

from omg.common.helper import age, extract_labels


# Simple out put with just name and age
def machineset_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    if show_labels:
        output_res[0].extend(['NAME','DESIRED', 'CURRENT', 'READY', 'AVAILABLE','AGE','LABELS'])
    else:
        output_res[0].extend(['NAME','DESIRED', 'CURRENT', 'READY', 'AVAILABLE','AGE'])
    # resources
    for r in res:
        ms = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(ms['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + ms['metadata']['name'])
        else:
            row.append(ms['metadata']['name'])
        # desired
        if 'spec' in ms and 'replicas' in ms['spec']:
            row.append(ms['spec']['replicas'])
        else:
            row.append(0)
        if 'status' in ms:
            # current
            if 'replicas' in ms['status']:
                row.append(ms['status']['replicas'])
            else:
                row.append(0)
            # ready
            if 'readyReplicas' in ms['status']:
                row.append(ms['status']['readyReplicas'])
            else:
                row.append('')
            # available
            if 'availableReplicas' in ms['status']:
                row.append(ms['status']['availableReplicas'])
            else:
                row.append('')
        else:
            row.extend(['?','?','?'])
        # age
        try:
            ct = str(ms['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # show-labels
        if show_labels:
            row.append(extract_labels(ms))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
