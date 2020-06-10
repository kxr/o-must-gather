from tabulate import tabulate

from omg.common.helper import age


# Simple out put with just name and age
def cm_out(t, ns, res, output, show_type):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
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
            ct = cm['metadata']['creationTimestamp']
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
