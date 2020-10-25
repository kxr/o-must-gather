from tabulate import tabulate

from omg.common.helper import age

def sc_out(t, ns, res, output, show_type):
    output_res=[[]]
    # header
    output_res[0].extend(['NAME','PROVISIONER','RECLAIMPOLICY','VOLUMEBINDINGMODE','ALLOWVOLUMEEXPANSION','AGE'])
    # resources
    for r in res:
        sc = r['res']
        row = []
        # name
        if show_type:
            row.append(t + '/' + sc['metadata']['name'])
        else:
            row.append(sc['metadata']['name'])
        # provisioner
        row.append(sc['provisioner'])
        # reclaimpolicy
        row.append(sc['reclaimPolicy'])
        # volumebindingmode
        row.append(sc['volumeBindingMode'])
        # allowvolumeexpansion
        try:
            row.append(sc['allowVolumeExpansion'])
        except:
            row.append('false')
        # age
        try:
            ct = str(sc['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
