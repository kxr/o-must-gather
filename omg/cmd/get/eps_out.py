from tabulate import tabulate

from omg.common.helper import age


# endpoint out
def eps_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','ADDRESSTYPE','PORTS','ENDPOINTS','AGE'])
    # resources
    for r in res:
        eps = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(eps['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + eps['metadata']['name'])
        else:
            row.append(eps['metadata']['name'])
        # addresstype
            row.append(eps['addressType'])
        # ports
        ports = []
        if 'ports' in eps and eps['ports'] is not None:
            for s in eps['ports']:
                ports.append(
                    str(str(s['port']))
                )
        if len(ports) == 0:
            row.append('<none>')
        elif len(ports) < 4:
            row.append(
                ','.join(ports)
            )
        else:
            row.append(
                ','.join(ports[:3]) +
                ' + ' +
                str(len(ports)-3) +
                ' more...'
            )
        
        # endpoints
        endpoints = []
        if 'endpoints' in eps and eps['endpoints'] is not None:
            for s in eps['endpoints']:
                endpoints.append(
                    str(s['addresses'][0])
                )
        if len(endpoints) == 0:
            row.append('<none>')
        elif len(endpoints) < 4:
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
        
        # age
        try:
            ct = str(eps['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
