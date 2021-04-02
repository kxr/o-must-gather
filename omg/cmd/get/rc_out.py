from tabulate import tabulate

from omg.common.helper import age, extract_labels


def rc_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','DESIRED','CURRENT','READY','AGE'])
    if output == 'wide':
        output_res[0].extend(['CONTAINERS','IMAGES'])
    if show_labels:
        output_res[0].extend(['LABELS'])
    # resources
    for r in res:
        rc = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(rc['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + rc['metadata']['name'])
        else:
            row.append(rc['metadata']['name'])
        # desired
        try:
            row.append(rc['status']['replicas'])
        except:
            row.append('0')
        # current
        try:
            row.append(rc['status']['fullyLabeledReplicas'])
        except:
            row.append('0')
        # ready
        try:
            row.append(rc['status']['readyReplicas'])
        except:
            row.append('0')
        # age
        try:
            ct = str(rc['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # -o wide
        if output == 'wide':
            # container:
            conts = [ c['name'] for c in rc['spec']['template']['spec']['containers'] ]
            row.append(','.join(conts))
            # images:
            images = [ c['image'] for c in rc['spec']['template']['spec']['containers'] ]
            row.append(','.join(images))
        # show-labels
        if show_labels:
            row.append(extract_labels(rc))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
