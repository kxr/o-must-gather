from tabulate import tabulate

from omg.common.helper import age


# endpoint out
def ep_out(t, ns, res, output, show_type):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','ENDPOINTS','AGE'])
    # resources
    for r in res:
        ep = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(ep['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + ep['metadata']['name'])
        else:
            row.append(ep['metadata']['name'])
        # endpoints
        endpoints = []
        if 'subsets' in ep:
            for s in ep['subsets']:
                if 'addresses' in s and 'ports' in s:
                    for a in s['addresses']:
                        for p in s['ports']:
                            endpoints.append(
                                str(a['ip']) + ':' + str(p['port'])
                            )
        if len(endpoints) < 4:
            row.append(
                ','.join(endpoints)
            )
        else:
            row.append(
                ','.join(endpoints[:3]) +
                ' + ' +
                str(len(endpoints)-3) +
                ' more...'
            )
            row.append('<none>')
        # age
        try:
            ct = ep['metadata']['creationTimestamp']
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
