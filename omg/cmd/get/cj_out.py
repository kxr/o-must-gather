from tabulate import tabulate

from omg.common.helper import age, extract_labels


def cj_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    if show_labels:
        output_res[0].extend(['NAME','SCHEDULE','SUSPEND','ACTIVE', 'LAST SCHEDULE','AGE','LABELS'])
    else:
        output_res[0].extend(['NAME','SCHEDULE','SUSPEND','ACTIVE', 'LAST SCHEDULE','AGE'])
    # resources
    for r in res:
        cj = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(cj['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + cj['metadata']['name'])
        else:
            row.append(cj['metadata']['name'])
        # schedule
        try:
            row.append(cj['spec']['schedule'])
        except:
            row.append('??')
        # suspend
        try:
            row.append(cj['spec']['suspend'])
        except:
            row.append('??')
        # active
        try:
            row.append(len(cj['status']['active']))
        except:
            row.append('0')
        # last schedule
        try:
            ct = str(cj['status']['lastScheduleTime'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # age
        try:
            ct = str(cj['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # show-labels
        if show_labels:
            row.append(extract_labels(cj))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
