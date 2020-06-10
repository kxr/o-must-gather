from tabulate import tabulate

from omg.common.helper import age


def pv_out(t, ns, res, output, show_type):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','CAPACITY','ACCESS MODES','RECLAIM POLICY',
                            'STATUS','CLAIM','STORAGECLASS','REASON','AGE'])
    # resources
    for r in res:
        p = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(p['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + p['metadata']['name'])
        else:
            row.append(p['metadata']['name'])
        # capacity
        row.append(p['spec']['capacity']['storage'])
        # access
        access = ",".join(p['spec']['accessModes'])
        row.append(access)
        # reclaim
        row.append(p['spec']['persistentVolumeReclaimPolicy'])
        # status
        row.append(p['status']['phase'])
        # claim
        try:
            cr_name = p['spec']['claimRef']['name']
            cr_ns = p['spec']['claimRef']['namespace']
            claim = cr_ns + '/' + cr_name
        except:
            claim = ''
        row.append(claim)
        # storage class
        if 'storageClassName' in p['spec']:
            row.append(p['spec']['storageClassName'])
        else:
            row.append('')
        
        # reason (?) TODO need sample of this yaml
        row.append('')
        # age
        try:
            ct = p['metadata']['creationTimestamp']
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
