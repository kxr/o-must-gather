from tabulate import tabulate

from omg.common.helper import age


def pvc_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','STATUS','VOLUME','CAPACITY','ACCESS MODES','STORAGECLASS','AGE'])
    if output == 'wide':
        output_res[0].extend(['VOLUMEMODE'])
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
        # status
        row.append(p['status']['phase'])
        # volume
        row.append(p['spec']['volumeName'])
        # capacity
        row.append(p['status']['capacity']['storage'])
        # access
        access = ",".join(p['spec']['accessModes'])
        if access == 'ReadWriteOnce':
          row.append('RWO')
        elif access == 'ReadOnlyMany':
          row.append('ROX')
        elif access == 'ReadWriteMany':
          row.append('RWX')
        # storage class
        if 'storageClassName' in p['spec']:
            row.append(p['spec']['storageClassName'])
        else:
            row.append('')
        
        # age
        try:
            ct = p['metadata']['creationTimestamp']
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # -o wide
        if output == 'wide':
            row.append(p['spec']['volumeMode'])

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
