from tabulate import tabulate
import sys, yaml, json

from omg.common.helper import age, extract_labels


def ds_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    if output == 'wide' and not show_labels:
        output_res[0].extend(['NAME','DESIRED','CURRENT','READY','UP-TO-DATE','AVAILABLE','NODE SELECTOR','AGE','CONTAINERS','IMAGES'])
    elif output == 'wide' and show_labels:
        output_res[0].extend(['NAME','DESIRED','CURRENT','READY','UP-TO-DATE','AVAILABLE','NODE SELECTOR','AGE','CONTAINERS','IMAGES','LABELS'])
    elif show_labels:
        output_res[0].extend(['NAME','DESIRED','CURRENT','READY','UP-TO-DATE','AVAILABLE','NODE SELECTOR','AGE','LABELS'])
    else:
        output_res[0].extend(['NAME','DESIRED','CURRENT','READY','UP-TO-DATE','AVAILABLE','NODE SELECTOR','AGE'])
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
        # show-labels
        if show_labels:
            row.append(extract_labels(ds))

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
