from tabulate import tabulate

from omg.common.helper import age, extract_labels

def mcp_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if show_labels:
        output_res[0].extend(['NAME','CONFIG','UPDATED','UPDATING','DEGRADED','MACHINECOUNT',
                              'READYMACHINECOUNT', 'UPDATEDMACHINECOUNT','DEGRADEDMACHINECOUNT','AGE','LABELS'])
    else:
        output_res[0].extend(['NAME','CONFIG','UPDATED','UPDATING','DEGRADED','MACHINECOUNT',
                          'READYMACHINECOUNT', 'UPDATEDMACHINECOUNT','DEGRADEDMACHINECOUNT','AGE'])
    # resources
    for r in res:
        mcp = r['res']
        row = []
        # name
        if show_type:
            row.append(t + '/' + mcp['metadata']['name'])
        else:
            row.append(mcp['metadata']['name'])
        # config
        try:
            row.append(mcp['spec']['configuration']['name'])
        except:
            row.append('')
        # updated, updating, degraded
        updated = ''
        updating = ''
        degraded = ''
        conds = mcp['status']['conditions']
        for c in conds:
            if c['type'] == 'Updated':
                updated = c['status']
            if c['type'] == 'Updating':
                updating = c['status']
            if c['type'] == 'Degraded':
                degraded = c['status']
        row.append(updated)
        row.append(updating)
        row.append(degraded)
        # machine count
        row.append(mcp['status']['machineCount'])
        row.append(mcp['status']['readyMachineCount'])
        row.append(mcp['status']['updatedMachineCount'])
        row.append(mcp['status']['degradedMachineCount'])
        # age
        try:
            ct = str(mcp['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # show-labels
        if show_labels:
            row.append(extract_labels(mcp))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
