from tabulate import tabulate

from omg.common.helper import age, extract_labels

# Config Map
def cm_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    if show_labels:
        output_res[0].extend(['NAME','DATA','AGE','LABELS'])
    else:
        output_res[0].extend(['NAME','DATA','AGE'])
    # resources
    for r in res:
        cm = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(cm['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + cm['metadata']['name'])
        else:
            row.append(cm['metadata']['name'])
        # data
        if 'data' in cm:
            row.append( len(cm['data']) )
        else:
            row.append('0')
        # age
        try:
            ct = str(cm['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # show-labels
        if show_labels:
            row.append(extract_labels(cm))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
