from tabulate import tabulate

from omg.common.helper import age, extract_labels


def machine_out(t, ns, res, output, show_type, show_labels):
    output_res=[]
    # header
    header = []
    if ns == '_all':
        header.append('NAMESPACE')
    if show_labels:
        header.extend(['NAME', 'PHASE', 'TYPE', 'REGION', 'ZONE', 'AGE','LABELS'])
    else:
        header.extend(['NAME', 'PHASE', 'TYPE', 'REGION', 'ZONE', 'AGE'])
    # resources
    for r in res:
        m = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(m['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + m['metadata']['name'])
        else:
            row.append(m['metadata']['name'])
        # phase
        if 'status' in m and 'phase' in m['status']:
            row.append(m['status']['phase'])
        else:
            row.append('')
        # type, region, zone
        for l in    [  'machine.openshift.io/instance-type',
                        'machine.openshift.io/region',
                        'machine.openshift.io/zone'         ]:
            if 'labels' in m['metadata'] and l in m['metadata']['labels']:
                row.append(m['metadata']['labels'][l])
            else:
                row.append('')
        try:
            ct = str(m['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # show-labels
        if show_labels:
            row.append(extract_labels(m))

        output_res.append(row)

    # sort by NAME column whose index will be
    # 1 if we are showing namespaces otherwise 0
    ni = 1 if ns == '_all' else 0
    sorted_output = sorted(output_res, key=lambda x: x[ni])
    sorted_output.insert(0,header)



    print(tabulate(sorted_output,tablefmt="plain"))
