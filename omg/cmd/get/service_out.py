from tabulate import tabulate

from omg.common.helper import age


def service_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    if output == 'wide' and not show_labels:
        output_res[0].extend(['NAME','TYPE','CLUSTER-IP','EXTERNAL-IP','PORT(S)','AGE','SELECTOR'])
    elif output == 'wide' and show_labels:
        output_res[0].extend(['NAME','TYPE','CLUSTER-IP','EXTERNAL-IP','PORT(S)','AGE','SELECTOR','LABELS'])
    elif show_labels:
        output_res[0].extend(['NAME','TYPE','CLUSTER-IP','EXTERNAL-IP','PORT(S)','AGE','LABELS'])
    else:
        output_res[0].extend(['NAME','TYPE','CLUSTER-IP','EXTERNAL-IP','PORT(S)','AGE'])
    # resources
    for r in res:
        svc = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(svc['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + svc['metadata']['name'])
        else:
            row.append(svc['metadata']['name'])
        # type
        row.append(svc['spec']['type'])
        # cluster-ip
        if 'clusterIP' in svc['spec']:
            row.append(svc['spec']['clusterIP'])
        else:
            row.append('<none>')
        # external-ip
        if 'externalName' in svc['spec']:
            row.append(svc['spec']['externalName'])
        elif 'externalIP' in svc['spec']:
            row.append(svc['spec']['externalIP'])
        else:
            row.append('<none>')
        # ports
        if 'ports' in svc['spec']:
            ports = ','.join(
                str(p['port']) + '/' + p['protocol'] 
                for p in svc['spec']['ports'] if 'port' in p
            )
            row.append(ports)
        else:
            row.append('<none>')
        # age
        try:
            ct = str(svc['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        #selector (-o wide)
        if output == 'wide':
            if 'selector' in svc['spec']:
                selector = ",".join(
                    [ label+'='+value for label,value in svc['spec']['selector'].items() ]
                )
                row.append(selector)
            else:
                row.append('<none>')
        # show-labels
        if show_labels and "labels" in svc['metadata']:
            row.append(svc['metadata']['labels'])

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
