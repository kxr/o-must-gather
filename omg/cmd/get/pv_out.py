from tabulate import tabulate

from omg.common.helper import age


def pv_out(t, ns, res, output, show_type, show_labels):
    output_res=[]
    # header
    # we will append the header array at last after sorting
    header = ['NAME','CAPACITY','ACCESS MODES','RECLAIM POLICY','STATUS','CLAIM','STORAGECLASS','REASON','AGE']
    # resources
    for r in res:
        p = r['res']
        row = []
        # name
        if show_type:
            row.append(t + '/' + p['metadata']['name'])
        else:
            row.append(p['metadata']['name'])
        # capacity
        row.append(p['spec']['capacity']['storage'])
        # access
        access = ",".join(p['spec']['accessModes'])
        if access == 'ReadWriteOnce':
          row.append('RWO')
        elif access == 'ReadOnlyMany':
          row.append('ROX')
        elif access == 'ReadWriteMany':
          row.append('RWX')
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

    # sort by 1st column
    sorted_output = sorted(output_res)
    sorted_output.insert(0,header)

    print(tabulate(sorted_output,tablefmt="plain"))
