from tabulate import tabulate

from omg.common.helper import age


def hpa_out(t, ns, res, output, show_type, show_labels):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','REFERENCE','TARGETS','MINPODS', 'MAXPODS','REPLICAS','AGE'])
    # resources
    for r in res:
        hpa = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(hpa['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + hpa['metadata']['name'])
        else:
            row.append(hpa['metadata']['name'])
        # reference
        try:
            row.append(hpa['spec']['scaleTargetRef']['kind'] + '/' + hpa['spec']['scaleTargetRef']['name'])
        except:
            row.append('??')
        # targets
        try:
            # test numerator
            try:
                target_num = str(hpa['status']['currentCPUUtilizationPercentage']) + '%'
            except:
                target_num = '<unknown>'
            # append denominator
            target_den = str(hpa['spec']['targetCPUUtilizationPercentage']) + '%'
            row.append(target_num + '/' + target_den)
        except:
            row.append('??')
        # minpods
        try:
            row.append(hpa['spec']['minReplicas'])
        except:
            row.append('??')
        # maxpods
        try:
            row.append(hpa['spec']['maxReplicas'])
        except:
            row.append('??')
        # replicas
        try:
            row.append(hpa['status']['currentReplicas'])
        except:
            row.append('??')
        # age
        try:
            ct = str(hpa['metadata']['creationTimestamp'])
            ts = r['gen_ts']
            row.append(age(ct,ts))
        except:
            row.append('Unknown')
        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
