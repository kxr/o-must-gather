from tabulate import tabulate

from omg.common.helper import age


def dc_out(t, ns, res, output, show_type):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','REVISION','DESIRED','CURRENT','TRIGGERED BY'])
    # resources
    for r in res:
        dc = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(dc['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + dc['metadata']['name'])
        else:
            row.append(dc['metadata']['name'])
        # revision
        try:
            row.append(dc['status']['latestVersion'])
        except:
            row.append('??')
        # desired
        try:
            row.append(dc['spec']['replicas'])
        except:
            row.append('??')
        # current
        try:
            row.append(dc['status']['readyReplicas'])
        except:
            row.append('??')
        # triggered by
        try:
            triggered_type = dc['spec']['triggers'][0].get('type')
            if triggered_type == 'ConfigChange':
                row.append('config')
            else:
                row.append(triggered_type)
        except:
            row.append('??')

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
