from tabulate import tabulate

from omg.common.helper import age, extract_labels


def secret_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    if show_labels:
        output_res[0].extend(['NAME','TYPE','DATA','AGE','LABELS'])
    else:
        output_res[0].extend(['NAME','TYPE','DATA','AGE'])
    # resources
    for r in res:
        sec = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(sec['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + sec['metadata']['name'])
        else:
            row.append(sec['metadata']['name'])
        # type
        row.append(sec['type'])
        # data
        if 'data' in sec:
            data = len(sec['data'])
        else:
            data = 0
        row.append(data)
        # age
        try:
            ct = str(sec['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # show-labels
        if show_labels:
            row.append(extract_labels(sec))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
