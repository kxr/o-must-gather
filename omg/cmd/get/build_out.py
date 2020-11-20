from tabulate import tabulate

from omg.common.helper import age


def build_out(t, ns, res, output, show_type):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','TYPE','FROM','STATUS', 'STARTED','DURATION'])
    # resources
    for r in res:
        build = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(build['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + build['metadata']['name'])
        else:
            row.append(build['metadata']['name'])
        # type
        try:
            row.append(build['spec']['strategy']['type'])
        except:
            row.append('??')
        # from
        try:
            row.append(build['spec']['source']['type'])
        except:
            row.append('??')
        # status
        try:
            row.append(build['status']['phase'])
        except:
            row.append('??')
        # started
        try:
            ct = str(build['status']['startTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # duration
        try:
            row.append(str(int((build['status']['duration']) / 1000000000)) + 's')
        except:
            row.append('Unknown')
        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
