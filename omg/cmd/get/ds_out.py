from tabulate import tabulate
import sys, yaml, json

from omg.common.helper import age


def ds_out(t, ns, res, output, show_type):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','DESIRED','CURRENT','READY','UP-TO-DATE','AVAILABLE','NODE SELECTOR','AGE'])
    if output == 'wide':
        output_res[0].extend(['CONTAINERS','IMAGES'])
    # resources
    for r in res:
        ds = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(ds['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + ds['metadata']['name'])
        else:
            row.append(ds['metadata']['name'])
        # desired
        try:
            row.append(ds['status']['desiredNumberScheduled'])
        except:
            row.append('??')
        # current
        try:
            row.append(ds['status']['currentNumberScheduled'])
        except:
            row.append('??')
        # ready
        try:
            row.append(ds['status']['numberReady'])
        except:
            row.append('??')
        # up-to-date
        try:
            row.append(ds['status']['updatedNumberScheduled'])
        except:
            row.append('??')
        # available
        try:
            row.append(ds['status']['numberAvailable'])
        except:
            row.append('??')
        # node selector
        try:
            nodeselector = ds['spec']['template']['spec']['nodeSelector']
            for k, v in nodeselector.items():
                row.append(k + '=' + v)
        except:
            row.append('??')
        # age
        try:
            ct = str(ds['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        # -o wide
        if output == 'wide':
            # container:
            conts = [ c['name'] for c in ds['spec']['template']['spec']['containers'] ]
            row.append(','.join(conts))
            # images:
            images = [ c['image'] for c in ds['spec']['template']['spec']['containers'] ]
            row.append(','.join(images))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
