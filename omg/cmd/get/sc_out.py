from tabulate import tabulate

from omg.common.helper import age, extract_labels

def sc_out(t, ns, res, output, show_type, show_labels):
    output_res=[]
    # header
    if show_labels:
        header = ['NAME','PROVISIONER','RECLAIMPOLICY','VOLUMEBINDINGMODE','ALLOWVOLUMEEXPANSION','AGE','LABELS']
    else:
        header = ['NAME','PROVISIONER','RECLAIMPOLICY','VOLUMEBINDINGMODE','ALLOWVOLUMEEXPANSION','AGE']
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
        # show-labels
        if show_labels:
            row.append(extract_labels(sc))

        output_res.append(row)

    # sort by 1st column
    sorted_output = sorted(output_res)
    sorted_output.insert(0,header)
    print(tabulate(sorted_output,tablefmt="plain"))
