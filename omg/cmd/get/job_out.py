from tabulate import tabulate

from omg.common.helper import age, extract_labels


def job_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    if show_labels:
        output_res[0].extend(['NAME','COMPLETIONS','DURATION','AGE','LABELS'])
    else:
        output_res[0].extend(['NAME','COMPLETIONS','DURATION','AGE'])
    # resources
    for r in res:
        job = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(job['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + job['metadata']['name'])
        else:
            row.append(job['metadata']['name'])
        # completions
        try:
            # test numerator
            try:
                comp_num = str(job['status']['succeeded'])
            except:
                comp_num = '0'
            # append denominator
            comp_den = str(job['spec']['completions'])
            row.append(comp_num + '/' + comp_den)
        except:
            row.append('??')
        # duration
        try:
            st = str(job['status']['startTime'])
            ct = str(job['status']['completionTime'])
            row.append(age(st,ct, ts2_type='iso'))
        except:
            row.append('Unknown')
        # age
        try:
            ct = str(job['status']['startTime'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # show-labels
        if show_labels:
            row.append(extract_labels(job))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
