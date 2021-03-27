from tabulate import tabulate

from omg.common.helper import age, extract_labels


# Simple out put with just name and age
def rs_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','DESIRED','CURRENT','READY','AGE'])
    if output == 'wide':
        output_res[0].extend(['CONTAINERS', 'IMAGES','SELECTOR'])
    if show_labels:
        output_res[0].extend(['LABELS'])

    # resources
    for r in res:
        rs = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(rs['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + rs['metadata']['name'])
        else:
            row.append(rs['metadata']['name'])
        # desired, current, ready
        for x in ['replicas', 'availableReplicas', 'readyReplicas']:
            if x in rs['status']:
                row.append(rs['status'][x])
            else:
                row.append('0')
        # age
        try:
            ct = str(rs['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # -o wide
        if output == 'wide':
            # containers
            conts = [ c['name'] for c in rs['spec']['template']['spec']['containers'] ]
            row.append(','.join(conts))
            # images
            images = [ c['image'] for c in rs['spec']['template']['spec']['containers'] ]
            row.append(','.join(images))
            # selector
            try:
                ml = ','.join(
                    [ k+'='+v 
                        for k,v in rs['spec']['selector']['matchLabels'].items()
                    ]
                )
            except:
                ml = '?'
            row.append(ml)
        # show-labels
        if show_labels:
            row.append(extract_labels(rs))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
